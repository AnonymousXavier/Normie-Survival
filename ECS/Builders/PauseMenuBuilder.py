# ECS/Builders/PauseMenuBuilder.py
import pygame
from Core import States
from Globals import Settings
from ECS.Components import (
    UITag,
    SpacialComponent,
    StatPanelComponent,
    PlayerStatsComponent,
    ArsenalComponent,
    ShieldComponent,
    CollectorComponent,
    AOEComponent,
    UIButtonComponent,
)


class PauseMenuBuilder:
    _ui_ids = []

    @staticmethod
    def build(world: dict):
        player = world.get(States.PLAYER_ID)
        if not player:
            return

        # GATHER DATA
        p_stats = player.get(PlayerStatsComponent)
        arsenal = player.get(ArsenalComponent)
        shield = player.get(ShieldComponent)
        collector = player.get(CollectorComponent)
        aoe = player.get(AOEComponent)

        # POPULATE VITALS
        vitals = {}
        if p_stats:
            vitals["Level"] = str(p_stats.level)
            vitals["XP"] = f"{p_stats.xp} / {p_stats.xp_to_next_level}"

            vitals["HP"] = f"{p_stats.current_hp:.1f} / {p_stats.final_max_hp}"

            if p_stats.regen_per_second > 0:
                vitals["Regen"] = f"+{p_stats.regen_per_second:.1f}/s"
            vitals["Speed"] = f"{p_stats.final_speed:.0f}"

        # POPULATE ARSENAL
        guns = {}
        wep_lvl = 0
        if arsenal and arsenal.primary_weapon in arsenal.inventory:
            p_wep = arsenal.primary_weapon
            w_stats = arsenal.inventory[p_wep]

            d_mult = p_stats.damage_mult if p_stats else 1.0
            fr_mult = p_stats.fire_rate_mult if p_stats else 1.0

            guns["Damage"] = str(w_stats.get_final_damage(d_mult))
            guns["Fire Rate"] = f"{w_stats.get_final_fire_rate(fr_mult):.2f}s"

            # USE THE NEW UPGRADE KEY
            wep_lvl = p_stats.upgrades_owned.get("primary_weapon", 0) if p_stats else 0

            # Calculate physical gun count dynamically based on the active weapon
            if p_wep == "shotgun":
                guns["Gun Count"] = str(1 + (wep_lvl // 4))
            elif p_wep == "sniper":
                guns["Gun Count"] = str(1 + (wep_lvl // 5))
            else:
                guns["Gun Count"] = "1"

            guns["Proj. Speed"] = f"{w_stats.speed:.0f}"
            guns["Spread"] = f"{w_stats.spread_angle:.0f}°"

        # POPULATE UTILITY
        utility = {}
        if aoe:
            utility["AOE Damage"] = str(aoe.damage)
            utility["AOE Range"] = f"{aoe.radius:.1f} Grids"
            utility["AOE Cooldown"] = f"{aoe.cooldown:.1f}s"

        if shield:
            utility["Shields"] = f"{shield.current_hits} / {shield.max_hits} Hits"

        if collector:
            utility["Magnet"] = f"{collector.range:.1f} Grids"

        # Add placeholders if they haven't unlocked anything in Utility yet
        if not utility:
            utility["Status"] = "No Utilities Unlocked"

        # BUILD UI PANELS
        w = Settings.WINDOW.DESKTOP_WIDTH
        h = Settings.WINDOW.DESKTOP_HEIGHT

        panel_w = int(w * 0.25)
        panel_h = int(h * 0.23)
        padding = int(h * 0.04)

        center_x = w // 2
        center_gap = 20  # The space between the left and right panels

        # LEFT SIDE (Stats): Center minus FULL panel width minus gap
        left_start_x = center_x - panel_w - center_gap

        # RIGHT SIDE (Options): Center plus gap
        right_start_x = center_x + center_gap

        start_y = int(h * 0.12)

        PauseMenuBuilder._ui_ids.clear()

        def spawn_panel(title, data_dict, color, y_offset):
            if not data_dict:
                return
            eid = States.NEXT_ENTITY_ID
            States.NEXT_ENTITY_ID += 1

            rect = pygame.Rect(left_start_x, start_y + y_offset, panel_w, panel_h)

            world[eid] = {
                UITag: UITag(),
                SpacialComponent: SpacialComponent(rect=rect),
                StatPanelComponent: StatPanelComponent(
                    title=title, stats=data_dict, theme_color=color
                ),
            }
            PauseMenuBuilder._ui_ids.append(eid)

        # Spawn the 3 Stats blocks on the LEFT
        spawn_panel("VITALS", vitals, (50, 255, 100), 0)
        spawn_panel(f"ARSENAL (LVL {wep_lvl})", guns, (255, 150, 50), panel_h + padding)
        spawn_panel("UTILITY", utility, (50, 150, 255), (panel_h + padding) * 2)

        # BUILD OPTIONS PANEL (Right Side)
        opt_bg_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1

        # Make one giant panel that spans the height of all 3 left panels
        total_height = (panel_h * 3) + (padding * 2)
        opt_rect = pygame.Rect(right_start_x, start_y, panel_w, total_height)

        world[opt_bg_id] = {
            UITag: UITag(),
            SpacialComponent: SpacialComponent(rect=opt_rect),
            # Empty stats dict so it just draws the background/header!
            StatPanelComponent: StatPanelComponent(
                title="SYSTEM OPTIONS", stats={}, theme_color=(200, 200, 200)
            ),
        }
        PauseMenuBuilder._ui_ids.append(opt_bg_id)

        # SPAWN TOGGLE BUTTON
        btn_y = start_y + 80
        btn_w = 200
        btn_h = 50

        sound_btn_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1

        sound_text = "SOUND: ON" if Settings.GAME_OPTIONS.SOUND else "SOUND: OFF"
        color = (50, 200, 50) if Settings.GAME_OPTIONS.SOUND else (200, 50, 50)

        world[sound_btn_id] = {
            UITag: UITag(),
            UIButtonComponent: UIButtonComponent(
                rect=pygame.Rect(
                    right_start_x + (panel_w // 2) - (btn_w // 2), btn_y, btn_w, btn_h
                ),
                text=sound_text,
                color=color,
                action={"type": "TOGGLE_SOUND"},
            ),
        }
        PauseMenuBuilder._ui_ids.append(sound_btn_id)

    @staticmethod
    def destroy(world: dict):
        for eid in PauseMenuBuilder._ui_ids:
            if eid in world:
                del world[eid]
        PauseMenuBuilder._ui_ids.clear()
