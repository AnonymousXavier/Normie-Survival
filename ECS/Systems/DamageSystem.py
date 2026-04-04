from Core import States
from Globals import Enums
from ECS.Components import DeathTimerComponent, SpacialComponent, HitboxComponent, EnemyTag, HealthComponent, ShieldComponent, PlayerInputTag, AnimationComponent, ArsenalComponent

def process(world: dict, spatial_grid: dict, dt: float):
    if States.PLAYER_ID not in world:
        return

    player = world[States.PLAYER_ID]
    p_health = player.get(HealthComponent)
    p_hitbox = player.get(HitboxComponent)
    p_grid_pos = player[SpacialComponent].grid_pos

    # Inside DamageSystem.py process()

    if not p_health or not p_hitbox: return
    p_hitbox = p_hitbox.rect

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
                    
                    if enemy and EnemyTag in enemy :
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
                                    # Inside the logic where Player HP <= 0:

                                    player = world[States.PLAYER_ID]

                                    # 1. Strip away agency (They can no longer move)
                                    if PlayerInputTag in player: 
                                        del player[PlayerInputTag]

                                    # 2. Strip away the arsenal (The orbiting guns stop firing)
                                    if ArsenalComponent in player: 
                                        del player[ArsenalComponent]

                                    # 3. Strip away the hitbox (Enemies will just walk over the corpse)
                                    if HitboxComponent in player: 
                                        del player[HitboxComponent]

                                    if DeathTimerComponent not in player: 
                                        player[DeathTimerComponent] = DeathTimerComponent()

                                    # 4. Trigger the Death Animation
                                    if AnimationComponent in player:
                                        player[AnimationComponent].state = Enums.ANIM_STATES.DEAD
                                        player[AnimationComponent].current_frame = 0
                                        player[AnimationComponent].speed = 0 # Lock the frame so it doesn't loop

                                    print("Player Tombstoned!")
                                return   
                            