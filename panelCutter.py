import json
import ollama

def load_transcript(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def chunk_transcript(transcript, chunk_size=10):
    """Split transcript into small chunks for LLM context."""
    return [transcript[i:i+chunk_size] for i in range(0, len(transcript), chunk_size)]

def find_panel_breaks(chunk, prev_context=None):
    """Ask Llama where new panels could start in this chunk."""
    chunk_text = "\n".join(
        [f"[{i}] Speaker {seg['speaker']}: {seg['text']}" for i, seg in enumerate(chunk)]
    )
    context_text = ""
    if prev_context:
        context_text = "Previous context:\n" + "\n".join(
            [f"Speaker {seg['speaker']}: {seg['text']}" for seg in prev_context[-3:]]
        ) + "\n\n"

    prompt = f"""
You are helping to turn a Dungeons & Dragons transcript into comic panels.

{context_text}Here is the next chunk of transcript:

\"\"\"{chunk_text}\"\"\"

Each panel should ideally contain a small, self-contained bit of dialogue or action.

List all **segment indices** (from this chunk) where a new comic panel should START. 
For example: [0, 3, 7] means panels start at segments 0, 3, and 7.

If this whole chunk should be a single panel, return [0].
If you think no new panel is needed beyond the first one, return [0].
If unsure, prefer to start a new panel when a new speaker talks or something changes.

Only return a Python list. No explanation.
"""
    response = ollama.chat(
        model="llama3.1",
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        return eval(response['message']['content'])
    except Exception as e:
        print(f"Error parsing response: {response['message']['content']}")
        return [0]  # default: treat all as one panel

def split_into_panels(transcript, chunk_size=10):
    chunks = chunk_transcript(transcript, chunk_size)
    panels = []
    prev_context = None
    panel_index = 0

    for chunk in chunks:
        panel_starts = find_panel_breaks(chunk, prev_context)
        for idx in panel_starts:
            if idx < len(chunk):
                panels.append({
                    "panel_index": panel_index,
                    "speaker": chunk[idx]['speaker'],
                    "text": chunk[idx]['text'],
                    "start": chunk[idx]['start'],
                    "end": chunk[idx]['end']
                })
                panel_index += 1
        prev_context = chunk  # update context for next chunk
    return panels

def save_panels(panels, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(panels, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    transcript_path = "audioCleanUp/clean_transcript_with_speakers.json"
    output_path = "comic_panels.json"

    print("Loading transcript...")
    transcript = load_transcript(transcript_path)

    print("Detecting comic panels...")
    panels = split_into_panels(transcript, chunk_size=10)

    print("Saving panels...")
    save_panels(panels, output_path)

    print(f"Comic panels saved to {output_path}")
