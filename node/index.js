// imports
const socketio = require("socket.io");
const cookieParser = require("cookie-parser");
const socketAuth = require("./auth.js");
const db = require("./models/db");
const Message = require("./models/Message");
const Conversation = require("./models/Conversation");
const Participation = require("./models/Participation");
// setting up servers
const app = require("express")();
const server = require("http").createServer(app);
const io = socketio(server, { path: "/socket" });

// middlewares
app.use(cookieParser());

//utlis functions
onlineUsers = [];
onlineSockets = [];
const removeUser = (id) => {
  onlineUsers.forEach((userId, index) => {
    if (userId == id) {
      return onlineUsers.splice(index, 1)[0];
    }
  });
};

const removeSocket = (id) => {
  onlineSockets.forEach((socket, index) => {
    if (socket.id == id) {
      return onlineSockets.splice(index, 1)[0];
    }
  });
};


// websockets methods   one -> two  two->read->sender one 
// client side socket using namespace /messenger and using auth_socket function to authorize
io.of("/messenger")
  .use(socketAuth)
  .on("connection", (socket) => {
    onlineUsers.push(socket.userId); //add  user to online users list
    onlineSockets.push(socket); //add sokcet to online sockets list
    io.of("/messenger").emit("onlineUsers", onlineUsers); //event send when new user connects
    // to mark message as read when client side emit read event
    socket.on("readMessage", async function (messageId) {
      try {
        let message = await Message.findOne({ id: messageId }).populate({
          path : 'conversation',
          populate : {
            path : 'participation',
            match: { user_id: socket.userId}
          }
        }).lean();
        if (
          message &&
          message.conversation.participation
        ) {
          await Message.findOneAndUpdate({ id: messageId }, { seen: true });
          if(messageId > message.conversation.participation.last_message_seen_id){
            await Participation.findOneAndUpdate({ id:message.conversation.participation.id  }, { last_message_seen_id: messageId });
          } 
        }
      } catch (error) { console.log(error)}
    });

    socket.on("disconnect", function () {
      removeUser(socket.userId);
      removeSocket(socket.id);
      io.of("/messenger").emit("onlineUsers", onlineUsers);
    });
  });

// namespace for django server to emit new messages for user who is online now
io.of("/internal").on("connection", (socket) => {
  console.log("django connected");
  socket.on("broadcastMessage", (data) => {
    onlineSockets.forEach((onlineSocket) => {
      if (onlineSocket.userId === data.to.id) {
        io.of("/messenger").to(onlineSocket.id).emit("newMessage", data);
      }
    });
  });
});

// server launch
server.listen(3000, () => {
  console.log("app is running on port 3000");
});
