from Core import States
from Globals import Enums
from ECS.Components import (DamageComponent, DeathTimerComponent, SpacialComponent, HitboxComponent, 
                            EnemyTag, HealthComponent, ShieldComponent, PlayerInputTag, 
                            AnimationComponent, ArsenalComponent, PlayerStatsComponent)

def process(world: dict, spatial_grid: dict, dt: float):
    if States.PLAYER_ID not in world:
        return

    player = world[States.PLAYER_ID]
    
    # 1. Pull BOTH components. 
    # HealthComponent manages i-frames. PlayerStatsComponent manages the actual math.
    stats = player.get(PlayerStatsComponent)
    p_health = player.get(HealthComponent) 
    p_hitbox = player.get(HitboxComponent)
    
    # If the player is a tombstone, they won't have a hitbox! Skip safely.
    if not stats or not p_health or not p_hitbox: 
        return
        
    p_hitbox = p_hitbox.rect
    p_grid_pos = player[SpacialComponent].grid_pos

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
        return 

    # --- Spatial Grid Collision Logic ---
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            cell = (p_grid_pos[0] + dx, p_grid_pos[1] + dy)
            
            if cell in spatial_grid:
                for entity_id in spatial_grid[cell]:
                    enemy = world.get(entity_id)
                    
                    if enemy and EnemyTag in enemy:
                        e_rect = enemy[HitboxComponent].rect if HitboxComponent in enemy else enemy[SpacialComponent].rect
                        
                        if p_hitbox.colliderect(e_rect):
                            if ShieldComponent in player and player[ShieldComponent].active:
                                player[ShieldComponent].active = False
                                p_health.inv_timer = p_health.inv_duration 
                                print("Shield Blocked Hit!")
                                
                            else:
                                dealable_damage = enemy[DamageComponent].amount
                                # 2. Subtract from the NEW current_hp stat
                                stats.current_hp -= dealable_damage
                                p_health.inv_timer = p_health.inv_duration
                                
                                # 3. Print using the new @property getter for Max HP
                                print(f"Ouch! HP: {stats.current_hp}/{stats.final_max_hp}")
                                
                                if stats.current_hp <= 0:
                                    # --- TOMBSTONING PROTOCOL ---
                                    if PlayerInputTag in player: del player[PlayerInputTag]
                                    if ArsenalComponent in player: del player[ArsenalComponent]
                                    if HitboxComponent in player: del player[HitboxComponent]

                                    if DeathTimerComponent not in player: 
                                        player[DeathTimerComponent] = DeathTimerComponent()

                                    if AnimationComponent in player:
                                        player[AnimationComponent].state = Enums.ANIM_STATES.DEAD
                                        player[AnimationComponent].current_frame = 0
                                        player[AnimationComponent].speed = 0 

                                    print("Player Tombstoned!")
                                return