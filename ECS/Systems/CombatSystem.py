import pygame
from random import randint
from Core import States
from Globals import Enums, Misc, Settings
from ECS.Components import (
    HealthComponent,
    ShieldComponent,
    EnemyTag,
    SpacialComponent,
    PlayerStatsComponent,
    PlayerInputTag,
    HitboxComponent,
    DeathTimerComponent,
    AnimationComponent,
    BossTag,
    StrongerEnemyTag,
    MegaGemTag,
)
from ECS import Factories
from Globals.AudioManager import AudioManager
from Globals.ParticleManager import ParticleManager


def take_damage(world, spatial_grid, target_id, amount, entities_to_delete=None):
    target = world.get(target_id)
    if not target:
        return

    # If the target is already dead, ignore this extra attack
    if HealthComponent in target and target[HealthComponent].hp <= 0:
        return
    if PlayerStatsComponent in target and target[PlayerStatsComponent].current_hp <= 0:
        return

    # SHIELD LOGIC
    if ShieldComponent in target:
        shield = target[ShieldComponent]
        if shield.active:
            shield.current_hits -= 1
            if shield.current_hits <= 0:
                shield.active = False
                shield.timer = 0
            return  # Damage fully absorbed

    # APPLY DAMAGE
    is_dead = False
    if PlayerStatsComponent in target:
        AudioManager.play_sfx("hit")
        stats = target[PlayerStatsComponent]
        stats.current_hp -= amount
        is_dead = stats.current_hp <= 0
    elif HealthComponent in target:
        health = target[HealthComponent]
        health.hp -= amount
        is_dead = health.hp <= 0

    target[HealthComponent].hit_timer = 0.1
    # DEATH
    if is_dead:
        States.KILLS_COUNT += 1
        enemy = target[SpacialComponent].rect
        ParticleManager.emit_sparks(enemy.x, enemy.y, color=(200, 50, 50), count=15)
        if BossTag in target:
            for e_id, e_obj in list(world.items()):
                if EnemyTag in e_obj and BossTag not in e_obj:
                    g_pos = e_obj[SpacialComponent].grid_pos

                    # Check if it was a Red Cyclops or a Green Cyclops
                    is_strong = StrongerEnemyTag in e_obj

                    # Calculate normal value, then cut it in half!
                    normal_gem_value = get_gem_value(
                        Settings.GAME.STRONGER_ENEMIES_MULTIPLIER if is_strong else 1
                    )
                    reduced_gem_value = max(1, normal_gem_value // 2)

                    # Add random scatter so they look natural
                    rx = g_pos[0] + (randint(-5, 5) / 10.0)
                    ry = g_pos[1] + (randint(-5, 5) / 10.0)

                    Factories.spawn_gem(
                        world, spatial_grid, rx, ry, value=reduced_gem_value
                    )

                    # Now delete the enemy
                    Misc.remove_entity_from_grid(e_id, g_pos, spatial_grid)
                    del world[e_id]
            pygame.time.wait(150)
            # Spawn Mega Gem exactly where the boss was
            mega_gem_id = Factories.spawn_gem(
                world,
                spatial_grid,
                target[SpacialComponent].grid_pos[0],
                target[SpacialComponent].grid_pos[1],
                value=get_gem_value(Settings.GAME.BOSS_STRENGTH_MULTIPLIER),
            )
            world[mega_gem_id][MegaGemTag] = MegaGemTag()

            # Clean up the Boss immediately
            Misc.remove_entity_from_grid(
                target_id, target[SpacialComponent].grid_pos, spatial_grid
            )
            del world[target_id]

        elif EnemyTag in target:
            # Handle standard enemy death
            is_strong = StrongerEnemyTag in target
            gem_value = get_gem_value(
                Settings.GAME.STRONGER_ENEMIES_MULTIPLIER if is_strong else 1
            )

            death_pos = target[SpacialComponent].grid_pos
            rx = death_pos[0] + (randint(-5, 5) / 10.0)
            ry = death_pos[1] + (randint(-5, 5) / 10.0)
            Factories.spawn_gem(world, spatial_grid, rx, ry, value=gem_value)

            # Add to the system's deletion set for the main cleanup pass
            if entities_to_delete is not None:
                entities_to_delete.add(target_id)

        elif PlayerInputTag in target:
            # Remove components that allow interaction/movement
            del target[PlayerInputTag]
            if HitboxComponent in target:
                del target[HitboxComponent]

            if DeathTimerComponent not in target:
                target[DeathTimerComponent] = DeathTimerComponent()

            if AnimationComponent in target:
                target[AnimationComponent].state = Enums.ANIM_STATES.DEAD
                target[AnimationComponent].current_frame = 0
                target[AnimationComponent].speed = 0


def get_gem_value(base_value):
    return base_value * (1 + int(States.GAME_TIME // 120))
