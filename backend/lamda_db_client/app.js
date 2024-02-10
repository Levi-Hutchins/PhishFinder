const express = require("express");
const mongoose = require("mongoose");
require("dotenv").config()
const app = express();
const PORT = process.env.PORT || 3000;


app.get("/", (req, res) => {
  res.status(200);
  res.send("Welcome to root URL of Server");
});
console.log(process.env.URI)
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


// mongoose
//   .connect(process.env.MONGODB_URI)
//   .then(() => {
//     console.log("Connected");
//     app.listen(PORT, (error) => {
//       if (!error) console.log("Success");
//     });
//   })
//   .catch((error) => {
//     console.log(error);
//   });
