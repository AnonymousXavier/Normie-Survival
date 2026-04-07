from dataclasses import dataclass, field
from typing import Optional
import pygame

from Globals import Settings


@dataclass
class CameraShakeComponent:
    intensity: float = 0.0


@dataclass
class UIImageComponent:
    image: pygame.Surface
    alpha: int = 255  # Just in case you want to fade things in later!


@dataclass
class TrailComponent:
    length: int = 5
    history: list = field(default_factory=list)


@dataclass(kw_only=True, slots=True)
class SpacialComponent:
    grid_pos: Optional[tuple] = None
    rect: pygame.Rect


@dataclass(kw_only=True, slots=True)
class RenderComponent:
    color: tuple
    sprite: Optional[pygame.Surface] = None
    base_sprite: Optional[pygame.Surface] = None  # Stores the original image
    z_index: int = 0


@dataclass(kw_only=True)
class StalkerComponent:
    target_id: int


@dataclass(kw_only=True)
class AnimationStateComponent:
    state: int


@dataclass(kw_only=True)
class AIStateComponent:
    state: int


@dataclass(kw_only=True, slots=True)
class AnimationComponent:
    frames: dict  # Maps ANIM_STATES to cached sprite sheets
    current_frame: float = 0.0
    state: int = 0
    direction: int = 0
    speed: float = 8.0  # Frames per second


@dataclass(kw_only=True)
class VelocityComponent:
    position: tuple
    target: tuple
    speed: float


@dataclass(kw_only=True)
class PathFindingComponent:
    path: Optional[list] = field(default_factory=list)


@dataclass(kw_only=True)
class PowerUpComponent:
    _id: int


@dataclass(kw_only=True)
class RotationComponent:
    angle: float = 0.0


@dataclass(kw_only=True)
class ProjectileComponent:
    dx: float
    dy: float
    speed: float
    damage: int
    pierce: int = 1
    # Rects convert floats to int
    exact_x: float = 0.0
    exact_y: float = 0.0


@dataclass(kw_only=True)
class CooldownComponent:
    fire_rate: float  # How many seconds between shots
    time_since_last_shot: float = 0.0


@dataclass(kw_only=True, slots=True)
class FacingDirectionComponent:
    dx: float = 1.0  # By default, faces right
    dy: float = 0.0


@dataclass(kw_only=True, slots=True)
class WeaponComponent:
    weapon_type: str = "shotgun"
    is_firing: bool = False
    aim_angle: float = 0.0
    has_target: bool = False


@dataclass
class OrbitalComponent:
    target_id: int
    radius: float
    angle: float
    spin_speed: float
    offset_angle: float = 0.0


@dataclass(kw_only=True, slots=True)
class HealthComponent:
    hp: int
    max_hp: int
    inv_duration: float = 0.5  # Half a second of invincibility
    inv_timer: float = 0.0
    hit_timer: float = 0.0


@dataclass(kw_only=True, slots=True)
class HitboxComponent:
    width: int
    height: int
    offset_x: int = 0
    offset_y: int = 0

    # This will be updated by the system to match world position
    rect: pygame.Rect = field(init=False)

    def __post_init__(self):
        self.rect = pygame.Rect(0, 0, self.width, self.height)


@dataclass(kw_only=True, slots=True)
class ExperienceGemComponent:
    value: int = 1  # How much XP it gives


@dataclass(kw_only=True, slots=True)
class CollectorComponent:
    range: float = 1.0  # Pickup radius in grid cells


@dataclass(kw_only=True)
class UIButtonComponent:
    rect: pygame.Rect
    text: str
    action: dict  # what this button actually does
    color: tuple = (50, 50, 50)
    hover_color: tuple = (100, 100, 100)
    is_hovered: bool = False


@dataclass(kw_only=True)
class StatsButtonComponent:
    rect: pygame.Rect
    title: str
    description: str
    action: dict
    color: tuple = (40, 40, 40)
    hover_color: tuple = (80, 80, 80)
    is_hovered: bool = False


@dataclass(kw_only=True, slots=True)
class AOEComponent:
    radius: float = 2.0  # In grid cells
    damage: int = 2
    cooldown: float = 3.0
    timer: float = 0.0


@dataclass(kw_only=True, slots=True)
class ShieldComponent:
    extra_hp_ratio: float = 0.0
    max_hits: int = 1
    current_hits: int = 1
    recharge_delay: float = 5.0
    timer: float = 0.0
    active: bool = True


@dataclass(kw_only=True)
class DeathTimerComponent:
    time_left: float = 3.0


@dataclass(kw_only=True, slots=True)
class WeaponStats:
    base_damage: int = 1
    base_fire_rate: float = 1.0
    projectile_count: int = 3
    spread_angle: float = 15.0
    speed: float = 35.0
    pierce: int = 1

    def get_final_damage(self, player_damage_mult: float) -> int:
        return int(self.base_damage * player_damage_mult)

    def get_final_fire_rate(self, player_fire_rate_mult: float) -> float:
        return self.base_fire_rate * player_fire_rate_mult


@dataclass
class ArsenalComponent:
    inventory: dict
    primary_weapon: str = ""


@dataclass(kw_only=True, slots=True)
class StatPanelComponent:
    title: str
    stats: dict = field(default_factory=dict)
    theme_color: tuple = (255, 255, 255)


@dataclass(kw_only=True, slots=True)
class TextComponent:
    text: str
    color: tuple = (255, 255, 255)
    is_header: bool = False  # Helps the renderer pick a font size


@dataclass(kw_only=True, slots=True)
class PlayerStatsComponent:
    xp: int = 0
    level: int = 1
    xp_to_next_level: int = 5

    # Base Stats
    base_speed: float = Settings.GAME.PLAYER_SPEED
    base_max_hp: int = Settings.GAME.DEFAULT_PLAYER_HP
    current_hp: int = Settings.GAME.DEFAULT_PLAYER_HP

    # Multipliers
    speed_mult: float = 1.0
    hp_mult: float = 1.0
    damage_mult: float = 1.0
    fire_rate_mult: float = 1.0
    regen_per_second: float = 0.0

    # The Tracker
    upgrades_owned: dict = field(default_factory=dict)

    @property
    def final_speed(self) -> float:
        return self.base_speed * self.speed_mult

    @property
    def final_max_hp(self) -> int:
        return int(self.base_max_hp * self.hp_mult)


@dataclass(kw_only=True, slots=True)
class DamageComponent:
    amount: int = 1


@dataclass(kw_only=True, slots=True)
class BossAIComponent:
    state: str = "CHASE"  # States: CHASE, GRAVITY_WELL, DASH_WINDUP, DASHING
    state_timer: float = 0.0
    ability_cooldown: float = 6.0
    ability_timer: float = 0.0
    dash_target_x: float = 0.0
    dash_target_y: float = 0.0


@dataclass(kw_only=True, slots=True)
class StunComponent:
    timer: float = 0.0


class UITag:
    pass


class PlayerInputTag:
    pass


class FloorTag:
    pass


class EnemyTag:
    pass


class PowerUpTag:
    pass


class PickupTag:
    pass


class BossTag:
    pass


class StrongerEnemyTag:
    pass


class MegaGemTag:
    pass
