const express = require("express");
const logger = require("./logger");

const mongoose = require("mongoose");
const Link = require("./models/linkModel");
const Email = require("./models/emailModel");

const { body, validationResult } = require("express-validator");

require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.use((error, req, res, next) => {
  logger.error("Occurred Here");
  logger.error(error.stack || error);
  res.status(500).send("An Error Occured");
});

app.get("/health_status", (req, res) => {
  logger.info("Request made - [GET] /health_status");
  res.send("Server Currently Running...");
});

app.post(
  "/insert_link_data",
  [
    body("link").isURL(),
    body("description").optional().isLength({ min: 1, max: 500 }),
  ],
  async (req, res) => {
    logger.info("Request made - [POST] /insert_link_data/");
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      logger.warn("Validation Failed - [POST] /insert_link_data");
      return res.status(500).json({ message: "Bad Input" });
    }

    const existingLink = await Link.findOne({ link: req.body.link });
    if (existingLink) {
      logger.warn("Duplicate Link - Not Inserted");
      return res.status(500).json({ message: "Duplicate Link" });
    }
    var link_data = null;
    try {
      link_data = await Link.create(req.body);
      res.status(200).json(link_data);
    } catch (error) {
      logger.error("Failed Link Insertion");
      logger.error(error);
      res.status(500).json({ message: "Failed Insertion" });
    }
    try {
      const isNewLinkInDB = await Link.findOne(link_data);
      if (isNewLinkInDB)
        logger.info(isNewLinkInDB.link + " Inserted Successfully");
    } catch (error) {
      logger.error("Link Not Found - After Insertion");
      logger.error(error);
    }
  }
);

app.post("/insert_email_data", async (req, res) => {
  logger.info("Request made - [POST] /insert_email_data/");

  const exisitingEmail = await Email.findOne({
    email_text: req.body.email_text,
  });
  console.log(exisitingEmail);
  if (exisitingEmail) {
    logger.warn("Duplicated Email Text - Not Inserted");
    return res.status(500).json({ message: "Duplicate Email" });
  }

  var email_data = null;
  try {
    email_data = await Email.create(req.body);
    res.status(200).json(email_data);
  } catch (error) {
    logger.error("Failed Email Insertion");
    logger.error(error);
    res.status(500).json({ message: "Failed Insertion" });
  }
  try {
    const isNewEmailInDB = await Email.findOne(email_data);
    if (isNewEmailInDB) logger.info("Email Inserted Successfully");
  } catch (error) {
    logger.error("Email Not Found - After Insertion");
    logger.error(error);
  }
});

app.get("/get_all_link_data", async (req, res) => {
  logger.info("Request made - [GET] /get_all_link_data/");

  if (req.body.auth != process.env.AUTH) {
    logger.warn("Authentication Failed", req.body);
    return res.status(500).json({ message: "Unauthorised" });
  }

  try {
    const all_data = await Link.find({});
    res.status(200).json(all_data);
    logger.info("All Data Successfully Returned");
  } catch (error) {
    logger.error("Error In Returning All Data");
    logger.error(error);
    res.status(500).json({ message: "Fetch Fail" });
  }
});

app.get("/get_all_email_data", async (req, res) => {
  logger.info("Request made - [GET] /get_all_link_data/");

  if (req.body.auth != process.env.AUTH) {
    logger.warn("Authentication Failed", req);
    return res.status(500).json({ message: "Unauthorised" });
  }
  try {
    const all_data = await Email.find({});
    res.status(200).json(all_data);
    logger.info("All Data Successfully Returned");
  } catch (error) {
    logger.error("Error In Returning All Data");
    logger.error(error);
    res.status(500).json({ message: error.message });
  }
});

const startServer = async () => {
  try {
    await mongoose.connect(process.env.MONGODB_URI, {
      useNewURLParser: true,
      useUnifiedTopology: true,
    });
    logger.silly("MongoDB Connected Established");
    app.listen(PORT, () => logger.silly("Server Now Running"));
  } catch (error) {
    logger.error("Error connection to MongoDB ", error);
  }
};

startServer();
