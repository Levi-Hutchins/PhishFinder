const winston = require('winston');
const {transports } = require("winston");
const { combine, timestamp, printf, colorize, align } = winston.format;
const timestampColorize = require("winston-timestamp-colorize");

require("winston-mongodb");
require("dotenv").config();

const mongodbUri = process.env.MONGODB_URI

const log = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: combine(
    colorize({ all: true }),
    timestamp({
      format: 'YYYY-MM-DD hh:mm:ss.SSS A',
    }),
    align(),
    timestampColorize({ color: "orange" }),
    printf((info) => `[${info.timestamp}] [${info.level}]: ${info.message}\n`)
  ),
  transports: [new winston.transports.Console()],
});

log.add(new transports.MongoDB({
  level: 'info', 
  db: mongodbUri, 
  collection: 'info-logs',
  options: { useUnifiedTopology: true },
  
}));

log.add(new transports.MongoDB({
  level: 'error', 
  db: mongodbUri, 
  collection: 'error-logs',
  options: { useUnifiedTopology: true },

}));
log.add(new transports.MongoDB({
  level: 'warn', 
  db: mongodbUri, 
  collection: 'warn-logs',
  options: { useUnifiedTopology: true },

}));

module.exports = log;