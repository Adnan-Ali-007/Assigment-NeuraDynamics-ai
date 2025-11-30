from src.weather.weather_api import get_weather
import re


def weather_node(state):
    user_input = state.get("user_input", "")
    lower = user_input.lower()

    if "weather" not in lower and "temperature" not in lower:
        return {"weather_info": ""}

    location = extract_location(lower)
    weather_info = get_weather(location)
    return {"weather_info": weather_info}


def extract_location(text: str) -> str:
    m = re.search(r"(?:weather|temperature|forecast)\s+(?:in|of|for)\s+([A-Za-z][A-Za-z .,'-]+)", text)
    if m:
        return m.group(1).strip().title()

    m = re.search(r"([A-Za-z][A-Za-z .,'-]+)\s+(?:weather|temperature|forecast)", text)
    if m:
        return m.group(1).strip().title()

    return "New York"
