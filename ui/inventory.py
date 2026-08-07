import pygame

from core.settings import (
    TECHNO_GREEN,
    TECHNO_GREEN_DIM,
    TECHNO_GREEN_DARK,
)


class InventoryScreen:

    def __init__(self):

        self.font_large = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 24)


    def draw(
        self,
        screen,
        *,
        credits,
        screen_width,
        screen_height,
    ):

        panel_width = 360
        panel_height = 260

        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - panel_height) // 2

        # --------------------------------------------------
        # Dim background
        # --------------------------------------------------

        overlay = pygame.Surface(
            (screen_width, screen_height),
            pygame.SRCALPHA,
        )

        overlay.fill(
            (0, 0, 0, 160)
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        # --------------------------------------------------
        # Panel
        # --------------------------------------------------

        panel_rect = pygame.Rect(
            panel_x,
            panel_y,
            panel_width,
            panel_height,
        )

        pygame.draw.rect(
            screen,
            TECHNO_GREEN_DARK,
            panel_rect,
        )

        pygame.draw.rect(
            screen,
            TECHNO_GREEN_DIM,
            panel_rect,
            2,
        )

        # --------------------------------------------------
        # Content
        # --------------------------------------------------

        title = self.font_large.render(
            "INVENTORY",
            True,
            TECHNO_GREEN,
        )

        screen.blit(
            title,
            (panel_x + 20, panel_y + 20)
        )

        credits_text = self.font_small.render(
            f"Credits: {credits}",
            True,
            TECHNO_GREEN,
        )

        screen.blit(
            credits_text,
            (panel_x + 20, panel_y + 70)
        )

        parts_text = self.font_small.render(
            "Ship Parts: (none yet)",
            True,
            TECHNO_GREEN_DIM,
        )

        screen.blit(
            parts_text,
            (panel_x + 20, panel_y + 100)
        )

        hint_text = self.font_small.render(
            "Press I to close",
            True,
            TECHNO_GREEN_DIM,
        )

        screen.blit(
            hint_text,
            (panel_x + 20, panel_y + panel_height - 36)
        )