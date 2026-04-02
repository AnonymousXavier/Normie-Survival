from ECS.Systems import FlowFieldSystem


def process(debug: dict, debug_grid: dict):
	FlowFieldSystem.store_arrows_in_degub(debug, debug_grid)