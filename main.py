import sys
import pygame

from core.settings import *
import core.game_state as game_state

from entities.player import Player

from world.starfield import Starfield
from world.hub_manager import HubManager
from world.sector_manager import SectorManager

from ui.hud import HUD


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids: The Ascent")

clock = pygame.time.Clock()


# --------------------------------------------------
# Game Objects
# --------------------------------------------------

player = Player(0, 0)

camera = pygame.Vector2(0, 0)

stars = Starfield()

hub_manager = HubManager()

sector_manager = SectorManager()

hud = HUD()

font = pygame.font.SysFont(None, 30)

state = game_state.EXPLORING


# --------------------------------------------------
# Main Loop
# --------------------------------------------------

running = True

while running:

    clock.tick(FPS)

    # ----------------------------
    # Events
    # ----------------------------

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ----------------------------
    # Game State Updates
    # ----------------------------

    if state == game_state.EXPLORING:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            player.rotate(-1)

        if keys[pygame.K_d]:
            player.rotate(1)

        if keys[pygame.K_w]:
            player.thrust()

        player.update()

        if sector_manager.check_sector_completion(player.position):
            state = game_state.BOSS

    elif state == game_state.BOSS:

        keys = pygame.key.get_pressed()

        # Temporary boss victory
        if keys[pygame.K_SPACE]:
            state = game_state.TRANSITION

    elif state == game_state.TRANSITION:

        sector_manager.load_next_sector()

        player.position = pygame.Vector2(0, 0)
        player.velocity = pygame.Vector2(0, 0)

        hub_manager = HubManager()

        state = game_state.EXPLORING

    # ----------------------------
    # Camera
    # ----------------------------

    target_camera = (
        player.position
        - pygame.Vector2(WIDTH // 2, HEIGHT // 2)
    )

    camera += (target_camera - camera) * 0.05

    # ----------------------------
    # Drawing
    # ----------------------------

    screen.fill(BLACK)

    if state == game_state.EXPLORING:

        stars.draw(screen, camera)

        # Sector boundary
        pygame.draw.circle(
            screen,
            (80, 80, 80),
            -camera,
            sector_manager.radius,
            2,
        )

        hub_manager.draw(screen, camera)

        player.draw(screen, camera)

        nearest_hub, hub_distance = hub_manager.get_nearest_hub(
            player.position
        )

        distance, radius = sector_manager.get_progress(
            player.position
        )

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

        screen.blit(text, (240, 280))

    elif state == game_state.TRANSITION:

        text = font.render(
            "ENTERING NEW SECTOR...",
            True,
            WHITE,
        )

        screen.blit(text, (220, 280))

    pygame.display.flip()

pygame.quit()
sys.exit()