import pygame

from core.settings import TECHNO_GREEN


class DockPrompt:

    def __init__(self):

        self.font = pygame.font.SysFont(
            None,
            28
        )


    def draw(
        self,
        screen,
        hub_name,
        screen_width,
        screen_height,
    ):

        text = self.font.render(
            f"Press E to Dock - {hub_name}",
            True,
            TECHNO_GREEN,
        )

        rect = text.get_rect()

        rect.centerx = screen_width // 2
        rect.bottom = screen_height - 40

        screen.blit(
            text,
            rect
        )