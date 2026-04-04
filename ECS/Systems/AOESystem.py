from Core import States
from ECS.Components import AOEComponent, SpacialComponent, EnemyTag, HealthComponent


def process(world: dict, spatial_grid: dict, dt: float):
    if States.PLAYER_ID not in world: return
    
    player = world[States.PLAYER_ID]
    if AOEComponent not in player: return

    aoe = player[AOEComponent]
    aoe.timer += dt

    if aoe.timer >= aoe.cooldown:
        aoe.timer = 0
        p_pos = player[SpacialComponent].grid_pos
        r = int(aoe.radius)

        # Scan the grid area
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                cell = (p_pos[0] + dx, p_pos[1] + dy)
                if cell in spatial_grid:
                    for e_id in list(spatial_grid[cell]):
                        enemy = world.get(e_id)
                        if enemy and EnemyTag in enemy:
                            enemy[HealthComponent].hp -= aoe.damage
                            # Visual feedback could go here