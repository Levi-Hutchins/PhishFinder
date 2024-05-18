const Email = require('../models/Email');

exports.findAllEmails = () => Email.find({});
exports.createEmail = (emailData) => Email.create(emailData);