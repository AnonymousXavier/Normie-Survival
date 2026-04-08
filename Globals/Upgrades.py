import random

UPGRADE_POOL = {
    "primary_weapon": {
        "text": "Primary Weopon",
        "max_level": 40,
    },
    "defensives": {"text": "Defensive Upgrades", "max_level": 30},
    "passives": {"text": "Personal Stats", "max_level": 30},
    "pickup": {"text": "XP Magnet", "max_level": 15},
}


def get_reward_description(key, next_lvl):
    """Generates the 'Relative to level' text for the StatsButton."""
    if key == "primary_weapon":
        # The big milestone upgrades
        if next_lvl % 4 == 0 or next_lvl % 5 == 0:
            return "EXTRA BARREL + DAMAGE & FIRE RATE"
        return "FIRE RATE & LETHALITY BOOST"

    if key == "passives":
        return "+SPEED, +MAX HP & HEALTH REGEN"

    if key == "shield":
        # New hit every 2 levels
        if next_lvl % 2 == 0:
            return "NEW ARMOR CHARGE & FASTER REPAIR"
        return "FASTER ARMOR RECHARGE"

    if key == "aoe":
        return "WIDER ATTACK RADIUS & MORE DAMAGE"

    return "PASSIVE STAT BOOST"


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
