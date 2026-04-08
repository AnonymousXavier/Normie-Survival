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
            UIImageComponent: UIImageComponent(image=cover_surf, alpha=50),
        }
        MainMenuBuilder._ui_ids.append(cover_id)

        # --- 2. THE DUAL-PANEL LAYOUT MATH ---
        gap = 20
        total_w = min(560, w - 40)
        panel_h = min(360, h - 140)  # Leaves room at the top for the title!

        # Left panel is narrow/vertical (40%) | Right panel is wider (60%)
        log_w = int((total_w - gap) * 0.40)
        menu_w = total_w - gap - log_w

        # Anchors for perfect centering
        panel_y = cy - (panel_h // 2) + 30
        log_x = cx - (total_w // 2)
        menu_x = log_x + log_w + gap

        # --- 3. PREMIUM TITLE (Top Center) ---
        title_y = panel_y - 70

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

        # --- 4. LEFT PANEL: MISSION LOG (Compressed & Vertical) ---
        save_data = SaveManager.load_data()
        log_stats = {}
        log_color = (200, 200, 200)

        # Using shorter keys so they fit beautifully in the compressed panel width
        if "last_successful_run" in save_data:
            run = save_data["last_successful_run"]
            log_title = "LAST WIN"
            log_color = (50, 255, 100)
            log_stats["Level"] = str(run["level"])
            log_stats["Kills"] = str(run["kills"])
            log_stats["Weapon"] = str(run["weapon"]).upper()
        elif "last_run" in save_data:
            run = save_data["last_run"]
            log_title = "LAST RUN"
            log_color = (255, 150, 50)

            # 1. Leave seconds as a raw float!
            mins = int(run["time_survived"] // 60)
            secs = run["time_survived"] % 60

            # 2. Format: 05 means 5 total characters (e.g. "04.50"), .2f means 2 decimal places
            log_stats["Time"] = f"{mins}:{secs:05.2f}"

            log_stats["Level"] = str(run["level"])
            log_stats["Kills"] = str(run.get("kills", 0))
        else:
            log_title = "LOG"
            log_stats["Status"] = "NO DATA"

        log_panel_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1
        world[log_panel_id] = {
            UITag: UITag(),
            SpacialComponent: SpacialComponent(
                rect=pygame.Rect(log_x, panel_y, log_w, panel_h)
            ),
            StatPanelComponent: StatPanelComponent(
                title=log_title, stats=log_stats, theme_color=log_color
            ),
        }
        MainMenuBuilder._ui_ids.append(log_panel_id)

        # --- 5. RIGHT PANEL: MAIN MENU (Deployment) ---
        menu_panel_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1
        world[menu_panel_id] = {
            UITag: UITag(),
            SpacialComponent: SpacialComponent(
                rect=pygame.Rect(menu_x, panel_y, menu_w, panel_h)
            ),
            StatPanelComponent: StatPanelComponent(
                title="PRIMARY WEOPON", stats={}, theme_color=(100, 200, 255)
            ),
        }
        MainMenuBuilder._ui_ids.append(menu_panel_id)

        # --- 6. DEPLOY BUTTONS ---
        btn_w = min(260, menu_w - 40)
        btn_h = 50
        btn_spacing = 15

        btn_center_x = menu_x + (menu_w // 2)
        btn_start_y = panel_y + 80

        def create_deploy_btn(text, weapon_key, color, y_offset):
            btn_id = States.NEXT_ENTITY_ID
            States.NEXT_ENTITY_ID += 1
            world[btn_id] = {
                UITag: UITag(),
                UIButtonComponent: UIButtonComponent(
                    rect=pygame.Rect(
                        btn_center_x - (btn_w // 2),
                        btn_start_y + y_offset,
                        btn_w,
                        btn_h,
                    ),
                    text=text,
                    color=color,
                    action={"type": "START_GAME", "weapon": weapon_key},
                ),
            }
            MainMenuBuilder._ui_ids.append(btn_id)

        create_deploy_btn("SHOTGUN", "shotgun", (200, 50, 50), 0)
        create_deploy_btn("SNIPER", "sniper", (50, 100, 200), btn_h + btn_spacing)

        # --- 7. CONTROLS IMAGE ---
        ctrl_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1

        # Scale dynamically so it never bleeds out of the right panel
        ctrl_w, ctrl_h = int(144 * 1.5), int(48 * 1.5)
        if ctrl_w > menu_w - 40:
            scale = (menu_w - 40) / ctrl_w
            ctrl_w, ctrl_h = int(ctrl_w * scale), int(ctrl_h * scale)

        ctrl_x = btn_center_x - (ctrl_w // 2)
        ctrl_y = panel_y + panel_h - ctrl_h - 20  # Anchored to the bottom padding!

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
