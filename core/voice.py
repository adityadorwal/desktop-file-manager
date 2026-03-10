"""
voice.py — Microphone input using SpeechRecognition + Google Web Speech API
(works offline fallback: returns empty string if no internet / mic unavailable)
"""

import speech_recognition as sr


def listen_once(timeout: int = 5, phrase_limit: int = 8) -> str:
    """
    Listen from the default microphone and return the transcribed text.

    Parameters
    ----------
    timeout      : seconds to wait for speech to start
    phrase_limit : max seconds to record a single phrase

    Returns
    -------
    str  — transcribed text, or empty string on failure
    """
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8   # slight pause ends phrase

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)

        text = recognizer.recognize_google(audio)
        return text.strip()

    except sr.WaitTimeoutError:
        print("[VOICE] No speech detected within timeout.")
        return ""
    except sr.UnknownValueError:
        print("[VOICE] Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"[VOICE] Speech service error: {e}")
        return ""
    except OSError as e:
        print(f"[VOICE] Microphone not found or unavailable: {e}")
        return ""
