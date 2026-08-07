import random
import math

from entities.hub import ShipHub


class HubManager:

    def __init__(self, sector_manager):

        self.sector_manager = sector_manager

        self.hubs = []

        self.generate_hubs()


    # ==================================================
    # GENERATE HUBS
    # ==================================================

    def generate_hubs(self):

        self.hubs.clear()

        # --------------------------------------------------
        # Current sector configuration
        # --------------------------------------------------

        sector_radius = (
            self.sector_manager.radius
        )

        outpost_count = (
            self.sector_manager.outpost_count
        )


        # --------------------------------------------------
        # Main hub at origin
        # --------------------------------------------------

        self.hubs.append(
            ShipHub(
                0,
                0,
                "Main Hub"
            )
        )


        # --------------------------------------------------
        # Generate outposts
        # --------------------------------------------------

        # Use a fresh random generator so that different
        # sectors get different hub layouts.

        rng = random.Random()


        for i in range(outpost_count):

            angle = rng.uniform(
                0,
                math.pi * 2
            )


            # Keep outposts away from the center and
            # slightly inside the sector boundary.

            minimum_distance = 2000

            maximum_distance = (
                sector_radius - 1000
            )


            if maximum_distance <= minimum_distance:

                distance = maximum_distance

            else:

                distance = rng.uniform(
                    minimum_distance,
                    maximum_distance
                )


            x = (
                math.cos(angle)
                * distance
            )

            y = (
                math.sin(angle)
                * distance
            )


            self.hubs.append(
                ShipHub(
                    x,
                    y,
                    f"Outpost {i + 1}"
                )
            )


    # ==================================================
    # GET NEAREST HUB
    # ==================================================

    def get_nearest_hub(
        self,
        position
    ):

        nearest = None

        nearest_distance = float(
            "inf"
        )


        for hub in self.hubs:

            distance = (
                position.distance_to(
                    hub.position
                )
            )


            if distance < nearest_distance:

                nearest = hub

                nearest_distance = distance


        return (
            nearest,
            nearest_distance
        )


    # ==================================================
    # DRAW
    # ==================================================

    def draw(
        self,
        screen,
        camera
    ):

        for hub in self.hubs:

            hub.draw(
                screen,
                camera
            )