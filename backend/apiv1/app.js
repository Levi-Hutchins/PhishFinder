const express = require("express");
const routes = require("./routes");

const logger = require("./api/utils/logger");
const mongoose = require("mongoose");

require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use('/api', routes);

app.use((error, req, res, next) => {
  logger.error("Unexpected Error Occured");
  res.status(500).send("An Error Occured");
});

const startServer = async () => {
  try {
    await mongoose.connect(process.env.MONGODB_URI, {
      useNewURLParser: true,
      useUnifiedTopology: true,
    });
    logger.info("MongoDB Connected Established");
    app.listen(PORT, () => logger.silly("Server Now Running"));
  } catch (error) {
    logger.error("Error connection to MongoDB ", error);
  }
};

startServer();
module.exports = app;