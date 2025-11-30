import requests
import requests
import os
from typing import Optional, Tuple


def _openweather_current(location: str, api_key: str) -> Optional[str]:
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": location, "appid": api_key, "units": "metric"}
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
        name = data.get("name", location)
        weather_desc = data.get("weather", [{}])[0].get("description", "Unknown").capitalize()
        temp = data.get("main", {}).get("temp")
        if temp is None:
            return None
        return f"Weather in {name}: {weather_desc}, Temperature: {temp}°C"
    except Exception:
        return None


def _geocode_open_meteo(location: str) -> Optional[Tuple[float, float, str]]:
    try:
        url = "https://geocoding-api.open-meteo.com/v1/search"
        resp = requests.get(url, params={"name": location, "count": 1}, timeout=10)
        data = resp.json()
        results = data.get("results")
        if not results:
            return None
        item = results[0]
        return float(item["latitude"]), float(item["longitude"]), item.get("name", location)
    except Exception:
        return None


def _open_meteo_current(lat: float, lon: float) -> Optional[dict]:
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "timezone": "UTC"
        }
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            return None
        return resp.json().get("current_weather")
    except Exception:
        return None


def _map_weathercode(code: int) -> str:
    mapping = {
        0: "Clear",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
    }
    return mapping.get(code, "Unknown")


def get_weather(location: str) -> str:
    key = os.getenv("OPENWEATHER_API_KEY")
    if key:
        res = _openweather_current(location, key)
        if res:
            return res

    geocoded = _geocode_open_meteo(location)
    if not geocoded:
        return f"Could not determine coordinates for '{location}'."

    lat, lon, resolved = geocoded
    current = _open_meteo_current(lat, lon)
    if not current:
        return f"Could not fetch weather for {resolved}."

    temp = current.get("temperature")
    wcode = current.get("weathercode")
    desc = _map_weathercode(int(wcode)) if wcode is not None else "Unknown"
    return f"Weather in {resolved}: {desc}, Temperature: {temp}°C"
