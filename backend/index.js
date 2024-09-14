// index.js
const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");

// Create an instance of Express
const app = express();

// Set the folder where files will be stored
// Shall be changed later
const uploadFolder = path.join(__dirname, "uploads");

// Ensure the upload folder exists
if (!fs.existsSync(uploadFolder)) {
  fs.mkdirSync(uploadFolder);
}

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadFolder); // Store in the 'uploads' directory
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + "-" + Math.round(Math.random() * 1e9);
    cb(null, uniqueSuffix + "-" + file.originalname); // Create a unique filename
  },
});

const upload = multer({ storage: storage });

// Create a POST route to handle the file upload
app.post("/upload", upload.single("file"), (req, res) => {
  // The file is available as req.file
  if (!req.file) {
    return res.status(400).send({ message: "No file uploaded" });
  }

  // Send success response
  res.status(200).send({
    message: "File uploaded successfully",
    fileName: req.file.filename,
    filePath: req.file.path,
  });
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
