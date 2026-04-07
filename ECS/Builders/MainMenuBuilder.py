import pygame
from Core import States
from Globals import Settings
from ECS.Components import UITag, SpacialComponent, TextComponent, UIButtonComponent


class MainMenuBuilder:
    _ui_ids = []

    @staticmethod
    def build(world: dict):
        MainMenuBuilder.destroy(world)
        w = Settings.WINDOW.DESKTOP_WIDTH
        h = Settings.WINDOW.DESKTOP_HEIGHT
        cx = w // 2

        # TITLE TEXT
        title_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1
        world[title_id] = {
            UITag: UITag(),
            SpacialComponent: SpacialComponent(
                rect=pygame.Rect(cx - 200, h * 0.2, 400, 100)
            ),
            TextComponent: TextComponent(
                text="NORMIE SURVIVAL", color=(255, 255, 255), is_header=True
            ),
        }
        MainMenuBuilder._ui_ids.append(title_id)

        # SHOTGUN BUTTON
        btn_w, btn_h = 300, 60
        sg_btn_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1
        world[sg_btn_id] = {
            UITag: UITag(),
            UIButtonComponent: UIButtonComponent(
                rect=pygame.Rect(cx - (btn_w // 2), h * 0.5, btn_w, btn_h),
                text="EQUIP SHOTGUN",
                color=(255, 150, 50),
                action={"type": "START_GAME", "weapon": "shotgun"},
            ),
        }
        MainMenuBuilder._ui_ids.append(sg_btn_id)

        # SNIPER BUTTON
        sn_btn_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1
        world[sn_btn_id] = {
            UITag: UITag(),
            UIButtonComponent: UIButtonComponent(
                rect=pygame.Rect(cx - (btn_w // 2), h * 0.65, btn_w, btn_h),
                text="EQUIP SNIPER",
                color=(250, 50, 50),
                action={"type": "START_GAME", "weapon": "sniper"},
            ),
        }
        MainMenuBuilder._ui_ids.append(sn_btn_id)

    @staticmethod
    def destroy(world: dict):
        for eid in MainMenuBuilder._ui_ids:
            if eid in world:
                del world[eid]
        MainMenuBuilder._ui_ids.clear()
