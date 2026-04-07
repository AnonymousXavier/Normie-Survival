from ECS.Components import HealthComponent, PlayerStatsComponent, ShieldComponent


def process(world: dict, dt: float):
    for obj in world.values():
        if HealthComponent in obj and PlayerStatsComponent in obj:
            s = obj[PlayerStatsComponent]

            # 1. Base Regen
            regen_rate = s.regen_per_second

            # Shield Logic: +100% current regen
            if ShieldComponent in obj and obj[ShieldComponent].active:
                regen_rate *= 2.0

            # Apply Heal
            if s.current_hp < s.final_max_hp:
                s.current_hp = min(s.final_max_hp, s.current_hp + (regen_rate * dt))
