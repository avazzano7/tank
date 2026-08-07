import pygame


class ShipHub:

    def __init__(self, x, y, name):

        self.position = pygame.Vector2(
            x,
            y
        )

        self.radius = 50

        self.name = name


    def draw(self, screen, camera):

        screen_position = (
            self.position - camera
        )


        pygame.draw.circle(
            screen,
            (255,255,255),
            screen_position,
            self.radius,
            2
        )


        font = pygame.font.SysFont(
            None,
            20
        )


        label = font.render(
            self.name,
            True,
            (255,255,255)
        )


        screen.blit(
            label,
            (
                screen_position.x - 30,
                screen_position.y - 70
            )
        )