from ECS.Components import PowerUpTag, SpacialComponent, RotationComponent, CooldownComponent
from ECS import Factories
from Core import States  # Import States to access the global stats

def process(world: dict, spatial_grid: dict, delta: float):
    stats = States.global_shotgun_stats  # Grab the global buff state
    
    for obj in list(world.values()): 
        if PowerUpTag in obj and CooldownComponent in obj and RotationComponent in obj:

            obj[CooldownComponent].fire_rate = stats.fire_rate
            obj[CooldownComponent].time_since_last_shot += delta
            
            if obj[CooldownComponent].time_since_last_shot >= obj[CooldownComponent].fire_rate:
                obj[CooldownComponent].time_since_last_shot = 0.0
                
                cx = obj[SpacialComponent].rect.centerx
                cy = obj[SpacialComponent].rect.centery
                base_angle = obj[RotationComponent].angle
                
                # --- SPREAD MATH ---
                count = stats.projectile_count
                spread = stats.spread_angle
                
                if count <= 1:
                    angles = [base_angle]
                else:
                    start_angle = base_angle - (spread / 2)
                    step_angle = spread / (count - 1)
                    angles = [start_angle + (i * step_angle) for i in range(count)]
                    
                # Spawn a bullet for every angle calculated
                for angle in angles:
                    Factories.spawn_bullet(world, spatial_grid, cx, cy, angle, stats.speed, stats.damage)