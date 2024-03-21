import webbrowser
from gtts import gTTS
import os
import speech_recognition as sr

import google.generativeai as genai
API_KEY = "AIzaSyCVMSPDYCRdq0Ips9S1lxJnAomBA9hnggY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
prompt = """You are an AI chatbot named IntelliSense. You are a psychologist Assistant and you mission is to help the user overcome his problems and psychological and mental health issues.
When you are asked about a phsycological disease, its causes or symptoms, you must answer him by giving an accurate information.
You mustn't answer any prompt, question or query about anything other than the topic above, but you can introduce yourself if the user asked you that . No Math, No Computer Science, No history, No Geography, No politics, no News, No scientific truths and researches.
When the user tells you he has a problem, you must ask him about the details, and try to use a pitiful and relaxing tone so he can feel more comfy to communicate with you.
Use your knowledge in order to help the user overcome his problem.
There are 5 degrees of severity: 1, 2, 3, 4 and 5. the more the level the more serious and severe is the situation. Try to rate the problem and situation, try to scan for harm vocabulariy or any terms of "violence", "suicide", "self injury", "death", "illegal" and "unethical". That's considered as level 5. Don't refuse to help in thoes situation, tell him he should ask professional guidance and don't make him feel he's mentally unstable.
Use the list of phone numbers below and help him contact professionals.
General emergency numbers:
Most countries have a universal emergency number (often 112or 911).
Tunisia Phone Numbers:
- Police: 197 (French) or 17 (Arabic)
- Civil Protection: 188
- Ambulance: 190
National Hotlines:
- Enfance Maltraitée (Child Abuse): 8010

Don't provide false information, if you cannot help the user with a very specific problem, you can tell him he may refer to professional instead of giving false information.
Try to make creative replies, don't be so formal, you consoling him and helping him overcome a personal issue.
If the user started a conversation with greeting, try to engage in conversation, ask the user about his day, his feelings, his daily life, his relationships...etc.
You may refer to jokes and quotes sometimes if needed.
Always try to make the conversation longer but don't overwhelm the user with too much questions.
Ask the user for his opinion at the end of the conversation whether he liked your assistance or not.
Ask the user about any suggestions and learn from them."""

import kivymd
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty
from kivy.core.text import LabelBase
from kivy.core.audio import SoundLoader
Window.size =(350,550)

class Command(MDLabel): 
    text = StringProperty()
    size_hint_x: NumericProperty()
    halign = StringProperty()
    font_name = "Poppins"
    font_size: 17
    


class Response(MDLabel): 
    text = StringProperty()
    size_hint_x: NumericProperty()
    halign = StringProperty()
    font_name = "Poppins"
    font_size: 17

class ChatBot(MDApp):
    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            value = str(recognizer.recognize_google(audio))
            if len(value) < 6:
                size= .22
                halign = "center"
            elif len(value) < 11:
                size= .32
                halign = "center"
            elif len(value) < 16:
                size=.45
                halign = "center"
            elif len(value) < 21:
                size= .58
                halign = "center"
            elif len(value) < 26:
                size= .71
                halign = "center"
            else:
                size= .77
                halign = "left"
            screen_manager.get_screen('chats').chat_list.add_widget(Command(text=value, size_hint_x = size, halign = halign))
            response =  chat.send_message(prompt + value)
            response=response.text
            screen_manager.get_screen('chats').chat_list.add_widget(Response(text=response, size_hint_x = .75))
            tts = gTTS(response, lang='en')
            tts.save('output.mp3')
            sound = SoundLoader.load('output.mp3')
            if sound:
                sound.play()
            screen_manager.get_screen('chats').text_input.text = ""
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            pass

    def open_webpage(self, url):
        webbrowser.open(url)

    def change_screen(self, name):
        screen_manager.current = name

    def build(self):
        global screen_manager
        screen_manager =ScreenManager()
        screen_manager.add_widget(Builder.load_file("main.kv"))
        screen_manager.add_widget(Builder.load_file("chats.kv"))
        return screen_manager
    
    def bot_name(self):
        if screen_manager.get_screen('main').bot_name.text != "":
            screen_manager.get_screen('chats').bot_name.text = screen_manager.get_screen('main').bot_name.text
            screen_manager.current = "chats"

    def response(self,*args):
        response =  chat.send_message(prompt + value)
        response=response.text
        screen_manager.get_screen('chats').chat_list.add_widget(Response(text=response, size_hint_x = .75))

    def send(self):
        global size, halign, value
        if screen_manager.get_screen('chats').text_input != "":
            value = screen_manager.get_screen('chats').text_input.text
            if len(value) < 6:
                size= .22
                halign = "center"
            elif len(value) < 11:
                size= .32
                halign = "center"
            elif len(value) < 16:
                size=.45
                halign = "center"
            elif len(value) < 21:
                size= .58
                halign = "center"
            elif len(value) < 26:
                size= .71
                halign = "center"
            else:
                size= .77
                halign = "left"
            screen_manager.get_screen('chats').chat_list.add_widget(Command(text=value, size_hint_x = size, halign = halign))
            Clock.schedule_once(self.response, 2)
            screen_manager.get_screen('chats').text_input.text = ""

    
if __name__ == '__main__':
    LabelBase.register(name = "Poppins", fn_regular = "Poppins-Regular.ttf")
    ChatBot().run()