import pygame
from Core import States
from ECS.Components import UIButtonComponent


def process(world: dict, events: list, pygame_event):
    mouse_pos = States.SCREEN_MOUSE_POS

    if (
        pygame_event.type == pygame.MOUSEBUTTONDOWN and pygame_event.button == 1
    ):  # Left Click
        for obj in world.values():
            if UIButtonComponent in obj:
                if obj[UIButtonComponent].rect.collidepoint(mouse_pos):
                    # The clicker doesn't care what this is, it just forwards it!
                    events.append(obj[UIButtonComponent].action)
                    print("Clicked")
                    return  # Prevent clicking multiple overlapping buttons
