import requests

def get_prayer_times(city, country, method=2):
    url = "https://api.aladhan.com/v1/timingsByCity"
    parameters = {
        "city": city,
        "country": country,
        "method": method
    }

    # Gets prayer times from Al Adhan API
    response = requests.get(url, params=parameters)
    response.raise_for_status()

    # Converts prayer times into a dictionary
    data = response.json()
    timings = data["data"]["timings"]

    return {
        "Fajr": timings["Fajr"],
        "Dhuhr": timings["Dhuhr"],
        "Asr": timings["Asr"],
        "Maghrib": timings["Maghrib"],
        "Isha": timings["Isha"]
    }