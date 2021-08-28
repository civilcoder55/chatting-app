const mongoose = require("mongoose");
const Schema = mongoose.Schema;

var DjangoSessionSchema = new Schema(
  {
    id: String,
    session_key: String,
    expire_date: Date,
    session_data: String
  },
  { collection: "django_session" }
);

module.exports = mongoose.model("djangosession", DjangoSessionSchema);
