import whisper
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
from pyannote.audio import Pipeline
import json

# Load Whisper model
whisper_model = whisper.load_model("turbo")

# Load punctuation restoration model
tokenizer = AutoTokenizer.from_pretrained("oliverguhr/fullstop-punctuation-multilang-large")
punct_model = AutoModelForTokenClassification.from_pretrained("oliverguhr/fullstop-punctuation-multilang-large")
punct_model.eval()

# Load pyannote diarization pipeline (this requires your HuggingFace token)
diarization_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")
diarization_pipeline.to(torch.device("cuda"))


def transcribe_with_segments(audio_path):
    """Transcribe audio and return timestamped segments."""
    result = whisper_model.transcribe(audio_path)
    return result.get("segments", [])

def restore_punctuation(text):
    """Restore punctuation and capitalization using the punctuation model."""
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        logits = punct_model(**inputs).logits
    predictions = torch.argmax(logits, dim=-1)[0].tolist()
    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])

    punctuated_text = ""
    for token, label in zip(tokens, predictions):
        if token.startswith("##"):
            punctuated_text += token[2:]
        else:
            punctuated_text += " " + token if punctuated_text else token

        # Labels: 0=O (no punctuation), 1=PERIOD, 2=COMMA, 3=QUESTION_MARK
        if label == 1:
            punctuated_text += "."
        elif label == 2:
            punctuated_text += ","
        elif label == 3:
            punctuated_text += "?"

    punctuated_text = punctuated_text.strip()
    if punctuated_text:
        punctuated_text = punctuated_text[0].upper() + punctuated_text[1:]
    return punctuated_text

def diarize_audio(audio_path):
    """Run diarization and return speaker segments with timestamps."""
    diarization = diarization_pipeline(audio_path)
    diarized_segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        diarized_segments.append({
            "start": turn.start,
            "end": turn.end,
            "speaker": speaker
        })
    return diarized_segments

def merge_transcript_and_diarization(transcript_segments, diarized_segments):
    """Match each transcript segment to a speaker based on overlap."""
    merged = []

    for t_seg in transcript_segments:
        # Find diarization segments overlapping this transcript segment
        candidates = [d for d in diarized_segments if not (d["end"] < t_seg["start"] or d["start"] > t_seg["end"])]

        if candidates:
            # Pick the speaker with the longest overlap
            best_speaker = None
            max_overlap = 0
            for c in candidates:
                overlap_start = max(t_seg["start"], c["start"])
                overlap_end = min(t_seg["end"], c["end"])
                overlap = overlap_end - overlap_start
                if overlap > max_overlap:
                    max_overlap = overlap
                    best_speaker = c["speaker"]
        else:
            best_speaker = "Unknown"

        merged.append({
            "start": t_seg["start"],
            "end": t_seg["end"],
            "speaker": best_speaker,
            "text": t_seg["text"]
        })

    return merged

def create_clean_transcript_with_speakers(audio_path, output_json):
    print("Transcribing audio with Whisper...")
    transcript_segments = transcribe_with_segments(audio_path)

    print("Restoring punctuation...")
    for seg in transcript_segments:
        seg["text"] = restore_punctuation(seg["text"])

    print("Running speaker diarization...")
    diarized_segments = diarize_audio(audio_path)

    print("Merging transcript and diarization...")
    merged = merge_transcript_and_diarization(transcript_segments, diarized_segments)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)

    print(f"Transcript with speakers saved to {output_json}")

if __name__ == "__main__":
    audio_file = "../audio/FedeNickWav.wav"  # Path to your audio file
    output_file = "clean_transcript_with_speakers.json"
    create_clean_transcript_with_speakers(audio_file, output_file)
