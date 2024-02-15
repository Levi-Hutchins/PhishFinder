const mongoose = require("mongoose");

const linkSchema = new mongoose.Schema(
  {
    link: {
      type: String,
      required: true,
      trim: true
    },
    link_classification: {
      type: Number,
      required: true,
      enum: [0,1]
    },
    scanned_by_VT: {
      type: Boolean,
      required: true,
    },
  },
  {
    timestamps: true,
  }
);

const Link = mongoose.model("Link",linkSchema );

module.exports = Link
