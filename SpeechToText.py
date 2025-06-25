import whisper

def transcribe_with_segments(audio_path):
    model = whisper.load_model("turbo")
    result = model.transcribe(audio_path)
    return result.get("segments", [])

if __name__ == "__main__":
    segments = transcribe_with_segments("audio.mp3")
    for seg in segments:
        print(f"[{seg['start']:.2f}-{seg['end']:.2f}] {seg['text']}")
