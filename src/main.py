from prayer_api import get_prayer_times
from time_utils import get_next_prayer
from config import load_settings, save_settings

def main():
    settings = load_settings()

    city = settings["city"]
    country = settings["country"]
    method = settings["method"]

    prayer_times = get_prayer_times(city, country)

    print("\nToday's Prayer Times:")
    for prayer, time in prayer_times.items():
        print(f"{prayer} {time}")
    
    next_prayer, time_remaining = get_next_prayer(prayer_times)
    hours, remainder = divmod(time_remaining.seconds, 3600)
    minutes = remainder // 60

    print(f"\nNext prayer: {next_prayer} in {hours}h {minutes}m")

if __name__ == "__main__":
    main()