import math

import pygame


class Enemy:

    # ==================================================
    # ENEMY CONFIGURATION
    # ==================================================

    CONFIGS = {

        "hunter": {

            "max_health": 100,

            "radius": 28,

            "speed": 140,

            "acceleration": 80,

            "max_speed": 140,

            "contact_damage": 20,

            "turn_speed": 3.0,

        },

    }


    # ==================================================
    # INITIALIZATION
    # ==================================================

    def __init__(
        self,
        position,
        enemy_type,
    ):

        if enemy_type not in self.CONFIGS:

            raise ValueError(
                f"Unknown enemy type: {enemy_type}"
            )

        config = self.CONFIGS[
            enemy_type
        ]

        self.enemy_type = enemy_type

        # --------------------------------------------------
        # Position / movement
        # --------------------------------------------------

        self.position = pygame.Vector2(
            position
        )

        self.velocity = pygame.Vector2(
            0,
            0
        )

        # Angle is stored in radians.
        self.angle = 0.0

        # --------------------------------------------------
        # Combat
        # --------------------------------------------------

        self.max_health = config[
            "max_health"
        ]

        self.health = self.max_health

        self.radius = config[
            "radius"
        ]

        self.contact_damage = config[
            "contact_damage"
        ]

        # --------------------------------------------------
        # Movement configuration
        # --------------------------------------------------

        self.speed = config[
            "speed"
        ]

        self.acceleration = config[
            "acceleration"
        ]

        self.max_speed = config[
            "max_speed"
        ]

        self.turn_speed = config[
            "turn_speed"
        ]

        # --------------------------------------------------
        # Target
        # --------------------------------------------------

        self.target = None


    # ==================================================
    # UPDATE
    # ==================================================

    def update(
        self,
        dt,
        player,
    ):

        self.target = player

        if self.enemy_type == "hunter":

            self._update_hunter(
                dt
            )

        # Move
        self.position += (
            self.velocity * dt
        )


    # ==================================================
    # HUNTER
    # ==================================================

    def _update_hunter(
        self,
        dt,
    ):

        if self.target is None:

            return

        direction = (
            self.target.position
            - self.position
        )

        if direction.length_squared() == 0:

            return

        direction = direction.normalize()

        # ----------------------------------------------
        # Determine target angle
        # ----------------------------------------------

        target_angle = math.atan2(
            direction.y,
            direction.x
        )

        # ----------------------------------------------
        # Smoothly rotate toward player
        # ----------------------------------------------

        angle_difference = (
            target_angle
            - self.angle
        )

        # Normalize angle difference to [-pi, pi]

        angle_difference = (
            angle_difference + math.pi
        ) % (
            math.pi * 2
        ) - math.pi

        max_rotation = (
            self.turn_speed * dt
        )

        if abs(angle_difference) <= max_rotation:

            self.angle = target_angle

        elif angle_difference > 0:

            self.angle += max_rotation

        else:

            self.angle -= max_rotation

        # ----------------------------------------------
        # Accelerate toward facing direction
        # ----------------------------------------------

        forward = pygame.Vector2(
            math.cos(self.angle),
            math.sin(self.angle)
        )

        self.velocity += (
            forward
            * self.acceleration
            * dt
        )

        # ----------------------------------------------
        # Clamp speed
        # ----------------------------------------------

        if self.velocity.length() > self.max_speed:

            self.velocity.scale_to_length(
                self.max_speed
            )


    # ==================================================
    # DAMAGE
    # ==================================================

    def take_damage(
        self,
        damage,
    ):

        self.health -= damage

        if self.health < 0:

            self.health = 0

        return self.health <= 0


    # ==================================================
    # ALIVE
    # ==================================================

    def is_alive(self):

        return self.health > 0


    # ==================================================
    # DRAW
    # ==================================================

    def draw(
        self,
        screen,
        camera,
    ):

        screen_position = (
            self.position
            - camera
        )

        # ----------------------------------------------
        # Enemy body
        # ----------------------------------------------

        forward = pygame.Vector2(
            math.cos(self.angle),
            math.sin(self.angle)
        )

        right = pygame.Vector2(
            -forward.y,
            forward.x
        )

        nose = (
            screen_position
            + forward * self.radius
        )

        left = (
            screen_position
            - forward * self.radius * 0.7
            + right * self.radius * 0.75
        )

        right_point = (
            screen_position
            - forward * self.radius * 0.7
            - right * self.radius * 0.75
        )

        pygame.draw.polygon(
            screen,
            (180, 40, 40),
            [
                nose,
                left,
                right_point,
            ]
        )

        # ----------------------------------------------
        # Inner body
        # ----------------------------------------------

        pygame.draw.circle(
            screen,
            (100, 20, 20),
            (
                int(screen_position.x),
                int(screen_position.y),
            ),
            max(
                4,
                int(self.radius * 0.35)
            )
        )

        # ----------------------------------------------
        # Health bar
        # ----------------------------------------------

        bar_width = self.radius * 2

        bar_height = 5

        bar_x = (
            screen_position.x
            - bar_width / 2
        )

        bar_y = (
            screen_position.y
            - self.radius
            - 12
        )

        pygame.draw.rect(
            screen,
            (40, 40, 40),
            (
                int(bar_x),
                int(bar_y),
                int(bar_width),
                bar_height,
            )
        )

        health_width = (
            bar_width
            * (
                self.health
                / self.max_health
            )
        )

        pygame.draw.rect(
            screen,
            (220, 50, 50),
            (
                int(bar_x),
                int(bar_y),
                int(health_width),
                bar_height,
            )
        )