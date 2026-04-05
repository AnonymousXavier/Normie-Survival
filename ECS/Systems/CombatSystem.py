from random import randint
from Core import States
from ECS.Components import (
    HealthComponent,
    ShieldComponent,
    EnemyTag,
    SpacialComponent,
    PlayerStatsComponent,
)
from ECS import Factories


def take_damage(world, spatial_grid, target_id, amount, entities_to_delete):
    entity = world.get(target_id)
    if not entity or HealthComponent not in entity:
        return

    # --- 1. SHIELD LOGIC (Priority) ---
    if ShieldComponent in entity:
        shield = entity[ShieldComponent]
        if shield.active:
            shield.current_hits -= 1
            print(f"Shield Tanked it! Hits left: {shield.current_hits}")

            if shield.current_hits <= 0:
                shield.active = False
                shield.timer = 0
                shield.current_hits = shield.max_hits
            return  # Damage fully absorbed

    # --- 2. APPLY DAMAGE ---
    # Use PlayerStatsComponent for current_hp if it's the player
    if PlayerStatsComponent in entity:
        stats = entity[PlayerStatsComponent]
        stats.current_hp -= amount
        is_dead = stats.current_hp <= 0
    else:
        # Standard enemy/prop health
        health = entity[HealthComponent]
        health.hp -= amount
        is_dead = health.hp <= 0

    # --- 3. DEATH PROTOCOL ---
    if is_dead:
        # Spawn Gems ONLY for enemies
        if EnemyTag in entity:
            death_pos = entity[SpacialComponent].grid_pos
            gem_value = 1 + int(States.GAME_TIME // 120)

            # Keep your offset logic for visual flair
            rx = death_pos[0] + (randint(-5, 5) / 10.0)
            ry = death_pos[1] + (randint(-5, 5) / 10.0)
            Factories.spawn_gem(world, spatial_grid, rx, ry, value=gem_value)

        entities_to_delete.add(target_id)
