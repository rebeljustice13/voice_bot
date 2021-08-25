import random
import string
import nltk
import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
from newspaper import Article

warnings.filterwarnings('ignore')
nltk.download('punkt', quiet=True)
article = Article("https://en.wikipedia.org/wiki/Cancer")
article.download()
article.parse()
article.nlp()
corpus = article.text

# from nltk import sent_tockenize
text = corpus
# nltk.download()
sentence_list = nltk.sent_tokenize(text)

# voice bot
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    command=''
    try:
        with sr.Microphone() as source:
            print('listening...')
            talk("hii how can i help you")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()

    except:
        print("someting went wrong")
        pass
    print(command)
    return command


def greeting_response(text):
    text = text.lower()


    bot_greetings = ['hii', 'hey', 'hola', 'hello']
    user_greetings = ['hii', 'hey', 'hello', 'hola']
    for word in text.split():
        if word in user_greetings:
            return talk(random.choice(bot_greetings))


def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))
    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    return list_index


def bot_response(user_input):
    #user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_score = cosine_similarity(cm[-1], cm)
    similarity_score_list = similarity_score.flatten()
    index = index_sort(similarity_score_list)
    index = index[1:]
    response_flag = 0

    j = 0
    for i in range(len(index)):
        if similarity_score_list[index[i]] > 0.0:
            bot_response = bot_response + " " + sentence_list[index[i]]
            response_flag = 1
            j += 1
        if j > 2:
            break

    if response_flag == 0:
        bot_response = bot_response + ' ' + ' i appologize i dont understand'
    sentence_list.remove(user_input)

    return bot_response


print('doc bot:i am docter bot .i will answer your quries')
exit_list = ['exit', 'see u later', 'bye', 'quite']

while (True):
    user_input = take_command()
    if user_input.lower() in exit_list:
        print("talk with you later")
        talk('talk with you later')
        break
    else:
        if greeting_response(user_input) != None:
            print(greeting_response(user_input))
            talk(greeting_response(user_input))
        else:
            print(bot_response(user_input))
            talk(bot_response(user_input))