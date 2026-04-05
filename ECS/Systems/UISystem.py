import pygame
import random

from Core import States
from ECS.Components import (
    UITag,
    PlayerStatsComponent,
    ShieldComponent,
    AOEComponent,
    WeaponStats,
)
from Globals import Upgrades

# Initialize font
pygame.font.init()
UI_FONT = pygame.font.SysFont("Arial", 20, bold=True)


def process_events(world: dict, events: list):
    for event in events:
        if event.get("type") == "UPGRADE_SELECTED":
            # 1. Apply the specific buff we discussed earlier
            apply_upgrade(event["buff"], world[States.PLAYER_ID])

            # 2. Destroy the Menu (Clean up the screen!)
            entities_to_delete = [e_id for e_id, obj in world.items() if UITag in obj]
            for e_id in entities_to_delete:
                del world[e_id]

            # 3. Unpause the game!
            States.IS_LEVELING_UP = False
            print("Game Resumed!")


def get_level_up_options(player: dict) -> list:
    owned = player[PlayerStatsComponent].upgrades_owned
    valid_keys = []

    for key, data in Upgrades.UPGRADE_POOL.items():
        # Check max level
        if owned.get(key, 0) >= data["max_level"]:
            continue

        # Check conflicts
        if any(conflict in owned for conflict in data.get("conflicts_with", [])):
            continue

        valid_keys.append(key)

    chosen_keys = random.sample(valid_keys, min(3, len(valid_keys)))

    # Return formatted data for your UI Builder
    return [
        {"key": key, "text": Upgrades.UPGRADE_POOL[key]["text"]} for key in chosen_keys
    ]


def apply_upgrade(action_key: str, player: dict):
    stats = player[PlayerStatsComponent]
    up_data = Upgrades.UPGRADE_POOL[action_key]
    inc = up_data["inc"]
    max_v = up_data["max_val"]

    # 1. PLAYER PASSIVES
    if action_key == "move_speed":
        stats.speed_mult = min(stats.speed_mult + inc, max_v)
    elif action_key == "damage_mult":
        stats.damage_mult += inc
    elif action_key == "max_hp":
        old_max = stats.final_max_hp
        stats.hp_mult += inc
        # Heal by the amount of HP gained
        stats.current_hp += stats.final_max_hp - old_max
    elif action_key == "regen":
        stats.regen_per_second += inc

    # 2. DEFENSIVES (Shield & AOE)
    elif action_key == "shield":
        if ShieldComponent not in player:
            player[ShieldComponent] = ShieldComponent(extra_hp_ratio=inc, max_hits=1)
        else:
            s = player[ShieldComponent]
            s.extra_hp_ratio = min(s.extra_hp_ratio + inc, max_v)
            s.max_hits = min(s.max_hits + 1, 5)  # Cap at 5 hits

    elif action_key.startswith("aoe_"):
        if AOEComponent not in player:
            player[AOEComponent] = AOEComponent()
        aoe = player[AOEComponent]
        if action_key == "aoe_rate":
            aoe.fire_rate = min(aoe.fire_rate + inc, max_v)
        elif action_key == "aoe_damage":
            aoe.damage += inc
        elif action_key == "aoe_radius":
            aoe.radius = min(aoe.radius + inc, max_v)

    # 3. SHOTGUN (Arsenal)
    elif action_key.startswith("sg_"):
        # Access the weapon stats inside the inventory
        sg = player[ArsenalComponent].inventory.get("shotgun")
        if sg:
            if action_key == "sg_fire_rate":
                sg.base_fire_rate = min(sg.base_fire_rate + inc, max_v)
            elif action_key == "sg_damage":
                sg.base_damage += inc
            elif action_key == "sg_projectiles":
                sg.projectile_count = min(sg.projectile_count + int(inc), max_v)
            elif action_key == "sg_spread":
                sg.spread_angle = min(sg.spread_angle + inc, max_v)
