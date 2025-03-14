#import require libs
from AppOpener import close, open as appopen #open and close apps
from webbrowser import open as webopen #browser functionality
from pywhatkit import search, playonyt #google search and yt playback
from dotenv import dotenv_values #import manage value env
from bs4 import BeautifulSoup #parsing html
from rich import print #styled console printing
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os # for os functionalities

#load env vars
env_vars = dotenv_values(".env")
GroqApiKey = env_vars.get("GroqApiKey")

#define css classes for parsing specific elements in html content

classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
"IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e",
"LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

#define user agent for making web requests
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

#init client groq
client = Groq(api_key=GroqApiKey)

#predefined professional responses for user interactions
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
]

#list to store chatbot messages
messages = []

#system messages to provide context to the chatbot
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

#function to perform a google search.
def GoogleSearch(Topic):
    search(Topic) #pywhatkit's search
    return True #indicate success
# GoogleSearch("Rayan Anthony Gomes ") TEST SUCCESS


#function to generate content using ai to save it to a file
def Content(Topic):

    #nested function to open a file in notepad
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])

    #nested function to generate content using the ai chat
    def ContentWriterAi(prompt):
        messages.append({"role": "user", "content": f"{prompt}"}) #add the user's prompt to msgs

        completion = client.chat.completions.create(
            model = "mixtral-8x7b-32768",
            messages = SystemChatBot + messages,
            max_tokens = 2048,
            temperature = 0.7,
            top_p = 1,
            stream = True,
            stop = None
        )

        Answer = "" #empty string for response

        #process streamed response chuncks
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer
    
    Topic: str = Topic.replace("content ", "")
    ContentByAI = ContentWriterAi(Topic) #gen content with ai
    
    #save the generated content to a text file
    with open(rf"Data\{Topic.lower().replace(' ','')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt")
    return True
# Content("application for a sick leave ") TEST SUCCESS


#function to search for a topic on youtube

def YoutubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True
# YoutubeSearch("Rayan Gomes Shunalal ")   TEST SUCCESS


#function to play a video on yt
def PlayYoutube(query):
    playonyt(query)
    return True
# PlayYoutube("Vibe ft shunalal rayan gomes gaming video") TEST SUCCESS


#func to open an app or a relevant webpage
def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser') #parse htm
            links = soup.find_all('a', {'jsname': 'UWckNb'}) #find relevant links
            return [link.get('href') for link in links] 
        
        #nested function to perform a google search and retrive html
        def search_google(query):
            url = f"https://www.google.com/search?q={query}" #construct google search url
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers = headers)

            if response.status_code == 200:
                return response.text
            else:
                print("Failed to retrieve search results.")
            return None
        html = search_google(app)

        if html:
            link = extract_links(html)[0] #extract first link from search results
            webopen(link)
        return True
    

# OpenApp("Discord") TEST SUCCESS


#function to close app
def CloseApp(app):
    if "chrome" in app:
        pass #skip if the app is chrome
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False

# CloseApp("Discord") TEST SUCCESS

       
#function to execute system level commands
def System(command):
    #nested func to mute sys volume
    def mute():
        keyboard.press_and_release("volume mute")
    #nested func to unmute
    def unmute():  
        keyboard.press_and_release("volume mute")

    #increase vol
    def volume_up():
         keyboard.press_and_release("volume up")
    #decrease vol
    def volume_down():
         keyboard.press_and_release("volume down")

#execute appropriate command
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True

#asyncrhonus function to translate and execute user commands
async def TranslateAndExecute(commands: list[str]):
    funcs = [] #list

    for command in commands:
        if command.startswith("open "): #handle open commands
            if "open it" in command: #ignore open it commands
                pass
            if "open file" == command: 
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)

        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)

        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)

        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search"))
            funcs.append(fun)

        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"No Function Found. For {command}")

    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result


#asynchronus function to automate command execution
async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True


