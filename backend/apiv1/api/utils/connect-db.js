const dotenv = require("dotenv");
const {MongoClient} = require("mongodb")
dotenv.config()



async function connectDB(uri){
    const client = new MongoClient(process.env.MONGODB_URI);
    try{
        await client.connect();
        console.log("Connected to MongoDB");
        return client;
    }finally{
        await client.close();
    }
}

module.exports = connectDB;