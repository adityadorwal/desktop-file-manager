from core.gui import launch_gui
from core.voice import listen_and_print

def on_mic_click():
    listen_and_print()

if __name__ == "__main__":
    launch_gui(on_mic_click)
