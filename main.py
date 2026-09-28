import os
import subprocess
import sys
import threading
import webbrowser
from datetime import datetime
from typing import Optional

try:
    import pyautogui
except Exception:
    pyautogui = None

import speech_recognition as sr
from dotenv import load_dotenv
from tkinter import *

import apps
import favourites
import gpt_credintials
from apps_intigration import spotify
from assistant_utils import build_local_response, extract_intent, normalize_query, parse_reminder
import time
MODEL = os.path.join(os.path.dirname(__file__), "en_US-amy-medium.onnx")

load_dotenv()

load_dotenv()


def get_env_value(value):
    return os.getenv(str(value))


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
def time_sleep(seconds):
    import time
    time.sleep(seconds)


def say(text, emotion="normal"):
    if not text:
        return

    text = str(text)
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

    try:
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
        audio = process.communicate(text.encode())[0]

        play = subprocess.Popen(
            [
                "aplay",
                "-r",
                "22050",
                "-f",
                "S16_LE",
                "-t",
                "raw",
                "-",
            ],
            stdin=subprocess.PIPE,
        )
        play.communicate(audio)
    except Exception:
        pass

    print(f"\033[1;33mLUTFA : {text}\033[0m")

# =========================
# Voice Recognition
# =========================

def takeCommand():
    r = sr.Recognizer()
    r.energy_threshold = 100
    r.dynamic_energy_threshold = True
    r.dynamic_energy_adjustment_damping = 0.15
    r.dynamic_energy_ratio = 1.5
    r.non_speaking_duration = 0.5
    r.pause_threshold = 1.2

    with sr.Microphone() as source:
        try:
            r.adjust_for_ambient_noise(source, duration=0.5)
        except Exception:
            pass

        print("\033[31mI AM LISTENING MY BABY...\033[0m")
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=12)
        except sr.WaitTimeoutError:
            return ""

        try:
            query = r.recognize_google(audio, language="en-us")
            print("SRIZON :", query)
            return query.lower()
        except Exception:
            try:
                query = r.recognize_google(audio, language="bn-BD")
                print("Lutfa:", query)
                return query.lower()
            except Exception:
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

def click_on_screen(x=None, y=None):
    if pyautogui is None:
        return False

    if os.name == "posix" and not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
        return False

    try:
        if x is not None and y is not None:
            pyautogui.click(x, y)
        else:
            pyautogui.click()
        return True
    except Exception:
        return False


def handle_query(query):
    if not query:
        return

    normalized_query = normalize_query(query)
    intent = extract_intent(normalized_query)

    for site, url in sites:
        if site in normalized_query:
            say(f"Opening {site} for you, boss.")
            open_url(url)
            return

    if "open school" in normalized_query:
        webbrowser.open("https://www.w3schools.com/python/numpy/numpy_array_slicing.asp")
        return

    if "open my applist" in normalized_query:
        say("Which app do you want to open, boss?")
        return

    if "exit now" in normalized_query or "exit" in normalized_query:
        say("Goodbye, boss.")
        raise SystemExit

    if "open your account" in normalized_query:
        value = getattr(favourites, "facebook_id", None)
        if value:
            say("Opening my profile for you.")
            webbrowser.open_new_tab(value)
        else:
            say("I could not find that profile link.")
        return

    if "please play" in normalized_query:
        song_name = normalized_query.split("please play", 1)[1].strip()
        say(f"Playing {song_name} for you. Enjoy your song, boss.")
        try:
            music_link = spotify.searchSong(song_name)
            webbrowser.open_new_tab(music_link)

            time.sleep(4.5)
            click_on_screen(675, 657)
        except Exception:
            say("I could not find that song right now.")
        return

    if "open image of yourself" in normalized_query:
        say("Opening my image for you, sweetheart.")
        try:
            favourites.open_image_of_lutfa()
        except Exception:
            say("I could not open that image right now.")
        return

    if intent["type"] == "reminder":
        reminder = parse_reminder(normalized_query)
        if reminder:
            delay_seconds = max(0, (reminder["time"] - datetime.now()).total_seconds())
            say(f"Reminder set for {reminder['message']}.")

            def _trigger_reminder(message, when):
                import time
                time.sleep(delay_seconds)
                say(f"Reminder: {message}")

            threading.Thread(target=_trigger_reminder, args=(reminder["message"], reminder["time"]), daemon=True).start()
        else:
            say("I could not understand that reminder. Try saying set reminder to drink water in 10 minutes.")
        return

    if intent["type"] == "browser_open":
        target = intent["payload"]
        if not target.startswith(("http://", "https://")):
            target = f"https://www.google.com/search?q={target.replace(' ', '+')}"
        webbrowser.open_new_tab(target)
        say(f"Opening {target} for you.")
        return

    if "latest news" in normalized_query or "news" in normalized_query:
        try:
            import news
            say("I am checking the latest news for you.")
            key = get_env_value("NEWS_API_KEY")
            value = news.getnews(key)
            say(value)
        except Exception:
            say("I could not fetch the news right now.")
        return

    if "weather" in normalized_query or "atmosphere" in normalized_query:
        try:
            import weather
            value = weather.getCityDetails(get_env_value("WEATHER_API_KEY"))
            say(value)
        except Exception:
            say("I could not fetch the weather right now.")
        return

    if intent["type"] in {"time", "date", "day", "date_time", "joke", "intro", "search", "browser_open", "calculate", "open_app"}:
        response = build_local_response(normalized_query)
        say(response)
        if intent["type"] == "search" and intent["payload"]:
            webbrowser.open_new_tab(f"https://www.google.com/search?q={intent['payload'].replace(' ', '+')}")
        elif intent["type"] == "open_app" and intent["payload"]:
            app_name = intent["payload"].strip()
            if app_name in apps.apps_info:
                say(f"Opening {app_name} for you.")
                subprocess.Popen([apps.apps_info[app_name]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return

    try:
        response = gpt_credintials.ai(normalized_query)
        say(response)
    except Exception:
        say("Sorry boss, I could not reach my AI service right now. I can still help with local tasks like time, jokes, and simple calculations.")


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
    say("Hi boss, I am Hinata, your lovely assistant. I am ready to help.")

    while True:
        try:
            query = takeCommand()
        except KeyboardInterrupt:
            break

        if not query:
            continue

        if "exit" in query or "বন্ধ" in query:
            say("Goodbye, boss.")
            break

        handle_query(query)