import pyperclip
import time
from deep_translator import GoogleTranslator
import tkinter as tk
from pynput.mouse import Controller
from screeninfo import get_monitors


def show_translation(translation, x, y):
    """Показывает перевод рядом с выделенным текстом, не выходя за края экрана"""
    screen = get_monitors()[0]
    screen_width = screen.width
    screen_height = screen.height

    popup = tk.Tk()
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)

    label = tk.Label(
        popup, text=translation, bg="yellow", fg="black", font=("Calibri", 14), padx=5, pady=5, wraplength=300
    )
    label.pack()

    popup.update_idletasks()
    window_width = popup.winfo_width()
    window_height = popup.winfo_height()

    if x + window_width > screen_width:
        x = screen_width - window_width - 10
    if y + window_height > screen_height:
        y = screen_height - window_height - 10

    popup.geometry(f"+{int(x)}+{int(y)}")

    popup.after(3000, popup.destroy)
    popup.mainloop()

def main():
    translator = GoogleTranslator(source='en', target='ru')
    mouse = Controller()
    last_text = ""

    print("Скрипт запущен. Копируйте текст для перевода...")

    while True:
        try:
            current_text = pyperclip.paste()
            if current_text != last_text:
                last_text = current_text

                translation = translator.translate(current_text)

                x, y = mouse.position

                show_translation(translation, x, y)
        except Exception as e:
            print(f"Ошибка: {e}")
        time.sleep(0.5)

if __name__ == "__main__":
    main()
