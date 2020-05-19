// imports
const path = require("path");
const http = require("http");
const express = require("express");
const socketio = require("socket.io");
const cookieParser = require("cookie-parser");
const authMiddlewares = require("./auth.js");
const db = require("./db.js");

const auth_socket = authMiddlewares.auth_socket;
const dialog = db.dialog;
const messages = db.messages;

// setting up servers
const app = express();
const server = http.createServer(app);
const io = socketio(server, { path: "/socket" });

// middlewares
app.use(cookieParser());

//utlis functions
onlineUsers = [];
onlineSockets = [];
const removeUser = (name) => {
  const index = onlineUsers.findIndex((user) => user === name);

  if (index !== -1) {
    return onlineUsers.splice(index, 1)[0];
  }
};

const removeSocket = (id) => {
  const index = onlineSockets.findIndex((socket) => socket === id);

  if (index !== -1) {
    return onlineSockets.splice(index, 1)[0];
  }
};

// websockets methods

// client side socket using namespace /messenger and using auth_socket function to authorize
io.of("/messenger")
  .use(auth_socket)
  .on("connection", (socket) => {
    onlineUsers.push(socket.username); //add  user to online users list
    onlineSockets.push(socket); //add sokcet to online sockets list

    io.of("/messenger").emit("onlineUsers", onlineUsers); //event send when new user connects

    socket.on("read", async function (messageId) {
      // to check message as read when front_end side emit read event
      try {
        message = await messages.findOne({ id: messageId }); //get the message from db by its id
        if (message) {
          check = await dialog.findOne({ id: message.toObject().dialog_id }).exec(); // check if the right user who read the message
          if (check.toObject().first_id == socket.usernameId || check.toObject().second_id == socket.usernameId) {
            await messages.findOneAndUpdate({ id: messageId }, { read: true });
          }
        }
      } catch (err) {
        console.log(err);
      }
    });

    socket.on("disconnect", function () {
      removeUser(socket.username); //remove user from online users list
      removeSocket(socket); //remove sokcet to online sockets list
      io.of("/messenger").emit("onlineUsers", onlineUsers); //event send when new socket user disconnects
    });
  });

// namespace for django server to emit new messages for user who is online now

io.of("/django").on("connection", (socket) => {
  console.log("django connected");
  socket.on("new", (data) => {
    onlineSockets.forEach((element) => {
      if (element.username === data.to) {
        io.of("/messenger").to(element.id).emit("message", data);
      }
    });
  });
});

// server launch
server.listen(3000, () => {
  console.log("app is running on port 3000");
});
