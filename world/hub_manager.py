import random
import math

from entities.hub import ShipHub
from core.settings import SECTOR_RADIUS, OUTPOST_COUNT


class HubManager:

    def __init__(self):

        random.seed(12345)


        self.hubs = []


        # Main hub at origin

        self.hubs.append(
            ShipHub(
                0,
                0,
                "Main Hub"
            )
        )


        # Generate outposts inside sector circle

        for i in range(OUTPOST_COUNT):

            angle = random.uniform(
                0,
                math.pi * 2
            )


            distance = random.randint(
                2000,
                SECTOR_RADIUS - 1000
            )


            x = math.cos(angle) * distance

            y = math.sin(angle) * distance


            self.hubs.append(
                ShipHub(
                    x,
                    y,
                    f"Outpost {i+1}"
                )
            )



    def get_nearest_hub(self, position):

        nearest = None

        nearest_distance = float("inf")


        for hub in self.hubs:

            distance = position.distance_to(
                hub.position
            )


            if distance < nearest_distance:

                nearest = hub

                nearest_distance = distance


        return nearest, nearest_distance



    def draw(self, screen, camera):

        for hub in self.hubs:

            hub.draw(
                screen,
                camera
            )