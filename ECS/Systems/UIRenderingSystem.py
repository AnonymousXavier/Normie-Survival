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
    ui_surface = pygame.Surface((log_w, log_h), pygame.SRCALPHA)

    for obj in world.values():
        if UITag not in obj:
            continue

        # STATS BUTTONS
        if StatsButtonComponent in obj:
            btn = obj[StatsButtonComponent]
            color = btn.hover_color if btn.is_hovered else btn.color
            pygame.draw.rect(ui_surface, color, btn.rect)
            pygame.draw.rect(ui_surface, (100, 200, 255), btn.rect, 2)  # Cyan border

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
            btn = obj[UIButtonComponent]
            draw_normal_btn(obj, ui_surface)

        if TextComponent in obj and SpacialComponent in obj:
            txt_comp = obj[TextComponent]
            rect = obj[SpacialComponent].rect

            # Choose the font based on the header flag
            if txt_comp.is_header:
                text_surface = TITLE_FONT.render(txt_comp.text, True, txt_comp.color)
            else:
                # RENDER NORMAL TEXT
                text_surface = UI_FONT.render(txt_comp.text, True, txt_comp.color)

            # Center and draw it
            text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery))
            ui_surface.blit(text_surface, text_rect)

        # --- NEW: RENDER UI IMAGES ---
        if UIImageComponent in obj and SpacialComponent in obj:
            img_comp = obj[UIImageComponent]
            rect = obj[SpacialComponent].rect

            # Apply alpha transparency if needed
            working_img = img_comp.image
            if img_comp.alpha < 255:
                working_img = working_img.copy()
                working_img.set_alpha(img_comp.alpha)

            # Draw it exactly inside the SpacialComponent's rectangle
            ui_surface.blit(working_img, rect)

        if StatPanelComponent in obj and SpacialComponent in obj:
            panel = obj[StatPanelComponent]
            rect = obj[SpacialComponent].rect

            # Background & Border
            pygame.draw.rect(ui_surface, (20, 20, 20, 230), rect, border_radius=10)
            pygame.draw.rect(
                ui_surface, panel.theme_color, rect, width=2, border_radius=10
            )

            # Title & Divider
            t_surf = UI_FONT.render(panel.title, True, panel.theme_color)
            ui_surface.blit(t_surf, (rect.x + 15, rect.y + 10))
            pygame.draw.line(
                ui_surface,
                (100, 100, 100),
                (rect.x + 10, rect.y + 40),
                (rect.right - 10, rect.y + 40),
            )

            # List the Stats!
            y_offset = 50
            for key, val in panel.stats.items():
                # Key (Left aligned)
                k_surf = DESC_FONT.render(key, True, (180, 180, 180))
                ui_surface.blit(k_surf, (rect.x + 15, rect.y + y_offset))

                # Value (Right aligned)
                v_surf = DESC_FONT.render(val, True, (255, 255, 255))
                ui_surface.blit(
                    v_surf, (rect.right - v_surf.get_width() - 15, rect.y + y_offset)
                )

                y_offset += 25

    if States.CURRENT_STATE == "PLAYING" and not States.IS_LEVELING_UP:
        minutes, seconds = int(States.BOSS_TIMER // 60), int(States.BOSS_TIMER % 60)
        timer_text = f"BOSS IN: {minutes:02}:{seconds:02}"
        timer_surf = UI_FONT.render(timer_text, True, (255, 50, 50))

        # Use window width and a small margin from the ACTUAL top
        timer_rect = timer_surf.get_rect(centerx=Settings.WINDOW.WIDTH // 2, top=10)

        pygame.draw.rect(window, (0, 0, 0, 150), timer_rect.inflate(20, 10))
        window.blit(timer_surf, timer_rect)

    # scale that large surface down to fit the actual window
    win_w, win_h = window.get_size()
    scale = min(win_w / log_w, win_h / log_h)

    scaled_ui = pygame.transform.scale(
        ui_surface, (int(log_w * scale), int(log_h * scale))
    )

    # Center the scaled UI (handling the black bars)
    offset_x = (win_w - scaled_ui.get_width()) // 2
    offset_y = (win_h - scaled_ui.get_height()) // 2

    window.blit(scaled_ui, (offset_x, offset_y))


def draw_normal_btn(obj: dict, ui_surface: pygame.Surface):
    # Draw all buttons to the Glass Pane using your static logical coordinates
    btn = obj[UIButtonComponent]

    color = btn.hover_color if btn.is_hovered else btn.color
    pygame.draw.rect(ui_surface, color, btn.rect)
    pygame.draw.rect(ui_surface, Settings.COLOURS.BLUE, btn.rect, 2)

    text_surf = UI_FONT.render(btn.text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=btn.rect.center)
    ui_surface.blit(text_surf, text_rect)
