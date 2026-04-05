import random

UPGRADE_POOL = {
    # --- PASSIVES ---
    "move_speed": {"text": "Move Speed +10%", "inc": 0.10, "max_val": 2.5},
    "damage_mult": {"text": "Damage +15%", "inc": 0.15, "max_val": float("inf")},
    "max_hp": {"text": "Max HP +20%", "inc": 0.20, "max_val": float("inf")},
    "regen": {"text": "Regeneration +0.2/s", "inc": 0.2, "max_val": float("inf")},
    # --- DEFENSIVES ---
    "shield": {
        "text": "Shield: Extra HP & Regen",
        "inc": 0.15,
        "max_val": 0.80,
    },  # Max 80% extra HP
    "aoe_rate": {"text": "AOE: Attack Rate", "inc": 0.5, "max_val": 5.0},
    "aoe_damage": {"text": "AOE: Damage", "inc": 2, "max_val": float("inf")},
    "aoe_radius": {"text": "AOE: Radius", "inc": 0.5, "max_val": 4.0},  # Max 4 cells
    # --- SHOTGUN ---
    "sg_fire_rate": {"text": "Shotgun: Fire Rate", "inc": 0.4, "max_val": 5.0},
    "sg_damage": {"text": "Shotgun: Damage", "inc": 1, "max_val": float("inf")},
    "sg_projectiles": {"text": "Shotgun: +1 Pellet", "inc": 1, "max_val": 10},
    "sg_spread": {"text": "Shotgun: Spread Angle", "inc": 15, "max_val": 180},
}


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
