const Link = require('../models/Link');

exports.findAllLinks = () => Link.find({});
exports.findLink = (link) => Link.findOne({link});
exports.createLink = (linkData) => Link.create(linkData);