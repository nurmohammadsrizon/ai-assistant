import os
import subprocess
import sys
# from google import genai
from tkinter import *
from tkinter import messagebox
import webbrowser
import speech_recognition as sr
import apps
import gpt_credintials
MODEL = os.path.join(os.path.dirname(__file__), "en_US-amy-medium.onnx")
import favourites
def AI():
  if not os.path.exists(MODEL):
    MODEL = "en_US-amy-medium.onnx"


import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()
def get_env_value(value):
# Access the variables using standard os.getenv
    secret_key = os.getenv(f"{value}")
    return secret_key


# =========================
# Websites List
# =========================

sites = [
    ["youtube", "https://www.youtube.com"],
    ["ইউটিউব", "https://www.youtube.com"],

    ["facebook", "https://www.facebook.com"],
    ["ফেসবুক", "https://www.facebook.com"],

    ["instagram", "https://www.instagram.com"],
    ["ইনস্টাগ্রাম", "https://www.instagram.com"],

    ["twitter", "https://twitter.com"],
    ["x", "https://x.com"],

    ["tiktok", "https://www.tiktok.com"],
    ["টিকটক", "https://www.tiktok.com"],

    ["linkedin", "https://www.linkedin.com"],
    ["লিংকডইন", "https://www.linkedin.com"],

    ["discord", "https://discord.com"],
    ["ডিসকর্ড", "https://discord.com"],

    ["telegram", "https://telegram.org"],
    ["টেলিগ্রাম", "https://telegram.org"],

    ["whatsapp", "https://web.whatsapp.com"],
    ["হোয়াটসঅ্যাপ", "https://web.whatsapp.com"],


    # Google Services

    ["google", "https://www.google.com"],
    ["গুগল", "https://www.google.com"],

    ["gmail", "https://mail.google.com"],
    ["জিমেইল", "https://mail.google.com"],

    ["google drive", "https://drive.google.com"],
    ["গুগল ড্রাইভ", "https://drive.google.com"],

    ["google maps", "https://maps.google.com"],
    ["গুগল ম্যাপ", "https://maps.google.com"],

    ["google translate", "https://translate.google.com"],
    ["গুগল ট্রান্সলেট", "https://translate.google.com"],


    # Other useful

    ["github", "https://github.com"],
    ["গিটহাব", "https://github.com"],

    ["chatgpt", "https://chat.openai.com"],
    ["চ্যাটজিপিটি", "https://chat.openai.com"],
    ["openai", "https://openai.com"],

    ["netflix", "https://www.netflix.com"],

    ["spotify", "https://open.spotify.com"],

    ["amazon", "https://www.amazon.com"],

    ["wikipedia", "https://www.wikipedia.org"],

    ["stackoverflow", "https://stackoverflow.com"],
]



# =========================
# Text To Speech
# =========================

# =========================
# Emotional Text To Speech
# =========================

def say(text, emotion="normal"):

    if not text:
        return


    # emotion settings
    if emotion == "happy":
        speed = "0.85"
        text = f"😊 {text}!"

    elif emotion == "excited":
        speed = "0.75"
        text = f"Wow!! {text}!!"

    elif emotion == "sad":
        speed = "1.25"
        text = f"Oh... {text}"

    elif emotion == "angry":
        speed = "0.9"
        text = f"Warning! {text}"

    elif emotion == "calm":
        speed = "1.35"

    else:
        speed = "1.0"



    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "piper",
            "--model",
            MODEL,
            "--length-scale",
            speed,
            "--output-raw",
        ],

        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )


    audio = process.communicate(
        str(text).encode()
    )[0]


    play = subprocess.Popen(
        [
            "aplay",
            "-r",
            "22050",
            "-f",
            "S16_LE",
            "-t",
            "raw",
            "-"
        ],

        stdin=subprocess.PIPE,
    )
    print(f"\033[1;33mLUTFA : {text}\033[0m")


    play.communicate(audio)

# =========================
# Voice Recognition
# =========================

def takeCommand():

    r = sr.Recognizer()

    r.energy_threshold = 200
    r.dynamic_energy_threshold = True
    r.non_speaking_duration = 0.7
    r.pause_threshold = 0.8


    with sr.Microphone() as source:

        print("\033[31mI AM LISTENING MY BABY...\033[0m")

        audio = r.listen(source)


        # Try Bangla first
        try:

            query = r.recognize_google(
                audio,
                language="en-us"
            )

            print("SRIZON :", query)

            return query.lower()



        except:


            # Try English

            try:

                query = r.recognize_google(
                    audio,
                    language="bn-BD"
                )


                print("Lutfa:", query)


                return query.lower()



            except:

                return ""





# =========================
# Open Website
# =========================

def open_url(url):

    if os.name == "posix":

        subprocess.Popen(
            [
                "xdg-open",
                url
            ],

            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )

        return True



    try:

        return webbrowser.open_new_tab(url)


    except:

        return False




# =========================
# Command Handler
# =========================

def handle_query(query):

    if not query:
        return


    for site, url in sites:


        if site in query:



            say(
                f"Opening {site} Baby . As your wish. I am loyal to you "
            )

            open_url(url)

            return
    if "open school" in query :
      webbrowser.open("https://www.w3schools.com/python/numpy/numpy_array_slicing.asp")
      return 
    if "open my applist" in query:
      applist = apps.apps_info
      # subprocess.Popen(applist[apps])
      say("Which app you want to open boss? ")
    elif "exit now" in query:
        sys.exit()
    # elif "i love you" or "i love u" in query:
        
    #     say("I love you too baby. why you are ask me like that .I am feeling ashamed.")
    elif "open your account" in query:
        value = favourites.facebook_id
        say("OPENING MY ID BABY. YOU CAN MESSAGE ME NOW")
        webbrowser.open_new_tab(value)
    elif "play song" in query:
        say("I played your one of the favourite song . baby are you happy? ")
        value = favourites.music_choice
        webbrowser.open_new_tab(value[0])
    elif "open image of yourself" in query:
        say("You are trying to watch my photo. Love you. weit a moment i am opening my photo. ")
        favourites.open_image_of_lutfa()
    # elif "love you" or "love u" in query:
    #     say("I Love you too baby . I am the online version of luutfaa. But i don't konow original version of me is even loyal to you. ")
    elif "give me the latest news" in query:
        import news
        key = get_env_value("NEWS_API_KEY")
        value = news.getnews(key)
        say(value)
    elif "atmosphere details"in query:
        import weather
        value = weather.getCityDetails(get_env_value("WEATHER_API_KEY"))
        say(value)
        
    else:
        try:
            say(gpt_credintials.ai(query))
            # print("\033[31mThis text is Red\033[0m")
        except Exception as e:
            say(gpt_credintials.BackupAi(query))
        except Exception as e:
            say(gpt_credintials.BackupAI_2(query))
        except Exception as e:
            say("Looks like you are offline boos. Fisrst of all connect to the network for accessing my advanced features. Because i can't run my big model in this pc. i need more spaceification boos. ")
        
    # If no website found


# =========================
# Main
# =========================
# class UI()
class UI(Tk):
    def __init__(self, name, title):
        self.window = name
        self.window = Tk()
        self.window.title(title)
        self.window.geometry("600x600")
        self.window.resizable(False, False)
    def Run(self):
        self.window.mainloop()
        pass
        
if __name__ == "__main__":
    
   
    say(
        "Hi, Switty?i am your luutfaa. your Love. Whats about today. My love?"
    )


    while True:


        query = takeCommand()


        if "exit" in query or "বন্ধ" in query:

            say(
                "Good bye Boss"
            )

            break


        handle_query(query)
AI()