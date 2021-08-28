const DjangoSession = require("./models/DjangoSession");
const DjangoUser = require("./models/DjangoUser");

// function to authorize socket by validate cookies (sent with socket) with user cookies in django system

async function socketAuth(socket, next) {
    const cookie = socket.handshake.headers.cookie; //catch cookies sent with the socket as string
    if (cookie) {
        cookie.split("; ").forEach(async (element) => {
            //extract the sessionid from cookies' string
            let split = element.split("=");
            if (split[0] == "sessionid") {
                let djangoSession = await DjangoSession.findOne({
                    session_key: split[1],
                });
                if (djangoSession) {
                    const sessionData = Buffer.from(
                        djangoSession.session_data,
                        "base64"
                    ).toString(); // if this sessionid exists then decode session data
                    const sessionObjString = sessionData.substring(
                        sessionData.indexOf(":") + 1
                    ); // get the useful information from decoded session data
                    const sessionObjJSON = JSON.parse(sessionObjString); // parse information as json object
                    let user = await DjangoUser.findOne({
                        id: sessionObjJSON._auth_user_id,
                    }); // get user object from database if exist by user_id from parsed useful information
                    if (user) {
                        socket.username = user.username; // if exist assign his name and id to socket object
                        socket.userId = user.id;
                        next(); // and finally if all this True then authorize the socket connection
                    }
                }
            }
        });
    }

    next(new Error("not authorized")); // or throw an error and don't authorize
}

module.exports = socketAuth;
