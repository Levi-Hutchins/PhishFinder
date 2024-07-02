const logger_ = require('../utils/logger');
require("dotenv").config;

exports.generalHealth = async (req, res) => {
    logger_.info("Request made - [GET] /health_status");
    res.send("Server Currently Running...");
}