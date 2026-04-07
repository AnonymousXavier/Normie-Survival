from ECS.Components import (
    PlayerStatsComponent,
    PowerUpTag,
    SpacialComponent,
    RotationComponent,
    CooldownComponent,
    ArsenalComponent,
    WeaponComponent,
    CameraShakeComponent,
)
from ECS import Factories
from Core import States


def process(world: dict, spatial_grid: dict, delta: float):
    player = world.get(States.PLAYER_ID)
    if not player or ArsenalComponent not in player:
        return

    inventory = player[ArsenalComponent].inventory

    # Find the camera entity once per frame
    camera_ent = States.camera

    for obj in list(world.values()):
        if PowerUpTag in obj and CooldownComponent in obj and WeaponComponent in obj:
            w_type = obj[WeaponComponent].weapon_type
            w_stats = inventory.get(w_type)
            if not w_stats:
                continue

            fire_rate = w_stats.get_final_fire_rate(
                player[PlayerStatsComponent].fire_rate_mult
            )
            bullet_dmg = w_stats.get_final_damage(
                player[PlayerStatsComponent].damage_mult
            )

            obj[CooldownComponent].fire_rate = fire_rate
            obj[CooldownComponent].time_since_last_shot += delta

            if (
                obj[CooldownComponent].time_since_last_shot
                >= obj[CooldownComponent].fire_rate
                and obj[WeaponComponent].has_target
            ):
                obj[CooldownComponent].time_since_last_shot = 0.0

                # TRIGGER THE SHAKE
                if camera_ent and CameraShakeComponent in camera_ent:
                    shake = camera_ent[CameraShakeComponent]
                    # Add punch
                    shake.intensity = min(shake.intensity + 1.0, 5.0)

                cx = obj[SpacialComponent].rect.centerx
                cy = obj[SpacialComponent].rect.centery
                base_angle = obj[RotationComponent].angle

                # SPREAD MATH
                count = w_stats.projectile_count
                spread = w_stats.spread_angle

                if count <= 1:
                    angles = [base_angle]
                else:
                    start_angle = base_angle - (spread / 2)
                    step_angle = spread / (count - 1)
                    angles = [start_angle + (i * step_angle) for i in range(count)]

                for angle in angles:
                    Factories.spawn_bullet(
                        world,
                        spatial_grid,
                        cx,
                        cy,
                        angle,
                        w_stats.speed,
                        bullet_dmg,
                        w_stats.pierce,
                    )
