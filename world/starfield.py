import random
import pygame

from core.settings import WIDTH, HEIGHT


class Starfield:

    def __init__(self, sector_manager):

        self.layers = sector_manager.starfield

        for layer in self.layers:

            for _ in range(layer["count"]):

                layer["stars"].append(
                    pygame.Vector2(
                        random.uniform(0, WIDTH),
                        random.uniform(0, HEIGHT),
                    )
                )

    def draw(self, screen, camera):

        for layer in self.layers:

            speed = layer["speed"]
            color = layer["color"]
            size = layer["size"]

            offset_x = (camera.x * speed) % WIDTH
            offset_y = (camera.y * speed) % HEIGHT

            for star in layer["stars"]:

                x = (star.x - offset_x) % WIDTH
                y = (star.y - offset_y) % HEIGHT

                pygame.draw.circle(
                    screen,
                    color,
                    (int(x), int(y)),
                    size,
                )