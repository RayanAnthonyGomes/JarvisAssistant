from groq import Groq #Groq Library for using its api
from json import load, dump #importing functions from json module to read + write json files
import datetime #importing datetime module to get current date and time
from dotenv import dotenv_values #library for reading .env files

#IMPORTATION COMPLETE

#load environment variables from .env file
env_vars = dotenv_values(".env")

#retrieve specific environment variables for username, assistant name, and api key
Username = env_vars.get("Username")
AssistantName = env_vars.get("AssistantName")
GroqApiKey = env_vars.get("GroqApiKey")

#initialize groq client using api key
client = Groq(api_key=GroqApiKey)

#init empty list to store user msg
messages = []

#Define a system msg that provides context to the ai chatbot about its role and how it behaves
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {AssistantName} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot =  [
    {"role": "system", "content": System}
]

#Attempt to load the chat log from a json file
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
        #if the file doesnt exist, create an empty json file to store logs
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f)

#Function to get real time data from groq api
def RealTimeInformation():
     current_date_time = datetime.datetime.now()
     day =  current_date_time.strftime("%A")
     date = current_date_time.strftime("%d")
     month = current_date_time.strftime("%B")
     year = current_date_time.strftime("%Y")
     hour = current_date_time.strftime("%I")
     minute = current_date_time.strftime("%M")
     second = current_date_time.strftime("%S")

     #format the info into a string 
     data = f"Please use this real-time information if needed,\n"
     data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"     
     data += f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
     return data

#function to modify the chatbots response for mbetter formatting
def AnswerModifier(Answer):
    lines = Answer.split('\n') #split the answer into lines
    non_empty_lines = [line for line in lines if line.strip()] #remove empty lines
    modified_answer = '\n'.join(non_empty_lines) #join the non-empty lines
    return modified_answer

#Main Chatbot function that takes user input and returns the chatbots response
def ChatBot(Query):
    """ This function sends the user's query to the chatbot and returs the AI's response """
    try:
        #load existing chat history from json file
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
        #append the users query to msg list
        messages.append({"role": "user", "content": f"{Query}"})

        #make requ to groq api for resp 
        completion = client.chat.completions.create(
             model = "llama3-70b-8192", #specify model to use
             messages = SystemChatBot + [{"role": "system", "content": RealTimeInformation()}] + messages, #specify chat history
             max_tokens=1024, #specify max tokens
                temperature=0.7, #specify creativity of model
                top_p=1, #specify,==> Use nucleus sampling for controling diversity of responses
                stream=True, #specify stream enable streaming respionse
                stop = None #allow the model to dermine when to stp
        )
    
        Answer = "" #init empty string to store chatbot response

        #process the response from the model
        for chunk in completion:
            if chunk.choices[0].delta.content: #check if the chunk contains content
                Answer += chunk.choices[0].delta.content #append the content to the response

        Answer = Answer.replace("</s>", "") #remove the </s> tag from the response --< clean up any unwanted tokens from the response

        #Append the chatbot's response to the msg list
        messages.append({"role": "assistant", "content": f"{Answer}"})
        #save the updated chat history to the json file

        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)
        #return the formatted respons
        return AnswerModifier(Answer=Answer)
    except Exception as e:
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return ChatBot(Query) #if an error occurs, recursively call the function
#Main program entry point 
if __name__ == "__main__":
    while True:
        user_input = input("Enter your question: ") #prompt user for input
        print(ChatBot(user_input)) #print the chatbots response

#END OF CODE

# 0. Explanation
# 1. All the required libraries are imported.
# 2. The environment variables are loaded from the .env file.
# 3. The function RealTimeInformation is defined to get the current date and time.
# 4. The function AnswerModifier is defined to format the chatbot's response.
# 5. The main ChatBot function is defined to interact with the chatbot and return its response.
# 6. The chat history is loaded from the ChatLog.json file.
# 7. The user's query is appended to the chat history.
# 8. The chat history is sent to the Groq API to get the chatbot's response.
# 9. The chatbot's response is processed and appended to the chat history.
# 10. The chat history is saved to the ChatLog.json file.
# 11. The chatbot's response is returned to the user.
# 12. If an error occurs, the function is recursively called.
# 13. The main program entry point continuously prompts the user for input and prints the chatbot's response.
# 14. The code is executed when the script is run.
# 15. The user is prompted for input.
# 16. The chatbot's response is printed.
# 17. The user is prompted for input again.
# 18. The chatbot's response is printed again.
# 19. The process continues until the program is terminated.



