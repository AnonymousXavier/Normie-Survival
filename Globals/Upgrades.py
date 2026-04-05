UPGRADE_POOL = {
    # --- ACTIVES ---
    "shield": {"text": "Shield Generator", "max_level": 1, "conflicts_with": ["aoe"]},
    "aoe": {"text": "AOE Pulse", "max_level": 1, "conflicts_with": ["shield"]},

    # --- PERCENTAGE PASSIVES ---
    "move_speed": {"text": "Movement Speed +10%", "max_level": 5, "increment": 0.10},
    "max_hp": {"text": "Max HP +20%", "max_level": 5, "increment": 0.20},
    "overall_damage": {"text": "Overall Damage +10%", "max_level": 10, "increment": 0.10},
    "overall_attack_speed": {"text": "Attack Speed +10%", "max_level": 10, "increment": -0.10} 
}