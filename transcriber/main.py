from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import openai
import logging
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.post("/transcribe")
async def transcribe(audio_file: UploadFile = File(...)):
    try:
        # Log file details
        logging.info(
            f"Received file: {audio_file.filename} with content type: {audio_file.content_type}"
        )

        # Validate file type
        if audio_file.content_type not in [
            "audio/flac",
            "audio/m4a",
            "audio/mp3",
            "audio/mp4",
            "audio/mpeg",
            "audio/mpga",
            "audio/oga",
            "audio/ogg",
            "audio/wav",
            "audio/webm",
        ]:
            logging.error("Unsupported file format")
            return JSONResponse(
                {
                    "error": "Unsupported file format. Please upload a supported audio file."
                },
                status_code=400,
            )

        # Save file temporarily
        temp_file_path = f"/tmp/{audio_file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await audio_file.read())

        # Transcribe using OpenAI
        with open(temp_file_path, "rb") as file_to_transcribe:
            response = openai.audio.transcriptions.create(
                model="whisper-1",
                file=file_to_transcribe,  # Correctly pass the file-like object
            )

        # Return transcription
        return {"transcription": response.text}

    except Exception as e:
        # Log exception details
        logging.error(f"Error occurred: {str(e)}", exc_info=True)
        return JSONResponse(
            {"error": f"Internal Server Error: {str(e)}"}, status_code=500
        )
