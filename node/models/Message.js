const mongoose = require("mongoose");
const Schema = mongoose.Schema;

var MessageSchema = new Schema(
  {
    id: Number,
    seen: Boolean,
    sender_id : Number,
  },
  { collection: "messenger_message" , toObject: { virtuals: true }}
);

MessageSchema.virtual('conversation', {
  ref: 'conversation',
  localField: 'conversation_id', 
  foreignField: 'id', 
  justOne: true
});

module.exports = mongoose.model("message", MessageSchema);
