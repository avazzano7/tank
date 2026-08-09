import pygame

from core.settings import (
    TECHNO_GREEN,
    TECHNO_GREEN_DIM,
    TECHNO_GREEN_DARK,
    PART_RARITY_COLORS,
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
        parts,
        screen_width,
        screen_height,
    ):

        panel_width = 360
        panel_height = 320

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

        parts_label = self.font_small.render(
            "Ship Parts",
            True,
            TECHNO_GREEN,
        )

        screen.blit(
            parts_label,
            (panel_x + 20, panel_y + 100)
        )

        counts = {
            "common": 0,
            "uncommon": 0,
            "rare": 0,
        }

        for part in parts:

            rarity = part.get("rarity", "common")

            counts[rarity] = counts.get(rarity, 0) + 1

        y = panel_y + 130

        for rarity in ("common", "uncommon", "rare"):

            color = PART_RARITY_COLORS.get(
                rarity,
                TECHNO_GREEN_DIM,
            )

            line = self.font_small.render(
                f"{rarity.capitalize()}: {counts[rarity]}",
                True,
                color,
            )

            screen.blit(
                line,
                (panel_x + 20, y)
            )

            y += 28

        hint_text = self.font_small.render(
            "Press I to close",
            True,
            TECHNO_GREEN_DIM,
        )

        screen.blit(
            hint_text,
            (panel_x + 20, panel_y + panel_height - 36)
        )