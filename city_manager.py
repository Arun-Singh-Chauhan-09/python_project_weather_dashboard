# saves and loads the favourite cities list from a local JSON file
import json
import os


class CityManager:

    def __init__(self, file_path="data/favourites.json"):
        self.file_path = file_path
        self.cities = self._load()

    def _load(self):
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r") as f:
                return json.load(f).get("cities", [])
        except json.JSONDecodeError:
            # file got corrupted somehow, just start fresh
            return []

    def _save(self):
        with open(self.file_path, "w") as f:
            json.dump({"cities": self.cities}, f, indent=4)

    def add_city(self, city):
        if city not in self.cities:
            self.cities.append(city)
            self._save()

    def remove_city(self, city):
        if city in self.cities:
            self.cities.remove(city)
            self._save()
