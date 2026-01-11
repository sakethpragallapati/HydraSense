const express = require("express");
const dotenv = require("dotenv");
const axios = require("axios");
const cors = require("cors");

dotenv.config()

app = express()
PORT = process.env.PORT || 5000;

app.use(cors())
app.use(express.json());
app.use(express.urlencoded({ extended: true }))

app.get("/",(req,res)=>{
    res.send("Hello World!!");
})

const ML_SERVICE_URL = process.env.FLASK_API_URL || "http://127.0.0.1:7000";
app.post("/predict",async(req,res)=>{

    try{
        const user_data = req.body;

    const response = await axios.post(
        `${ML_SERVICE_URL}/predictData`,
        user_data,
         {
            headers: {
                "Content-Type": "application/json"
            }
        }  
    );
    res.json(response.data)
    }catch(error){
        if (error.response) {
            console.error("Error from Flask Server:", error.response.data);
            res.status(error.response.status).json(error.response.data);
        } else {
            console.error("Error connecting to Flask:", error.message);
            res.status(500).json({ error: "Failed to connect to ML Service" });
        }
    }
})

app.listen(PORT,()=>{
    console.log(`Connected to PORT: ${PORT}`);
})