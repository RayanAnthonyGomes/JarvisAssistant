from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

#load env
env_vars = dotenv_values(".env")

#get input language setting from the environment variable
InputLanguage = env_vars.get("InputLanguage")

#define the html code for the speech recognitoon interface
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

#replace the language setting in the html code with the language from env vars
HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

#write the html code to a file
with open(r"Data\Voice.html", "w") as f:
    f.write(HtmlCode)

#get the current working directory
current_dir = os.getcwd()
#gen the file path for the html file
Link = f"{current_dir}/Data/Voice.html"

#set chrome options for Webdriver
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

#init chrome webdriver using chrome driver manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

#define the path for temp files
TempDirPath = rf"{current_dir}/Frontend/Files"

#functions to set the assistant's status by writing to a file
def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}/Status.data',"w", encoding = 'utf-8') as file:
        file.write(Status)

#function to modify a query to ensure proper punctuation and format
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "who's", "where's", "when's", "why's", "which's", "whose's", "whom's", "how's", "where's"]

    #check if the query is a question and add a question mark if necessary
    if any(word + " " in new_query for word in question_words):
       if query_words[-1][-1] in { '.' , '!', '?'}:
           new_query = new_query[:-1] + "."
       else:
           new_query += "?"
    else:
        #add a period if the query does not end with punctuation
        if query_words[-1][-1] in { '.' , '!', '?'}:
            new_query = new_query[:-1] + "."
        
        else:
            new_query += "."
    
    return new_query.capitalize()

#function to translate a text into English using the mtranslate library
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

#function to perform speech recognition using the webdriver
def SpeechRecognition():
    #open the html file in the browser
    driver.get("file:///" + Link)
    #start speech recog by clicking the start button
    driver.find_element(by=By.ID, value="start").click()

    while True:
        try:
            #get the recoged text from the html output element 
            Text = driver.find_element(by=By.ID, value="output").text

            if Text:
                #Stop the speech recog by clicking the stop button
                driver.find_element(by=By.ID, value="end").click()

                #if the input lang is eng return the modified query
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    #if the input in not eng translate text and return it
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))
        except:
            pass

#main exec
if __name__ == "__main__":
    while True:
        #continuously perform speech recog
        Text = SpeechRecognition()
        print(Text)


#0.Explanation Kmne ki hoilo
#1. Selenium Used, mtranslate used
#2. Html COde> Chrome webdriver use kortese Speech Recognition model use kortese
