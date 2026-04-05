import pygame

from Core import States
from ECS import Factories
from ECS.Components import SpacialComponent
from ECS.Systems import (
    AINavigationSystem,
    AOESystem,
    AnimationStateSystem,
    CollectionSystem,
    CollisionSystem,
    AimingSystem,
    DamageSystem,
    HitboxSystem,
    PickUpSystem,
    RegenSystem,
    UIHoverSystem,
    UIRenderingSystem,
    UISystem,
    WeaponSystem,
    CameraSystem,
    DebugRenderingSystem,
    EnemySpawner,
    FlowFieldSystem,
    InputSystem,
    OrbitalSystem,
    ProjectileSystem,
    RenderingSystem,
    DebugSystem,
    MovementSystem,
    AnimationSystem,
    BossAISystem,
)
from Globals import Settings, Misc

visible_entities = []

dt = 0


class Main:
    def __init__(self) -> None:
        States.PLAYER_ID = Factories.spawn_player(
            States.world, States.spatial_grid, 0, 0
        )
        States.camera = Factories.new_camera(
            (0, 0), Settings.CAMERA.SIZE, States.PLAYER_ID
        )

        # Spawn two shotguns, opposite to each other, rotating at 90 degrees per second
        UISystem.apply_upgrade("shotgun", States.world[States.PLAYER_ID])

    def draw(self):
        Settings.window.fill(Settings.COLOURS.BLACK)
        RenderingSystem.process(
            surface=Settings.window,
            world=States.world,
            visible_entities=visible_entities,
            camera=States.camera,
            dt=dt,
        )
        UIRenderingSystem.process(States.world, Settings.window)

    def handle_debug(self):
        debug = {}
        debug_spatial_grid = {}

        DebugSystem.process(debug, debug_spatial_grid)
        DebugRenderingSystem.process(
            surface=Settings.window,
            debug=debug,
            debug_grid=debug_spatial_grid,
            camera=States.camera,
            real_world=States.world,
        )

    def update(self):
        global visible_entities
        global dt

        events = []

        dt = Settings.WINDOW.CLOCK.tick(Settings.UPDATE.FPS) / 1000

        InputSystem.process(States.world, events, dt)

        if not States.IS_LEVELING_UP and not States.IS_PAUSED:
            States.GAME_TIME += dt
            States.BOSS_TIMER -= dt

            AimingSystem.process(States.world, States.spatial_grid, States.camera)

            AINavigationSystem.process(States.world, events)
            BossAISystem.process(States.world, States.spatial_grid, dt)

            MovementSystem.process(States.world, States.spatial_grid, events, dt)
            AnimationStateSystem.process(States.world)
            AnimationSystem.process(States.world, dt)
            HitboxSystem.process(States.world)
            RegenSystem.process(States.world, dt)

            ProjectileSystem.process(
                States.world, States.spatial_grid, States.camera, dt
            )
            WeaponSystem.process(States.world, States.spatial_grid, dt)
            AOESystem.process(States.world, States.spatial_grid, dt)
            CollectionSystem.process(States.world, States.spatial_grid, dt)

            # Run collisions after movement but before spawning new things
            DamageSystem.process(States.world, States.spatial_grid, dt)
            CollisionSystem.process(States.world, States.spatial_grid)
            PickUpSystem.process(States.world, States.spatial_grid)

            EnemySpawner.process(States.world, States.spatial_grid, dt)
            OrbitalSystem.process(States.world, States.spatial_grid, dt)

            CameraSystem.process(States.world, States.camera, dt)
            FlowFieldSystem.flow_field = FlowFieldSystem.create_flow_field(
                States.world[States.PLAYER_ID][SpacialComponent].grid_pos
            )

            if States.BOSS_TIMER <= 0:
                self.trigger_boss_spawn()
                States.BOSS_TIMER = Settings.GAME.BOSS_SPAWN_TIME_DELAY

        UISystem.process_events(States.world, events)
        UIHoverSystem.process(States.world)

        visible_entities = Misc.get_entities_on_screen(
            States.spatial_grid, CameraSystem.get_boundary_of(States.camera)
        )

    def trigger_boss_spawn(self):
        Factories.spawn_boss(
            States.world,
            States.spatial_grid,
            EnemySpawner.get_difficulty_mult(),
        )

    def run(self):
        while States.GAME_RUNNING:
            self.update()
            self.draw()
            if Settings.DEBUG.ENABLED:
                self.handle_debug()

            pygame.display.update()


Main().run()
