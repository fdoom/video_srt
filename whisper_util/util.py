import whisper, torch, os
from whisper.utils import get_writer
from nllb import util as nllb_util
from fastapi import HTTPException
whisper_model = None
whisper_lang = whisper.tokenizer.LANGUAGES
device = "cuda" if torch.cuda.is_available() else "cpu"

def init():
    global whisper_model
    whisper_model = whisper.load_model("large-v2", device=device)

def transcribe(request, AUDIO_PATH: str):
    global whisper_model
    init()
    result = whisper_model.transcribe(AUDIO_PATH, language=request.lang_from, beam_size=10, best_of=10)
    end()
    
    if request.lang_to is not None:
        result = nllb_util.srt_translate(result, request)
    writer = get_writer(output_format='srt', output_dir='./')
    writer(result, AUDIO_PATH)

def support_language_list():
    return whisper_lang

def end():
    global whisper_model
    del whisper_model
    torch.cuda.empty_cache()

def find_keys_by_value(request):
    global whisper_lang
    request.lang_from = [key for key, value in whisper_lang.items() if value == request.lang_from]
    if not request.lang_from:
        raise HTTPException(status_code=422, detail="This lnag_from is not supported")
    else:
        request.lang_from = request.lang_from[0]
    return request