from binascii import Error
import requests
import geocoder
import pyttsx3
# For API KEY visit this site https://openweathermap.org/api
API_KEY = "0de27b66a5cbaaf5b92fbe57c1c860a0"
BASE_URL = "https://api.openweathermap.org/data/2.5/"

engine = pyttsx3.init()

def speak(text):
    #Speak ou the given text
    engine.say(text)
    engine.runAndWait()
def get_weather(city=None, lat=None, lon=None):
    # Fetch weather data by city name or coordiantes
    if city:
        url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    else:
        url = f"{BASE_URL}weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    return response.json()

def get_forecast(city=None, lat=None, lon=None):
    """Fetch 5-day forecast """
    if city:
        url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric"
    else:
        url = f"{BASE_URL}forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    return response.json()

def display_weather(data):
    """Display current weather conditions."""
    """200 means success"""
    if data.get("cod") != 200:
        error_msgv = Error
        print(" Error:", data.get("message", "Unknown error"))
        speak(error_msgv)
        return

    city = data["name"]
    temp = data["main"]["temp"]
    condition = data["weather"][0]["description"].title()
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]

    print(f"\n Weather in {city}:")
    print(f"🌡 Temperature: {temp}°C")
    print(f"☁ Condition: {condition}")
    print(f"💧 Humidity: {humidity}%")
    print(f"💨 Wind Speed: {wind} m/s")
    speak(f"Weather in {city}:, Temperature: {temp},Condition: {condition}, Humidity: {humidity}, Wind Speed: {wind}")

def display_forecast(data):
    """Display 3-day forecast summary."""
    if data.get("cod") != "200":
        print(" Error:", data.get("message", "Unknown error"))
        return

    print("\n📅 3-Day Forecast:")
    forecasts = data["list"]

    # Display 1 forecast per day (every 8 intervals = 24h)
    for i in range(0, 24, 8):  
        day = forecasts[i]
        date = day["dt_txt"].split(" ")[0]
        temp = day["main"]["temp"]
        condition = day["weather"][0]["description"].title()
        print(f" {date} → 🌡 {temp}°C | ☁ {condition}")

def main():
    print(" Weather App with Auto Location Detection + Voice ")

    # Try detecting location
    g = geocoder.ip("me")
    if g.ok:
        lat, lon = g.latlng
        print(f"Detected Location: {g.city}, {g.country}")
        data = get_weather(lat=lat, lon=lon)
        forecast = get_forecast(lat=lat, lon=lon)
    else:
        print("⚠ Could not detect location. Please enter a city name.")
        city = input("Enter city name: ")
        data = get_weather(city=city)
        forecast = get_forecast(city=city)

        
    display_weather(data)
    display_forecast(forecast)

if __name__ == "__main__":
    main()