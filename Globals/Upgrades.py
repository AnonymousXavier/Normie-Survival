import random

# Globals/Upgrades.py
UPGRADE_POOL = {
    "shotgun": {"text": "Shotgun Mastery", "max_level": 40},
    "defensives": {"text": "Defensive Systems", "max_level": 20},
    "passives": {"text": "Fitness Survival", "max_level": 20},
    "pickup": {"text": "Magnetism", "max_level": 10},
}


def get_reward_description(key, next_lvl):
    # ... existing cases ...
    if key == "pickup":
        return f"+{1.0} Grid Cells Pickup Range"
    return "Passive Stat Boost"


def get_random_upgrades(owned_upgrades: dict) -> list:
    valid_keys = []

    for key, data in UPGRADE_POOL.items():
        current_lvl = owned_upgrades.get(key, 0)
        if current_lvl >= data.get("max_level", 99):
            continue

        # Check for conflicts (e.g., can't have Shield if you have AOE)
        conflict = False
        for c_key in data.get("conflicts_with", []):
            if c_key in owned_upgrades:
                conflict = True
                break
        if conflict:
            continue

        valid_keys.append(key)

    # 3. Pick 3 unique random keys (or fewer if the pool is dry)
    chosen_keys = random.sample(valid_keys, min(3, len(valid_keys)))

    # 4. Format them for the LevelUpMenuBuilder
    return [{"key": k, "text": UPGRADE_POOL[k]["text"]} for k in chosen_keys]
