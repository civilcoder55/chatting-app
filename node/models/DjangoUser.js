const mongoose = require("mongoose");
const Schema = mongoose.Schema;

var DjangoUserSchema = new Schema(
  {
    id: Number,
    last_login: Date,
    is_superuser: Boolean,
    username: String,
    first_name: String,
    last_name: String,
    email: String,
    is_staff: Boolean,
    is_active: Boolean,
    date_joined: Date,
  },
  { collection: "users_user" }
);

module.exports = mongoose.model("djangouser", DjangoUserSchema);
