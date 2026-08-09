import pygame

from core.settings import (
    TECHNO_GREEN,
    TECHNO_GREEN_DIM,
    TECHNO_GREEN_DARK,
)


class HubScreen:

    def __init__(self):

        self.font_title = pygame.font.SysFont(None, 44)
        self.font_section = pygame.font.SysFont(None, 30)
        self.font_small = pygame.font.SysFont(None, 22)


    def draw(
        self,
        screen,
        *,
        hub_name,
        credits,
        screen_width,
        screen_height,
    ):

        # --------------------------------------------------
        # Backdrop
        # --------------------------------------------------

        screen.fill(
            (5, 15, 10)
        )

        # --------------------------------------------------
        # Title
        # --------------------------------------------------

        title = self.font_title.render(
            hub_name,
            True,
            TECHNO_GREEN,
        )

        screen.blit(
            title,
            (60, 50)
        )

        credits_text = self.font_small.render(
            f"Credits: {credits}",
            True,
            TECHNO_GREEN,
        )

        screen.blit(
            credits_text,
            (60, 100)
        )

        # --------------------------------------------------
        # Upgrades panel
        # --------------------------------------------------

        upgrades_rect = pygame.Rect(
            60, 150, 320, 260
        )

        pygame.draw.rect(
            screen,
            TECHNO_GREEN_DARK,
            upgrades_rect,
        )

        pygame.draw.rect(
            screen,
            TECHNO_GREEN_DIM,
            upgrades_rect,
            2,
        )

        upgrades_label = self.font_section.render(
            "UPGRADES",
            True,
            TECHNO_GREEN,
        )

        screen.blit(
            upgrades_label,
            (80, 165)
        )

        upgrade_lines = [
            "Fire Rate  (coming soon)",
            "Bullet Damage  (coming soon)",
            "Max Health  (coming soon)",
        ]

        y = 210

        for line in upgrade_lines:

            line_text = self.font_small.render(
                line,
                True,
                TECHNO_GREEN_DIM,
            )

            screen.blit(
                line_text,
                (80, y)
            )

            y += 32

        # --------------------------------------------------
        # Advanced (ship parts) panel
        # --------------------------------------------------

        advanced_rect = pygame.Rect(
            400, 150, 320, 260
        )

        pygame.draw.rect(
            screen,
            TECHNO_GREEN_DARK,
            advanced_rect,
        )

        pygame.draw.rect(
            screen,
            TECHNO_GREEN_DIM,
            advanced_rect,
            2,
        )

        advanced_label = self.font_section.render(
            "ADVANCED",
            True,
            TECHNO_GREEN,
        )

        screen.blit(
            advanced_label,
            (420, 165)
        )

        advanced_text = self.font_small.render(
            "Requires Ship Parts",
            True,
            TECHNO_GREEN_DIM,
        )

        screen.blit(
            advanced_text,
            (420, 210)
        )

        advanced_subtext = self.font_small.render(
            "(coming soon)",
            True,
            TECHNO_GREEN_DIM,
        )

        screen.blit(
            advanced_subtext,
            (420, 236)
        )

        # --------------------------------------------------
        # Undock hint
        # --------------------------------------------------

        hint = self.font_small.render(
            "Press E to Undock",
            True,
            TECHNO_GREEN_DIM,
        )

        hint_rect = hint.get_rect()

        hint_rect.centerx = screen_width // 2
        hint_rect.bottom = screen_height - 30

        screen.blit(
            hint,
            hint_rect
        )