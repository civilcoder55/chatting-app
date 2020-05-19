
const db = require('./db.js')

const DjangoSession = db.DjangoSession
const DjangoUsers = db.DjangoUsers


// function to authorize socket by validate cookies (sent with socket) with user cookies in django system  

function auth_socket(socket, next){
    const cookie = socket.handshake.headers.cookie //catch cookies sent with the socket as string
    if (cookie){
        cookie.split('; ').forEach((elemnt)=>{ //extract the sessionid from cookies' string
            var split = elemnt.split('=')
            if (split[0] == 'sessionid'){
                DjangoSession.findOne({session_key:split[1]},async function (err, djangoSession){  // check if database has this sessionid 
                    if(djangoSession){
                        const sessionData = Buffer.from(djangoSession.session_data, 'base64').toString(); // if this sessionid exists then decode session data
                        const sessionObjString = sessionData.substring(sessionData.indexOf(":") + 1); // get the useful information from decoded session data
                        const sessionObjJSON = JSON.parse(sessionObjString); // parse information as json object
                        user = await DjangoUsers.findOne({id:sessionObjJSON._auth_user_id}).exec() // get user object from database if exist by user_id from parsed useful information 
                        if(user){ 
                        socket.username = user.username // if exist assign his name and id to socket object
                        socket.usernameId = user.id
                        next() // and finally if all this True then authorize the socket connection 
                        }
                    }
                })
            }
        })
    }

    
    next(new Error('not authorized')) // or throw an error and don't authorize

  }
    


  module.exports = {auth_socket}

