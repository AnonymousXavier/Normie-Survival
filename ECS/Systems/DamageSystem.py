import pygame
from Core import States
from ECS.Components import SpacialComponent, HitboxComponent, EnemyTag, HealthComponent, ShieldComponent

def process(world: dict, spatial_grid: dict, dt: float):
    if States.PLAYER_ID not in world:
        return

    player = world[States.PLAYER_ID]
    p_health = player[HealthComponent]
    p_hitbox = player[HitboxComponent].rect
    p_grid_pos = player[SpacialComponent].grid_pos

    # Inside DamageSystem.py process()

    # Recharge Shield
    if ShieldComponent in player:
        s = player[ShieldComponent]
        if not s.active:
            s.timer += dt
            if s.timer >= s.recharge_delay:
                s.active = True
                s.timer = 0
                print("Shield Recharged!")

    # Invincibility countdown
    if p_health.inv_timer > 0:
        p_health.inv_timer -= dt
        return # Skip damage check while invincible


    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            cell = (p_grid_pos[0] + dx, p_grid_pos[1] + dy)
            
            if cell in spatial_grid:
                for entity_id in spatial_grid[cell]:
                    enemy = world.get(entity_id)
                    
                    if enemy and EnemyTag in enemy:
                        # Use enemy hitbox if they have one, else use their sprite rect
                        e_rect = enemy[HitboxComponent].rect if HitboxComponent in enemy else enemy[SpacialComponent].rect
                        
                        # Damage mitigation
                        if p_hitbox.colliderect(e_rect):
                            if ShieldComponent in player and player[ShieldComponent].active:
                                player[ShieldComponent].active = False
                                p_health.inv_timer = p_health.inv_duration # Grant i-frames on shield break
                                print("Shield Blocked Hit!")
                                
                            else:
                                # DEAL DAMAGE
                                p_health.hp -= 1
                                p_health.inv_timer = p_health.inv_duration
                                
                                print(f"Ouch! HP: {p_health.hp}/{p_health.max_hp}")
                                
                                if p_health.hp <= 0:
                                    trigger_game_over()
                                return   
                            

def trigger_game_over():
    print("FATAL ERROR: Player offline.")
    States.GAME_RUNNING = False # This will break the Main().run() loop