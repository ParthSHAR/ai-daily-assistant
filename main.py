import requests
import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Fetch current weather
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code != 200:
        return f"Unable to fetch weather for {city}. Please check the city name or try again later."
    weather = data['weather'][0]['description']
    temp = data['main']['temp']
    return f"It's {temp}°C with {weather} in {city}."

# Generate journal entry
def generate_journal(weather_report, mood):
    prompt = f"""
Write a short, cozy, slightly poetic journal entry for today.
Include this weather update: "{weather_report}"
Reflect the user's current mood: "{mood}"
Make it feel warm, personal, and gentle.
"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Daily Assistant"
    }
    payload = {
    "model": "mistralai/mistral-small-3.2-24b-instruct-2506",  # <- Updated model name
    "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    result = response.json()
    print("🔍 API Response Debug:", result)
    if "choices" in result:
        return result['choices'][0]['message']['content']
    else:
        return "❌ Failed to generate journal. Please check API key or model settings."

# Get daily quote or affirmation
def get_daily_quote():
    prompt = "Give me one short, inspiring quote or affirmation for today. Keep it under 20 words."
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Daily Assistant"
    }
    payload = {
        "model": "mistralai/mistral-small-3.2-24b-instruct-2506",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    result = response.json()
    print("💬 Quote Debug:", result)
    if "choices" in result:
        return result['choices'][0]['message']['content'].strip('"\n ')
    else:
        return "❌ Quote generation failed."

# Get a short reflection prompt
def get_reflection_prompt():
    prompt = "Give me a gentle, thoughtful reflection question to ask at the end of a journal entry. Keep it short and personal."
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Daily Assistant"
    }
    payload = {
        "model": "mistralai/mistral-small-3.2-24b-instruct-2506",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    result = response.json()
    print("🪞 Reflection Prompt Debug:", result)
    if "choices" in result:
        return result['choices'][0]['message']['content'].strip('"\n ')
    else:
        return "❌ Reflection prompt generation failed."

# Generate daily goals based on mood and weather
def generate_goals(weather_report, mood):
    prompt = f"""
Suggest 3 short, practical goals someone could aim for today,
given this mood: "{mood}" and this weather: "{weather_report}".

Keep them:
- Positive
- Specific
- Under 15 words each
- Output as a numbered list
"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Daily Assistant"
    }
    payload = {
        "model": "mistralai/mistral-small-3.2-24b-instruct-2506",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    result = response.json()
    print("🎯 Goals Debug:", result)
    if "choices" in result:
        return result['choices'][0]['message']['content'].strip()
    else:
        return "❌ Goal generation failed."

# Main program flow
def main():
    print("📍 Enter your city: ", end="")
    city = input()
    print("\n😊 How are you feeling today? (e.g., happy, tired, stressed): ", end="")
    mood = input()

    print("\n🔍 Fetching weather info...")
    weather_report = get_weather(city)
    print("\n🌤️ Weather Report:", weather_report)

    if "Unable to fetch" in weather_report:
        return

    print("\n🧠 Generating your AI journal entry...")
    journal_entry = generate_journal(weather_report, mood)

    print("\n🌟 Getting your daily quote...")
    quote = get_daily_quote()

    print("\n🎯 Generating 3 practical goals for your day...")
    goals = generate_goals(weather_report, mood)

    print("\n🪞 Generating a reflection prompt for your journal...")
    reflection_prompt = get_reflection_prompt()

    print("\n📝 Your AI Weather Journal Entry:")
    print("----------------------------------")
    print(journal_entry)
    print("\n💬 Daily Quote:", quote)
    print("\n🎯 Today's Goals:\n" + goals)
    print("\n🪞 Reflection Prompt:", reflection_prompt)

    save_option = input("\n💾 Do you want to save this entry to a file? (yes/no): ").strip().lower()
    if save_option.startswith("y"):
        try:
            file_path = os.path.abspath("weather_journal.txt")
            with open(file_path, "a", encoding="utf-8") as file:
                file.write("\n" + "-"*40 + "\n")
                file.write(f"City: {city}\n")
                file.write(f"Weather: {weather_report}\n")
                file.write(f"Mood: {mood}\n")
                file.write(journal_entry + "\n")
                file.write(f"Quote: {quote}\n")
                file.write("Goals:\n" + goals + "\n")
                file.write(f"Reflection Prompt: {reflection_prompt}\n")
            print("📂 Saving to path:", os.path.abspath("weather_journal.txt"))
            print(f"✅ Journal entry saved to '{file_path}'")
        except Exception as e:
            print("❌ Failed to save entry:", e)


if __name__ == "__main__":
    main()