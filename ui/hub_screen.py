import pygame

from core.settings import (
    TECHNO_GREEN,
    TECHNO_GREEN_DIM,
    TECHNO_GREEN_DARK,
    PART_RARITY_COLORS,
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
        upgrades,
        advanced,
        part_counts,
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

        y = 205

        for index, upgrade in enumerate(upgrades):

            number = index + 1

            if upgrade["maxed"]:

                status = "MAXED"

                affordable = False

            else:

                status = f"{upgrade['cost']}cr"

                affordable = credits >= upgrade["cost"]

            color = (
                TECHNO_GREEN
                if affordable
                else TECHNO_GREEN_DIM
            )

            line = self.font_small.render(
                f"[{number}] {upgrade['label']}  "
                f"Lv {upgrade['level']}/{upgrade['max_level']}  "
                f"{status}",
                True,
                color,
            )

            screen.blit(
                line,
                (80, y)
            )

            y += 32

        hint = self.font_small.render(
            "1/2/3 = Upgrades   4+ = Advanced",
            True,
            TECHNO_GREEN_DIM,
        )

        screen.blit(
            hint,
            (60, 420)
        )

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

        y = 205

        for index, entry in enumerate(advanced):

            number = len(upgrades) + index + 1

            currency = entry["currency"]

            available = part_counts.get(
                currency,
                0,
            )

            currency_color = PART_RARITY_COLORS.get(
                currency,
                TECHNO_GREEN,
            )

            if entry["maxed"]:

                status = "MAXED"

                affordable = False

            else:

                status = f"{entry['cost']} {currency}"

                affordable = available >= entry["cost"]

            color = (
                currency_color
                if affordable
                else TECHNO_GREEN_DIM
            )

            line = self.font_small.render(
                f"[{number}] {entry['label']}  "
                f"Lv {entry['level']}/{entry['max_level']}  "
                f"{status}",
                True,
                color,
            )

            screen.blit(
                line,
                (420, y)
            )

            y += 32

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