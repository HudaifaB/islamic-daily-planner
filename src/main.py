from datetime import datetime, timedelta
from prayer_api import get_prayer_times
from time_utils import get_next_prayer
from config import load_settings, save_settings

def main():
    settings = load_settings()

    city = settings["city"]
    country = settings["country"]
    method = settings["method"]

    now = datetime.now()
    today_date = now.date()

    today_times = get_prayer_times(city, country, method=method, on_date=today_date)

    print("\nToday's Prayer Times:")
    for prayer, time in today_times.items():
        print(f"{prayer}: {time}")
    
    # Try to compute next prayer (without tomorrow)
    next_prayer, time_remaining = get_next_prayer(today_times, today_date, now)

    # If next_prayer indicates tomorrow, fetch tomorrow_times and recompute next prayer
    if "tomorrow" in next_prayer:
        tomorrow_date = today_date + timedelta(days=1)
        tomorrow_times = get_prayer_times(city, country, method=method, on_date=tomorrow_date)
        next_prayer, time_remaining = get_next_prayer(today_times, today_date, now, tomorrow_times=tomorrow_times)

    hours, remainder = divmod(int(time_remaining.total_seconds()), 3600)
    minutes = remainder // 60
    print(f"\nNext prayer: {next_prayer} in {hours}h {minutes}m")

if __name__ == "__main__":
    main()