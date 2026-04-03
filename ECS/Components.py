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

class PlayerInputTag: 
	pass
class FloorTag: 
	pass
class EnemyTag: 
	pass
class PowerUpTag:
	pass
