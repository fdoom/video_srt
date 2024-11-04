FROM pytorch/pytorch:2.3.0-cuda11.8-cudnn8-runtime

RUN pip3 install fastapi uvicorn[standard] yt-dlp moviepy openai-whisper pydub transformers==4.41.1 python-multipart

WORKDIR /app

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]