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

### 1. Clone the repo

```
git clone https://github.com/Arun-Singh-Chauhan-09/python_project_weather_dashboard.git
cd python_project_weather_dashboard
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

If you are on Python 3.14 and see any errors, try:

```
python -m pip install -r requirements.txt
```

### 3. Set up the API key

Run this command in the project folder to create the `.env` file automatically:

```
echo OPENWEATHER_API_KEY=a696f9459525284760d0cd74e3fb4fca > .env
```

That's it — no need to create or edit the file manually. If the key ever
stops working, get a free replacement at https://openweathermap.org/api
(registration takes about a minute).

The `.gitignore` file already excludes `.env` so your key won't accidentally get
pushed to GitHub.

### 4. Run the app

```
python main.py
```

The window will open. Type any city name and press Enter or click Search.

### Troubleshooting

| Problem | Fix |
|---|---|
| "API key missing" popup | Check `.env` has the key on its own line with no extra spaces |
| "City not found" error | Check spelling — use English names (e.g. `Munich` not `Munchen`) |
| "No internet connection" | Check your network and try again |
| Chart is blank on startup | Search for a city first — chart only shows after a successful search |

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
      a second on slow connections, that's normal.
- Tested on Windows with Python 3.14

## Things I want to add eventually

- toggle between celsius and fahrenheit
- auto-refresh every few minutes
- wind direction display
- maybe package it as a .exe so it runs without needing Python installed
