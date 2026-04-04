from ECS.Components import EnemyTag, FacingDirectionComponent, SpacialComponent, VelocityComponent
from Globals import Enums
from ECS.Systems import FlowFieldSystem

def process(world: dict, global_event: list):
	for obj_id in world:
		if EnemyTag in world[obj_id] and VelocityComponent not in world[obj_id]:
			obj = world[obj_id]
			
			gx, gy = obj[SpacialComponent].grid_pos
			if (gx, gy) in FlowFieldSystem.flow_field:
				dx, dy = FlowFieldSystem.flow_field[(gx, gy)]
				
				if dx != 0 or dy != 0:
					global_event.append({
						"type": Enums.EVENT_TYPES.MOVEMENT_INTENT, 
						"entity_id": obj_id, 
						"dx": dx, 
						"dy": dy
					})
					world[obj_id][FacingDirectionComponent].dx = dx
					world[obj_id][FacingDirectionComponent].dy = dy