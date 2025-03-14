import pygame #for handling audio playback
import random #for gen random choices
import asyncio #for asynchronus operat
import edge_tts #text to speech functionality
import os
from dotenv import dotenv_values

#load env vars 
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice") #get assistant voice from env variables

#asynchronus function to convert text to an audio file
async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3" #define the path where the speech file will be saved

    if os.path.exists(file_path):
        os.remove(file_path)

    #create the communicate object to generate speech
    communicate = edge_tts.Communicate(text, AssistantVoice, rate='+13%') # pitch='+5hz', pith dilam shorayah
    await communicate.save(r'Data\speech.mp3')

#function to manage tts functiuonality
def TTS(Text, func=lambda r=None: True):
    while True:
         try:
            #convert text to an audio file asynchronusly
            asyncio.run(TextToAudioFile(Text))

            #init pygame mixer for audio playback
            pygame.mixer.init()

            #load the generated speech file into the pygame mixer
            pygame.mixer.music.load(r"Data\speech.mp3")
            pygame.mixer.music.play() #plays the audio

            #loop until the audio is done playing or the func stops
            while pygame.mixer.music.get_busy():
                if func() == False:
                    break
                pygame.time.Clock().tick(10) #C BORO HAAT dilam karon chatgpt bolse

            return True
         
         except Exception as e:
             print(f"Error in TTS: {e}")
         finally:
             try:
                 #call the provided function with false to singal the end of tts
                 func(False)
                 pygame.mixer.music.stop()
                 pygame.mixer.quit()

             except Exception as e: #handle any exceptions during cleanup
                 print(f"Error in finally block: {e}")

#function to manage TTS with additional responcs for long text
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".") #split text by . into list of sentences

    #list of predefined responses for cases where the text is too long
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    #if the text is very long (more than 4 sentences and 250 chars), add a response message
    if len(Data) > 4 and len(Text) >= 250:
        TTS(" ".join(Text.split(".")[0:2]) + ". " + random.choice(responses),func)

    #otherwise just play the whole text
    else: 
        TTS(Text, func)

#main exec
if __name__ == "__main__":
    while True:
        #prompt user fort input and pass it to tts func
        TextToSpeech(input("Enter the text: "))

#code fixed finally
# --> Pitch = 5hz shoray dewate run kortese

# #Explanation
# 0. add libraries
# 1. AssistantVoice define korsi env e. Liam re disi canadian bhai amago
# 2. Async er function ta use kore everytime speech.mp3 banaitesi 
# 3. File ta play koraitesi pygame diya, file shesh hoile stop
# 4. Main--> TTS == 4 line theke boro or 250 char theke boro hoile responses follow korbe.
# 5. Boro text ta porbe kmne? jodi last line e TextToSpeech er bodole TTS use kori
