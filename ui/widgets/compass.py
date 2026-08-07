import math
import pygame


class Compass:

    def __init__(self):

        self.size = 12

    def draw(
        self,
        screen,
        center,
        player_position,
        target_position,
    ):

        direction = target_position - player_position

        if direction.length_squared() == 0:
            return

        angle = math.atan2(direction.y, direction.x)

        points = []

        for offset in (0, 140, -140):

            a = angle + math.radians(offset)

            points.append(
                center
                + pygame.Vector2(
                    math.cos(a),
                    math.sin(a),
                )
                * self.size
            )

        pygame.draw.polygon(
            screen,
            (255, 255, 255),
            points,
            2,
        )
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            center,
            self.size + 4,
            2,
        )