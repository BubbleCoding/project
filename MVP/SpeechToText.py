import whisper

def transcribe_audio():
    model = whisper.load_model("turbo")
    result = model.transcribe("audio.mp3")
    print(result["text"])
    return(result["text"])