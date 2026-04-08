import pygame
from Core import States
from ECS.Components import UIButtonComponent, StatsButtonComponent
from Globals.AudioManager import AudioManager


def process(world: dict, events: list, pygame_event):
    if pygame_event.type == pygame.MOUSEBUTTONDOWN and pygame_event.button == 1:
        mouse_pos = States.SCREEN_MOUSE_POS
        for obj in world.values():
            btn = obj.get(UIButtonComponent) or obj.get(StatsButtonComponent)
            if btn and btn.rect.collidepoint(mouse_pos):
                events.append(btn.action)
                AudioManager.play_sfx("ui_click")
                return
