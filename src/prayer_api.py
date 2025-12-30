import requests
from datetime import date as DateType

def _clean_time(t: str) -> str:
    '''
    API sometimes returns strings like '05:41 (EST)'.
    Keep only HH:MM
    '''
    return t.split()[0]

def get_prayer_times(city: str, country: str, method: int = 2, on_date: DateType | None = None) -> dict:
    '''
    Fetch prayer times for a city/country.
    If on_date is None, fetches today's times.
    If on_date is provided, fetches times for that date.
    '''
    if on_date is None:
        url = "https://api.aladhan.com/v1/timingsByCity"
    else:
        date_str = on_date.strftime("%d-%m-%Y") # DD-MM-YYYY
        url = f"https://api.aladhan.com/v1/timingsByCity/{date_str}"

    parameters = {
        "city": city,
        "country": country,
        "method": method
    }

    # Gets prayer times from Al Adhan API
    response = requests.get(url, params=parameters, timeout=15)
    response.raise_for_status()

    # Converts prayer times into a dictionary
    data = response.json()
    timings = data["data"]["timings"]

    return {
        "Fajr": _clean_time(timings["Fajr"]),
        "Dhuhr": _clean_time(timings["Dhuhr"]),
        "Asr": _clean_time(timings["Asr"]),
        "Maghrib": _clean_time(timings["Maghrib"]),
        "Isha": _clean_time(timings["Isha"])
    }