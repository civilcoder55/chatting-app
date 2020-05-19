// modules imports 

const mongoose = require('mongoose')


// mongoose configs
mongoose.connect('mongodb://localhost:27017/database', {useNewUrlParser: true, useUnifiedTopology: true});
mongoose.set('useFindAndModify', false);


// mongoose schemas
const DjangoSession = mongoose.model('DjangoSession', new mongoose.Schema({id : String,session_key:String,expire_date : Date,session_data : String,}, { collection: 'django_session' }))
const DjangoUsers = mongoose.model('DjangoUsers', new mongoose.Schema({id: Number,last_login: Date,is_superuser: Boolean,username: String,first_name: String,last_name: String,email: String,is_staff: Boolean,is_active: Boolean,date_joined: Date}, { collection: 'auth_user' }))
const dialog = mongoose.model('dialog', new mongoose.Schema({id:Number,first_id:Number,second_id:Number}, { collection: 'messenger_dialog' }))
const messages = mongoose.model('messages', new mongoose.Schema({id:Number,read:Boolean} , { collection: 'messenger_message' }))


// exports 

module.exports = {DjangoSession,DjangoUsers,messages,dialog}