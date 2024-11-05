# 영상 다운로드 및 자막 번역 프로그램

이 프로그램는 여러 사이트([지원 사이트 목록](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md))에서 영상을 다운로드하고, 영상의 음성을 자막으로 변환한 후 번역하는 기능을 제공

## 주요 기능

- **영상 다운로드**: 지정된 URL에서 영상을 다운로드
- **음성 인식**: Whisper-large-v2(전사모델: [허깅페이스](https://huggingface.co/openai/whisper-large-v2))을 활용하여 음성을 텍스트로 변환하고 자막을 생성, [지원 언어 목록](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py#L10)
- **자막 번역**: NLLB-200-3.3B(번역모델: [허깅페이스](https://huggingface.co/facebook/nllb-200-3.3B))을 활용하여 자막의 번역을 진행, [지원 언어 목록](https://scontent-gmp1-1.xx.fbcdn.net/v/t39.8562-6/292295068_402295381932691_8903854229220968087_n.pdf?ccb=1-7&_nc_sid=e280be&_nc_ohc=UvBRoLJCRZoQ7kNvgFZHTK2&_nc_zt=14&_nc_ht=scontent-gmp1-1.xx&_nc_gid=ATURscYil2lHJ0q3etjO5VB&oh=00_AYAcwu4SXzptlY3zImE45C4UbjKlXKGGR2STT6nH77Ss_g&oe=672F5453#page=13)

## 설치 및 진행
1. `git`과 `Docker`를 설치
2. `git clone https://github.com/fdoom/video_srt.git`
3. `cd video_srt`
4. `docker compose up --build` 이후 whisper와 nllb 모델을 다운받는 과정을 거친다.
5. `http://localhost:81/docs` 혹은 `http://localhost:8001/docs` 접속 후 `POST /` 요청에 `url`은 웹 주소, `lang_from`은 Whsiper 모델이 지원하는 언어를, `lang_to`는 nllb 모델이 지원하는 언어를 기입 후 `Execute` 버튼 클릭하면 원하는 영상과 자막이 zip파일로 압축되어 반환된다.
    - 기본적으로 서버이기에 해당 프로그램을 이용해서 서버로서 활용 가능하다.

## 권장 사양
1. NVIDIA 그래픽 카드 VRAM 16GB 이상
2. RAM 48GB 이상
