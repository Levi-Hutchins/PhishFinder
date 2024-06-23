const emailService = require('../services/emailService');
const logger = require('../utils/logger');
const logger_ = require('../utils/logger');
require("dotenv").config;

exports.getEmailData = async (req, res) => {
    logger_.info("Request made - [GET] /getEmailData");
    if (req.headers["auth"] !== process.env.AUTH) {
        logger_.warn("Authentication Failed"+ req.body +"\nHeaders: "+ req.headers);
        return res.status(500).json({ message: "Unauthorised" });
      }
      try{
        const emailData = await emailService.findAllEmails({});
        logger_.info("All Data Successfully Returned");
        return res.status(200).json(emailData);
      }catch(error){
        logger_.error("Error occured fetching all emails");
        logger_.error(error.message);
        res.status(500).json({ message: error.message });
      }
}

exports.insertEmailData = async(req, res) =>{
  logger_.info("Request made - [POST] /insert_email_data/");

  const exisitingEmail = await emailService.findEmail(req.body.email_text);
  if (exisitingEmail) {
    logger_.warn("Duplicated Email Text - Not Inserted");
    return res.status(200).json({ message: "Duplicate Email" });
  }

  var email_data = null;
  try {
    email_data = await emailService.createEmail(req.body);
    logger_.info("Successful Insertion: " ,req.body);
    res.status(200).json(email_data);
  } catch (error) {
    logger_.error("Failed Email Insertion ", error);
    res.status(500).json({ message: "Failed Insertion" });
  }
  try {
    const isNewEmailInDB = await emailService.findEmail(email_data);
    if (isNewEmailInDB) logger_.info("Email Inserted Successfully");
  } catch (error) {
    logger_.error("Email Not Found - After Insertion ", error);
  }
}