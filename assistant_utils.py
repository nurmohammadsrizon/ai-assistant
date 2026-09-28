from datetime import datetime, timedelta
import math
import re


def normalize_query(query: str) -> str:
    if not query:
        return ""
    return " ".join(str(query).strip().lower().split())


def extract_intent(query: str):
    q = normalize_query(query)
    if not q:
        return {"type": "empty", "payload": ""}

    if any(keyword in q for keyword in ["who are you", "what are you", "introduce yourself", "your name"]):
        return {"type": "intro", "payload": ""}

    if any(keyword in q for keyword in ["what time", "current time", "time now"]):
        return {"type": "time", "payload": ""}

    if any(keyword in q for keyword in ["what date", "today's date", "date today"]):
        return {"type": "date", "payload": ""}

    if any(keyword in q for keyword in ["what day", "day today"]):
        return {"type": "day", "payload": ""}

    if any(keyword in q for keyword in ["date and time", "say the date and time", "tell me the date and time", "what is the date and time", "what's the date and time"]):
        return {"type": "date_time", "payload": ""}

    if any(keyword in q for keyword in ["tell me a joke", "joke", "funny"]):
        return {"type": "joke", "payload": ""}

    if any(keyword in q for keyword in ["set reminder", "remind me", "reminder"]):
        return {"type": "reminder", "payload": q}

    if q.startswith("search for "):
        return {"type": "search", "payload": q.replace("search for ", "", 1).strip()}

    if q.startswith("go to "):
        return {"type": "browser_open", "payload": q.replace("go to ", "", 1).strip()}

    if "open browser" in q or "open the browser" in q:
        return {"type": "browser_open", "payload": "https://www.google.com"}

    if q.startswith("calculate "):
        return {"type": "calculate", "payload": q.replace("calculate ", "", 1).strip()}

    if q.startswith("open "):
        return {"type": "open_app", "payload": q.replace("open ", "", 1).strip()}

    return {"type": "general", "payload": q}


def safe_calculate(expression: str):
    cleaned = re.sub(r"[^0-9.+\-*/() ]", "", expression)
    if not cleaned:
        raise ValueError("No valid expression")
    return str(eval(cleaned, {"__builtins__": {}}, {"math": math}))


def parse_reminder(query: str, now: datetime | None = None):
    q = normalize_query(query)
    if not q:
        return None

    now = now or datetime.now()
    cleaned = re.sub(r"^(set reminder|reminder|remind me)\s*(to)?\s*", "", q).strip()
    if not cleaned:
        return None

    message = cleaned
    reminder_time = None

    minute_match = re.search(r"\bin (\d+) minute(s)?\b", cleaned)
    if minute_match:
        reminder_time = now + timedelta(minutes=int(minute_match.group(1)))
        message = cleaned[:minute_match.start()].strip().strip("to").strip()

    hour_match = re.search(r"\bin (\d+) hour(s)?\b", cleaned)
    if hour_match:
        reminder_time = now + timedelta(hours=int(hour_match.group(1)))
        message = cleaned[:hour_match.start()].strip().strip("to").strip()

    time_match = re.search(r"\bat (\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b", cleaned)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2) or 0)
        meridiem = (time_match.group(3) or "").lower()
        if meridiem == "pm" and hour < 12:
            hour += 12
        if meridiem == "am" and hour == 12:
            hour = 0
        reminder_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if reminder_time <= now:
            reminder_time = reminder_time + timedelta(days=1)
        message = cleaned[:time_match.start()].strip().strip("to").strip()

    if not reminder_time:
        return None

    return {"message": message or "Reminder", "time": reminder_time}


def build_local_response(query: str, now: datetime | None = None):
    q = normalize_query(query)
    if not q:
        return "I did not catch that. Please say it again."

    now = now or datetime.now()
    intent = extract_intent(q)

    if intent["type"] == "intro":
        return "I am Lutfa, your voice assistant. I can open websites, play music, give news, weather, and help with simple tasks."

    if intent["type"] == "time":
        return f"The current time is {now.strftime('%I:%M %p')}."

    if intent["type"] == "date":
        return f"Today is {now.strftime('%B %d, %Y')}."

    if intent["type"] == "day":
        return f"Today is {now.strftime('%A')}."

    if intent["type"] == "date_time":
        return f"Today is {now.strftime('%B %d, %Y')} and the time is {now.strftime('%I:%M %p')}."

    if intent["type"] == "joke":
        return "Why do programmers prefer dark mode? Because light attracts bugs."

    if intent["type"] == "search":
        return f"I will open a web search for {intent['payload']} now."

    if intent["type"] == "browser_open":
        return f"Opening {intent['payload']} for you."

    if intent["type"] == "calculate":
        try:
            return f"The result is {safe_calculate(intent['payload'])}."
        except Exception:
            return "I could not calculate that expression."

    if intent["type"] == "open_app":
        return f"I can try to open {intent['payload']} for you."

    return "I am here and ready to help. You can ask me to open websites, play music, check weather, or get news."
