from datetime import datetime, timedelta, date as DateType

PRAYER_ORDER = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]

def _to_datetime(on_date: DateType, time_str: str) -> datetime:
    hour, minute = map(int, time_str.split(":"))
    return datetime(on_date.year, on_date.month, on_date.day, hour, minute, 0)

def get_next_prayer(today_times: dict, today_date: DateType, now: datetime, tomorrow_times: dict | None = None):
    '''
    Returns (next_prayer_name, time_remaining_timedelta).

    - Checks remaining prayers today.
    - If all passed, uses tomorrow_times['Fajr'] if provided (accurate).
    - If tomorrow_times is not provided, falls back to approximate (today Fajr + 1 day).
    '''
    # Find the next prayer for today
    for prayer in PRAYER_ORDER:
        prayer_dt = _to_datetime(today_date, today_times[prayer])
        if prayer_dt > now:
            return prayer, prayer_dt - now
    
    # If all prayers passed, use tomorrow's actual Fajr if available
    if tomorrow_times is not None:
        tomorrow_date = today_date + timedelta(days=1)
        fajr_dt = _to_datetime(tomorrow_date, tomorrow_times["Fajr"])
        return "Fajr (tomorrow)", fajr_dt - now
    
    # Fallback approximation if tomorrow's prayer times not fetched
    fajr_today_dt = _to_datetime(today_date, today_times["Fajr"])
    fajr_approx_dt = fajr_today_dt + timedelta(days=1)
    return "Fajr (tomorrow approx)", fajr_approx_dt - now