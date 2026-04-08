import pygame
import os
from Globals import Settings


class AudioManager:
    SFX = {}
    MUSIC_TRACKS = {}

    @classmethod
    def load_assets(cls):
        audio_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "Assets", "Audio"
        )

        try:
            # Match the exact file names from your screenshot
            cls.SFX["shoot_shotgun"] = pygame.mixer.Sound(
                os.path.join(audio_dir, "shotgun.wav")
            )
            cls.SFX["shoot_sniper"] = pygame.mixer.Sound(
                os.path.join(audio_dir, "sniper.wav")
            )
            cls.SFX["gem_pickup"] = pygame.mixer.Sound(
                os.path.join(audio_dir, "gem.wav")
            )
            cls.SFX["ui_click"] = pygame.mixer.Sound(
                os.path.join(audio_dir, "click.wav")
            )
            cls.SFX["hit"] = pygame.mixer.Sound(os.path.join(audio_dir, "hit.wav"))
            cls.SFX["player_death"] = pygame.mixer.Sound(
                os.path.join(audio_dir, "GameOver.wav")
            )
            cls.SFX["victory"] = pygame.mixer.Sound(
                os.path.join(audio_dir, "Success.wav")
            )
            cls.SFX["level_up"] = pygame.mixer.Sound(
                os.path.join(audio_dir, "level_up.wav")
            )

            # Audio Mixing: Turn down the gem pickup so it doesn't drown out the guns
            cls.SFX["gem_pickup"].set_volume(0.3)
            cls.SFX["shoot_shotgun"].set_volume(0.6)
            cls.SFX["shoot_sniper"].set_volume(0.7)

        except FileNotFoundError as e:
            print(f"⚠️ Audio File Missing: {e}")

        try:
            cls.MUSIC_TRACKS["bg_music"] = os.path.join(audio_dir, "bg_music.ogg")
        except Exception as e:
            print(f"Music File Error: {e}")

        print("Audio Loaded successfully")

    @classmethod
    def play_sfx(cls, sound_name):
        if Settings.GAME_OPTIONS.SOUND and sound_name in cls.SFX:
            cls.SFX[sound_name].play()

    @classmethod
    def play_music(cls, track_name):
        if Settings.GAME_OPTIONS.MUSIC and track_name in cls.MUSIC_TRACKS:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(cls.MUSIC_TRACKS[track_name])
                pygame.mixer.music.play(-1)  # Loop forever
        else:
            pygame.mixer.music.stop()

    @classmethod
    def stop_music(cls):
        pygame.mixer.music.stop()
