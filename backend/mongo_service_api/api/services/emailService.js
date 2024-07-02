const Email = require('../models/Email');
const validator = require('validator')

exports.findAllEmails = () => Email.find({});
exports.findEmail = (emailText) => Email.findOne({email_text: validator.escape(emailText)});
exports.createEmail = (emailData) => Email.create(emailData);