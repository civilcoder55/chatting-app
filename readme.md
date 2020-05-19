# chatapp

# Django & Nodejs private chat app

<a href="http://chat.backenddev.co"><img src="https://stream.backenddev.co/img/logo.svg"></a>

> this project is a simple app written in python with django framework also with node.js socketio library .

[chat.backenddev.co](https://chat.backenddev.co)
<img src="/preview.gif" >

this app hosted via gunicorn & nginx on linux server & nodejs server as socket server
static files served via nginx

simple one to one private chat application written in two frameworks with single database .. django to serve all frontend and handle authentication & storing messages in database (mongodb) and node.js app to handle sockets and real time stuff like online status / deliver messages for online users and mark message as read once user see it.

i tried in this project to mix django with nodejs as one component
both using same domain
both using same database
both using same authentication system --> django authentication and nodejs using middleware to authenticate cookies based on django session storage.

```
as in scr/auth.js
```

## Built With

- Django
- Socket.io
- Mongodb

## Authors

- **Civilcoder** - [civilcoder](https://backenddev.co)

## TO DO

- refactor some code
- adding some comments
- add file send ability
