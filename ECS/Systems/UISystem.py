import pygame
import random

from Core import States
from ECS.Components import (
    UITag,
    PlayerStatsComponent,
    ShieldComponent,
    AOEComponent,
    ArsenalComponent,
    CollectorComponent,
)
from ECS import Factories
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
    stats = player[PlayerStatsComponent]
    owned = stats.upgrades_owned

    # 1. Filter out maxed upgrades
    valid_keys = [
        k
        for k, d in Upgrades.UPGRADE_POOL.items()
        if owned.get(k, 0) < d.get("max_level", 20)
    ]

    # 2. Pick 3 random options
    chosen_keys = random.sample(valid_keys, min(3, len(valid_keys)))

    # 3. FORMAT FOR THE STATSBUTTON (Fixes the KeyError)
    formatted_options = []
    for key in chosen_keys:
        next_lvl = owned.get(key, 0) + 1
        name = Upgrades.UPGRADE_POOL[key]["text"]

        formatted_options.append(
            {
                "key": key,
                "title": f"LVL {next_lvl} {name.upper()}",
                "reward": get_reward_description(key, next_lvl),
            }
        )

    return formatted_options


# ECS/Systems/UISystem.py


def apply_upgrade(action_key: str, player: dict):
    stats = player[PlayerStatsComponent]
    # Update tracker
    stats.upgrades_owned[action_key] = stats.upgrades_owned.get(action_key, 0) + 1
    lvl = stats.upgrades_owned[action_key]

    # --- 1. FITNESS SURVIVAL (Passives) ---
    if action_key == "passives":
        stats.speed_mult = 1.0 + (lvl * 0.05)
        stats.hp_mult = 1.0 + (lvl * 0.15)
        stats.regen_per_second = lvl * 0.2

    # --- 2. DEFENSIVES (AOE / Shield) ---
    elif action_key == "defensives":
        # Handle AOE
        if AOEComponent not in player:
            player[AOEComponent] = AOEComponent()
        aoe = player[AOEComponent]
        aoe.radius = 2.0 + (lvl * 0.3)
        aoe.damage = 2 + (lvl * 1)
        aoe.cooldown = 3.0 / (1 + (lvl * 0.1))  # Harmonic scaling!

        # Handle Shield (Unlocks at Level 3 Defensive)
        if lvl >= 3:
            if ShieldComponent not in player:
                player[ShieldComponent] = ShieldComponent()
            s = player[ShieldComponent]
            s.max_hits = 1 + (lvl // 3)
            s.current_hits = s.max_hits

    # --- 3. MAGNETISM (Pickup) ---
    elif action_key == "pickup":
        if CollectorComponent in player:
            player[CollectorComponent].range = 2.0 + (lvl * 0.8)

    # --- 4. SHOTGUN MASTERY (The Arsenal) ---
    elif action_key == "shotgun":
        sg_stats = player[ArsenalComponent].inventory["shotgun"]

        # A. Harmonic Fire Rate: Scaled down from 0.4 to 0.15 for better control
        # This fixes the "spraying at level 5" issue.
        sg_stats.base_fire_rate = 1.0 / (1 + (lvl * 0.15))

        # B. Damage
        sg_stats.base_damage = 1 + (lvl // 2)

        # C. Gun Count Cycle (1 + lvl // 4)
        new_count = 1 + (lvl // 4)

        # D. Physical Respawn + STAGGERING
        # We call the factory to refresh the physical shotgun entities with timing offsets
        from ECS import Factories

        Factories.refresh_player_shotguns(
            States.world, States.spatial_grid, States.PLAYER_ID, new_count
        )

    print(f"🛠️ [MASTER UPGRADE] {action_key.upper()} reached Level {lvl}")


def get_reward_description(key, next_lvl):
    """Generates the 'Relative to level' text for the StatsButton."""
    if key == "shotgun":
        # Every 4 levels adds a physical gun
        if next_lvl % 4 == 0:
            return "+1 Gun, +Damage & Fire Rate"
        return "+Damage & Fire Rate Boost"

    if key == "passives":
        return "+Speed, +Max HP & +0.2 Regen"

    if key == "shield":
        # New hit every 2 levels
        if next_lvl % 2 == 0:
            return "+1 Max Hit & Faster Recharge"
        return "Faster Shield Recharge"

    if key == "aoe":
        return "+Radius, +Damage & Faster Pulse"

    return "Passive Stat Boost"
