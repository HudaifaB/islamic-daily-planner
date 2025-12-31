from datetime import datetime, timedelta
from prayer_api import get_prayer_times
from time_utils import get_next_prayer
from config import load_settings, save_settings

def print_prayer_times(title: str, prayer_times: dict):
    '''
    Prints the prayer times for today or tomorrow.
    '''
    print(f"\n{title}")
    print("-" * len(title))
    for prayer, t in prayer_times.items():
        print(f"{prayer:<8} {t}")

def show_today(settings: dict):
    '''
    Prints today's prayer times.
    '''
    now = datetime.now()
    today_date = now.date()

    today_times = get_prayer_times(
        settings["city"], settings["country"],
        method=settings["method"],
        on_date=today_date
    )

    print_prayer_times("Today's Prayer Times", today_times)

    # Next prayer logic (accurate tomorrow fajr if needed)
    next_prayer, time_remaining = get_next_prayer(today_times, today_date, now)

    if "tomorrow" in next_prayer:
        tomorrow_date = today_date + timedelta(days=1)
        tomorrow_times = get_prayer_times(
            settings["city"], settings["country"],
            method=settings["method"],
            on_date=tomorrow_date
        )
        next_prayer, time_remaining = get_next_prayer(today_times, today_date, now, tomorrow_times=tomorrow_times)

    total_seconds = int(time_remaining.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    print(f"\nNext prayer: {next_prayer} in {hours}h {minutes}m")

def show_tomorrow(settings: dict):
    '''
    Prints tomorrow's prayer times.
    '''
    tomorrow_date = (datetime.now().date() + timedelta(days=1))
    tomorrow_times = get_prayer_times(
        settings["city"], settings["country"],
        method=settings["method"],
        on_date=tomorrow_date
    )
    print_prayer_times("Tomorrow's Prayer Times", tomorrow_times)

def change_location(settings: dict):
    '''
    Changes location or keeps current location.
    '''
    print("\nChange location (press Enter to keep current)")
    city = input(f"City [Current: {settings['city']}]: ").strip()
    country = input(f"Country [Current: {settings['country']}]: ").strip()

    if city:
        city = city[0].upper() + city[1:] # Capitalize first letter
        settings["city"] = city
    if country:
        country = country[0].upper() + country[1:] # Capitalize first letter
        settings["country"] = country
    
    save_settings(settings)
    print("Saved location.")

def change_method(settings: dict):
    print("\nCalculation method (AlAdhan 'method' parameter)")
    print("Common examples:")
    print("  2  = ISNA (North America)")
    print("  3  = MWL")
    print("  4  = Umm al-Qura")
    print("  5  = Egyptian General Authority")
    print("  7  = University of Islamic Sciences, Karachi")
    print("  8  = Gulf Region")
    print("  9  = Kuwait")
    print("  10 = Qatar")
    print("  12 = Singapore")

    raw = input(f"Enter method number [Current: {settings['method']}]: ").strip()
    if not raw:
        print("Kept current calculation method.")
        return
    
    try:
        method = int(raw)
        if method <= 0:
            raise ValueError
        settings["method"] = method
        save_settings(settings)
        print("Saved calculation method.")
    except ValueError:
        print("Please enter a valid positive integer method number.")

def menu():
    settings = load_settings()

    while True:
        print("\n=== Islamic Daily Planner ===")
        print(f"Location: {settings['city']}, {settings['country']} | Method: {settings['method']}")
        print("1) Show today's prayer times")
        print("2) Show tomorrow's prayer times")
        print("3) Change location")
        print("4) Change calculation method")
        print("5) Exit")

        choice = input("Choose an option above (1-5): ").strip()

        if choice == "1":
            show_today(settings)
        elif choice == "2":
            show_tomorrow(settings)
        elif choice == "3":
            change_location(settings)
            # reload settings in case settings were changed
            settings = load_settings()
        elif choice == "4":
            change_method(settings)
            settings = load_settings()
        elif choice == "5":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number from 1-5.")

if __name__ == "__main__":
    menu()