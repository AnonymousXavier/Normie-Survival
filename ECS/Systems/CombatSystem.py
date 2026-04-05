# ECS/Systems/CombatSystem.py
from random import randint
from Core import States
from Globals import Enums, Misc
from ECS.Components import (
    HealthComponent,
    ShieldComponent,
    EnemyTag,
    SpacialComponent,
    PlayerStatsComponent,
    PlayerInputTag,
    ArsenalComponent,
    HitboxComponent,
    DeathTimerComponent,
    AnimationComponent,
    BossTag,
    StrongerEnemyTag,
)
from ECS import Factories


# ECS/Systems/CombatSystem.py


def take_damage(world, spatial_grid, target_id, amount, entities_to_delete=None):
    target = world.get(target_id)
    if not target:
        return

    # --- 0. PREVENT OVERKILL (Moved to the top) ---
    # If the target is already dead/dying, ignore this extra projectile/hit
    if HealthComponent in target and target[HealthComponent].hp <= 0:
        return
    if PlayerStatsComponent in target and target[PlayerStatsComponent].current_hp <= 0:
        return

    # --- 1. SHIELD LOGIC ---
    if ShieldComponent in target:
        shield = target[ShieldComponent]
        if shield.active:
            shield.current_hits -= 1
            if shield.current_hits <= 0:
                shield.active = False
                shield.timer = 0
            return  # Damage fully absorbed

    # --- 2. APPLY DAMAGE ---
    is_dead = False
    if PlayerStatsComponent in target:
        stats = target[PlayerStatsComponent]
        stats.current_hp -= amount
        is_dead = stats.current_hp <= 0
    elif HealthComponent in target:
        health = target[HealthComponent]
        health.hp -= amount
        is_dead = health.hp <= 0

    target[HealthComponent].hit_timer = 0.1
    # --- 3. DEATH LOGIC ---
    if is_dead:
        if BossTag in target:
            print("🏆 BOSS DEFEATED: CLEARING THE HORDE!")
            # Use 'e_id' and 'e_obj' to avoid overwriting our 'target' reference
            for e_id, e_obj in list(world.items()):
                if EnemyTag in e_obj and BossTag not in e_obj:
                    g_pos = e_obj[SpacialComponent].grid_pos
                    Misc.remove_entity_from_grid(e_id, g_pos, spatial_grid)
                    del world[e_id]

            # Spawn Mega Gem exactly where the boss was
            Factories.spawn_gem(
                world,
                spatial_grid,
                target[SpacialComponent].grid_pos[0],
                target[SpacialComponent].grid_pos[1],
                value=get_gem_value(100),
            )

            # Bosses are deleted immediately to stop them from dealing contact damage
            Misc.remove_entity_from_grid(
                target_id, target[SpacialComponent].grid_pos, spatial_grid
            )
            del world[target_id]

        elif EnemyTag in target:
            # Handle standard enemy death
            is_strong = StrongerEnemyTag in target
            gem_value = get_gem_value(5 if is_strong else 1)

            death_pos = target[SpacialComponent].grid_pos
            rx = death_pos[0] + (randint(-5, 5) / 10.0)
            ry = death_pos[1] + (randint(-5, 5) / 10.0)
            Factories.spawn_gem(world, spatial_grid, rx, ry, value=gem_value)

            # Add to the system's deletion set for the main cleanup pass
            if entities_to_delete is not None:
                entities_to_delete.add(target_id)

        elif PlayerInputTag in target:
            # --- TOMBSTONING PROTOCOL ---
            # Remove components that allow interaction/movement
            del target[PlayerInputTag]
            if ArsenalComponent in target:
                del target[ArsenalComponent]
            if HitboxComponent in target:
                del target[HitboxComponent]

            if DeathTimerComponent not in target:
                target[DeathTimerComponent] = DeathTimerComponent()

            if AnimationComponent in target:
                target[AnimationComponent].state = Enums.ANIM_STATES.DEAD
                target[AnimationComponent].current_frame = 0
                target[AnimationComponent].speed = 0
            print("Player Tombstoned!")


def get_gem_value(base_value):
    return base_value * (1 + int(States.GAME_TIME // 120))
