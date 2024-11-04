from fastapi import FastAPI, BackgroundTasks, HTTPException, File, UploadFile, Body
from fastapi.responses import FileResponse
from starlette.requests import Request
from content import util as content_util
from DTO.UrlRequestDTO import UrlRequestDTO
from DTO.NllbRequestDTO import NllbRequestDTO
from DTO.AudioRequestDTO import AudioRequestDTO
from whisper_util import util as whisper_util
from contextlib import asynccontextmanager
from typing import List, Dict
import torch, os, whisper, json
from whisper.utils import get_writer
from nllb import util as nllb_util
from pydub import AudioSegment
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    whisper_util.init()
    whisper_util.end()
    nllb_util.init()
    nllb_util.end()
    yield
    print("pytorch end")

app = FastAPI(lifespan=lifespan)

semaphore = asyncio.Semaphore(1)

@app.middleware("http")
async def limit_requests(request: Request, call_next):
    async with semaphore:
        response = await call_next(request)
    return response

VIDEO_PATH = 'download_video.mp4'
AUDIO_PATH = 'download_video.wav'
SRT_PATH = 'download_video.srt'
ZIP_PATH = 'download.zip'

paths_to_remove = [VIDEO_PATH, AUDIO_PATH, SRT_PATH, ZIP_PATH]
def remove_file():
    for path in paths_to_remove:
        if os.path.exists(path):
            os.remove(path)

@app.post("/")
def read_url(request: UrlRequestDTO, background_tasks: BackgroundTasks):
    request = find_keys_by_value(request)
    try:
        content_util.youtube_download(request, VIDEO_PATH, AUDIO_PATH, SRT_PATH, ZIP_PATH)
    except Exception as e:
        raise HTTPException(status_code=422, detail="This URL is not supported")
    
    background_tasks.add_task(remove_file)
    return FileResponse(
        ZIP_PATH,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={ZIP_PATH}"}
    )

@app.get("/lang_from_list")
async def whisper_support_lang_list():
    return whisper_util.support_language_list()

@app.get("/lang_to_list")
async def nllb200_support_lang_list():
    return nllb_util.support_language_list()

def find_keys_by_value(request):
    if request.lang_from is not None:
        request = whisper_util.find_keys_by_value(request)
    if request.lang_to is not None:
        request = nllb_util.find_keys_by_value(request)
    return request

@app.post("/contents_translate")
def contents_translate(request: NllbRequestDTO):
    if not request.lang_to or not request.content:
        raise HTTPException(status_code=400, detail="Invalid input data")
    request = nllb_util.find_keys_by_value(request)
    return nllb_util.str_list_translate(request)

@app.post("/upload/")
def upload_file(background_tasks: BackgroundTasks, lang_from: str = None, lang_to: str = None, file: UploadFile = File(...)):
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Invalid file extension. Only .wav files are allowed.")

    file_content = file.file.read()
    with open(AUDIO_PATH, 'wb') as out_file:
        out_file.write(file_content)

    try:
        audio = AudioSegment.from_wav(AUDIO_PATH)
    except Exception as e:
        os.remove(AUDIO_PATH)
        raise HTTPException(status_code=400, detail="Invalid audio file.")

    request = AudioRequestDTO(lang_from=lang_from, lang_to=lang_to)
    request = find_keys_by_value(request)
    content_util.audio_transcribe(request, AUDIO_PATH, SRT_PATH, ZIP_PATH)
    background_tasks.add_task(remove_file)
    return FileResponse(
        ZIP_PATH,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={ZIP_PATH}"}
    )