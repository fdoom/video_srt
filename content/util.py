import os, zipfile,subprocess
from DTO.UrlRequestDTO import UrlRequestDTO
from DTO.AudioRequestDTO import AudioRequestDTO
from fastapi import HTTPException
from moviepy.editor import VideoFileClip
from whisper_util import util as whisper_util

def youtube_download(request: UrlRequestDTO, VIDEO_PATH: str, AUDIO_PATH: str, SRT_PATH: str, ZIP_PATH: str):
    command = [
        'yt-dlp',
        '-f', 'bestvideo+bestaudio/best',
        '--audio-format', 'wav',
        '--merge-output-format', 'mp4',
        '--recode-video', 'mp4',
        '-o', VIDEO_PATH,
        request.url
    ]
    subprocess.run(command)

    video = VideoFileClip(VIDEO_PATH)
    video.audio.write_audiofile(AUDIO_PATH, codec='pcm_s16le')
    whisper_util.transcribe(request, AUDIO_PATH)
    
    with zipfile.ZipFile(ZIP_PATH, 'w') as zipf:
        zipf.write(VIDEO_PATH)
        zipf.write(SRT_PATH)


def audio_transcribe(request: AudioRequestDTO, AUDIO_PATH: str, SRT_PATH: str, ZIP_PATH: str):
    whisper_util.transcribe(request, AUDIO_PATH)
    with zipfile.ZipFile(ZIP_PATH, 'w') as zipf:
        zipf.write(SRT_PATH)