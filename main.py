import tkinter as tk
from tkinter import messagebox
from gui import WeatherGUI
import os
from dotenv import load_dotenv

# loads the .env file so we can grab the API key safely
load_dotenv()

def main():
    api_key = os.getenv("OPENWEATHER_API_KEY")

    # if key is missing or still the placeholder, show a helpful message
    if not api_key or api_key == "your_api_key_here":
        messagebox.showerror(
            "API Key Missing",
            "Couldn't find your API key.\n\n"
            "Open the .env file and set it like this:\n"
            "OPENWEATHER_API_KEY=paste_your_key_here\n\n"
            "You can get a free key from openweathermap.org"
        )
        return

    root = tk.Tk()
    WeatherGUI(root, api_key)
    root.mainloop()

if __name__ == "__main__":
    main()
