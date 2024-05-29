const Email = require('../models/Email');

exports.findAllEmails = () => Email.find({});
exports.findEmail = (email) => Email.findOne({email});
exports.createEmail = (emailData) => Email.create(emailData);