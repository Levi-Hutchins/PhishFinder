const emailService = require('../services/emailService');
const logger_ = require('../utils/logger');
require("dotenv").config;

exports.getEmailData = async (req, res) => {
    logger_.info("Request made - [GET] /getEmailData");

    if (req.headers["auth"] != process.env.AUTH || req.headers["auth"] == undefined) {
        logger_.warn("Authentication Failed"+ JSON.stringify(req.body) +"\nHeaders: "+ JSON.stringify(req.headers));
        return res.status(401).json({ message: "Unauthorised" });
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

  if (req.headers["auth"] !== process.env.AUTH || req.headers["auth"] == undefined) {
    logger_.warn("Authentication Failed"+ JSON.stringify(req.body) +"\nHeaders: "+ JSON.stringify(req.headers));
    return res.status(401).json({ message: "Unauthorised" });
  }

  const exisitingEmail = await emailService.findEmail(req.body.email_text);
  if (exisitingEmail) {
    logger_.warn("Duplicated Email Text - Not Inserted");
    return res.status(200).json({ message: "Duplicate Email" });
  }

  var emailData = null;
  try {
    emailData = await emailService.createEmail(req.body);
    logger_.info("Successful Insertion: " ,JSON.stringify(req.body));
    res.status(200).json(emailData);
  } catch (error) {
    logger_.error("Failed Email Insertion ", JSON.stringify(error));
    res.status(500).json({ message: "Failed Insertion" });
  }
  try {
    const isNewEmailInDB = await emailService.findEmail(emailData);
    if (isNewEmailInDB) logger_.info("Email Inserted Successfully");
  } catch (error) {
    logger_.error("Email Not Found - After Insertion ", JSON.stringify(error));
  }
}