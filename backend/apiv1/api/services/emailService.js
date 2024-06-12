const Email = require('../models/Email');

exports.findAllEmails = () => Email.find({});
exports.findEmail = (emailText) => Email.findOne({email_text: emailText});
exports.createEmail = (emailData) => Email.create(emailData);