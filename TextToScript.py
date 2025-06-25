import ollama
import json

def create_comic_script(transcript):
    transcript = transcript
    content = load_content()
    characters = load_characters()
    script = run_ollama(content, characters)
    #print(script)
    return script

def load_content():
    f = open('recording.txt', 'r')
    content = f.read()
    f.close
    return content

def load_characters():
    characters = [{"Magnus": "A tall male human carpenter, red beard and sturdy "}, {"Taco": "A short half elven wizard who is also a chef"}, {"Rock Seeker": "A big burly human male"}, {"Merle": "A stout dwarf cleric"}]
    return characters

def run_ollama(content, characters):
    prompt = f"""
You are given a segment of a Dungeons & Dragons session transcript.

Session Content:
{content}

Your task is to transform this into a detailed comic book script, broken down into individual panels.

Each panel must be represented as a JSON object with the following **specific keys**:

1. "setting": A short description of the environment or background.
2. "characters": A list of character names present in the panel.
3. "objects": A list of important objects or props present in the scene.
4. "action": A description of what the characters are doing.
5. "mood": The overall mood or atmosphere of the panel (e.g., "tense", "relaxed", "mysterious").
6. "camera_view": Suggestion for the camera angle (choose one: "close-up", "wide shot", "action shot", "overhead shot").
7. "lighting": Description of the lighting (e.g., "dim candlelight", "bright midday sun").
8. "text": The dialogue or narration for the panel, based on the transcript. Rephrase if needed for clarity, but keep the original meaning.

Output format: a JSON array of such panel objects. Example:

[
{{
    "setting": "Dimly lit tavern interior with wooden furniture and flickering candles.",
    "characters": ["Magnus", "Taco", "Merle"],
    "objects": ["wooden table", "mugs of ale"],
    "action": "Magnus sits at the table, clinking mugs with Taco and Merle.",
    "mood": "relaxed, cozy",
    "camera_view": "wide shot",
    "lighting": "warm candlelight",
    "text": "So our story begins with the three of you sitting at this tavern."
}},
{{
    "setting": "Tavern interior, focusing on the table.",
    "characters": ["Magnus"],
    "objects": ["wooden mug"],
    "action": "Magnus lifts his mug and smiles sheepishly.",
    "mood": "playful",
    "camera_view": "close-up",
    "lighting": "soft candlelight",
    "text": "Nobody wants chairs anymore. Everyone’s into wrought iron now."
}}
]

Important:
- Every panel **must include all 8 keys**.
- If an element does not apply, use an empty string ("") or an empty list [] as appropriate.
- Do not include any introductions, explanations, or comments. Output ONLY the raw JSON array, starting with [ and ending with ].
"""
    stream = ollama.chat(
    model="llama3.1",
    messages=[{"role": "user", "content": prompt}],
    stream=True,
    )
    script = ""
    for chunk in stream:
        script += chunk['message']['content']
        if script.strip().endswith(']'):
            break  # likely complete
    json_script = json.loads(script)
    return json_script