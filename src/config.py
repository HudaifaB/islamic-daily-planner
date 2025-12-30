import json
from pathlib import Path

SETTINGS_PATH = Path(__file__).resolve().parent.parent / "data" / "user_settings.json"

DEFAULT_SETTINGS = {
    "city": "Ottawa",
    "country": "Canada",
    "method": 2
}

def load_settings():
    '''
    Loads user settings from JSON.
    If the file doesn't exist or is invalid, returns defaults.
    '''
    try:
        with open(SETTINGS_PATH, "r", encoding = "utf-8") as f:
            settings = json.load(f)
        
        # Merge with defaults (handles missing keys gracefully)
        return {**DEFAULT_SETTINGS, **settings}
    
    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    '''
    Saves user settings to JSON.
    '''
    with open(SETTINGS_PATH, "w", encoding = "utf-8") as f:
        json.dump(settings, f, indent = 4)