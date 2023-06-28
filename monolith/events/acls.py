from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import requests
import json

def get_photo(city, state):
    try:
        url = "https://api.pexels.com/v1/search"
        params = {
            "query": city + " " + state,
            "per_page": 1,
        }
        headers = {
            "Authorization": PEXELS_API_KEY
        }
        r = requests.get(url, headers=headers, params=params)
        photo_info = json.loads(r.content)

        url = photo_info["photos"][0]["url"]

        return {"picture_url": url}
    except (KeyError):
        return {"picture_url": None}

def get_weather_data(city, state):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},US&limit=1&appid={OPEN_WEATHER_API_KEY}"
    r = requests.get(url)
    try:
        lat = json.loads(r.content)[0]["lat"]
        lon = json.loads(r.content)[0]["lon"]
    except IndexError:
        return None

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_API_KEY}"
    r = requests.get(url)
    try:
        description = json.loads(r.content)["weather"][0]["description"]
        temp = json.loads(r.content)["main"]["temp"]
        weather = {"temp": temp, "description": description}

    except IndexError:
        return None

    return weather
