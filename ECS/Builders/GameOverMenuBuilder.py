import pygame
from Core import States
from Globals import Settings
from ECS.Components import (
    UITag,
    SpacialComponent,
    TextComponent,
    UIButtonComponent,
    PlayerStatsComponent,
)


class GameOverMenuBuilder:
    _ui_ids = []

    @staticmethod
    def build(world: dict):
        GameOverMenuBuilder.destroy(world)
        w = Settings.WINDOW.DESKTOP_WIDTH
        h = Settings.WINDOW.DESKTOP_HEIGHT
        cx = w // 2

        # 1. THE GRIM TITLE
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

        # 2. SURVIVAL STATS
        stats_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1

        # Format the raw seconds into MM:SS
        mins = int(States.GAME_TIME // 60)
        secs = int(States.GAME_TIME % 60)

        world[stats_id] = {
            UITag: UITag(),
            SpacialComponent: SpacialComponent(
                rect=pygame.Rect(cx - 200, h * 0.4, 400, 50)
            ),
            TextComponent: TextComponent(
                text=f"Survived: {mins}:{secs:02d}   |   Kills: {States.KILLS_COUNT}",
                color=(255, 255, 255),
                is_header=False,
            ),
        }
        GameOverMenuBuilder._ui_ids.append(stats_id)

        # 3. EXIT BUTTON
        btn_w, btn_h = 300, 60
        quit_btn_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1
        world[quit_btn_id] = {
            UITag: UITag(),
            UIButtonComponent: UIButtonComponent(
                rect=pygame.Rect(cx - (btn_w // 2), h * 0.6, btn_w, btn_h),
                text="EXIT GAME",
                color=(150, 50, 50),
                action={
                    "type": "QUIT_GAME"
                },  # Reuses the exact same logic from the Victory screen!
            ),
        }
        GameOverMenuBuilder._ui_ids.append(quit_btn_id)

    @staticmethod
    def destroy(world: dict):
        for eid in GameOverMenuBuilder._ui_ids:
            if eid in world:
                del world[eid]
        GameOverMenuBuilder._ui_ids.clear()
