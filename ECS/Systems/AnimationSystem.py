from ECS.Components import AnimationComponent, RenderComponent

def process(world: dict, dt: float):
    for obj in world.values():
        if AnimationComponent in obj and RenderComponent in obj:
            anim = obj[AnimationComponent]

            # 1. Grab the correct sprite sheet based on current state (Idle or Walk)
            if anim.state in anim.frames:

                active_sheet = anim.frames[anim.state]

                # 2. Grab the specific row based on direction (Down, Up, Left, Right)
                direction_row = anim.direction if anim.direction < len(active_sheet) else 0
                frame_sequence = active_sheet[direction_row]

                # 3. Tick the animation forward
                anim.current_frame += anim.speed * dt

                # Loop back to 0 if the animation finishes
                if anim.current_frame >= len(frame_sequence):
                    anim.current_frame = 0

                # 4. Push the current frame to the Render Component
                frame_index = int(anim.current_frame)
                obj[RenderComponent].sprite = frame_sequence[frame_index]