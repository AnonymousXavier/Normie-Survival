import pygame
from Core import States
from ECS.Components import UIButtonComponent, UITag
from Globals import Settings

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
                apply_upgrade(btn.action)
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

def apply_upgrade(action: dict):
    stats = States.global_shotgun_stats
    player = States.world[States.PLAYER_ID]
    
    # Passive upgrades
    stats = States.global_shotgun_stats
    if action["buff"] == "projectile":
        stats.projectile_count += 1
    elif action["buff"] == "damage":
        stats.damage += 1
    elif action["buff"] == "fire_rate":
        stats.fire_rate = max(0.1, stats.fire_rate - 0.1) 

    # Active Upgrades
    if action["buff"] == "aoe":
        # Add AOE, remove Shield if it exists to force the choice
        if ShieldComponent in player: del player[ShieldComponent]
        player[AOEComponent] = AOEComponent()
        print("AOE Pulse Active!")
        
    elif action["buff"] == "shield":
        # Add Shield, remove AOE if it exists
        if AOEComponent in player: del player[AOEComponent]
        player[ShieldComponent] = ShieldComponent()
        print("Shield Generator Active!")

    print(f"Applied Buff: {action['buff']}!")