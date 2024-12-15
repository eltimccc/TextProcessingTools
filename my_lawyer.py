import os
import requests
import pyperclip
from time import sleep
import threading
import tkinter as tk
from pynput.mouse import Controller
from screeninfo import get_monitors
import urllib3
from dotenv import load_dotenv

load_dotenv()


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = os.getenv('URL')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}

def paraphrase_text(original_text):
    """Перефразирует текст через API."""
    payload = {
        "model": os.getenv("MODEL"),
        "messages": [
            {"role": "system", "content": os.getenv('ROLE_CONTENT')},
            {"role": "user", "content": original_text}
        ],
        "stream": False,
        "repetition_penalty": 1
    }
    try:
        response = requests.post(URL, headers=HEADERS, json=payload, verify=False)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Ошибка ответа API.")
    except requests.RequestException as e:
        return f"Ошибка API: {e}"

def show_translation(text, x, y):
    """Отображает текст рядом с курсором."""
    screen = get_monitors()[0]
    popup = tk.Toplevel()
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)

    text_widget = tk.Text(popup, bg="yellow", fg="black", font=("Calibri", 14), wrap="word", height=10, width=40)
    text_widget.insert("1.0", text)
    text_widget.config(state="normal")
    text_widget.pack(padx=5, pady=5)

    popup.update_idletasks()
    window_width, window_height = popup.winfo_width(), popup.winfo_height()

    x = int(min(x, screen.width - window_width - 10))
    y = int(min(y, screen.height - window_height - 10))

    popup.geometry(f"+{x}+{y}")
    popup.after(15000, popup.destroy)

def clipboard_listener():
    """Отслеживает изменения в буфере обмена."""
    mouse = Controller()
    previous_text = ""
    while True:
        try:
            current_text = pyperclip.paste()
            if current_text and current_text != previous_text:
                previous_text = current_text
                paraphrased_text = paraphrase_text(current_text)
                x, y = mouse.position
                root.after(0, show_translation, paraphrased_text, x, y)
        except Exception as e:
            print(f"Ошибка: {e}")
        sleep(1)

if __name__ == "__main__":
    threading.Thread(target=clipboard_listener, daemon=True).start()
    root = tk.Tk()
    root.withdraw()
    root.mainloop()
