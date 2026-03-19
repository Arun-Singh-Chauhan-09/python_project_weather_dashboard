import requests

class WeatherAPI:

    def __init__(self, api_key):
        self.api_key = api_key
        # both endpoints i need from openweathermap
        self.current_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

    def _get(self, url, params):
        # adds the key and metric units to every request so i dont repeat it
        params["appid"] = self.api_key
        params["units"] = "metric"

        try:
            res = requests.get(url, params=params, timeout=10)

            # give a clearer message than the default http errors
            if res.status_code == 401:
                raise Exception("API key looks wrong - double check your .env file")
            if res.status_code == 404:
                raise Exception(f"Couldn't find '{params.get('q', '')}' - check spelling?")

            res.raise_for_status()
            return res.json()

        except requests.exceptions.ConnectionError:
            raise Exception("No internet connection")
        except requests.exceptions.Timeout:
            raise Exception("Request took too long, try again")
        except Exception as e:
            raise Exception(str(e))

    def fetch_current_weather(self, city):
        return self._get(self.current_url, {"q": city})

    def fetch_forecast(self, city):
        return self._get(self.forecast_url, {"q": city})
