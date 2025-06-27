from tkinter import *
from tkinter import messagebox
from datetime import datetime
import requests
import random
import pygame

# --- Color Themes ---
DAY_THEME = {"bg": "#f5f5f5", "fg": "#222222", "text_bg": "#ffffff", "text_fg": "#000000"}
NIGHT_THEME = {"bg": "#1e1e1e", "fg": "#f1f1f1", "text_bg": "#2d2d2d", "text_fg": "#ffffff"}
theme = DAY_THEME

is_night = False
music_playing = False

# --- Suggestions ---
suggestions = [
    "Reflect on something you're grateful for today.",
    "Describe a challenge you faced and how you handled it.",
    "What was a moment of joy or peace you experienced recently?",
    "Write about something you're looking forward to.",
    "Note one thing you learned today.",
    "Describe a dream or goal you have.",
    "How do you feel right now, and why?",
]

# --- Toggle Theme ---
def toggle_mode():
    global is_night, theme
    is_night = not is_night
    theme = NIGHT_THEME if is_night else DAY_THEME
    apply_theme()

def apply_theme():
    root.config(bg=theme["bg"])
    journal_frame.config(bg=theme["bg"])
    city_frame.config(bg=theme["bg"])
    button_frame.config(bg=theme["bg"])
    bottom_frame.config(bg=theme["bg"])

    journal_text.config(bg=theme["text_bg"], fg=theme["text_fg"], insertbackground=theme["text_fg"])
    city_entry.config(bg=theme["text_bg"], fg=theme["text_fg"], insertbackground=theme["text_fg"])

    weather_label.config(bg=theme["bg"], fg=theme["fg"])
    quote_label.config(bg=theme["bg"], fg=theme["fg"])
    suggestion_label.config(bg=theme["bg"], fg=theme["fg"])
    title_label.config(bg=theme["bg"], fg=theme["fg"])

    for btn in [save_btn, weather_btn, quote_btn, mode_btn, suggest_btn, music_btn]:
        btn.config(bg=theme["bg"], fg=theme["fg"], activebackground=theme["text_bg"], activeforeground=theme["text_fg"])

    mode_btn.config(text="☀️ Day Mode" if is_night else "🌙 Night Mode")

# --- Save Journal ---
def save_entry():
    entry = journal_text.get("1.0", END).strip()
    if not entry:
        messagebox.showwarning("Empty Entry", "Please write something in the journal before saving.")
        return

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    city = city_entry.get() if city_entry.get() != "Enter city" else "Unknown"
    mood = "Happy"
    weather = weather_label.cget("text") if weather_label.cget("text") else "❌ Could not fetch weather data."
    quote = quote_label.cget("text") if quote_label.cget("text") else "❌ Could not fetch quote at this time."
    prompt = suggestion_label.cget("text").replace("📝 Prompt: ", "") if suggestion_label.cget("text") else "❌ No prompt."
    affirmation = "😊 Keep smiling! Today is your day!"

    formatted_entry = (
        "\n----------------------------------------\n"
        "--- Journal Entry (Morning) ---\n"
        f"🕒 Time: {time_now}\n"
        f"📍 City: {city}\n"
        f"🧠 Mood: {mood}\n"
        f"🌦 Weather: {weather}\n"
        f"🧘 Affirmation: {affirmation}\n"
        f"💬 Prompt: {prompt}\n"
        f"💡 Quote: {quote}\n\n"
        "✍️ Entry:\n"
        f"{entry}\n"
        "----------------------------------------\n"
    )

    with open("journal.txt", "a", encoding="utf-8") as f:
        f.write(formatted_entry)

    messagebox.showinfo("Saved", "Your journal entry has been saved.")
    journal_text.delete("1.0", END)

# --- Weather Fetch ---
def get_weather():
    try:
        city = city_entry.get().strip()
        if not city or city == "Enter city":
            raise ValueError("Enter a valid city name.")
        api_key = "3411eb616b292a6d673f822a61a1d3bc"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200 or "main" not in data:
            raise ValueError(data.get("message", "Failed to retrieve weather."))
        temp = data["main"]["temp"]
        condition = data["weather"][0]["description"].title()
        weather_label.config(text=f"{city.title()}: {temp}°C, {condition}")
    except Exception as e:
        weather_label.config(text=f"Error: {e}")

# --- Music Selection Window ---
def play_music():
    def select_track(track):
        pygame.mixer.music.load(f"music/{track}")
        pygame.mixer.music.play(-1)
        music_window.destroy()

    music_window = Toplevel(root)
    music_window.title("Choose Your Vibe 🎶")
    music_window.geometry("300x200")
    music_window.config(bg=theme["bg"])

    tracks = {
        "Calm Vibes": "calm.mp3",
        "Lo-Fi Chill": "lofi.mp3",
        "Focus Boost": "focus.mp3"
    }

    for name, file in tracks.items():
        btn = Button(music_window, text=name, command=lambda f=file: select_track(f),
                     bg=theme["bg"], fg=theme["fg"], width=20)
        btn.pack(pady=5)

    stop_btn = Button(music_window, text="🛑 Stop Music", command=lambda: pygame.mixer.music.stop(),
                      bg=theme["bg"], fg=theme["fg"], width=20)
    stop_btn.pack(pady=10)

# --- Quote Fetch ---
def get_quote():
    try:
        response = requests.get("https://api.quotable.io/random", timeout=5)
        if response.status_code == 200:
            data = response.json()
            quote = f"{data['content']} — {data['author']}"
            quote_label.config(text=quote)
        else:
            raise Exception("Primary quote API failed.")
    except:
        try:
            response = requests.get("https://zenquotes.io/api/random", timeout=5)
            if response.status_code == 200:
                data = response.json()
                quote = f"{data[0]['q']} — {data[0]['a']}"
                quote_label.config(text=quote)
            else:
                quote_label.config(text="Could not fetch quote.")
        except:
            quote_label.config(text="Could not fetch quote.")

# --- Random Prompt ---
def show_suggestion():
    suggestion = random.choice(suggestions)
    suggestion_label.config(text=f"📝 Prompt: {suggestion}")
    journal_text.insert(END, f"\n💬 Prompt Response: {suggestion}\n")

# --- GUI Setup ---
root = Tk()
pygame.mixer.init()
root.title("AI Daily Assistant")
root.iconbitmap("icon.ico")  
root.geometry("500x600")
root.config(bg=theme["bg"])

title_label = Label(root, text="🧠 AI Daily Assistant", font=("Helvetica", 20, "bold"), bg=theme["bg"], fg=theme["fg"])
title_label.pack(pady=15)

journal_frame = Frame(root, bg=theme["bg"])
journal_frame.pack(padx=20, pady=5, fill=BOTH, expand=False)

journal_scroll = Scrollbar(journal_frame)
journal_scroll.pack(side=RIGHT, fill=Y)

journal_text = Text(journal_frame, height=4, font=("Segoe UI", 11), wrap=WORD,
                    yscrollcommand=journal_scroll.set, bg=theme["text_bg"],
                    fg=theme["text_fg"], insertbackground=theme["text_fg"])
journal_text.pack(side=LEFT, fill=BOTH, expand=True)
journal_scroll.config(command=journal_text.yview)

save_btn = Button(root, text="💾 Save Entry", font=("Segoe UI", 10), command=save_entry)
save_btn.pack(pady=8)

# --- Weather & City Entry ---
def on_entry_click(event):
    if city_entry.get() == "Enter city":
        city_entry.delete(0, "end")
        city_entry.config(fg="black")

def on_focusout(event):
    if city_entry.get() == "":
        city_entry.insert(0, "Enter city")
        city_entry.config(fg="grey")

city_frame = Frame(root, bg=theme["bg"])
city_frame.pack(pady=5)

city_entry = Entry(city_frame, width=22, font=("Segoe UI", 10))
city_entry.insert(0, "Enter city")
city_entry.config(fg="grey")
city_entry.bind('<FocusIn>', on_entry_click)
city_entry.bind('<FocusOut>', on_focusout)
city_entry.grid(row=0, column=0, padx=4)

weather_btn = Button(city_frame, text="🌦", font=("Segoe UI", 9), command=get_weather, width=3)
weather_btn.grid(row=0, column=1, padx=3)

weather_label = Label(root, text="", font=("Segoe UI", 9), bg=theme["bg"], fg=theme["fg"])
weather_label.pack(pady=2)

# --- Quote & Prompt Buttons ---
button_frame = Frame(root, bg=theme["bg"])
button_frame.pack(pady=5)

quote_btn = Button(button_frame, text="💡 Quote", font=("Segoe UI", 9), command=get_quote, width=14)
quote_btn.grid(row=0, column=0, padx=5)

suggest_btn = Button(button_frame, text="📝 Prompt", font=("Segoe UI", 9), command=show_suggestion, width=14)
suggest_btn.grid(row=0, column=1, padx=5)

music_btn = Button(button_frame, text="🎵 Music", font=("Segoe UI", 9), command=play_music, width=14)
music_btn.grid(row=0, column=2, padx=5)

quote_label = Label(root, text="", wraplength=460, justify=LEFT, font=("Segoe UI", 9), bg=theme["bg"], fg=theme["fg"])
quote_label.pack(pady=3)

suggestion_label = Label(root, text="", font=("Segoe UI", 9), bg=theme["bg"], fg=theme["fg"])
suggestion_label.pack(pady=2)

# --- Bottom Button Bar ---
bottom_frame = Frame(root, bg=theme["bg"])
bottom_frame.pack(pady=8)

mode_btn = Button(bottom_frame, text="🌙 Night Mode", font=("Segoe UI", 9), command=toggle_mode, width=14)
mode_btn.grid(row=0, column=0, padx=6)

footer_label = Label(root, text="Made with ❤️ by Parth Sharma", font=("Segoe UI", 8), bg=theme["bg"], fg=theme["fg"])
footer_label.pack(side="bottom", pady=4)

# --- Finalize ---
apply_theme()
root.mainloop()
