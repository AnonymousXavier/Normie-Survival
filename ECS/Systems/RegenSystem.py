from ECS.Components import HealthComponent, PlayerStatsComponent, ShieldComponent


def process(world: dict, dt: float):
    for entity_id, obj in world.items():
        if HealthComponent in obj and PlayerStatsComponent in obj:
            h = obj[HealthComponent]
            s = obj[PlayerStatsComponent]

            # 1. Base Regen
            regen_rate = s.regen_per_second

            # 2. Shield Logic: +100% current regen (Double it)
            if ShieldComponent in obj and obj[ShieldComponent].active:
                regen_rate *= 2.0

            # 3. Apply Heal (don't exceed max HP)
            if s.current_hp < s.final_max_hp:
                s.current_hp = min(s.final_max_hp, s.current_hp + (regen_rate * dt))
