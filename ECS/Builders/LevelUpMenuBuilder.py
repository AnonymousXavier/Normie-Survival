import pygame
from Core import States
from Globals import Settings
from ECS.Components import UITag, SpacialComponent, StatsButtonComponent, TextComponent


class LevelUpMenuBuilder:
    @staticmethod
    def build(options: list, current_level: int):
        w = Settings.WINDOW.DESKTOP_WIDTH
        h = Settings.WINDOW.DESKTOP_HEIGHT

        title_text = f"LEVEL UP! YOU REACHED LEVEL {current_level}"

        btn_width = int(w * 0.3)
        btn_height = int(h * 0.08)
        padding = int(h * 0.02)

        total_height = (len(options) * btn_height) + ((len(options) - 1) * padding)

        start_x = (w // 2) - (btn_width // 2)
        start_y = (h // 2) - (total_height // 2)

        # --- 1. SPAWN THE TITLE TEXT ---
        title_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1

        # Place it above the first button
        title_y = start_y - int(h * 0.1)
        title_rect = pygame.Rect(
            0, title_y, w, 40
        )  # Span the whole width so we can center the text

        States.world[title_id] = {
            UITag: UITag(),
            SpacialComponent: SpacialComponent(rect=title_rect),
            # We use a TextComponent to hold the string and color
            TextComponent: TextComponent(
                text=title_text, color=(255, 215, 0), is_header=True
            ),
        }

        # --- 2. SPAWN THE BUTTONS ---
        for i, option in enumerate(options):
            new_id = States.NEXT_ENTITY_ID
            States.NEXT_ENTITY_ID += 1

            button_y = start_y + (i * (btn_height + padding))
            rect = pygame.Rect(start_x, button_y, btn_width, btn_height)

            States.world[new_id] = {
                UITag: UITag(),
                SpacialComponent: SpacialComponent(rect=rect),
                StatsButtonComponent: StatsButtonComponent(
                    rect=rect,
                    title=option["title"],
                    description=option["reward"],
                    action={"type": "UPGRADE_SELECTED", "buff": option["key"]},
                ),
            }
