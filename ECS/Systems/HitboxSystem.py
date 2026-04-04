from ECS.Components import SpacialComponent, HitboxComponent

def process(world: dict):
    for obj in world.values():
        if SpacialComponent in obj and HitboxComponent in obj:
            spacial = obj[SpacialComponent]
            hitbox = obj[HitboxComponent]
            
            # Center the hitbox on the main sprite rect
            hitbox.rect.centerx = spacial.rect.centerx + hitbox.offset_x
            hitbox.rect.centery = spacial.rect.centery + hitbox.offset_y