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
    DashComponent,
)
from ECS.Builders.MainMenuBuilder import MainMenuBuilder
from ECS.Builders.PauseMenuBuilder import PauseMenuBuilder
from ECS.Builders.VictoryMenuBuilder import VictoryMenuBuilder
from ECS.Builders.GameOverMenuBuilder import GameOverMenuBuilder

from ECS import Factories
from Globals import Upgrades
from Globals import Settings
from Globals.AudioManager import AudioManager

# Initialize font
pygame.font.init()
UI_FONT = pygame.font.SysFont("Arial", 20, bold=True)


def process_events(world: dict, events: list):
    for event in events:
        if event.get("type") == "RETURN_TO_MENU":
            AudioManager.stop_music()

            # Delete everything that isn't a UI element
            entities_to_delete = [
                e_id for e_id, obj in States.world.items() if UITag not in obj
            ]
            for e_id in entities_to_delete:
                del States.world[e_id]

            # Clear the physical collision grid
            States.spatial_grid.clear()

            # Reset all Global Tracking States
            States.reset()

            # Destroy any lingering overlay menus

            GameOverMenuBuilder.destroy(States.world)
            VictoryMenuBuilder.destroy(States.world)
            PauseMenuBuilder.destroy(States.world)

            # Rebuild the Main Menu and shift the engine state
            MainMenuBuilder.build(States.world)
            States.CURRENT_STATE = "MENU"
            States.UI_DIRTY = True

        elif event.get("type") == "UPGRADE_SELECTED":
            apply_upgrade(event["buff"], world[States.PLAYER_ID])

            entities_to_delete = [e_id for e_id, obj in world.items() if UITag in obj]
            for e_id in entities_to_delete:
                del world[e_id]

            States.IS_LEVELING_UP = False
            States.UI_DIRTY = True

        elif event.get("type") == "TOGGLE_SOUND":
            Settings.GAME_OPTIONS.SOUND = not Settings.GAME_OPTIONS.SOUND

            PauseMenuBuilder.destroy(world)
            PauseMenuBuilder.build(world)
            States.UI_DIRTY = True

        elif event.get("type") == "TOGGLE_SCREEN_SHAKE":
            Settings.GAME_OPTIONS.SCREEN_SHAKE = not Settings.GAME_OPTIONS.SCREEN_SHAKE

            PauseMenuBuilder.destroy(world)
            PauseMenuBuilder.build(world)
            States.UI_DIRTY = True

        elif event.get("type") == "TOGGLE_MUSIC":
            Settings.GAME_OPTIONS.MUSIC = not Settings.GAME_OPTIONS.MUSIC

            if Settings.GAME_OPTIONS.MUSIC:
                AudioManager.play_music("bg_music")
            else:
                AudioManager.stop_music()

            PauseMenuBuilder.destroy(world)
            PauseMenuBuilder.build(world)
            States.UI_DIRTY = True

        elif event.get("type") == "START_GAME":
            chosen_weapon = event.get("weapon")

            # Clear the menu UI

            MainMenuBuilder.destroy(world)

            # Set the engine state to playing!
            States.CURRENT_STATE = "PLAYING"

            States.PLAYER_ID = Factories.spawn_player(
                States.world, States.spatial_grid, 0, 0, chosen_weapon
            )

            player_ent = States.world[States.PLAYER_ID]
            player_ent[ArsenalComponent].primary_weapon = chosen_weapon

            Factories.refresh_weapon(
                States.world, States.spatial_grid, States.PLAYER_ID, chosen_weapon, 1
            )

            States.camera = Factories.new_camera(
                (0, 0), Settings.CAMERA.SIZE, States.PLAYER_ID
            )
            States.UI_DIRTY = True

        elif event.get("type") == "QUIT_GAME":
            States.GAME_RUNNING = False
            States.UI_DIRTY = True

        elif event.get("type") == "CONTINUE_RUN":
            VictoryMenuBuilder.destroy(world)
            AudioManager.play_music("main_bgm")
            States.CURRENT_STATE = "PLAYING"
            States.UI_DIRTY = True


def get_level_up_options(player: dict) -> list:
    stats = player[PlayerStatsComponent]
    owned = stats.upgrades_owned

    # Filter out maxed upgrades
    valid_keys = [
        k
        for k, d in Upgrades.UPGRADE_POOL.items()
        if owned.get(k, 0) < d.get("max_level", 20)
    ]

    # Pick 3 random options
    chosen_keys = random.sample(valid_keys, min(3, len(valid_keys)))

    # FORMAT FOR THE STATSBUTTON (Fixes the KeyError)
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


def apply_upgrade(action_key: str, player: dict):
    stats = player[PlayerStatsComponent]
    # Update tracker
    stats.upgrades_owned[action_key] = stats.upgrades_owned.get(action_key, 0) + 1
    lvl = stats.upgrades_owned[action_key]

    # FITNESS SURVIVAL (Passives)
    if action_key == "passives":
        stats.speed_mult = 1.0 + (lvl * 0.05)
        stats.hp_mult = 1.0 + (lvl * 0.15)
        stats.regen_per_second = lvl * 0.2

    # DEFENSIVES (AOE / Shield)
    elif action_key == "defensives":
        # Handle AOE
        if AOEComponent not in player:
            player[AOEComponent] = AOEComponent()
        aoe = player[AOEComponent]

        # Bigger base radius, faster growth
        aoe.radius = 2.0 + (lvl * 0.4)

        # Massive damage scaling so it stays relevant
        aoe.damage = 5 + (lvl * 4)
        aoe.cooldown = max(0.2, 2.5 - (lvl * 0.25))

        # Handle Shield (Unlocks at Level 3 Defensive)
        if lvl >= 3:
            if ShieldComponent not in player:
                player[ShieldComponent] = ShieldComponent()
            s = player[ShieldComponent]
            s.max_hits = 1 + (lvl // 3)
            s.current_hits = s.max_hits

    # QUALITY OF LIFE & MAGNETISM (Pickup)
    elif action_key == "pickup":
        if CollectorComponent in player:
            player[CollectorComponent].range = 2.0 + (lvl * 0.8)

        # Recalculate the Dash Cooldown exactly once per level up!
        if DashComponent in player:
            player[DashComponent].cooldown = (
                Settings.COMPONENTS_BASE_VALUES.DASH.cooldown
                + (lvl / Settings.UPGRADES_MAX_LEVELS.QOL)
                * Settings.COMPONENTS_BASE_VALUES.DASH.duration
            )
            player[
                DashComponent
            ].duration = Settings.COMPONENTS_BASE_VALUES.DASH.duration + (
                lvl / Settings.UPGRADES_MAX_LEVELS.QOL
            )

    # PRIMARY WEAPON MASTERY
    elif action_key == "primary_weapon":
        w_type = player[ArsenalComponent].primary_weapon
        w_stats = player[ArsenalComponent].inventory[w_type]

        # Apply specific scaling based on the chosen weapon
        if w_type == "shotgun":
            w_stats.base_fire_rate = max(0.15, 1.0 - (lvl * 0.08))
            w_stats.base_damage = 1 + lvl
            w_stats.projectile_count = 3 + lvl
            new_count = 1 + (lvl // 3)

        elif w_type == "pistol":
            w_stats.base_damage = 15 + (lvl * 5)
            w_stats.base_fire_rate = max(0.15, 1.5 - (lvl * 0.2))

            # Pistol shoots 2 heavy round and it PIERCES!
            w_stats.projectile_count = 2
            w_stats.pierce = 1 + lvl

            # Physical orbiting guns: Adds 2 extra pistol every 3 levels
            new_count = 1 + int(lvl / 2)

        else:
            new_count = 1

        Factories.refresh_weapon(
            States.world, States.spatial_grid, States.PLAYER_ID, w_type, new_count
        )


def get_reward_description(key, next_lvl):
    """Generates the 'Relative to level' text for the StatsButton."""
    if key == "primary_weapon":
        # Generic text that works for any primary weapon
        if next_lvl % 4 == 0 or next_lvl % 5 == 0:
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
