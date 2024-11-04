from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from DTO.UrlRequestDTO import UrlRequestDTO
from DTO.NllbRequestDTO import NllbRequestDTO
from fastapi import HTTPException
import torch, json

model_name = 'facebook/nllb-200-3.3B'
nllb_model = None
tokenizer = None
device = "cuda" if torch.cuda.is_available() else "cpu"



def init():
    global nllb_model, tokenizer, device
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    nllb_model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)

nllb_lang = None
with open('nllb-mapping.json', 'r') as f:
    nllb_lang = json.load(f)

def support_language_list():
    return nllb_lang

def end():
    global nllb_model, tokenizer
    del nllb_model
    del tokenizer
    torch.cuda.empty_cache()

def find_keys_by_value(request):
    global nllb_lang
    request.lang_to = [key for key, value in nllb_lang.items() if value == request.lang_to]
    if not request.lang_to:
        raise HTTPException(status_code=422, detail="This lang_to is not supported")
    else:
        request.lang_to = request.lang_to[0]
    return request

def srt_translate(result, request: UrlRequestDTO):
    init()
    for segment in result['segments']:
        segment['text'] = translate(segment['text'], request.lang_to)
    end()
    return result

def str_list_translate(request: NllbRequestDTO):
    init()
    request.content = [translate(text, request.lang_to) for text in request.content]
    end()
    return request

def translate(text: str, lang_to: str):
    global nllb_model, tokenizer
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
    translated_tokens = nllb_model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id[lang_to], early_stopping=True, num_beams=10)
    return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]