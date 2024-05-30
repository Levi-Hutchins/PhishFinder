const { createLogger, format, transports } = require("winston");
const winstonDevConsole = require("@epegzz/winston-dev-console").default;
require("dotenv").config;
require("winston-mongodb");

const mongodbUri = process.env.MONGODB_URI


let log = createLogger({
  level: 'silly',
  format: format.combine(
    format.timestamp(),
    format.json()
  )
});

log = winstonDevConsole.init(log);
log.add(
  winstonDevConsole.transport({
    showTimestamps: true,
    addLineSeparation: true,
  })
);


log.add(new transports.MongoDB({
  level: 'info', 
  db: mongodbUri, 
  collection: 'logs',
  options: { useUnifiedTopology: true }
}));

module.exports = log;
