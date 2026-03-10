"""
commands.py — Command parser and local data management for Dorwal AI.

Handles:
  - add / view / delete notes
  - add / view / delete reminders
  - file operations (open folder, list files)
"""

import json
import os
import subprocess
import platform

# ── File paths ───────────────────────────────────────────────────────────────

_BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_NOTES_FILE  = os.path.join(_BASE_DIR, "data", "notes.json")
_REMIND_FILE = os.path.join(_BASE_DIR, "data", "reminders.json")


# ── JSON helpers ─────────────────────────────────────────────────────────────

def _load(path: str) -> list:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save(path: str, data: list) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ── Notes ────────────────────────────────────────────────────────────────────

def get_notes() -> list:
    return _load(_NOTES_FILE)


def add_note(note: str) -> str:
    notes = _load(_NOTES_FILE)
    notes.append(note.strip())
    _save(_NOTES_FILE, notes)
    return f"Note saved: \"{note.strip()}\""


def delete_note(index: int) -> str:
    notes = _load(_NOTES_FILE)
    if 0 <= index < len(notes):
        removed = notes.pop(index)
        _save(_NOTES_FILE, notes)
        return f"Deleted note: \"{removed}\""
    return "Note index out of range."


# ── Reminders ────────────────────────────────────────────────────────────────

def get_reminders() -> list:
    return _load(_REMIND_FILE)


def add_reminder(reminder: str) -> str:
    reminders = _load(_REMIND_FILE)
    reminders.append(reminder.strip())
    _save(_REMIND_FILE, reminders)
    return f"Reminder set: \"{reminder.strip()}\""


def delete_reminder(index: int) -> str:
    reminders = _load(_REMIND_FILE)
    if 0 <= index < len(reminders):
        removed = reminders.pop(index)
        _save(_REMIND_FILE, reminders)
        return f"Deleted reminder: \"{removed}\""
    return "Reminder index out of range."


# ── File / system helpers ─────────────────────────────────────────────────────

def open_folder(path: str) -> str:
    """Open a folder in the system file explorer."""
    if not os.path.isdir(path):
        return f"Folder not found: {path}"
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(path)
        elif system == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        return f"Opened folder: {path}"
    except Exception as e:
        return f"Could not open folder: {e}"


def list_files(path: str = ".") -> str:
    """Return a formatted list of files in a directory."""
    try:
        entries = os.listdir(path)
        if not entries:
            return f"No files found in {path}"
        return "\n".join(sorted(entries))
    except PermissionError:
        return f"Permission denied: {path}"
    except FileNotFoundError:
        return f"Directory not found: {path}"


# ── Main command dispatcher ──────────────────────────────────────────────────

def execute_command(text: str) -> str:
    """
    Parse a text string and execute the matching command.

    Returns a result string, or empty string if no command matched.
    """
    if not text:
        return ""

    t = text.lower().strip()

    # ── Notes ────────────────────────────────────────────────
    # "add note <content>"  |  "note <content>"  |  "save note <content>"
    for prefix in ("add note ", "save note ", "note ", "create note "):
        if t.startswith(prefix):
            content = text[len(prefix):].strip()
            if content:
                return add_note(content)
            return "Please provide the note content."

    # "show notes"  |  "view notes"  |  "list notes"  |  "my notes"
    if any(t == kw or t.startswith(kw) for kw in ("show notes", "view notes", "list notes", "my notes", "show my notes")):
        notes = get_notes()
        if not notes:
            return "You have no notes yet."
        return "Your notes:\n" + "\n".join(f"  [{i}] {n}" for i, n in enumerate(notes))

    # "delete note <index>"
    if t.startswith("delete note "):
        idx_str = t[len("delete note "):].strip()
        if idx_str.isdigit():
            return delete_note(int(idx_str))
        return "Please specify a note number, e.g. 'delete note 0'."

    # ── Reminders ────────────────────────────────────────────
    # "remind me to <content>"  |  "add reminder <content>"  |  "set reminder <content>"
    for prefix in ("remind me to ", "remind me ", "add reminder ", "set reminder ", "reminder "):
        if t.startswith(prefix):
            content = text[len(prefix):].strip()
            if content:
                return add_reminder(content)
            return "Please provide the reminder content."

    # "show reminders"  |  "view reminders"  |  "my reminders"
    if any(t == kw or t.startswith(kw) for kw in ("show reminders", "view reminders", "list reminders", "my reminders")):
        reminders = get_reminders()
        if not reminders:
            return "You have no reminders yet."
        return "Your reminders:\n" + "\n".join(f"  [{i}] {r}" for i, r in enumerate(reminders))

    # "delete reminder <index>"
    if t.startswith("delete reminder "):
        idx_str = t[len("delete reminder "):].strip()
        if idx_str.isdigit():
            return delete_reminder(int(idx_str))
        return "Please specify a reminder number, e.g. 'delete reminder 0'."

    # ── Files ────────────────────────────────────────────────
    # "open folder <path>"  |  "open <path>"
    if t.startswith("open folder "):
        path = text[len("open folder "):].strip()
        return open_folder(path)

    # "list files"  |  "list files in <path>"
    if t.startswith("list files in "):
        path = text[len("list files in "):].strip()
        return list_files(path)
    if t in ("list files", "show files"):
        return list_files(os.path.expanduser("~"))

    return ""   # no command matched — let ai.py handle it
