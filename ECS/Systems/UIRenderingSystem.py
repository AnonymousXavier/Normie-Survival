import pygame
from ECS.Components import UIButtonComponent, UITag
from Globals import Settings

pygame.font.init()
UI_FONT = pygame.font.SysFont("Arial", 24, bold=True)


def process(world: dict, window: pygame.Surface):
    # FORCE the logical size here
    log_w = Settings.WINDOW.DESKTOP_WIDTH
    log_h = Settings.WINDOW.DESKTOP_HEIGHT

    ui_surface = pygame.Surface((log_w, log_h), pygame.SRCALPHA)

    # 2. Draw all buttons to the Glass Pane using your static logical coordinates
    for obj in world.values():
        if UIButtonComponent in obj and UITag in obj:
            btn = obj[UIButtonComponent]

            color = btn.hover_color if btn.is_hovered else btn.color
            pygame.draw.rect(ui_surface, color, btn.rect)
            pygame.draw.rect(ui_surface, Settings.COLOURS.BLUE, btn.rect, 2)

            text_surf = UI_FONT.render(btn.text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=btn.rect.center)
            ui_surface.blit(text_surf, text_rect)

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
