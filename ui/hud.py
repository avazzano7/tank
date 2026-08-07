import pygame

from ui.widgets.progress_bar import ProgressBar
from ui.widgets.compass import Compass


class HUD:

    def __init__(self):

        self.font_large = pygame.font.SysFont(None, 28)
        self.font_small = pygame.font.SysFont(None, 22)

        self.progress_bar = ProgressBar(
            width=220,
            height=18,
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
    ):

        x = 20
        y = 20

        title = self.font_large.render(
            f"SECTOR {sector}",
            True,
            (255, 255, 255),
        )

        screen.blit(title, (x, y))

        y += 40

        screen.blit(
            self.font_small.render(
                "Progress",
                True,
                (220, 220, 220),
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
                (255, 255, 255),
            ),
            (x, y),
        )

        y += 30

        screen.blit(
            self.font_small.render(
                nearest_hub_name,
                True,
                (255, 255, 255),
            ),
            (x, y),
        )

        y += 26

        screen.blit(
            self.font_small.render(
                f"{int(nearest_hub_distance):,} km",
                True,
                (200, 200, 200),
            ),
            (x, y),
        )

        self.compass.draw(
            screen,
            pygame.Vector2(x + 100, y),
            player_position,
            nearest_hub_position,
        )