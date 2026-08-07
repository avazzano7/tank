import pygame


class ProgressBar:

    def __init__(
        self,
        width,
        height,
        fill_color=(255, 255, 255),
        border_color=(180, 180, 180),
        background_color=(40, 40, 40),
    ):
        self.width = width
        self.height = height
        self.fill_color = fill_color
        self.border_color = border_color
        self.background_color = background_color

    def draw(self, screen, x, y, percent):

        percent = max(0.0, min(1.0, percent))

        rect = pygame.Rect(x, y, self.width, self.height)

        pygame.draw.rect(screen, self.background_color, rect)

        fill = pygame.Rect(
            x,
            y,
            int(self.width * percent),
            self.height,
        )

        pygame.draw.rect(screen, self.fill_color, fill)

        pygame.draw.rect(screen, self.border_color, rect, 2)