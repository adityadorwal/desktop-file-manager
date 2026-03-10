"""
ai.py — Rule-based AI response engine for Dorwal AI.

Provides meaningful responses for common queries without requiring
any internet connection or external model. Can be extended later
with a local LLM (e.g., llama.cpp / Ollama).
"""

import datetime
import random

# ── Small knowledge base ────────────────────────────────────────────────────

GREETINGS = ["hello", "hi", "hey", "good morning", "good evening", "good afternoon", "howdy"]
FAREWELLS  = ["bye", "goodbye", "see you", "exit", "quit", "take care"]
THANKS     = ["thank you", "thanks", "thank u", "thx"]

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
    "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads.",
    "Why did the developer go broke? Because he used up all his cache.",
    "A SQL query walks into a bar, walks up to two tables and asks… 'Can I join you?'",
    "Why do Java developers wear glasses? Because they don't C#.",
]

MOTIVATIONS = [
    "Keep going — every line of code brings you closer to your goal! 💪",
    "Great things take time. You're building something amazing.",
    "Progress, not perfection. You've got this! 🚀",
    "Every expert was once a beginner. Stay consistent!",
]


def _get_time_greeting() -> str:
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"


def respond_to_input(text: str) -> str:
    """
    Generate a response to the given user input.

    Parameters
    ----------
    text : str — user's raw input

    Returns
    -------
    str — assistant's reply (empty string if nothing matched)
    """
    if not text:
        return ""

    t = text.lower().strip()

    # Greetings
    if any(g in t for g in GREETINGS):
        return f"{_get_time_greeting()}! I'm Dorwal AI, your desktop assistant. How can I help you today?"

    # Farewells
    if any(f in t for f in FAREWELLS):
        return "Goodbye! Have a productive day. 👋"

    # Thanks
    if any(tk in t for tk in THANKS):
        return "You're welcome! 😊 Let me know if there's anything else I can do."

    # Time / date
    if "time" in t:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."

    if "date" in t or "today" in t:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        return f"Today is {today}."

    # Day of week
    if "day" in t:
        day = datetime.datetime.now().strftime("%A")
        return f"Today is {day}."

    # Joke
    if "joke" in t or "funny" in t or "laugh" in t:
        return random.choice(JOKES)

    # Motivation
    if any(w in t for w in ["motivat", "inspire", "encourag", "cheer"]):
        return random.choice(MOTIVATIONS)

    # Who are you
    if any(w in t for w in ["who are you", "what are you", "your name", "introduce yourself"]):
        return (
            "I'm Dorwal AI — an offline desktop assistant inspired by JARVIS. "
            "I can manage notes, reminders, answer questions, and more!"
        )

    # Help
    if "help" in t or "what can you do" in t:
        return (
            "Here's what I can do:\n"
            "• answer questions about time & date\n"
            "• add / view notes  (try: 'add note Buy groceries')\n"
            "• add / view reminders  (try: 'remind me to call Mom')\n"
            "• tell jokes\n"
            "• motivate you\n"
            "• respond to voice commands via the 🎤 button"
        )

    # Weather (offline — cannot fetch real data)
    if "weather" in t:
        return "I'm running fully offline, so I can't fetch live weather. Try a weather website or app!"

    # Default
    return (
        "I'm not sure how to respond to that yet. "
        "Try 'help' to see what I can do, or use the command 'add note …' / 'remind me …'."
    )
