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


def take_damage(world, spatial_grid, target_id, amount, entities_to_delete=None):
    entity = world.get(target_id)
    boss_entity = world.get(target_id)  # Rename to keep it safe
    if not boss_entity:
        return
    if not entity:
        return

    # --- 1. SHIELD LOGIC ---
    if ShieldComponent in entity:
        shield = entity[ShieldComponent]
        if shield.active:
            shield.current_hits -= 1
            print(f"Shield Hit! Hits left: {shield.current_hits}")

            if shield.current_hits <= 0:
                shield.active = False
                shield.timer = 0
                # Note: hits will be reset in DamageSystem/ShieldSystem when timer finishes
            return  # Damage fully absorbed

    # --- 2. APPLY DAMAGE ---
    is_dead = False
    if PlayerStatsComponent in entity:
        stats = entity[PlayerStatsComponent]
        stats.current_hp -= amount
        is_dead = stats.current_hp <= 0
        print(f"Player Hit! HP: {stats.current_hp}/{stats.final_max_hp}")
    elif HealthComponent in entity:
        health = entity[HealthComponent]
        health.hp -= amount
        is_dead = health.hp <= 0

    # --- 3. DEATH & TOMBSTONING ---
    if is_dead:
        if BossTag in boss_entity:
            print("🏆 BOSS DEFEATED: CLEARING THE HORDE!")
            # Use a different variable name for the loop (e.g., 'e_id', 'e_obj')
            for e_id, e_obj in list(world.items()):
                if EnemyTag in e_obj and BossTag not in e_obj:
                    g_pos = e_obj[SpacialComponent].grid_pos
                    Misc.remove_entity_from_grid(e_id, g_pos, spatial_grid)
                    del world[e_id]

            # Now 'boss_entity' is still valid for the gem spawn
            Factories.spawn_gem(
                world,
                spatial_grid,
                boss_entity[SpacialComponent].grid_pos[0],
                boss_entity[SpacialComponent].grid_pos[1],
                value=get_gem_value(100),
            )

        elif EnemyTag in entity:
            # Spawn Gems for enemies
            is_strong = StrongerEnemyTag in entity

            # Apply difficulty scaling to gem value too?
            gem_value = 5 if is_strong else 1

            death_pos = entity[SpacialComponent].grid_pos
            gem_value = get_gem_value(gem_value)
            rx = death_pos[0] + (randint(-5, 5) / 10.0)
            ry = death_pos[1] + (randint(-5, 5) / 10.0)
            Factories.spawn_gem(world, spatial_grid, rx, ry, value=gem_value)

            if entities_to_delete is not None:
                entities_to_delete.add(target_id)

        elif PlayerInputTag in entity:
            # --- TOMBSTONING PROTOCOL ---
            # Remove components that allow interaction/movement
            del entity[PlayerInputTag]
            if ArsenalComponent in entity:
                del entity[ArsenalComponent]
            if HitboxComponent in entity:
                del entity[HitboxComponent]

            if DeathTimerComponent not in entity:
                entity[DeathTimerComponent] = DeathTimerComponent()

            if AnimationComponent in entity:
                entity[AnimationComponent].state = Enums.ANIM_STATES.DEAD
                entity[AnimationComponent].current_frame = 0
                entity[AnimationComponent].speed = 0
            print("Player Tombstoned!")


def get_gem_value(base_value):
    return base_value * (1 + int(States.GAME_TIME // 120))
