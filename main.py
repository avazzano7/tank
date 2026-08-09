import sys

import pygame

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(32)

from core.settings import *
import core.game_state as game_state

from entities.player import Player
from entities.bullet import Bullet
from entities.missile import Missile

from world.starfield import Starfield
from world.hub_manager import HubManager
from world.sector_manager import SectorManager
from world.asteroid_manager import AsteroidManager
from world.salvage_manager import SalvageManager
from world.part_manager import PartManager

from ui.hud import HUD
from ui.inventory import InventoryScreen
from ui.dock_prompt import DockPrompt
from ui.hub_screen import HubScreen

from sound_handling.ui import inventory_open_sound, inventory_close_sound
from sound_handling.player import death_sound


# ==================================================
# DISPLAY
# ==================================================

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Asteroids: The Ascent"
)

clock = pygame.time.Clock()


# ==================================================
# GAME OBJECTS
# ==================================================

player = Player(
    0,
    0
)

camera = pygame.Vector2(
    0,
    0
)

stars = Starfield()

sector_manager = SectorManager()

hub_manager = HubManager(
    sector_manager
)

asteroid_manager = AsteroidManager(
    player,
    sector_manager
)

salvage_manager = SalvageManager()

part_manager = PartManager()

hud = HUD()

inventory = InventoryScreen()

dock_prompt = DockPrompt()

hub_screen = HubScreen()

show_inventory = False

# Nearest hub tracking, updated every EXPLORING frame
nearest_hub = None
hub_distance = float("inf")
in_dock_range = False

# The hub the player is currently docked at (None if not docked)
docked_hub = None

bullets = []

missiles = []
# ==================================================

font = pygame.font.SysFont(
    None,
    30
)


# ==================================================
# GAME STATE
# ==================================================

state = game_state.EXPLORING


# ==================================================
# MAIN LOOP
# ==================================================

main_music = pygame.mixer.music.load("assets/sounds/music/Dark Man Piano.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop indefinitely

running = True

while running:

    dt = clock.tick(FPS) / 1000.0


    # ==================================================
    # EVENTS
    # ==================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_i:
                if show_inventory:
                    inventory_close_sound.play()
                    show_inventory = False
                else:
                    inventory_open_sound.play()
                    show_inventory = True


            if event.key == pygame.K_e:

                if (
                    state == game_state.EXPLORING
                    and in_dock_range
                ):

                    inventory_open_sound.play()

                    state = game_state.DOCKED

                    docked_hub = nearest_hub

                    player.velocity = pygame.Vector2(
                        0,
                        0
                    )


                elif state == game_state.DOCKED:

                    inventory_close_sound.play()

                    state = game_state.EXPLORING

                    docked_hub = None


            if state == game_state.DOCKED:

                purchase_keys = {
                    pygame.K_1: 0,
                    pygame.K_2: 1,
                    pygame.K_3: 2,
                }

                if event.key in purchase_keys:

                    index = purchase_keys[event.key]

                    summary = player.get_upgrade_summary()

                    if index < len(summary):

                        player.purchase_upgrade(
                            summary[index]["key"]
                        )


                advanced_keys = {
                    pygame.K_4: 0,
                }

                if event.key in advanced_keys:

                    index = advanced_keys[event.key]

                    advanced_summary = player.get_advanced_summary()

                    if index < len(advanced_summary):

                        entry_key = advanced_summary[index]["key"]

                        if entry_key == "missiles":

                            player.purchase_missile_upgrade()


    # ==================================================
    # EXPLORING
    # ==================================================

    if state == game_state.EXPLORING:

        keys = pygame.key.get_pressed()


        # ----------------------------------------------
        # Rotation
        # ----------------------------------------------

        if keys[pygame.K_a]:

            player.rotate(-1)


        if keys[pygame.K_d]:

            player.rotate(1)


        # ----------------------------------------------
        # Thrust
        # ----------------------------------------------

        if keys[pygame.K_w]:

            player.thrust()


        # ----------------------------------------------
        # Fire
        # ----------------------------------------------

        if keys[pygame.K_SPACE]:

            if player.can_fire():

                direction = (
                    player.get_forward_direction()
                )

                bullet_position = (
                    player.position
                    + direction * 20
                )

                bullets.append(
                    Bullet(
                        bullet_position,
                        direction
                    )
                )

                player.fire()


        # ----------------------------------------------
        # Fire missile
        # ----------------------------------------------

        if keys[pygame.K_q]:

            if player.can_fire_missile():

                direction = (
                    player.get_forward_direction()
                )

                missile_position = (
                    player.position
                    + direction * 20
                )

                stats = player.fire_missile()

                missiles.append(
                    Missile(
                        missile_position,
                        direction,
                        stats["damage"],
                        stats["splash_radius"],
                    )
                )


        # ----------------------------------------------
        # Player
        # ----------------------------------------------

        player.update(dt)


        # ----------------------------------------------
        # Hub proximity / docking check
        # ----------------------------------------------

        nearest_hub, hub_distance = (
            hub_manager.get_nearest_hub(
                player.position
            )
        )

        in_dock_range = (
            hub_distance <= HUB_DOCKING_RANGE
        )


        # ----------------------------------------------
        # Asteroids
        # ----------------------------------------------

        asteroid_manager.update()


        # ----------------------------------------------
        # Player / asteroid collision
        # ----------------------------------------------

        asteroid_manager.check_player_collision(
            player
        )

        if not player.is_alive():
            death_sound.play()
            state = game_state.GAME_OVER


        # ----------------------------------------------
        # Bullet collisions
        # ----------------------------------------------

        remaining_bullets = []

        for bullet in bullets:

            if asteroid_manager.check_bullet_collision(
                bullet
            ):

                continue

            remaining_bullets.append(
                bullet
            )

        bullets = remaining_bullets


        # ----------------------------------------------
        # Missile collisions
        # ----------------------------------------------

        remaining_missiles = []

        for missile in missiles:

            if asteroid_manager.check_missile_collision(
                missile
            ):

                continue

            remaining_missiles.append(
                missile
            )

        missiles = remaining_missiles


        # ----------------------------------------------
        # Salvage: spawn drops from destroyed asteroids
        # ----------------------------------------------

        drops = asteroid_manager.pop_drops()

        salvage_manager.spawn_from_drops(
            drops
        )

        salvage_manager.update(dt)

        salvage_manager.check_player_collision(
            player
        )


        # ----------------------------------------------
        # Ship parts: spawn drops from destroyed asteroids
        # ----------------------------------------------

        part_drops = asteroid_manager.pop_part_drops()

        part_manager.spawn_from_drops(
            part_drops
        )

        part_manager.update(dt)

        part_manager.check_player_collision(
            player
        )


        # ----------------------------------------------
        # Sector completion
        # ----------------------------------------------

        if sector_manager.check_sector_completion(
            player.position
        ):

            state = game_state.BOSS


        # ----------------------------------------------
        # Bullets
        # ----------------------------------------------

        active_bullets = []

        for bullet in bullets:

            if bullet.update(dt):

                active_bullets.append(
                    bullet
                )

        bullets = active_bullets


        # ----------------------------------------------
        # Missiles
        # ----------------------------------------------

        active_missiles = []

        for missile in missiles:

            if missile.update(dt):

                active_missiles.append(
                    missile
                )

        missiles = active_missiles


        # ----------------------------------------------
        # Maintain asteroid population
        # ----------------------------------------------

        asteroid_manager.maintain_population()


    # ==================================================
    # DOCKED
    # ==================================================

    elif state == game_state.DOCKED:

        # World is frozen while docked.
        # Undocking is handled in the event loop (K_e).

        pass


    # ==================================================
    # BOSS
    # ==================================================

    elif state == game_state.BOSS:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:

            state = game_state.TRANSITION


    # ==================================================
    # TRANSITION
    # ==================================================

    elif state == game_state.TRANSITION:

        sector_manager.load_next_sector()

        player.position = pygame.Vector2(
            0,
            0
        )

        player.velocity = pygame.Vector2(
            0,
            0
        )

        bullets.clear()

        missiles.clear()

        hub_manager = HubManager(
            sector_manager
        )


        # New sector asteroid configuration

        asteroid_manager = AsteroidManager(
            player,
            sector_manager
        )


        # New sector salvage

        salvage_manager = SalvageManager()


        # New sector ship parts

        part_manager = PartManager()


        state = game_state.EXPLORING


    # ==================================================
    # GAME OVER
    # ==================================================

    elif state == game_state.GAME_OVER:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:

            sector_manager.load_sector(1)

            player.position = pygame.Vector2(
                0,
                0
            )

            player.velocity = pygame.Vector2(
                0,
                0
            )

            player.reset_health()

            bullets.clear()

            missiles.clear()

            hub_manager = HubManager(
                sector_manager
            )

            asteroid_manager = AsteroidManager(
                player,
                sector_manager
            )

            salvage_manager = SalvageManager()

            part_manager = PartManager()

            state = game_state.EXPLORING


    # ==================================================
    # CAMERA
    # ==================================================

    camera_target_position = (
        player.position
        + player.velocity * 20
    )

    target_camera = (
        camera_target_position
        - pygame.Vector2(
            WIDTH // 2,
            HEIGHT // 2
        )
    )

    camera += (
        target_camera - camera
    ) * 0.12


    # ==================================================
    # DRAW
    # ==================================================

    screen.fill(BLACK)


    if state == game_state.EXPLORING:

        stars.draw(
            screen,
            camera
        )


        # Sector boundary

        pygame.draw.circle(
            screen,
            (80, 80, 80),
            -camera,
            sector_manager.radius,
            2
        )


        # Hubs

        hub_manager.draw(
            screen,
            camera
        )


        # Asteroids

        asteroid_manager.draw(
            screen,
            camera
        )


        # Salvage

        salvage_manager.draw(
            screen,
            camera
        )


        # Ship parts

        part_manager.draw(
            screen,
            camera
        )


        # Bullets

        for bullet in bullets:

            bullet.draw(
                screen,
                camera
            )


        # Missiles

        for missile in missiles:

            missile.draw(
                screen,
                camera
            )


        # Player

        player.draw(
            screen,
            camera
        )


        # Navigation

        distance, radius = (
            sector_manager.get_progress(
                player.position
            )
        )


        # HUD

        hud.draw(
            screen,
            sector=sector_manager.current_sector,
            distance_from_home=distance,
            sector_radius=radius,
            nearest_hub_name=nearest_hub.name,
            nearest_hub_distance=hub_distance,
            player_position=player.position,
            nearest_hub_position=nearest_hub.position,
            player_health=player.health,
            player_max_health=player.max_health,
        )


        # Dock prompt

        if in_dock_range:

            dock_prompt.draw(
                screen,
                nearest_hub.name,
                WIDTH,
                HEIGHT,
            )


    elif state == game_state.DOCKED:

        hub_screen.draw(
            screen,
            hub_name=docked_hub.name,
            credits=player.credits,
            upgrades=player.get_upgrade_summary(),
            advanced=player.get_advanced_summary(),
            part_counts=player.get_part_counts(),
            screen_width=WIDTH,
            screen_height=HEIGHT,
        )


    elif state == game_state.BOSS:

        text = font.render(
            "BOSS FIGHT - PRESS SPACE",
            True,
            WHITE,
        )

        screen.blit(
            text,
            (240, 280)
        )


    elif state == game_state.TRANSITION:

        text = font.render(
            "ENTERING NEW SECTOR...",
            True,
            WHITE,
        )

        screen.blit(
            text,
            (220, 280)
        )


    elif state == game_state.GAME_OVER:

        text = font.render(
            "SHIP DESTROYED - PRESS R TO RESTART",
            True,
            WHITE,
        )

        screen.blit(
            text,
            (160, 280)
        )


    # ----------------------------------------------------
    # Inventory overlay (drawn on top of everything)
    # ----------------------------------------------------

    if show_inventory:

        inventory.draw(
            screen,
            credits=player.credits,
            parts=player.get_part_counts(),
            screen_width=WIDTH,
            screen_height=HEIGHT,
        )


    pygame.display.flip()


# ==================================================
# SHUTDOWN
# ==================================================

pygame.quit()

sys.exit()