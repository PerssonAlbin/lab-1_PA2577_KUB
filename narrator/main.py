from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import openai
import io

app = FastAPI()

# Set your OpenAI API key
openai.api_key = None


class TextInput(BaseModel):
    text: str
    voice: str = "alloy"  # Default voice


@app.post("/narrate")
async def narrate(text_input: TextInput):
    response = openai.audio.speech.create(
        model="tts-1", input=text_input.text, voice=text_input.voice
    )

    audio_content = await response.aread()
    audio_stream = io.BytesIO(audio_content)
    return StreamingResponse(audio_stream, media_type="audio/mpeg")
