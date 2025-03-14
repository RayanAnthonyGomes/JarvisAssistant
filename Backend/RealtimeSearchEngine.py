from googlesearch import search
from groq import Groq
from json import load,dump
import datetime
from dotenv import dotenv_values

#load env val
env_vars = dotenv_values(".env")

#retrive env variables for chatbot confiq
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqApiKey = env_vars.get("GroqApiKey")

#init client 
client = Groq(api_key= GroqApiKey)

#define system instructions for chatbot
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""
#try to load the chat log from a json file or create empty one

try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

#funtion to perform a google search
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer =  f"The search results for '{query}' are:\n[start]\n"

    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
    Answer += "[end]"
    
    return Answer

#func to clean up empty lines
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

#predefined funcs for chatbot 
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, How can I help you?" }
]

#current time date

def Information():
    data = ""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data += f"Use this Real-Time Information if needed"
    data += f"Day : {day}\n"
    data += f"Date : {date}\n"
    data += f"Month : {month}\n"
    data += f"Year : {year}\n"
    data += f"Time : {hour} hours, {minute} minutes, {second} seconds.\n"
    return data

#function to handle real time search and respons gen

def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    #load chat log
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
    messages.append({"role": "user", "content": f"{prompt}"})
    #add google search results to chatbots mesgs
    SystemChatBot.append({"role": "assistant", "content": GoogleSearch(prompt)})

    #generate response using groq client
    completion = client.chat.completions.create(
        model = "llama3-70b-8192",
        messages = SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature = 0.7,
        max_tokens = 2048,
        top_p = 1,
        stream = True,
        stop = None
    )


    Answer = ""

    #response chunnks from streaming output
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
    #cleanup
    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant","content": Answer})

    #save chat log
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)
    #remove most recent system chatbot message
    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

#main entry point of the program for interactive query
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))
