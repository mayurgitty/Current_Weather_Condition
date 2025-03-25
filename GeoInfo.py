import requests
import tkinter as tk
from tkinter import messagebox
from geopy.geocoders import Nominatim

def get_coordinates(city):
    """Convert city name to latitude & longitude."""
    geolocator = Nominatim(user_agent="weather_assistant")
    location = geolocator.geocode(city)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def get_weather():
    """Fetch weather details and display in GUI."""
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    lat, lon = get_coordinates(city)
    if lat is None or lon is None:
        messagebox.showerror("Error", "City not found. Please check the name.")
        return

    API_URL = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(API_URL)

    if response.status_code == 200:
        data = response.json()
        weather = data["current_weather"]
        temp = weather["temperature"]
        wind_speed = weather["windspeed"]
        conditions = weather["weathercode"]

        result_text.set(f"Weather in {city}:\nTemperature: {temp}°C\nWind Speed: {wind_speed} km/h\nCondition Code: {conditions}")
    else:
        messagebox.showerror("Error", "Error fetching weather data.")

# Create GUI window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x300")
root.configure(bg="#ADD8E6")

# Input field
tk.Label(root, text="Enter City Name:", font=("Arial", 12)).pack(pady=10)
city_entry = tk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=5)

# Fetch Weather Button
fetch_button = tk.Button(root, text="Get Weather", font=("Arial", 12), command=get_weather)
fetch_button.pack(pady=10)

# Result Label
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, font=("Arial", 12), bg="#ADD8E6", justify="left")
result_label.pack(pady=10)

# Run the application
root.mainloop()
