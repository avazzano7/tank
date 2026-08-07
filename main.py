import sys

import pygame

from core.settings import *
import core.game_state as game_state

from entities.player import Player
from entities.bullet import Bullet

from world.starfield import Starfield
from world.hub_manager import HubManager
from world.sector_manager import SectorManager
from world.asteroid_manager import AsteroidManager

from ui.hud import HUD


pygame.init()


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

hud = HUD()

bullets = []


# ==================================================
# TEMPORARY FONT
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

running = True

while running:

    dt = clock.tick(FPS) / 1000.0


    # ==================================================
    # EVENTS
    # ==================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


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
        # Player
        # ----------------------------------------------

        player.update(dt)


        # ----------------------------------------------
        # Asteroids
        # ----------------------------------------------

        asteroid_manager.update()


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
        # Maintain asteroid population
        # ----------------------------------------------

        asteroid_manager.maintain_population()


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


        # New sector hubs

        hub_manager = HubManager(
            sector_manager
        )


        # New sector asteroid configuration

        asteroid_manager = AsteroidManager(
            player,
            sector_manager
        )


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


        # Bullets

        for bullet in bullets:

            bullet.draw(
                screen,
                camera
            )


        # Player

        player.draw(
            screen,
            camera
        )


        # Navigation

        nearest_hub, hub_distance = (
            hub_manager.get_nearest_hub(
                player.position
            )
        )


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


    pygame.display.flip()


# ==================================================
# SHUTDOWN
# ==================================================

pygame.quit()

sys.exit()