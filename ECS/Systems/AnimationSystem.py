from ECS.Components import AnimationComponent, RenderComponent


def process(world: dict, dt: float):
    for obj in world.values():
        if AnimationComponent in obj and RenderComponent in obj:
            anim = obj[AnimationComponent]

            # Get sprite based on current state
            if anim.state in anim.frames:
                active_sheet = anim.frames[anim.state]

                # Grab row based on direction
                direction_row = (
                    anim.direction if anim.direction < len(active_sheet) else 0
                )
                frame_sequence = active_sheet[direction_row]

                anim.current_frame += anim.speed * dt

                if anim.current_frame >= len(frame_sequence):
                    anim.current_frame = 0

                # Push the current frame to the Render Component
                frame_index = int(anim.current_frame)
                obj[RenderComponent].sprite = frame_sequence[frame_index]
