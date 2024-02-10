const mongoose = require("mongoose");

const linkSchema = mongoose.Schema(
  {
    link: {
      type: String,
      required: true,
    },
    link_classification: {
      type: Number,
      required: true,
    },
    scanned_by_VT: {
      type: Number,
      required: true,
    },
  },
  {
    timestamps: true,
  }
);

const Link = mongoose.model("Link",linkSchema );

module.exports = Link
