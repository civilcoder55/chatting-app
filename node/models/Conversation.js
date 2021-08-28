const mongoose = require("mongoose");
const Schema = mongoose.Schema;

var ConversationSchema = new Schema(
  {
    id: Number,
  },
  { collection: "messenger_conversation" }
);

ConversationSchema.virtual('participation', {
  ref: 'participation',
  localField: 'id', 
  foreignField: 'conversation_id', 
  justOne: true
});

module.exports = mongoose.model("conversation", ConversationSchema);
