import os
import shutil
import datetime

from typing import List
import uvicorn
from fastapi import FastAPI
from fastapi import File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from blenderbot import Chatbot
# from dialog_gpt import Chatbot
from tts import TTS
from stt import STT
from sadtalker import SadTalker

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
stt = STT(size='small')

checkpoint_dir = '../SadTalker/checkpoints'
config_path = '../SadTalker/src/config'
talker = SadTalker(
    checkpoint_path=checkpoint_dir, config_path=config_path
)

img_path = './avater/no_back_crop1.png'
movies_path = './movies'

# リクエストbodyを定義
class HistoryMessage(BaseModel):
    history: List[str] = []
    user_wav_path: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/upload/sound")
def upload(file: UploadFile=File(...)):
    if file:
        fileobj = file.file

        now = datetime.datetime.now()
        ts = datetime.datetime.timestamp(now)
        out_file = f'user_{ts}.wav'

        path = os.path.join('./stt_in', out_file)
        upload_dir = open(path,'wb+')
        shutil.copyfileobj(fileobj, upload_dir)
        upload_dir.close()
        res = {'filename': out_file}
    else:
        res = {"Error": "アップロードファイルが見つかりません。"}
    return res

@app.post("/user/response")
def user_response(body: HistoryMessage):
    print(body)
    path = os.path.join('./stt_in', body.user_wav_path)
    raw_text = stt.stt(path, language='en')
    history = body.history
    print("you->", raw_text)

    out_text = chatbot.response(raw_text)
    print("bot->", out_text)
    print("--------------------------------")

    now = datetime.datetime.now()
    ts = datetime.datetime.timestamp(now)
    out_file = f'bot_{ts}.wav'
    audio_file_path = f'./tts_out/{out_file}'
    tts.speech(out_text, output_path=audio_file_path)

    tmp_img_path = "./tmp/image.png"
    tmp_audio_path = "./tmp/audio.wav"
    shutil.copyfile(img_path, tmp_img_path)
    shutil.copyfile(audio_file_path, tmp_audio_path)
    output_path = talker.execute(
        tmp_img_path, tmp_audio_path,
        preprocess='resize',
        still_mode=False,
        use_enhancer=False,
        result_dir=movies_path
    )

    return {
        'response_url': f'/download/response/{out_file}',
        'user_uttence': raw_text,
        'bot_response': out_text
    }

@app.get('/download/response/{out_file}')
def download(out_file):
    audio_file_path = f'./tts_out/{out_file}'
    return FileResponse(audio_file_path, filename=out_file, media_type="application/octet-stream")