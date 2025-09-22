import transcribe
import CreateComicPage
import TextToScriptgtp
import scriptToImageGPT
import scriptToPrompt

def main():
    transcribe.main()
    TextToScriptgtp.main()
    scriptToPrompt.main()
    scriptToImageGPT.main()
    CreateComicPage.main()

if __name__ == "__main__":
    main()