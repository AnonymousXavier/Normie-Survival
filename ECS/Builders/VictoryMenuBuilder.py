import pygame
from Core import States
from Globals import Settings
from Globals.SaveManager import SaveManager
from ECS.Components import (
    UITag,
    SpacialComponent,
    TextComponent,
    UIButtonComponent,
    PlayerStatsComponent,
    ArsenalComponent,
)


class VictoryMenuBuilder:
    _ui_ids = []

    @staticmethod
    def build(world: dict):
        VictoryMenuBuilder.destroy(world)
        w = Settings.WINDOW.DESKTOP_WIDTH
        h = Settings.WINDOW.DESKTOP_HEIGHT
        cx = w // 2

        # Safely grab player stats for the final score
        player = world.get(States.PLAYER_ID)
        p_stats = player.get(PlayerStatsComponent) if player else None
        lvl = p_stats.level if p_stats else 0

        # Grab the weapon used
        arsenal = player.get(ArsenalComponent) if player else None
        wep = arsenal.primary_weapon if arsenal else "Unknown"

        # --- THE SAVE HOOK ---
        SaveManager.save_run(
            level=lvl,
            kills=States.KILLS_COUNT,
            time_survived=States.GAME_TIME,
            is_victory=True,
            weapon=wep,
        )

        # GOLDEN TITLE TEXT
        title_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1
        world[title_id] = {
            UITag: UITag(),
            SpacialComponent: SpacialComponent(
                rect=pygame.Rect(cx - 250, h * 0.2, 500, 100)
            ),
            TextComponent: TextComponent(
                text="VICTORY ACHIEVED", color=Settings.COLOURS.GOLD, is_header=True
            ),
        }
        VictoryMenuBuilder._ui_ids.append(title_id)

        # FINAL STATS TEXT
        stats_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1
        world[stats_id] = {
            UITag: UITag(),
            SpacialComponent: SpacialComponent(
                rect=pygame.Rect(cx - 200, h * 0.4, 400, 50)
            ),
            TextComponent: TextComponent(
                text=f"Level Reached: {lvl}   |   Total Kills: {States.KILLS_COUNT}",
                color=(255, 255, 255),
                is_header=False,
            ),
        }
        VictoryMenuBuilder._ui_ids.append(stats_id)

        # QUIT BUTTON
        btn_w, btn_h = 300, 60
        quit_btn_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1
        world[quit_btn_id] = {
            UITag: UITag(),
            UIButtonComponent: UIButtonComponent(
                rect=pygame.Rect(cx - (btn_w // 2), h * 0.6, btn_w, btn_h),
                text="EXIT GAME",
                color=(200, 50, 50),
                action={"type": "QUIT_GAME"},
            ),
        }
        VictoryMenuBuilder._ui_ids.append(quit_btn_id)

    @staticmethod
    def destroy(world: dict):
        for eid in VictoryMenuBuilder._ui_ids:
            if eid in world:
                del world[eid]
        VictoryMenuBuilder._ui_ids.clear()
