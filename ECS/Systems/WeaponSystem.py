from ECS.Components import PowerUpTag, SpacialComponent, RotationComponent, CooldownComponent
from ECS import Factories

def process(world: dict, spatial_grid: dict, delta: float):
    for obj_id in list(world.keys()): 
        obj = world[obj_id]
        if PowerUpTag in obj and CooldownComponent in obj and RotationComponent in obj:
            obj[CooldownComponent].time_since_last_shot += delta
            
            if obj[CooldownComponent].time_since_last_shot >= obj[CooldownComponent].fire_rate:
                obj[CooldownComponent].time_since_last_shot = 0.0
                
                cx = obj[SpacialComponent].rect.centerx
                cy = obj[SpacialComponent].rect.centery
                angle = obj[RotationComponent].angle
                
                Factories.spawn_bullet(world, spatial_grid, cx, cy, angle)