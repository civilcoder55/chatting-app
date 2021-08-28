// modules imports 
const mongoose = require('mongoose')
mongoose.Promise = global.Promise;

// mongoose configs
const host = process.env.MONGO_HOST || 'mongodb://localhost:27017/database'
mongoose.connect(host, {useNewUrlParser: true, useUnifiedTopology: true});
mongoose.set('useFindAndModify', false);