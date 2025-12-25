from datetime import datetime, timedelta

def get_next_prayer(prayer_times):
    now = datetime.now()

    prayer_datetimes = {}
    for prayer, time_str in prayer_times.items():
        hour, minute = map(int, time_str.split(":"))
        prayer_datetimes[prayer] = now.replace(hour = hour, minute = minute, second = 0)

    for prayer, time in prayer_datetimes.items():
        if time > now:
            return prayer, time - now
    
    # If all prayers passed, next prayer is tomorrow's Fajr
    # Currently, we return today's Fajr with tomorrow's date (approximation)
    fajr_time_tomorrow = prayer_datetimes["Fajr"] + timedelta(days = 1)
    return "Fajr", fajr_time_tomorrow - now