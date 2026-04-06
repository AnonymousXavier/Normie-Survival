# ECS/Systems/BossSystem.py
import math
from Core import States
from ECS.Components import BossAIComponent, SpacialComponent, StunComponent
from Globals import Settings, Misc


def process(world: dict, spatial_grid: dict, dt: float):
    if States.PLAYER_ID not in world:
        return

    player = world[States.PLAYER_ID]
    p_rect = player[SpacialComponent].rect
    p_pos = p_rect.center

    for e_id, entity in list(world.items()):
        if BossAIComponent in entity:
            boss_ai = entity[BossAIComponent]
            b_rect = entity[SpacialComponent].rect
            b_pos = b_rect.center

            # --- 1. COOLDOWN MANAGEMENT ---
            if boss_ai.state == "CHASE":
                boss_ai.ability_timer += dt
                if boss_ai.ability_timer >= boss_ai.ability_cooldown:
                    boss_ai.state = "GRAVITY_WELL"
                    boss_ai.state_timer = 2.0  # Pull for 2 seconds
                    boss_ai.ability_timer = 0.0

                    # SHORT CIRCUIT XAVIER'S CONTROLS
                    player[StunComponent] = StunComponent(timer=2.0)
                    print("⚠️ BOSS ACTIVATING GRAVITY WELL! PLAYER PARALYZED!")

            # --- 2. THE GRAVITY WELL ---
            elif boss_ai.state == "GRAVITY_WELL":
                boss_ai.state_timer -= dt

                # Calculate vector to pull the player
                dist_x = b_pos[0] - p_pos[0]
                dist_y = b_pos[1] - p_pos[1]
                dist = math.sqrt(dist_x**2 + dist_y**2)

                # Pull strength: Drags player at 120 pixels/sec
                if dist > 10 and dist < Settings.SPRITE.WIDTH * 15:
                    pull_speed = 180 * dt
                    p_rect.x += (dist_x / dist) * pull_speed
                    p_rect.y += (dist_y / dist) * pull_speed

                    # Update player spatial grid seamlessly
                    Misc.remove_entity_from_grid(
                        States.PLAYER_ID,
                        player[SpacialComponent].grid_pos,
                        spatial_grid,
                    )
                    new_p_grid = (
                        int(p_rect.x // Settings.SPRITE.WIDTH),
                        int(p_rect.y // Settings.SPRITE.HEIGHT),
                    )
                    player[SpacialComponent].grid_pos = new_p_grid
                    Misc.register_entity_in_grid(
                        States.PLAYER_ID, new_p_grid, spatial_grid
                    )

                if boss_ai.state_timer <= 0:
                    boss_ai.state = "DASH_WINDUP"
                    boss_ai.state_timer = 0.3
                    boss_ai.dash_target_x = p_pos[0]
                    boss_ai.dash_target_y = p_pos[1]
                    print("🔴 BOSS IS DASHING!")

            # --- 3. THE WINDUP (Telegraph) ---
            elif boss_ai.state == "DASH_WINDUP":
                boss_ai.state_timer -= dt
                # The boss stands perfectly still here, locking in the target
                if boss_ai.state_timer <= 0:
                    boss_ai.state = "DASHING"

            # --- 4. THE DASH ---
            elif boss_ai.state == "DASHING":
                dist_x = boss_ai.dash_target_x - b_pos[0]
                dist_y = boss_ai.dash_target_y - b_pos[1]
                dist = math.sqrt(dist_x**2 + dist_y**2)

                dash_speed = 800 * dt  # Extremely fast!

                if dist > dash_speed:
                    b_rect.x += (dist_x / dist) * dash_speed
                    b_rect.y += (dist_y / dist) * dash_speed
                else:
                    # Dash complete
                    b_rect.center = (boss_ai.dash_target_x, boss_ai.dash_target_y)
                    boss_ai.state = "CHASE"
                    boss_ai.ability_cooldown = 3.5  # Wait 6 secs before next combo

                # Update boss spatial grid
                Misc.remove_entity_from_grid(
                    e_id, entity[SpacialComponent].grid_pos, spatial_grid
                )
                new_grid = (
                    int(b_rect.x // Settings.SPRITE.WIDTH),
                    int(b_rect.y // Settings.SPRITE.HEIGHT),
                )
                entity[SpacialComponent].grid_pos = new_grid
                Misc.register_entity_in_grid(e_id, new_grid, spatial_grid)
