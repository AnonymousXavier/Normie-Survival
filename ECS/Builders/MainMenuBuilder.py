import pygame
from Core import States
from Globals import Settings, Cache
from Globals.SaveManager import SaveManager
from ECS.Components import (
    UITag,
    SpacialComponent,
    TextComponent,
    UIButtonComponent,
    StatPanelComponent,
    UIImageComponent,
)


class MainMenuBuilder:
    _ui_ids = []

    @staticmethod
    def build(world: dict):
        MainMenuBuilder.destroy(world)
        w = Settings.WINDOW.DESKTOP_WIDTH
        h = Settings.WINDOW.DESKTOP_HEIGHT
        cx = w // 2
        cy = h // 2

        # --- 1. COVER ART (Moody Background Watermark) ---
        # Scales the 450x450 image to cover the window while keeping its 1:1 aspect ratio
        bg_size = min(w, h)
        bg_x = cx - (bg_size // 2)
        bg_y = cy - (bg_size // 2)

        cover_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1
        cover_surf = pygame.transform.smoothscale(
            Cache.SPRITES.MENU.COVER_ART, (bg_size, bg_size)
        )

        world[cover_id] = {
            UITag: UITag(),
            SpacialComponent: SpacialComponent(
                rect=pygame.Rect(bg_x, bg_y, bg_size, bg_size)
            ),
            # Drops the opacity so the art bleeds beautifully through the dark terminal!
            UIImageComponent: UIImageComponent(image=cover_surf, alpha=50),
        }
        MainMenuBuilder._ui_ids.append(cover_id)

        # --- 2. MISSION TERMINAL (The Center Core) ---
        # Responsive sizing: Fills the screen leaving a crisp 20px border on small windows
        panel_w = min(500, w - 40)
        panel_h = min(450, h - 40)
        panel_x = cx - (panel_w // 2)
        panel_y = cy - (panel_h // 2)

        terminal_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1
        world[terminal_id] = {
            UITag: UITag(),
            SpacialComponent: SpacialComponent(
                rect=pygame.Rect(panel_x, panel_y, panel_w, panel_h)
            ),
            StatPanelComponent: StatPanelComponent(
                title="MAIN MENU", stats={}, theme_color=(100, 200, 255)
            ),
        }
        MainMenuBuilder._ui_ids.append(terminal_id)

        # --- 3. THE PREMIUM TITLE ---
        # Tucked nicely right below the terminal's divider line
        title_y = panel_y + 80

        shadow_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1
        world[shadow_id] = {
            UITag: UITag(),
            SpacialComponent: SpacialComponent(
                rect=pygame.Rect(cx + 4, title_y + 4, 0, 0)
            ),
            TextComponent: TextComponent(
                text="NORMIE SURVIVAL", color=(20, 20, 20), is_header=True
            ),
        }
        MainMenuBuilder._ui_ids.append(shadow_id)

        title_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1
        world[title_id] = {
            UITag: UITag(),
            SpacialComponent: SpacialComponent(rect=pygame.Rect(cx, title_y, 0, 0)),
            TextComponent: TextComponent(
                text="NORMIE SURVIVAL", color=(255, 215, 0), is_header=True
            ),
        }
        MainMenuBuilder._ui_ids.append(title_id)

        # --- 4. SAVE DATA (Anchored beneath title) ---
        save_data = SaveManager.load_data()
        if "last_successful_run" in save_data:
            run = save_data["last_successful_run"]
            status_text = f"LAST WIN: Lvl {run['level']} | Kills: {run['kills']} | Wpn: {run['weapon'].upper()}"
            status_color = (50, 255, 100)
        elif "last_run" in save_data:
            run = save_data["last_run"]
            mins = int(run["time_survived"] // 60)
            secs = int(run["time_survived"] % 60)
            status_text = f"LAST ATTEMPT: {mins}:{secs:02d} | Lvl {run['level']}"
            status_color = (255, 150, 50)
        else:
            status_text = "FIRST DEPLOYMENT"
            status_color = (200, 200, 200)

        stats_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1
        world[stats_id] = {
            UITag: UITag(),
            SpacialComponent: SpacialComponent(
                rect=pygame.Rect(cx, panel_y + 140, 0, 0)
            ),
            TextComponent: TextComponent(
                text=status_text, color=status_color, is_header=False
            ),
        }
        MainMenuBuilder._ui_ids.append(stats_id)

        # --- 5. DEPLOY BUTTONS ---
        btn_w = min(320, panel_w - 60)
        btn_h = 50
        btn_start_y = panel_y + 200

        def create_deploy_btn(text, weapon_key, color, y_offset):
            btn_id = States.NEXT_ENTITY_ID
            States.NEXT_ENTITY_ID += 1
            world[btn_id] = {
                UITag: UITag(),
                UIButtonComponent: UIButtonComponent(
                    rect=pygame.Rect(
                        cx - (btn_w // 2), btn_start_y + y_offset, btn_w, btn_h
                    ),
                    text=text,
                    color=color,
                    action={"type": "START_GAME", "weapon": weapon_key},
                ),
            }
            MainMenuBuilder._ui_ids.append(btn_id)

        create_deploy_btn("DEPLOY: SHOTGUN", "shotgun", (200, 50, 50), 0)
        create_deploy_btn("DEPLOY: SNIPER", "sniper", (50, 100, 200), btn_h + 15)

        # --- 6. CONTROLS IMAGE (Tucked inside Terminal Bottom) ---
        ctrl_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1

        # Scales up 1.5x for readability, but clamps if the window is tiny
        ctrl_w, ctrl_h = int(144 * 1.5), int(48 * 1.5)
        if ctrl_w > panel_w - 40:
            ctrl_w, ctrl_h = 144, 48

        ctrl_x = cx - (ctrl_w // 2)
        ctrl_y = (
            panel_y + panel_h - ctrl_h - 15
        )  # Fixed to the bottom padding of the terminal

        ctrl_surf = pygame.transform.scale(
            Cache.SPRITES.MENU.CONTROLS, (ctrl_w, ctrl_h)
        )

        world[ctrl_id] = {
            UITag: UITag(),
            SpacialComponent: SpacialComponent(
                rect=pygame.Rect(ctrl_x, ctrl_y, ctrl_w, ctrl_h)
            ),
            UIImageComponent: UIImageComponent(image=ctrl_surf, alpha=255),
        }
        MainMenuBuilder._ui_ids.append(ctrl_id)

    @staticmethod
    def destroy(world: dict):
        for eid in MainMenuBuilder._ui_ids:
            if eid in world:
                del world[eid]
        MainMenuBuilder._ui_ids.clear()
