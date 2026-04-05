import pygame
from Core import States
from ECS.Components import UIButtonComponent, UITag, StatsButtonComponent
from Globals import Settings

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

        # --- Handle STATS BUTTONS (Two-line) ---
        if StatsButtonComponent in obj:
            btn = obj[StatsButtonComponent]
            color = btn.hover_color if btn.is_hovered else btn.color
            pygame.draw.rect(ui_surface, color, btn.rect)
            pygame.draw.rect(ui_surface, (100, 200, 255), btn.rect, 2)  # Cyan border

            # Title: Top Half
            t_surf = UI_FONT.render(btn.title, True, (255, 255, 255))
            t_rect = t_surf.get_rect(
                centerx=btn.rect.centerx, centery=btn.rect.top + 22
            )
            ui_surface.blit(t_surf, t_rect)

            # Description: Bottom Half
            d_surf = DESC_FONT.render(btn.description, True, (200, 200, 200))
            d_rect = d_surf.get_rect(
                centerx=btn.rect.centerx, centery=btn.rect.bottom - 18
            )
            ui_surface.blit(d_surf, d_rect)

        # --- Handle REGULAR BUTTONS (One-line) ---
        elif UIButtonComponent in obj:
            btn = obj[UIButtonComponent]
            draw_normal_btn(obj, ui_surface)

    if not States.IS_LEVELING_UP:
        minutes, seconds = int(States.BOSS_TIMER // 60), int(States.BOSS_TIMER % 60)
        timer_text = f"BOSS IN: {minutes:02}:{seconds:02}"
        timer_surf = UI_FONT.render(timer_text, True, (255, 50, 50))

        # Use window width and a small margin from the ACTUAL top
        timer_rect = timer_surf.get_rect(centerx=Settings.WINDOW.WIDTH // 2, top=10)

        pygame.draw.rect(window, (0, 0, 0, 150), timer_rect.inflate(20, 10))
        window.blit(timer_surf, timer_rect)

    # NOW scale that large surface down to fit the actual window
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
