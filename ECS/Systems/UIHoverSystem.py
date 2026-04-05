import pygame
from Core import States
from ECS.Components import UIButtonComponent

def process(world: dict):
    mouse_pos = States.SCREEN_MOUSE_POS
    
    for obj in world.values():
        if UIButtonComponent in obj:
            btn = obj[UIButtonComponent]
            # Update the boolean based on Pygame's collision check
            btn.is_hovered = btn.rect.collidepoint(mouse_pos)