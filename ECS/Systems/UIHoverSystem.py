import pygame
from Core import States
from ECS.Components import UIButtonComponent, StatsButtonComponent


def process(world: dict):
    mouse_pos = States.SCREEN_MOUSE_POS
    for obj in world.values():
        # Check both types of buttons
        btn = obj.get(UIButtonComponent) or obj.get(StatsButtonComponent)
        if btn:
            btn.is_hovered = btn.rect.collidepoint(mouse_pos)
