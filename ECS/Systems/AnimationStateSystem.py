from ECS.Components import (
    AnimationComponent,
    VelocityComponent,
    FacingDirectionComponent,
)
from Globals import Enums


def process(world: dict):
    for obj in world.values():
        # Check if the entity is capable of animating and can face directions
        if AnimationComponent in obj and FacingDirectionComponent in obj:
            anim = obj[AnimationComponent]
            facing = obj[FacingDirectionComponent]

            old_state = anim.state

            # Determine State (Walking or Idle)
            if VelocityComponent in obj:
                anim.state = Enums.ANIM_STATES.WALK
            else:
                anim.state = Enums.ANIM_STATES.IDLE

            # Reset the frame if they just started or stopped moving
            if old_state != anim.state:
                anim.current_frame = 0.0

            # Determine Direction based on the Enum mappings
            if facing.dx == 1:
                anim.direction = Enums.ANIM_DIRS.RIGHT
            elif facing.dx == -1:
                anim.direction = Enums.ANIM_DIRS.LEFT
            elif facing.dy == 1:
                anim.direction = Enums.ANIM_DIRS.DOWN
            elif facing.dy == -1:
                anim.direction = Enums.ANIM_DIRS.UP
