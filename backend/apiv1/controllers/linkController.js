const linkService = require("../services/linkService");
const logger_ = require("../utils/logger");
require("dotenv").config;

exports.getLinkData = async (req, res) => {
  logger_.info("Request made - [GET] /getLinkData");
  if (req.headers["auth"] !== process.env.AUTH) {
    logger_.warn("Authentication Failed", req.body);
    return res.status(500).json({ message: "Unauthorised" });
  }

  try {
    const all_data = await linkService.findAllLinks({});
    res.status(200).json(all_data);
    logger_.info("All Data Successfully Returned");
  } catch (error) {
    logger_.error("Error In Returning All Data");
    logger_.error(error);
    res.status(500).json({ message: "Fetch Fail" });
  }
};

exports.insertLinkData = async (req, res) => {
  logger_.info("Request made - [POST] /insert_link_data");
  if (!errors.isEmpty()) {
    logger_.error("Validation Failed - [POST] /insert_link_data");
    return res.status(400).json({ message: "Bad Input" });
  }
  const existingLink = await linkService.findOne({ link: req.body.link });
  if (existingLink) {
    logger_.warn("Duplicate Link - Not Inserted");
    return res.status(409).json({ message: "Duplicate Link" });
  }

  try {
    const link_data = await linkService.createLink(req.body);
    res.status(201).json(link_data);
    logger_.info(`${link_data.link} Inserted Successfully`);
  } catch (error) {
    logger_.error(`Failed Insertion: ${error.message}`);
    res.status(500).json({ message: "Failed Insertion" });
  }
};
