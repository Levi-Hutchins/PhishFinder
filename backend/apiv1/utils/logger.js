const { createLogger, format, transports } = require("winston");
const winstonDevConsole = require("@epegzz/winston-dev-console").default;
const util = require("util");

let log = createLogger({
  level: 'silly', // or use process.env.LOG_LEVEL
});

log = winstonDevConsole.init(log);
log.add(
  winstonDevConsole.transport({
    showTimestamps: true,
    addLineSeparation: true,
  })
);


module.exports = log