const express = require('express');
const axios = require('axios');
const multer = require('multer');
const FormData = require('form-data');
const upload = multer();
const db = require('./db');
const app = express();
const port = process.env.PORT || 4000;

app.use(express.json());

const transcriberServiceUrl = process.env.TRANSCRIBER_SERVICE_URL || 'http://transcriber-service:8000';
const narratorServiceUrl = process.env.NARRATOR_SERVICE_URL || 'http://narrator-service:8000';

const logToDatabase = async (message) => {
    try {
        await db.query(
            'INSERT INTO logs (message, created_at) VALUES ($1, NOW())',
            [message]
        );
    } catch (error) {
        console.error('Error logging to database:', error);
    }
};

app.post('/transcribe', upload.single('audio_file'), async (req, res) => {
    try {
        const formData = new FormData();
        formData.append('audio_file', req.file.buffer, {
            filename: req.file.originalname,
            contentType: req.file.mimetype,
        });

        const response = await axios.post(`${transcriberServiceUrl}/transcribe`, formData, {
            headers: formData.getHeaders(),
        });

				await logToDatabase(response.data.text);
        res.json(response.data);
    } catch (error) {
        console.error('Error in /transcribe:', error);
        res.status(500).json({ error: 'Error processing transcription' });
    }
});

app.post('/narrate', async (req, res) => {
	try {
		await logToDatabase(req.body.text);

  	const response = await axios.post(`${narratorServiceUrl}/narrate`, req.body, {
    	responseType: 'arraybuffer',
    });
    res.set('Content-Type', 'audio/mpeg');
    res.send(response.data);
  } catch (error) {
  	let errorData;
    if (error.response && error.response.data) {
    	errorData = Buffer.from(error.response.data).toString('utf-8');
    } else {
    	errorData = error.message;
    }
    console.error('Error in /narrate:', errorData);
    res.status(500).json({ error: 'Error processing narration' });
  }
});


app.listen(port, () => {
    console.log(`Backend listening at http://localhost:${port}`);
});
