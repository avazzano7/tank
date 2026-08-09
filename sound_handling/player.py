import pygame

# Load sound files (and set volume)
fire_sound = pygame.mixer.Sound("assets/sounds/player/fire.wav")
fire_sound.set_volume(0.1)

thrust_sound = pygame.mixer.Sound("assets/sounds/player/thrust.wav")
thrust_sound.set_volume(1.0)

hit_sound = pygame.mixer.Sound("assets/sounds/player/hit.wav")
hit_sound.set_volume(0.8)

death_sound = pygame.mixer.Sound("assets/sounds/player/death.wav")
death_sound.set_volume(1.0)