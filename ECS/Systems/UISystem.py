import pygame
import random

from Core import States
from ECS.Components import UIButtonComponent, UITag, PlayerStatsComponent, ShieldComponent, AOEComponent
from Globals import Settings, Upgrades

# Initialize font
pygame.font.init()
UI_FONT = pygame.font.SysFont("Arial", 20, bold=True)

def process(world: dict, surface: pygame.Surface):
    if not States.IS_LEVELING_UP: return

    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_just_pressed()[0] 

    # Draw a semi-transparent dark overlay 
    overlay = pygame.Surface(Settings.WINDOW.SIZE, pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    ui_entities_to_delete = []

    for obj_id, obj in list(world.items()):
        if UITag in obj and UIButtonComponent in obj:
            btn = obj[UIButtonComponent]

            # Hover logic
            btn.is_hovered = btn.rect.collidepoint(mouse_pos)

            # Click logic
            if btn.is_hovered and mouse_clicked:
                apply_upgrade(btn.action, world[States.PLAYER_ID])
                States.IS_LEVELING_UP = False
                
                # Mark all UI elements to be destroyed so the screen clears
                for u_id in list(world.keys()):
                    if UITag in world[u_id]:
                        ui_entities_to_delete.append(u_id)
                break # Stop processing to avoid double-clicks

            # Draw Button Background
            color = btn.hover_color if btn.is_hovered else btn.color
            pygame.draw.rect(surface, color, btn.rect)
            pygame.draw.rect(surface, Settings.COLOURS.BLUE, btn.rect, 2) # Border
            
            # Draw Text
            text_surf = UI_FONT.render(btn.text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=btn.rect.center)
            surface.blit(text_surf, text_rect)

    # Clean up the entities
    for u_id in ui_entities_to_delete:
        if u_id in world:
            del world[u_id]

def get_level_up_options(player: dict) -> list:
    owned = player[PlayerStatsComponent].upgrades_owned
    valid_keys = []

    for key, data in Upgrades.UPGRADE_POOL.items():
        # Check max level
        if owned.get(key, 0) >= data["max_level"]:
            continue
            
        # Check conflicts
        if any(conflict in owned for conflict in data.get("conflicts_with", [])):
            continue

        valid_keys.append(key)

    chosen_keys = random.sample(valid_keys, min(3, len(valid_keys)))
    
    # Return formatted data for your UI Builder
    return [{"key": key, "text": Upgrades.UPGRADE_POOL[key]["text"], "y_offset": i * 60} for i, key in enumerate(chosen_keys)]

def apply_upgrade(action_key: str, player: dict):
    stats = player[PlayerStatsComponent]
    stats.upgrades_owned[action_key] = stats.upgrades_owned.get(action_key, 0) + 1
    
    increment = Upgrades.UPGRADE_POOL[action_key].get("increment", 0)
    
    # Passives
    if action_key == "move_speed":
        stats.speed_mult += increment
    elif action_key == "max_hp":
        stats.hp_mult += increment
        stats.current_hp += int(stats.base_max_hp * increment) # Heal the newly gained HP
    elif action_key == "overall_damage":
        stats.damage_mult += increment
    elif action_key == "overall_attack_speed":
        stats.fire_rate_mult += increment
        
    # Actives
    elif action_key == "aoe":
        player[AOEComponent] = AOEComponent()
    elif action_key == "shield":
        player[ShieldComponent] = ShieldComponent()