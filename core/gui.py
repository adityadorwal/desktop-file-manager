import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import threading
from core.voice import listen_once
from core.ai import respond_to_input
from core.commands import execute_command


def launch_gui():
    root = tk.Tk()
    root.title("Dorwal AI — Desktop Assistant")
    root.geometry("700x520")
    root.resizable(False, False)
    root.configure(bg="#1e1e2e")

    # ── Header ──────────────────────────────────────────────
    header = tk.Label(
        root,
        text="🤖  Dorwal AI",
        font=("Helvetica", 20, "bold"),
        bg="#1e1e2e",
        fg="#cdd6f4",
    )
    header.pack(pady=(16, 4))

    status_var = tk.StringVar(value="Ready")
    status_label = tk.Label(
        root,
        textvariable=status_var,
        font=("Helvetica", 10),
        bg="#1e1e2e",
        fg="#a6e3a1",
    )
    status_label.pack()

    # ── Output log ───────────────────────────────────────────
    output_box = scrolledtext.ScrolledText(
        root,
        width=80,
        height=14,
        font=("Courier", 10),
        bg="#181825",
        fg="#cdd6f4",
        insertbackground="white",
        state="disabled",
        borderwidth=0,
        relief="flat",
    )
    output_box.pack(padx=20, pady=10)

    def log(msg: str, tag: str = "normal"):
        output_box.configure(state="normal")
        output_box.insert(tk.END, msg + "\n", tag)
        output_box.see(tk.END)
        output_box.configure(state="disabled")

    output_box.tag_config("normal", foreground="#cdd6f4")
    output_box.tag_config("ai",     foreground="#89dceb")
    output_box.tag_config("user",   foreground="#a6e3a1")
    output_box.tag_config("error",  foreground="#f38ba8")
    output_box.tag_config("info",   foreground="#fab387")

    log("Dorwal AI initialised. Type a command or press 🎤 to speak.", "info")

    # ── Text input row ───────────────────────────────────────
    input_frame = tk.Frame(root, bg="#1e1e2e")
    input_frame.pack(padx=20, pady=(0, 6), fill="x")

    text_entry = tk.Entry(
        input_frame,
        font=("Helvetica", 11),
        bg="#313244",
        fg="#cdd6f4",
        insertbackground="white",
        relief="flat",
        bd=6,
    )
    text_entry.pack(side="left", fill="x", expand=True, ipady=4)

    def handle_text_input(event=None):
        text = text_entry.get().strip()
        if not text:
            return
        text_entry.delete(0, tk.END)
        log(f"You: {text}", "user")
        process_input(text)

    text_entry.bind("<Return>", handle_text_input)

    send_btn = tk.Button(
        input_frame,
        text="Send",
        font=("Helvetica", 10, "bold"),
        bg="#89b4fa",
        fg="#1e1e2e",
        relief="flat",
        padx=10,
        command=handle_text_input,
    )
    send_btn.pack(side="left", padx=(8, 0))

    # ── Button row ───────────────────────────────────────────
    btn_frame = tk.Frame(root, bg="#1e1e2e")
    btn_frame.pack(pady=6)

    def make_button(parent, text, color, cmd):
        return tk.Button(
            parent,
            text=text,
            font=("Helvetica", 10, "bold"),
            bg=color,
            fg="#1e1e2e",
            relief="flat",
            padx=14,
            pady=6,
            command=cmd,
        )

    def process_input(text: str):
        """Route text through command parser then AI."""
        result = execute_command(text)
        if result:
            log(f"[CMD] {result}", "info")
        ai_reply = respond_to_input(text)
        if ai_reply:
            log(f"Dorwal: {ai_reply}", "ai")

    # Mic button — runs voice recognition in a background thread
    def on_mic_click():
        status_var.set("🎙  Listening…")
        mic_btn.configure(state="disabled")

        def _listen():
            transcript = listen_once()
            root.after(0, _on_voice_done, transcript)

        threading.Thread(target=_listen, daemon=True).start()

    def _on_voice_done(transcript: str):
        mic_btn.configure(state="normal")
        if transcript:
            log(f"You (voice): {transcript}", "user")
            status_var.set("Processing…")
            process_input(transcript)
            status_var.set("Ready")
        else:
            log("Could not understand audio. Please try again.", "error")
            status_var.set("Ready")

    mic_btn = make_button(btn_frame, "🎤  Speak", "#a6e3a1", on_mic_click)
    mic_btn.pack(side="left", padx=6)

    # Notes button
    def on_notes_click():
        from core.commands import add_note, get_notes
        notes = get_notes()
        if not notes:
            note_text = "No notes saved yet."
        else:
            note_text = "\n".join(f"• {n}" for n in notes)
        messagebox.showinfo("📝 Your Notes", note_text or "No notes.")

    make_button(btn_frame, "📝  Notes", "#fab387", on_notes_click).pack(side="left", padx=6)

    # Reminders button
    def on_reminders_click():
        from core.commands import get_reminders
        reminders = get_reminders()
        if not reminders:
            r_text = "No reminders saved yet."
        else:
            r_text = "\n".join(f"• {r}" for r in reminders)
        messagebox.showinfo("⏰ Reminders", r_text or "No reminders.")

    make_button(btn_frame, "⏰  Reminders", "#cba6f7", on_reminders_click).pack(side="left", padx=6)

    # Clear log
    def on_clear():
        output_box.configure(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.configure(state="disabled")
        log("Log cleared.", "info")

    make_button(btn_frame, "🗑  Clear", "#f38ba8", on_clear).pack(side="left", padx=6)

    root.mainloop()
