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
    characters = [{"Magnus": "A tall male human carpenter, red beard and sturdy "}, {"Taco": "A short half elven wizard"}, {"Rock Seeker": "A big"}, {"Merle": "A stout dwarf cleric"}]
    return characters

def run_ollama(content, characters):
    prompt = f"""
    You are given a segment of a Dungeons & Dragons session transcript:

    Session Content:
    {content}

    Your task is to transform this into a comic book script, broken down into individual panels.

    Each panel must include:
    - A detailed visual description suitable for image generation (key: "panel art")
    - A line of dialogue or narration (key: "text")

    Instructions:
    - Structure the output as a JSON array of objects.
    - Each object must contain exactly two keys:
    - "panel art": A vivid, standalone description of the panel art. Include setting, characters, action, and mood.
    - "text": A single line of spoken dialogue or narration. Rephrase as a proper sentence if needed, but keep the meaning true to the original session.
    - Process the entire input and split it into as many panels as necessary.
    - Do **not** include any additional explanation, commentary, or text outside of the JSON array.

    Output only a valid JSON array. Example format:

    [
    {{
        "panel art": "A dimly lit tavern filled with laughing patrons. Magnus, a red-bearded human, clinks mugs with Taco and Merle at a wooden table.",
        "text": "So our story begins with the three of you sitting at this tavern."
    }},
    {{
        "panel art": "Close-up of Magnus, his face lit by candlelight, a sheepish grin on his face.",
        "text": "Nobody wants chairs anymore. Everyone’s into wrought iron now."
    }}
    ]
    """

    stream = ollama.chat(
    model="llama3.1",
    messages=[{"role": "user", "content": prompt}],
    stream=True,
    )
    script = ""
    for chunk in stream:
        script += chunk['message']['content']
    json_script = json.loads(script)
    return json_script