# ECS/Systems/DamageSystem.py
from Core import States
from ECS.Components import (
    DamageComponent,
    SpacialComponent,
    HitboxComponent,
    EnemyTag,
    HealthComponent,
    ShieldComponent,
    PlayerStatsComponent,
)
from ECS.Systems import CombatSystem


def process(world: dict, spatial_grid: dict, dt: float):
    if States.PLAYER_ID not in world:
        return

    player = world[States.PLAYER_ID]
    stats = player.get(PlayerStatsComponent)
    p_health = player.get(HealthComponent)
    p_hitbox = player.get(HitboxComponent)

    if not stats or not p_health or not p_hitbox:
        return

    # --- SHIELD RECHARGE TIMER ---
    if ShieldComponent in player:
        s = player[ShieldComponent]
        if not s.active:
            s.timer += dt
            if s.timer >= s.recharge_delay:
                s.active = True
                s.timer = 0
                s.current_hits = s.max_hits  # Reset hits on recharge!
                print("Shield Recharged!")

    if p_health.inv_timer > 0:
        p_health.inv_timer -= dt
        return

    # --- CONTACT SENSOR ---
    p_rect = p_hitbox.rect
    p_grid_pos = player[SpacialComponent].grid_pos

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            cell = (p_grid_pos[0] + dx, p_grid_pos[1] + dy)
            if cell in spatial_grid:
                for entity_id in spatial_grid[cell]:
                    enemy = world.get(entity_id)
                    if enemy and EnemyTag in enemy:
                        e_rect = (
                            enemy[HitboxComponent].rect
                            if HitboxComponent in enemy
                            else enemy[SpacialComponent].rect
                        )

                        if p_rect.colliderect(e_rect):
                            # Trigger the centralized damage
                            damage = enemy[DamageComponent].amount
                            CombatSystem.take_damage(
                                world, spatial_grid, States.PLAYER_ID, damage
                            )

                            # Set i-frames
                            p_health.inv_timer = p_health.inv_duration
                            return
