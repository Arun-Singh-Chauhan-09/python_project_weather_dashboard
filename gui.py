import tkinter as tk
from tkinter import messagebox
from weather_api import WeatherAPI
from city_manager import CityManager
from data_processor import WeatherDataProcessor
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import requests
from PIL import Image, ImageTk
from io import BytesIO
import threading


class WeatherGUI:

    def __init__(self, root, api_key):
        self.root = root
        self.root.title("Advanced Weather Dashboard")
        self.root.geometry("1200x700")
        self.root.minsize(900, 600)

        self.api          = WeatherAPI(api_key)
        self.city_manager = CityManager()
        self.chart_type   = "temp"  # toggles between temp and humidity

        # storing last fetch so toggle chart doesnt re-request the api
        self.dates    = []
        self.temps    = []
        self.humidity = []

        self._build_layout()

        # pressing enter should work the same as clicking search
        self.city_entry.bind("<Return>", lambda e: self.search())

    # --- layout ---

    def _build_layout(self):
        self.root.configure(bg="#1e1e2f")

        # top search bar
        top = tk.Frame(self.root, bg="#1e1e2f")
        top.pack(pady=15)

        self.city_entry = tk.Entry(top, font=("Arial", 14), width=25)
        self.city_entry.grid(row=0, column=0, padx=10)
        self.city_entry.focus_set()

        self.search_btn = tk.Button(top, text="Search", bg="#4CAF50", fg="white",
                                    command=self.search)
        self.search_btn.grid(row=0, column=1)

        tk.Button(top, text="Toggle Chart", bg="#2196F3", fg="white",
                  command=self.toggle_chart).grid(row=0, column=2, padx=10)

        # small status bar just below the search
        self.status_var = tk.StringVar(value="Type a city name and hit Search")
        tk.Label(self.root, textvariable=self.status_var, bg="#13131f",
                 fg="#aaaaaa", anchor="w", font=("Arial", 9),
                 padx=10).pack(fill="x")

        # main area splits into left info panel and right chart panel
        main = tk.Frame(self.root, bg="#1e1e2f")
        main.pack(fill="both", expand=True, padx=20, pady=5)

        self._build_left_panel(main)
        self._build_right_panel(main)

    def _build_left_panel(self, parent):
        self.left = tk.Frame(parent, bg="#2b2b45", padx=20, pady=20)
        self.left.pack(side="left", fill="both", expand=True, padx=10)

        self.city_label = tk.Label(self.left, font=("Arial", 24, "bold"),
                                   bg="#2b2b45", fg="white")
        self.city_label.pack(pady=10)

        self.icon_label = tk.Label(self.left, bg="#2b2b45")
        self.icon_label.pack()

        self.temp_label = tk.Label(self.left, font=("Arial", 20),
                                   bg="#2b2b45", fg="#FFD700")
        self.temp_label.pack()

        self.feels_label = tk.Label(self.left, font=("Arial", 11),
                                    bg="#2b2b45", fg="#aaaaaa")
        self.feels_label.pack()

        self.details_label = tk.Label(self.left, font=("Arial", 12),
                                      bg="#2b2b45", fg="white", justify="left")
        self.details_label.pack(pady=10)

        tk.Button(self.left, text="Add to Favourites", bg="#ff9800", fg="white",
                  command=self.add_favourite).pack(pady=5)

        tk.Button(self.left, text="Remove Selected", bg="#e53935", fg="white",
                  command=self.remove_favourite).pack(pady=5)

        tk.Label(self.left, text="Favourite Cities",
                 bg="#2b2b45", fg="white").pack(pady=5)

        self.fav_listbox = tk.Listbox(self.left, width=25, bg="#1e1e2f",
                                      fg="white", selectbackground="#4CAF50")
        self.fav_listbox.pack(pady=5)
        self.fav_listbox.bind("<<ListboxSelect>>", self._on_favourite_click)

        self._refresh_favourites()

    def _build_right_panel(self, parent):
        self.right = tk.Frame(parent, bg="#2b2b45", padx=10, pady=10)
        self.right.pack(side="right", fill="both", expand=True, padx=10)
        self.chart_canvas = None

    # --- fetching weather ---

    def search(self):
        city = self.city_entry.get().strip().title()
        if not city:
            messagebox.showerror("Oops", "Please enter a city name first")
            return

        # disable the button so user cant spam click while loading
        self.search_btn.config(state="disabled", text="Loading...")
        self.status_var.set(f"Looking up {city}...")

        # run the API calls in a thread so the window doesnt freeze
        t = threading.Thread(target=self._fetch, args=(city,), daemon=True)
        t.start()

    def _fetch(self, city):
        try:
            current  = self.api.fetch_current_weather(city)
            forecast = self.api.fetch_forecast(city)

            processed                        = WeatherDataProcessor.process_current(current)
            self.dates, self.temps, self.humidity = WeatherDataProcessor.process_forecast(forecast)

            # hand off to main thread to update the UI
            self.root.after(0, self._show_results, processed, current)

        except Exception as err:
            self.root.after(0, self._show_error, str(err))

    def _show_results(self, processed, current):
        self._update_info_panel(processed, current["weather"][0]["icon"])
        self._draw_chart()
        self.status_var.set(f"Showing weather for {processed['city']}")
        self.search_btn.config(state="normal", text="Search")

    def _show_error(self, msg):
        messagebox.showerror("Error", msg)
        self.status_var.set(f"Something went wrong: {msg}")
        self.search_btn.config(state="normal", text="Search")

    def _update_info_panel(self, data, icon_code):
        self.city_label.config(text=data["city"])
        self.temp_label.config(text=f"{data['temperature']} °C")
        self.feels_label.config(text=f"Feels like {data['feels_like']} °C")

        self.details_label.config(text=(
            f"\nCondition: {data['description']}\n"
            f"Humidity: {data['humidity']}%\n"
            f"Pressure: {data['pressure']} hPa\n"
            f"Visibility: {data['visibility']} km\n"
            f"Wind Speed: {data['wind_speed']} m/s\n"
            f"Sunrise: {data['sunrise']}\n"
            f"Sunset: {data['sunset']}\n"
        ))

        # try to load the weather icon - not a big deal if it fails
        try:
            url  = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
            img  = Image.open(BytesIO(requests.get(url, timeout=5).content))
            photo = ImageTk.PhotoImage(img)
            self.icon_label.config(image=photo)
            self.icon_label.image = photo  # keep reference so it doesnt get garbage collected
        except Exception:
            pass

    # --- chart ---

    def _draw_chart(self):
        if not self.dates:
            return

        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()

        fig = plt.Figure(figsize=(6, 4), dpi=100)
        fig.patch.set_facecolor("#2b2b45")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#1e1e2f")

        if self.chart_type == "temp":
            ax.plot(self.dates, self.temps, color="#FFD700", marker="o", linewidth=2)
            ax.fill_between(self.dates, self.temps, alpha=0.15, color="#FFD700")
            ax.set_title("5-Day Average Temperature", color="white")
            ax.set_ylabel("Temperature (°C)", color="white")
        else:
            ax.plot(self.dates, self.humidity, color="#2196F3", marker="o", linewidth=2)
            ax.fill_between(self.dates, self.humidity, alpha=0.15, color="#2196F3")
            ax.set_title("5-Day Average Humidity", color="white")
            ax.set_ylabel("Humidity (%)", color="white")

        ax.tick_params(axis='x', rotation=45, colors="white")
        ax.tick_params(axis='y', colors="white")
        for spine in ax.spines.values():
            spine.set_edgecolor("#555555")

        fig.tight_layout()

        self.chart_canvas = FigureCanvasTkAgg(fig, self.right)
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)
        self.chart_canvas.draw()

    def toggle_chart(self):
        self.chart_type = "humidity" if self.chart_type == "temp" else "temp"
        self._draw_chart()

    # --- favourites ---

    def add_favourite(self):
        city = self.city_entry.get().strip().title()
        if city:
            self.city_manager.add_city(city)
            self._refresh_favourites()
            self.status_var.set(f"Added {city} to favourites")

    def remove_favourite(self):
        sel = self.fav_listbox.curselection()
        if sel:
            city = self.fav_listbox.get(sel[0])
            self.city_manager.remove_city(city)
            self._refresh_favourites()
            self.status_var.set(f"Removed {city} from favourites")

    def _refresh_favourites(self):
        self.fav_listbox.delete(0, tk.END)
        if not self.city_manager.cities:
            self.fav_listbox.insert(tk.END, "No favourites yet")
        else:
            for city in self.city_manager.cities:
                self.fav_listbox.insert(tk.END, city)

    def _on_favourite_click(self, event):
        sel = self.fav_listbox.curselection()
        if sel:
            city = self.fav_listbox.get(sel[0])
            self.city_entry.delete(0, tk.END)
            self.city_entry.insert(0, city)
            self.search()

