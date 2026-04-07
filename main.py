import pygame

from Core import States
from ECS import Factories
from Globals import Settings, Misc

from ECS.Components import SpacialComponent, DeathTimerComponent
from ECS.Builders.GameOverMenuBuilder import GameOverMenuBuilder
from ECS.Builders.MainMenuBuilder import MainMenuBuilder

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

visible_entities = []

dt = 0


class Main:
    def __init__(self) -> None:
        MainMenuBuilder.build(States.world)

    def draw(self):
        Settings.window.fill(Settings.COLOURS.BLACK)

        # Only render the actual game world if we are playing
        if States.CURRENT_STATE == "PLAYING":
            RenderingSystem.process(
                surface=Settings.window,
                world=States.world,
                visible_entities=visible_entities,
                camera=States.camera,
                dt=dt,
            )

        # The UI always renders tho
        UIRenderingSystem.process(States.world, Settings.window)

    def handle_debug(self):
        if States.CURRENT_STATE != "PLAYING":
            return

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

        # --- MENU STATE  ---
        if States.CURRENT_STATE == "MENU":
            UISystem.process_events(States.world, events)
            UIHoverSystem.process(States.world)
            return  # Stops the rest of the engine from running!

        # --- VICTORY STATE  ---
        if States.CURRENT_STATE == "VICTORY":
            UISystem.process_events(States.world, events)
            UIHoverSystem.process(States.world)
            return  # Stops the swarm from moving while you look at your score

        # --- PLAYING STATE ---
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

            DamageSystem.process(States.world, States.spatial_grid, dt)
            CollisionSystem.process(States.world, States.spatial_grid)
            PickUpSystem.process(States.world, States.spatial_grid)

            EnemySpawner.process(States.world, States.spatial_grid, dt)
            OrbitalSystem.process(States.world, States.spatial_grid, dt)

            CameraSystem.process(States.world, States.camera, dt)
            FlowFieldSystem.flow_field = FlowFieldSystem.create_flow_field(
                States.world[States.PLAYER_ID][SpacialComponent].grid_pos
            )

            # --- DEATH COUNTDOWN ---
            player = States.world.get(States.PLAYER_ID)
            if player and DeathTimerComponent in player:
                player[DeathTimerComponent].time_left -= dt

                if player[DeathTimerComponent].time_left <= 0:
                    print("💀 DEATH ANIMATION FINISHED! TRIGGERING GAME OVER!")
                    States.CURRENT_STATE = "GAME_OVER"

                    GameOverMenuBuilder.build(States.world)

                    # Remove the component so this if-statement doesn't trigger again
                    del player[DeathTimerComponent]

            if States.BOSS_TIMER <= 0:
                self.trigger_boss_spawn()
                States.BOSS_TIMER = Settings.GAME.BOSS_SPAWN_TIME_DELAY

        UISystem.process_events(States.world, events)
        UIHoverSystem.process(States.world)

        # Moved inside so it doesn't crash trying to find the camera during the menu!
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
