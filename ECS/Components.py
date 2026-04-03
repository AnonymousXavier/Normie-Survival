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
	angle = 90

class PlayerInputTag: 
	pass
class FloorTag: 
	pass
class EnemyTag: 
	pass
class PowerUpTag:
	pass
