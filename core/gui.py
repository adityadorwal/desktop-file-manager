import tkinter as tk

def launch_gui(on_mic_click):
    root = tk.Tk()
    root.title("Dorwal AI")

    mic_button = tk.Button(root, text="🎤 Speak", command=on_mic_click)
    mic_button.pack(padx=20, pady=20)

    root.mainloop()
