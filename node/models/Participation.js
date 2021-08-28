const mongoose = require("mongoose");
const Schema = mongoose.Schema;

var ParticipationSchema = new Schema(
  {
    id: Number,
    conversation_id:Number,
    user_id:Number,
    with_user_id:Number,
    last_message_seen_id:Number,
  },
  { collection: "messenger_participation" }
);



module.exports = mongoose.model("participation", ParticipationSchema);
