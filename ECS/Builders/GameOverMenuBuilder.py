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


class GameOverMenuBuilder:
    _ui_ids = []

    @staticmethod
    def build(world: dict):
        GameOverMenuBuilder.destroy(world)
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
            is_victory=False,
            weapon=wep,
        )

        # TITLE
        title_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1
        world[title_id] = {
            UITag: UITag(),
            SpacialComponent: SpacialComponent(
                rect=pygame.Rect(cx - 200, h * 0.2, 400, 100)
            ),
            TextComponent: TextComponent(
                text="YOU DIED", color=(255, 50, 50), is_header=True
            ),
        }
        GameOverMenuBuilder._ui_ids.append(title_id)

        # SURVIVAL STATS
        stats_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1

        # Leave secs as a float!
        mins = int(States.GAME_TIME // 60)
        secs = States.GAME_TIME % 60

        world[stats_id] = {
            UITag: UITag(),
            SpacialComponent: SpacialComponent(
                rect=pygame.Rect(cx - 200, h * 0.4, 400, 50)
            ),
            TextComponent: TextComponent(
                # Apply the :05.2f formatter here too!
                text=f"Survived: {mins}:{secs:05.2f}   |   Kills: {States.KILLS_COUNT}",
                color=(255, 255, 255),
                is_header=False,
            ),
        }
        GameOverMenuBuilder._ui_ids.append(stats_id)

        # --- END GAME BUTTONS ---
        btn_w, btn_h = 350, 60
        btn_spacing = 20
        start_y = h * 0.55

        # 1. RETURN TO MENU BUTTON
        retry_btn_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1
        world[retry_btn_id] = {
            UITag: UITag(),
            UIButtonComponent: UIButtonComponent(
                rect=pygame.Rect(cx - (btn_w // 2), start_y, btn_w, btn_h),
                text="RETURN TO MAINMENU",
                color=(50, 150, 255),  # Sleek Blue
                action={"type": "RETURN_TO_MENU"},
            ),
        }
        GameOverMenuBuilder._ui_ids.append(retry_btn_id)

        # 2. QUIT TO DESKTOP BUTTON
        quit_btn_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1
        world[quit_btn_id] = {
            UITag: UITag(),
            UIButtonComponent: UIButtonComponent(
                rect=pygame.Rect(
                    cx - (btn_w // 2), start_y + btn_h + btn_spacing, btn_w, btn_h
                ),
                text="QUIT GAME",
                color=(200, 50, 50),  # Aggressive Red
                action={"type": "QUIT_GAME"},
            ),
        }
        GameOverMenuBuilder._ui_ids.append(quit_btn_id)

    @staticmethod
    def destroy(world: dict):
        for eid in GameOverMenuBuilder._ui_ids:
            if eid in world:
                del world[eid]
        GameOverMenuBuilder._ui_ids.clear()
