import random

UPGRADE_POOL = {
    "primary_weapon": {
        "text": "Weapon Mastery",
        "max_level": 40,
    },  # Replaces "shotgun" and "sniper"
    "defensives": {"text": "Defensive Systems", "max_level": 20},
    "passives": {"text": "Physical Upgrades", "max_level": 20},
    "pickup": {"text": "XP Magnet", "max_level": 10},
}


def get_reward_description(key, next_lvl):
    """Generates the 'Relative to level' text for the StatsButton."""
    if key == "shotgun":
        if next_lvl % 4 == 0:
            return "+1 Gun, +Damage & Fire Rate"
        return "+Damage & Fire Rate Boost"
    if key == "passives":
        return "+Speed, +Max HP & +0.2 Regen"
    if key == "defensives":
        if next_lvl == 3:
            return "Unlocks Energy Shield"
        return "+AOE Radius & Damage"
    if key == "pickup":
        return f"+{0.8} Grid Cells Pickup Range"
    return "Passive Stat Boost"


def get_random_upgrades(owned_upgrades: dict) -> list:
    valid_keys = []

    for key, data in UPGRADE_POOL.items():
        current_lvl = owned_upgrades.get(key, 0)
        if current_lvl >= data.get("max_level", 99):
            continue
        valid_keys.append(key)

    chosen_keys = random.sample(valid_keys, min(3, len(valid_keys)))

    # Format the dictionaries with 'title' and 'reward' for the LevelUpMenuBuilder
    formatted_options = []
    for key in chosen_keys:
        next_lvl = owned_upgrades.get(key, 0) + 1
        name = UPGRADE_POOL[key]["text"]

        formatted_options.append(
            {
                "key": key,
                "title": f"LVL {next_lvl} {name.upper()}",
                "reward": get_reward_description(
                    key, next_lvl
                ),  # The sub-text description
            }
        )

    return formatted_options
