import pygame
from Core import States
from ECS.Components import (
    UIButtonComponent,
    UITag,
    StatsButtonComponent,
    TextComponent,
    SpacialComponent,
    StatPanelComponent,
    UIImageComponent,
)
from Globals import Settings

TITLE_FONT = pygame.font.SysFont("Arial", 48, bold=True)

pygame.font.init()
UI_FONT = pygame.font.SysFont("Arial", 24, bold=True)
DESC_FONT = pygame.font.SysFont("Arial", 18, bold=False)

log_w = Settings.WINDOW.DESKTOP_WIDTH
log_h = Settings.WINDOW.DESKTOP_HEIGHT


def process(world: dict, window: pygame.Surface):
    # Calculate scale right away because BOTH the Cache AND the Live HUD need it
    win_w, win_h = window.get_size()
    scale = min(win_w / log_w, win_h / log_h)

    if States.UI_DIRTY:
        ui_surface = pygame.Surface((log_w, log_h), pygame.SRCALPHA)

        for obj in world.values():
            if UITag not in obj:
                continue

            # STATS BUTTONS
            if StatsButtonComponent in obj:
                btn = obj[StatsButtonComponent]
                color = btn.hover_color if btn.is_hovered else btn.color
                pygame.draw.rect(ui_surface, color, btn.rect)
                pygame.draw.rect(
                    ui_surface, (100, 200, 255), btn.rect, 2
                )  # Cyan border

                # Title
                t_surf = UI_FONT.render(btn.title, True, (255, 255, 255))
                t_rect = t_surf.get_rect(
                    centerx=btn.rect.centerx, centery=btn.rect.top + 22
                )
                ui_surface.blit(t_surf, t_rect)

                # Description
                d_surf = DESC_FONT.render(btn.description, True, (200, 200, 200))
                d_rect = d_surf.get_rect(
                    centerx=btn.rect.centerx, centery=btn.rect.bottom - 18
                )
                ui_surface.blit(d_surf, d_rect)

            # REGULAR BUTTONS
            elif UIButtonComponent in obj:
                draw_normal_btn(obj, ui_surface)

            # TEXT
            if TextComponent in obj and SpacialComponent in obj:
                txt_comp = obj[TextComponent]
                rect = obj[SpacialComponent].rect

                if txt_comp.is_header:
                    text_surface = TITLE_FONT.render(
                        txt_comp.text, True, txt_comp.color
                    )
                else:
                    text_surface = UI_FONT.render(txt_comp.text, True, txt_comp.color)

                text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery))
                ui_surface.blit(text_surface, text_rect)

            # UI IMAGES
            if UIImageComponent in obj and SpacialComponent in obj:
                img_comp = obj[UIImageComponent]
                rect = obj[SpacialComponent].rect

                working_img = img_comp.image
                if img_comp.alpha < 255:
                    working_img = working_img.copy()
                    working_img.set_alpha(img_comp.alpha)

                ui_surface.blit(working_img, rect)

            # STAT PANELS
            if StatPanelComponent in obj and SpacialComponent in obj:
                panel = obj[StatPanelComponent]
                rect = obj[SpacialComponent].rect

                pygame.draw.rect(ui_surface, (20, 20, 20, 230), rect, border_radius=10)
                pygame.draw.rect(
                    ui_surface, panel.theme_color, rect, width=2, border_radius=10
                )

                t_surf = UI_FONT.render(panel.title, True, panel.theme_color)
                ui_surface.blit(t_surf, (rect.x + 15, rect.y + 10))
                pygame.draw.line(
                    ui_surface,
                    (100, 100, 100),
                    (rect.x + 10, rect.y + 40),
                    (rect.right - 10, rect.y + 40),
                )

                y_offset = 50
                for key, val in panel.stats.items():
                    k_surf = DESC_FONT.render(key, True, (180, 180, 180))
                    ui_surface.blit(k_surf, (rect.x + 15, rect.y + y_offset))

                    v_surf = DESC_FONT.render(val, True, (255, 255, 255))
                    ui_surface.blit(
                        v_surf,
                        (rect.right - v_surf.get_width() - 15, rect.y + y_offset),
                    )
                    y_offset += 25

        # Perform the heavy scale ONLY when dirty, save to global cache
        States.CACHED_UI_SURFACE = pygame.transform.smoothscale(
            ui_surface, (int(log_w * scale), int(log_h * scale))
        )

        # Reset the flag
        States.UI_DIRTY = False

    if States.CACHED_UI_SURFACE:
        offset_x = (win_w - States.CACHED_UI_SURFACE.get_width()) // 2
        offset_y = (win_h - States.CACHED_UI_SURFACE.get_height()) // 2
        window.blit(States.CACHED_UI_SURFACE, (offset_x, offset_y))

    if States.CURRENT_STATE == "PLAYING" and not States.IS_LEVELING_UP:
        # 1. BOSS TIMER (Top Center)
        minutes, seconds = int(States.BOSS_TIMER // 60), int(States.BOSS_TIMER % 60)
        timer_text = f"BOSS IN: {minutes:02}:{seconds:02}"

        base_timer_surf = TITLE_FONT.render(timer_text, True, (255, 50, 50))
        t_w, t_h = int(base_timer_surf.get_width() * scale), int(
            base_timer_surf.get_height() * scale
        )
        timer_surf = pygame.transform.smoothscale(base_timer_surf, (t_w, t_h))

        timer_rect = timer_surf.get_rect(centerx=win_w // 2, top=int(20 * scale))
        bg_rect = timer_rect.inflate(int(30 * scale), int(15 * scale))

        bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, (0, 0, 0, 150), bg_surf.get_rect(), border_radius=5)
        window.blit(bg_surf, bg_rect)
        window.blit(timer_surf, timer_rect)

        # KILL COUNT (Top Right)
        kills_text = f"KILLS: {States.KILLS_COUNT}"
        base_kills_surf = TITLE_FONT.render(kills_text, True, (255, 215, 0))

        k_w, k_h = int(base_kills_surf.get_width() * scale), int(
            base_kills_surf.get_height() * scale
        )
        kills_surf = pygame.transform.smoothscale(base_kills_surf, (k_w, k_h))

        kills_rect = kills_surf.get_rect(
            topright=(win_w - int(20 * scale), int(20 * scale))
        )
        k_bg_rect = kills_rect.inflate(int(30 * scale), int(15 * scale))

        k_bg_surf = pygame.Surface(k_bg_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            k_bg_surf, (0, 0, 0, 150), k_bg_surf.get_rect(), border_radius=5
        )
        window.blit(k_bg_surf, k_bg_rect)
        window.blit(kills_surf, kills_rect)

        # FPS COUNTER (Top Left)
        fps_color = (
            (0, 255, 0)
            if States.CURRENT_FPS >= 55
            else (255, 255, 0)
            if States.CURRENT_FPS >= 30
            else (255, 50, 50)
        )
        fps_text = f"FPS: {States.CURRENT_FPS}"
        base_fps_surf = UI_FONT.render(fps_text, True, fps_color)

        f_w, f_h = int(base_fps_surf.get_width() * scale), int(
            base_fps_surf.get_height() * scale
        )
        fps_surf = pygame.transform.smoothscale(base_fps_surf, (f_w, f_h))

        fps_rect = fps_surf.get_rect(topleft=(int(20 * scale), int(20 * scale)))
        f_bg_rect = fps_rect.inflate(int(20 * scale), int(10 * scale))

        f_bg_surf = pygame.Surface(f_bg_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            f_bg_surf, (0, 0, 0, 150), f_bg_surf.get_rect(), border_radius=3
        )
        window.blit(f_bg_surf, f_bg_rect)
        window.blit(fps_surf, fps_rect)


def draw_normal_btn(obj: dict, ui_surface: pygame.Surface):
    btn = obj[UIButtonComponent]

    color = btn.hover_color if btn.is_hovered else btn.color
    pygame.draw.rect(ui_surface, color, btn.rect)
    pygame.draw.rect(ui_surface, Settings.COLOURS.BLUE, btn.rect, 2)

    text_surf = UI_FONT.render(btn.text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=btn.rect.center)
    ui_surface.blit(text_surf, text_rect)
