const express = require("express");
const mongoose = require("mongoose");
require("dotenv").config()
const app = express();
const PORT = process.env.PORT || 3000;
const Link = require("./models/linkModel")
const Email = require("./models/emailModel")
app.use(express.json())
app.get("/", (req, res) => {
  res.status(200);
  res.send("Welcome to root URL of Server");
});

app.post("/insert_link_data", async(req, res) => {
    try{
        const link_data = await Link.create(req.body)
        res.status(200).json(link_data);
    }catch(error){
        console.error(error)
        res.status(500).json({message: error.message});
    }
})

app.post("/insert_email_data", async(req, res) => {
    try{
        const email_data = await Email.create(req.body)
        res.status(200).json(email_data);
    }catch(error){
        console.error(error)
        res.status(500).json({message: error.message});
    }
})


const startServer = async () => {
    try{
        await mongoose.connect(process.env.MONGODB_URI,{
            useNewURLParser: true,
            useUnifiedTopology: true,
        });
        console.log("DB Connected")
        app.listen(PORT, () => console.log("Server running on port ",PORT))
    }catch(error){
        console.log("Error connection to MongoDB ", error)
    }
}

startServer()


