import ctypes

# --- THE WINDOWS 150% SCALING FIX ---
# This forces Windows to give Pygame the TRUE physical resolution
# instead of a zoomed-in, blurry virtual resolution.
# Fixes change in resolution bug (150% and 175%)

try:
    ctypes.windll.user32.SetProcessDPIAware()
except AttributeError:
    pass  # Safely ignores the code if running on Mac or Linux

# Above just prevents scaling inconsistencies

import pygame
from Core import States
from ECS import Factories
from Globals import Settings, Misc
from Globals.AudioManager import AudioManager

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
frame = 0

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(64)
AudioManager.load_assets()


class Main:
    def __init__(self) -> None:
        self.clock = pygame.Clock()
        MainMenuBuilder.build(States.world)

        AudioManager.play_music("bg_music")

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
        global dt, frame

        events = []
        dt = self.clock.tick(Settings.UPDATE.FPS) / 1000

        InputSystem.process(States.world, events, dt)

        UIHoverSystem.process(States.world)

        # --- MENU STATE  ---
        if States.CURRENT_STATE == "MENU":
            UISystem.process_events(States.world, events)
            UIHoverSystem.process(States.world)

            # If we just clicked deploy, DO NOT return so the engine can initialize the new frame!
            if States.CURRENT_STATE != "PLAYING":
                visible_entities = []  # Actively purge old render lists to be safe
                return

            return

        # --- VICTORY STATE  ---
        if States.CURRENT_STATE == "VICTORY":
            UISystem.process_events(States.world, events)
            UIHoverSystem.process(States.world)

            return

        # --- GAME OVER STATE ---
        if States.CURRENT_STATE == "GAME_OVER":
            UISystem.process_events(States.world, events)
            UIHoverSystem.process(States.world)

            return

        # --- PLAYING STATE ---
        if not States.IS_LEVELING_UP and not States.IS_PAUSED:
            # THE HIT-STOP CHECK
            if States.HIT_STOP_TIMER > 0:
                States.HIT_STOP_TIMER -= dt  # Tick down the freeze timer
            else:
                # NORMAL GAMEPLAY UPDATES
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
                if frame >= (
                    Settings.UPDATE.FPS // Settings.UPDATE.FIELD_UPDATES_PER_SEC
                ):
                    FlowFieldSystem.flow_field = FlowFieldSystem.create_flow_field(
                        States.world[States.PLAYER_ID][SpacialComponent].grid_pos
                    )
                    frame = 0

                # --- DEATH COUNTDOWN ---
                player = States.world.get(States.PLAYER_ID)
                if player and DeathTimerComponent in player:
                    player[DeathTimerComponent].time_left -= dt

                    if player[DeathTimerComponent].time_left <= 0:
                        States.CURRENT_STATE = "GAME_OVER"

                        GameOverMenuBuilder.build(States.world)
                        AudioManager.play_sfx("player_death")

                        del player[DeathTimerComponent]

                if States.BOSS_TIMER <= 0:
                    self.trigger_boss_spawn()
                    States.BOSS_TIMER = Settings.GAME.BOSS_SPAWN_TIME_DELAY
        UISystem.process_events(States.world, events)

        # Moved inside so it doesn't crash trying to find the camera during the menu!
        visible_entities = Misc.get_entities_on_screen(
            States.spatial_grid, CameraSystem.get_boundary_of(States.camera)
        )

        States.CURRENT_FPS = int(self.clock.get_fps())

        frame += 1

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
