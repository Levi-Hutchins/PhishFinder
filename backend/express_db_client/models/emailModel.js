const mongoose = require("mongoose");

const emailSchema = new mongoose.Schema(
  {
    email_text: {
      type: String,
      required: true,
      trim: true,
    },
    email_classification: {
      type: Number,
      required: true,
      enum: [0,1]
    },
  },
  {
    timestamps: true,
  }
);

const Email = mongoose.model("Email", emailSchema);

module.exports = Email;
