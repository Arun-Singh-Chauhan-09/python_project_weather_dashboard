# Weather Dashboard

A Python desktop app I built to practice working with REST APIs and tkinter GUIs.
It pulls live weather data from OpenWeatherMap and displays current conditions
plus a 5-day forecast chart.

## What it does

- search any city and see current weather (temp, humidity, wind, pressure etc.)
- shows a 5-day average temperature or humidity chart
- click Toggle Chart to switch between the two
- save cities you check often to a favourites list
- click a favourite to instantly load that city

## Tech used

- Python 3
- tkinter for the GUI
- OpenWeatherMap API for weather data
- matplotlib for the charts
- pillow for loading weather icons
- python-dotenv to keep the API key out of the code

## Setup

1. Get a free API key from https://openweathermap.org/api

2. Clone or download the project

3. Open the `.env` file and replace the placeholder with your key:
   ```
   OPENWEATHER_API_KEY=paste_your_key_here
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run it:
   ```
   python main.py
   ```

## Project structure

```
weather_dashboard/
├── main.py              # entry point, loads the API key
├── gui.py               # all the tkinter window and layout code
├── weather_api.py       # handles the two API calls
├── data_processor.py    # cleans up the raw JSON into something usable
├── city_manager.py      # saves/loads favourite cities from a json file
├── data/
│   └── favourites.json  # stored favourites (auto-created on first run)
├── .env                 # your API key goes here (not committed to git)
├── .gitignore
└── requirements.txt
```

## Notes

- The `.env` file is listed in `.gitignore` so your API key wont accidentally
  get pushed to GitHub
- Weather icons are loaded from OpenWeatherMap's CDN - they might take
  a second on slow connections, thats normal
- Tested on Windows with Python 3.14

## Things I want to add eventually

- toggle between celsius and fahrenheit
- auto-refresh every few minutes
- wind direction display
- maybe package it as a .exe so it runs without needing Python installed
