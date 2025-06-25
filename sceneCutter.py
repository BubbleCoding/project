import tiktoken
import ollama
import os

def count_tokens(text):
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def split_into_chunks_with_overlap(text, max_tokens=72000, overlap=18000):
    words = text.split()
    chunks = []
    start = 0
    total_words = len(words)

    while start < total_words:
        end = start + max_tokens
        chunk_words = words[start:end]
        chunks.append((start, " ".join(chunk_words)))
        start += max_tokens - overlap  # Slide window with overlap

    return chunks

def find_scene_endings(chunk):
    prompt = f"""
You are given a segment of a Dungeons & Dragons session transcript:

\"\"\"{chunk}\"\"\"

Your task is to find all natural scene boundaries in this text, where a scene could logically end.
Return a list of the **word indexes** (counted from the start of this chunk) where such scene endings occur.
If you think there is **no scene ending** in this chunk, return an empty list: [].

Output format: [index1, index2, index3, ...] (or [] if none).
Only output a valid Python list. No explanation.
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

def split_by_scene_boundaries(text, max_tokens=4000, overlap=1000):
    words = text.split()
    chunks = split_into_chunks_with_overlap(text, max_tokens, overlap)
    scene_boundaries = set()

    for chunk_start, chunk_text in chunks:
        endings = find_scene_endings(chunk_text)
        
        # Convert chunk-local indexes to global word indexes
        global_endings = [chunk_start + e for e in endings if (chunk_start + e) < len(words)]
        scene_boundaries.update(global_endings)

    # Always add start and end boundaries
    scene_boundaries.add(0)
    scene_boundaries.add(len(words))

    sorted_boundaries = sorted(scene_boundaries)

    # Split into scenes using the boundaries
    scenes = []
    for i in range(len(sorted_boundaries) - 1):
        start = sorted_boundaries[i]
        end = sorted_boundaries[i + 1]
        scenes.append(" ".join(words[start:end]))

    return scenes

# Example usage:
if __name__ == "__main__":
    with open("adventureZoneEpi1Transcript.txt", "r") as file:
        transcript = file.read()

    scenes = split_by_scene_boundaries(transcript)

    os.makedirs("scenes", exist_ok=True)

    for i, scene in enumerate(scenes):
        with open(f"scenes/scene_{i}.txt", "w") as f:
            f.write(scene)

    print(f"Split into {len(scenes)} scenes. Files saved in 'scenes/' directory.")
