import os
import shutil

import uvicorn
from fastapi import FastAPI
from fastapi import File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from blenderbot import Chatbot
from tts import TTS
import stt

app = FastAPI()
origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chatbot = Chatbot()
tts = TTS('kan-bayashi/ljspeech_vits')

# リクエストbodyを定義
class User(BaseModel):
    user_id: int
    name: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/user/sound")
def user_sound():
    return {}

@app.post("/user/response")
def user_response(file: UploadFile=File(...)):
    if file:
        filename = file.filename
        fileobj = file.file
        path = os.path.join('./stt_in', filename)
        upload_dir = open(path,'wb+')
        shutil.copyfileobj(fileobj, upload_dir)
        upload_dir.close()
        
        raw_text = stt.stt(path, language='en')
        print("you->", raw_text)

        
        out_text = chatbot.response(raw_text)
        print("bot->", out_text)
        print("--------------------------------")

        out_file = 'bot.wav'
        audio_file_path = f'./tts_out/{out_file}'
        tts.speech(out_text, output_path=audio_file_path)
        return {'response_url': '/download/response'}

    return {"Error": "アップロードファイルが見つかりません。"}

@app.get('/download/response')
def download():
    out_file = 'bot.wav'
    audio_file_path = f'./tts_out/{out_file}'
    return FileResponse(audio_file_path, filename=out_file, media_type="application/octet-stream")