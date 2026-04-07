import json
import os


class SaveManager:
    SAVE_FILE = "normie_save.json"

    @staticmethod
    def load_data():
        """Loads the save file, or returns an empty dict if it's a new player."""
        if not os.path.exists(SaveManager.SAVE_FILE):
            return {}
        try:
            with open(SaveManager.SAVE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}  # Failsafe in case the file gets corrupted

    @staticmethod
    def save_run(level, kills, time_survived, is_victory, weapon):
        """Updates the JSON file with the latest run data."""
        data = SaveManager.load_data()

        current_run = {
            "level": level,
            "kills": kills,
            "time_survived": time_survived,
            "weapon": weapon,
        }

        # Always track the most recent attempt
        data["last_run"] = current_run

        # Only overwrite the 'last_successful_run' if they actually beat the boss
        if is_victory:
            data["last_successful_run"] = current_run

        # Write it back to the local directory
        with open(SaveManager.SAVE_FILE, "w") as f:
            json.dump(data, f, indent=4)
