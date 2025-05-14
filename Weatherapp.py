import tkinter as tk
from tkinter import messagebox
import requests
import json

class WeatherApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Weather App")
        self.window.geometry("400x300")
        
        # API key for OpenWeatherMap (users should replace with their own)
        self.api_key = "YOUR_API_KEY_HERE"
        
        # Create and pack widgets
        self.city_label = tk.Label(self.window, text="Enter City:")
        self.city_label.pack(pady=10)
        
        self.city_entry = tk.Entry(self.window)
        self.city_entry.pack(pady=5)
        
        self.search_button = tk.Button(self.window, text="Get Weather", command=self.get_weather)
        self.search_button.pack(pady=10)
        
        self.result_label = tk.Label(self.window, text="", wraplength=350)
        self.result_label.pack(pady=20)

    def get_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return
            
        try:
            # Make API request
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            data = json.loads(response.text)
            
            if response.status_code == 200:
                # Extract weather information
                temp = data['main']['temp']
                humidity = data['main']['humidity']
                desc = data['weather'][0]['description']
                
                # Update result label
                weather_info = f"Temperature: {temp}°C\n"
                weather_info += f"Humidity: {humidity}%\n"
                weather_info += f"Conditions: {desc.capitalize()}"
                self.result_label.config(text=weather_info)
            else:
                messagebox.showerror("Error", "City not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = WeatherApp()
    app.run()
    # Let's explain how this weather app works with example cities:
    print("\nChecking weather for major South Indian cities:")
    
    example_cities = ["Hyderabad", "Vijayawada", "Chennai", "Bangalore", "Thiruvananthapuram"]
    
    for city in example_cities:
        try:
            # Make API request for each city
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={app.api_key}&units=metric"
            response = requests.get(url)
            data = json.loads(response.text)
            
            if response.status_code == 200:
                # Extract and display weather information
                temp = data['main']['temp']
                humidity = data['main']['humidity']
                desc = data['weather'][0]['description']
                
                print(f"\nWeather in {city}:")
                print(f"Temperature: {temp}°C")
                print(f"Humidity: {humidity}%") 
                print(f"Conditions: {desc.capitalize()}")
            else:
                print(f"\nCould not fetch weather for {city}")
                
        except Exception as e:
            print(f"\nError getting weather for {city}: {str(e)}")
            continue
            # Record temperature for the city
            try:
                with open(f"{city}_temp_record.txt", "a") as f:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"{timestamp}: {temp}°C\n")
                print(f"Temperature recorded for {city}")
            except Exception as e:
                print(f"Could not record temperature for {city}: {str(e)}")
