import pygame
from Core import States
from Globals import Settings
from ECS.Components import UITag, SpacialComponent, StatsButtonComponent


class LevelUpMenuBuilder:
    @staticmethod
    def build(options: list):
        w = Settings.WINDOW.DESKTOP_WIDTH
        h = Settings.WINDOW.DESKTOP_HEIGHT

        btn_width = int(w * 0.3)
        btn_height = int(h * 0.08)
        padding = int(h * 0.02)

        total_height = (len(options) * btn_height) + ((len(options) - 1) * padding)

        start_x = (w // 2) - (btn_width // 2)
        start_y = (h // 2) - (total_height // 2)

        for i, option in enumerate(options):
            new_id = States.NEXT_ENTITY_ID
            States.NEXT_ENTITY_ID += 1

            # Use the loop index 'i' for perfect spacing
            button_y = start_y + (i * (btn_height + padding))
            rect = pygame.Rect(start_x, button_y, btn_width, btn_height)

            States.world[new_id] = {
                UITag: UITag(),
                SpacialComponent: SpacialComponent(rect=rect),
                StatsButtonComponent: StatsButtonComponent(
                    rect=rect,
                    title=option["title"],
                    description=option["reward"],  # This is the "+1 Gun" text
                    action={"type": "UPGRADE_SELECTED", "buff": option["key"]},
                ),
            }
