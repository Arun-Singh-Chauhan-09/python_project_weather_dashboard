#cleans up raw JSON from the API into usable dictionaries

from datetime import datetime
from collections import defaultdict


class WeatherDataProcessor:

    @staticmethod
    def process_current(data):
        # convert unix timestamps to readable time
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
        sunset  = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")

        return {
            "city":        data["name"],
            "temperature": round(data["main"]["temp"], 1),
            "feels_like":  round(data["main"]["feels_like"], 1),
            "humidity":    data["main"]["humidity"],
            "pressure":    data["main"]["pressure"],
            "visibility":  round(data.get("visibility", 0) / 1000, 1),  # metres -> km
            "description": data["weather"][0]["description"].capitalize(),
            "wind_speed":  data["wind"]["speed"],
            "sunrise":     sunrise,
            "sunset":      sunset,
        }

    @staticmethod
    def process_forecast(data):
        # group all the 3-hour readings by day, then average them
        daily_temps    = defaultdict(list)
        daily_humidity = defaultdict(list)

        for item in data["list"]:
            day = datetime.fromtimestamp(item["dt"]).strftime("%d %b")
            daily_temps[day].append(item["main"]["temp"])
            daily_humidity[day].append(item["main"]["humidity"])

        dates, avg_temps, avg_humidity = [], [], []

        for day in daily_temps:
            dates.append(day)
            avg_temps.append(round(sum(daily_temps[day]) / len(daily_temps[day]), 1))
            avg_humidity.append(round(sum(daily_humidity[day]) / len(daily_humidity[day]), 1))

        # only need 5 days max
        return dates[:5], avg_temps[:5], avg_humidity[:5]
