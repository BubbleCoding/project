import json
import ollama

def chunk_transcript(transcript, chunk_size=50):
    """Split transcript into chunks of N segments each."""
    return [transcript[i:i + chunk_size] for i in range(0, len(transcript), chunk_size)]

def transcript_to_text(chunk):
    """Convert a list of transcript segments into plain text."""
    return " ".join([f"{seg['speaker']}: {seg['text']}" for seg in chunk])

def find_scene_endings_with_context(prev_chunk, curr_chunk, next_chunk):
    prev_text = transcript_to_text(prev_chunk) if prev_chunk else "None"
    curr_text = transcript_to_text(curr_chunk)
    next_text = transcript_to_text(next_chunk) if next_chunk else "None"

    prompt = f"""
You are analyzing a transcript of a Dungeons & Dragons session.

Here is the **previous part** of the transcript (for context):
\"\"\"{prev_text}\"\"\"

Here is the **current part** you are analyzing for scene endings:
\"\"\"{curr_text}\"\"\"

Here is the **next part** of the transcript (for context):
\"\"\"{next_text}\"\"\"

Your task: Identify all scene boundaries in the CURRENT PART. 
A scene boundary is where the situation clearly shifts, such as entering a new room, meeting new characters, or changing the narrative flow.

If no boundary is present in the current part, return an empty list [].

Output format: [index1, index2, ...] (Word indexes within the CURRENT PART only)
No explanation.
"""

    response = ollama.chat(
        model="llama3.1",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        return eval(response['message']['content'])
    except Exception as e:
        print(f"Error parsing response: {response['message']['content']}")
        return []

def detect_scene_endings(transcript_path, chunk_size=50):
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript = json.load(f)

    chunks = chunk_transcript(transcript, chunk_size)
    scene_boundaries = []

    for i, curr_chunk in enumerate(chunks):
        prev_chunk = chunks[i - 1] if i > 0 else []
        next_chunk = chunks[i + 1] if i + 1 < len(chunks) else []

        endings = find_scene_endings_with_context(prev_chunk, curr_chunk, next_chunk)
        
        # Calculate absolute segment index for boundaries
        chunk_start_index = i * chunk_size
        absolute_endings = [chunk_start_index + idx for idx in endings]

        scene_boundaries.extend(absolute_endings)

    return scene_boundaries

def split_transcript_into_scenes(transcript_path, output_path, chunk_size=50):
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript = json.load(f)

    boundaries = detect_scene_endings(transcript_path, chunk_size)

    # Split into scenes
    scenes = []
    start = 0
    for end in boundaries:
        scenes.append(transcript[start:end + 1])
        start = end + 1
    scenes.append(transcript[start:])  # Add last scene

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(scenes, f, indent=2, ensure_ascii=False)

    print(f"Scene-split transcript saved to {output_path}")

if __name__ == "__main__":
    transcript_file = "audioCleanUp/clean_transcript_with_speakers.json"
    output_file = "scenes.json"
    split_transcript_into_scenes(transcript_file, output_file)
