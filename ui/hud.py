import pygame

from core.settings import (
    TECHNO_GREEN,
    TECHNO_GREEN_DIM,
    TECHNO_GREEN_DARK,
)

from ui.widgets.progress_bar import ProgressBar
from ui.widgets.compass import Compass


class HUD:

    def __init__(self):

        self.font_large = pygame.font.SysFont(None, 28)
        self.font_small = pygame.font.SysFont(None, 22)

        self.progress_bar = ProgressBar(
            width=220,
            height=18,
            fill_color=TECHNO_GREEN,
            border_color=TECHNO_GREEN_DIM,
            background_color=TECHNO_GREEN_DARK,
        )

        self.health_bar = ProgressBar(
            width=220,
            height=18,
            fill_color=TECHNO_GREEN,
            border_color=TECHNO_GREEN_DIM,
            background_color=TECHNO_GREEN_DARK,
        )

        self.compass = Compass()

    def draw(
        self,
        screen,
        *,
        sector,
        distance_from_home,
        sector_radius,
        nearest_hub_name,
        nearest_hub_distance,
        player_position,
        nearest_hub_position,
        player_health,
        player_max_health,
    ):

        x = 20
        y = 20

        title = self.font_large.render(
            f"SECTOR {sector}",
            True,
            TECHNO_GREEN,
        )

        screen.blit(title, (x, y))

        y += 40

        screen.blit(
            self.font_small.render(
                "Progress",
                True,
                TECHNO_GREEN_DIM,
            ),
            (x, y),
        )

        percent = distance_from_home / sector_radius

        self.progress_bar.draw(
            screen,
            x,
            y + 24,
            percent,
        )

        y += 60

        screen.blit(
            self.font_small.render(
                f"Home: {int(distance_from_home):,} km",
                True,
                TECHNO_GREEN,
            ),
            (x, y),
        )

        y += 30

        screen.blit(
            self.font_small.render(
                nearest_hub_name,
                True,
                TECHNO_GREEN,
            ),
            (x, y),
        )

        y += 26

        screen.blit(
            self.font_small.render(
                f"{int(nearest_hub_distance):,} km",
                True,
                TECHNO_GREEN_DIM,
            ),
            (x, y),
        )

        self.compass.draw(
            screen,
            pygame.Vector2(x + 100, y),
            player_position,
            nearest_hub_position,
        )

        y += 50

        screen.blit(
            self.font_small.render(
                "Hull",
                True,
                TECHNO_GREEN_DIM,
            ),
            (x, y),
        )

        health_percent = (
            player_health / player_max_health
        )

        self.health_bar.draw(
            screen,
            x,
            y + 24,
            health_percent,
        )

        y += 60

        screen.blit(
            self.font_small.render(
                f"{int(player_health)} / {int(player_max_health)}",
                True,
                TECHNO_GREEN,
            ),
            (x, y),
        )