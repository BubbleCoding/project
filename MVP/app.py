import SpeechToText
import ScriptToImage
import AddTextToImage
import CreateComicPage
import TextToScript

def create_comic_book():
    # Step 1: Convert speech to text
    #session_transcript = SpeechToText.transcribe_audio()
    print("Session Transcript Generation Successful!")

    # Step 2: Create a comic book script
    comic_script = TextToScript.create_comic_script("Test")
    print("Comic Script Generation Successful!")

    # Step 3: Generate images from the script
    ScriptToImage.generate_images_from_script(comic_script)
    print("Panel Images Generation Successful!")

    # Step 4: Add text to the images
    #AddTextToImage.add_text_to_images(comic_script)
    #print("Panel Images Added Text Successful!")

    # Step 5: Create a comic page from the images
    CreateComicPage.create_strip()
    print("Comic Creation Successful!")

create_comic_book()