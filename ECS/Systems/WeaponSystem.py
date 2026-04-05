from ECS.Components import PlayerStatsComponent, PowerUpTag, SpacialComponent, RotationComponent, CooldownComponent, ArsenalComponent
from ECS import Factories
from Core import States  # Import States to access the global stats

def process(world: dict, spatial_grid: dict, delta: float):
    player = world.get(States.PLAYER_ID)
    if not player or ArsenalComponent not in player:
        return 

    shotgun_stats = player[ArsenalComponent].inventory.get("shotgun")
    if not shotgun_stats:
        return 
    
    for obj in list(world.values()):
        if PowerUpTag in obj and CooldownComponent in obj:
            # ... run your shooting math ...
            fire_rate = shotgun_stats.get_final_fire_rate(player[PlayerStatsComponent].fire_rate_mult)
            bullet_dmg = shotgun_stats.get_final_damage(player[PlayerStatsComponent].damage_mult)

            obj[CooldownComponent].fire_rate = fire_rate
            obj[CooldownComponent].time_since_last_shot += delta
            
            if obj[CooldownComponent].time_since_last_shot >= obj[CooldownComponent].fire_rate:
                obj[CooldownComponent].time_since_last_shot = 0.0
                
                cx = obj[SpacialComponent].rect.centerx
                cy = obj[SpacialComponent].rect.centery
                base_angle = obj[RotationComponent].angle
                
                # --- SPREAD MATH ---
                count = shotgun_stats.projectile_count
                spread = shotgun_stats.spread_angle
                
                if count <= 1:
                    angles = [base_angle]
                else:
                    start_angle = base_angle - (spread / 2)
                    step_angle = spread / (count - 1)
                    angles = [start_angle + (i * step_angle) for i in range(count)]
                    
                # Spawn a bullet for every angle calculated
                for angle in angles:
                    Factories.spawn_bullet(world, spatial_grid, cx, cy, angle, shotgun_stats.speed, bullet_dmg)