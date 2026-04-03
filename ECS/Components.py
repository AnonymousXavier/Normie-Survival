from dataclasses import dataclass, field
from typing import Optional
import pygame

@dataclass(kw_only=True)
class SpacialComponent:
	grid_pos: Optional[tuple] = None
	rect: pygame.Rect

@dataclass(kw_only=True)
class RenderComponent:
	color: tuple
	sprite: Optional[pygame.Surface] = None
	base_sprite: Optional[pygame.Surface] = None # Stores the original image
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

@dataclass(kw_only=True)
class AnimationComponent:
	frames: dict
	current_frame: int
	state: int
	direction: int

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

@dataclass(kw_only=True)
class CooldownComponent:
    fire_rate: float # How many seconds between shots
    time_since_last_shot: float = 0.0

@dataclass(kw_only=True, slots=True)
class FacingDirectionComponent:
    dx: float = 1.0 # Default facing right
    dy: float = 0.0

@dataclass(kw_only=True, slots=True)
class WeaponComponent:
    weapon_type: str = "shotgun"
    is_firing: bool = False
    aim_angle: float = 0.0

@dataclass(kw_only=True)
class OrbitalComponent:
    target_id: int     
    radius: float       
    angle: float = 0.0  
    spin_speed: float = 0.0 # Degrees per second

@dataclass
class WeaponStats:
    projectile_count: int = 3
    spread_angle: float = 30.0  # Total arc of the cone in degrees
    damage: int = 1
    speed: float = 300.0
    fire_rate: float = 1.0  # Seconds between shots

@dataclass(kw_only=True, slots=True)
class HealthComponent:
    hp: int = 1

@dataclass(kw_only=True, slots=True)
class ExperienceGemComponent:
    value: int = 1  # How much XP it gives

@dataclass(kw_only=True, slots=True)
class CollectorComponent:
    range: float = 2.0  # Pickup radius in grid cells

@dataclass(kw_only=True, slots=True)
class PlayerStatsComponent:
    xp: int = 0
    level: int = 1
    xp_to_next_level: int = 5

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
