const Link = require('../models/Link');

exports.findAllLinks = () => Link.find({});
exports.createLink = (linkData) => Link.create(linkData);