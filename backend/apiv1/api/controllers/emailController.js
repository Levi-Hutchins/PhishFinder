const emailService = require('../services/emailService');
const logger_ = require('../utils/logger');
require("dotenv").config;

exports.getEmailData = async (req, res) => {
    logger_.info("Request made - [GET] /getEmailData");
    if (req.headers["auth"] !== process.env.AUTH) {
        logger_.warn("Authentication Failed", req.body);
        logger_.warn("Headers: ", req.headers )
        return res.status(41).json({ message: "Unauthorised" });
      }
}