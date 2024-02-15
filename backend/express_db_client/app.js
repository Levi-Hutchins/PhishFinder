const express = require("express");
const { body, validationResult } = require("express-validator");
const helmet = require("helmet");
const serverless = require("serverless-http");
const { exec } = require("child_process");
const rateLimit = require("express-rate-limit");
const morgan = require("morgan");
const mongoose = require("mongoose");
const Link = require("./models/linkModel");
const Email = require("./models/emailModel");

require("dotenv").config();
const app = express();
//const PORT = process.env.PORT || 3000;

// some limitting to prevent any spamming
const limiter = rateLimit({
  // 100 requests per 15 min
  windowsMs: 15 * 50 * 100,
  max: 100,
});

app.use(limiter);
app.use(express.json());
app.use(helmet());
app.use(morgan);

app.use((error, req, res, next) => {
  console.error(error.stack || error);
  res.status(500).send("An Error Occured");
});

app.get("/home", (req, res) => {
  res.status(200);
  res.send("Welcome to root URL of Server");
});

app.post(
  "/insert_link_data",
  [
    body("url").isURL(),
    body("description").optional().isLength({ min: 1, max: 500 }),
  ],
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    try {
      const link_data = await Link.create(req.body);
      res.status(200).json(link_data);
    } catch (error) {
      console.error(error);
      res.status(500).json({ message: error.message });
    }
  }
);

app.post("/insert_email_data", async (req, res) => {
  try {
    const email_data = await Email.create(req.body);
    res.status(200).json(email_data);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: error.message });
  }
});

app.get("/get_all_link_data", async (req, res) => {
  try {
    const all_data = await Link.find({});
    res.status(200).json(all_data);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: error.message });
  }
});
app.get("/get_all_email_data", async (req, res) => {
  try {
    const all_data = await Email.find({});
    res.status(200).json(all_data);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: error.message });
  }
});

app.get("/health_status", (req, res) => {
  exec("npm test", (error, stdout, stderr) => {
    console.log("here");
    if (error) {
      console.error("test error ", error);
      return res.status(500).json({ success: false, output: stderr });
    }
    res.status(200).json({ success: true, output: stdout });
  });
});

async function connectToDatabase() {
  if (
    mongoose.connection.readyState === 0 ||
    mongoose.connection.readyState === 3
  ) {
    await mongoose.connect(process.env.MONGODB_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log("DB Connected");
  }
}
// module.exports.handler = async (event, context) => {
//   context.callbackWaitsForEmptyEventLoop = false;
//   await connectToDatabase();

//   return serverless(app)(event, context);
// };
