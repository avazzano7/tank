import sys
import pygame
import random
import time  # Import the time module for bullet delay
rotation_angle = 0

tank = "challenger"
# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
TANK_WIDTH, TANK_HEIGHT = 100, 100
TANK_SPEED = 5
BULLET_SPEED = 10
BULLET_WIDTH, BULLET_HEIGHT = 5, 20
if tank == "ChatGpt1":
    BULLET_WIDTH, BULLET_HEIGHT = 10, 20
MACHINEGUN_BULLET_SPEED = 20
MACHINEGUN_BULLET_WIDTH, MACHINEGUN_BULLET_HEIGHT = 3, 10
MACHINEGUN_SHOT_DELAY = 0.01  # Adjust the delay between machine gun shots
KNOCKBACK_DISTANCE = 10

ENEMY_WIDTH, ENEMY_HEIGHT = 100, 100
ENEMY_COLOR = (0, 0, 0)
ENEMY_SPAWN_INTERVAL = 2000
ENEMY_SPEED = 0.5
ENEMY_HEALTH = 100
enemies = []
enemies_health = []
boss = 'no'
x_offshift = 0
y_offshift = 0

BULLET_DAMAGE = 34
MACHINEGUN_BULLET_DAMAGE = 2

# load enemy image
enemy_img = pygame.image.load(f"C:/Users/ajvaz/Documents/{tank}_tank.png")
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
enemy_img = pygame.transform.rotate(enemy_img, 180)

# load explosion images
red_explosion_img_1 = pygame.image.load(f"C:/Users/ajvaz/Documents/tank_explosion.png")
red_explosion_img_1 = pygame.transform.scale(red_explosion_img_1, (ENEMY_WIDTH, ENEMY_HEIGHT))
red_explosion_img_2 = pygame.image.load(f"C:/Users/ajvaz/Documents/tank_explosion_2.png")
red_explosion_img_2 = pygame.transform.scale(red_explosion_img_2, (ENEMY_WIDTH, ENEMY_HEIGHT))
red_explosion_img_3 = pygame.image.load(f"C:/Users/ajvaz/Documents/tank_explosion_3.png")
red_explosion_img_3 = pygame.transform.scale(red_explosion_img_3, (ENEMY_WIDTH, ENEMY_HEIGHT))

blue_explosion_img_1 = pygame.image.load(f"C:/Users/ajvaz/Documents/boss_explosion_1.png")
blue_explosion_img_1 = pygame.transform.scale(blue_explosion_img_1, (ENEMY_WIDTH, ENEMY_HEIGHT))
blue_explosion_img_2 = pygame.image.load(f"C:/Users/ajvaz/Documents/boss_explosion_2.png")
blue_explosion_img_2 = pygame.transform.scale(blue_explosion_img_2, (ENEMY_WIDTH, ENEMY_HEIGHT))
blue_explosion_img_3 = pygame.image.load(f"C:/Users/ajvaz/Documents/boss_explosion_3.png")
blue_explosion_img_3 = pygame.transform.scale(blue_explosion_img_3, (ENEMY_WIDTH, ENEMY_HEIGHT))     

big_explosion_img_1 = pygame.image.load(f"C:/Users/ajvaz/Documents/big_explosion_1.png")
big_explosion_img_1 = pygame.transform.scale(big_explosion_img_1, (1400, 1000))
big_explosion_img_2 = pygame.image.load(f"C:/Users/ajvaz/Documents/big_explosion_2.png")
big_explosion_img_2 = pygame.transform.scale(big_explosion_img_2, (1400, 1000))
big_explosion_img_3 = pygame.image.load(f"C:/Users/ajvaz/Documents/big_explosion_3.png")
big_explosion_img_3 = pygame.transform.scale(big_explosion_img_3, (1400, 1000))     

explosion_img_1 = red_explosion_img_1
explosion_img_2 = red_explosion_img_2
explosion_img_3 = red_explosion_img_3


# create a function to spawn in enemies
def spawn_enemy():
    x = random.randint(0, WIDTH - ENEMY_WIDTH)
    y = 0
    enemy_rect = enemy_img.get_rect()
    enemy_rect.x = x
    enemy_rect.y = y
    enemy_health = ENEMY_HEALTH  # Set initial health
    enemies.append(enemy_rect)
    enemies_health.append(enemy_health)
    
# create a function to detect collision between bullets and enemies
def bullet_hits_enemy(bullet, enemy):
    bullet_x, bullet_y = bullet
    enemy_x, enemy_y = enemy.topleft  # Use .topleft to get the top-left corner coordinates of the enemy rectangle
    enemy_width, enemy_height = enemy.size  # Get the width and height of the enemy rectangle
    
    if (enemy_x < bullet_x < enemy_x + enemy_width) and (enemy_y < bullet_y < enemy_y + enemy_height):
        return True
    return False


def handle_bullet_enemy_collisions(bullet_list, damage):
    for bullet in bullet_list.copy():
        for enemy in enemies.copy():
            
            if bullet_hits_enemy(bullet, enemy):
                enemy_index = enemies.index(enemy)
                bullet_list.remove(bullet)
                enemies_health[enemy_index] -= damage
                if enemies_health[enemy_index] <= 0:
                    screen.blit(explosion_img_1, (enemies[enemy_index].x - x_offshift, enemies[enemy_index].y - y_offshift))
                    pygame.display.update()
                    screen.blit(explosion_img_1, (enemies[enemy_index].x - x_offshift, enemies[enemy_index].y - y_offshift))
                    pygame.display.update()                    
                    screen.blit(explosion_img_2, (enemies[enemy_index].x - x_offshift, enemies[enemy_index].y - y_offshift))
                    pygame.display.update()
                    screen.blit(explosion_img_2, (enemies[enemy_index].x - x_offshift, enemies[enemy_index].y - y_offshift))
                    pygame.display.update()                    
                    screen.blit(explosion_img_3, (enemies[enemy_index].x - x_offshift, enemies[enemy_index].y - y_offshift))
                    pygame.display.update()
                    screen.blit(explosion_img_3, (enemies[enemy_index].x - x_offshift, enemies[enemy_index].y - y_offshift))
                    pygame.display.update()                    
                    enemies.remove(enemies[enemy_index])
                    enemies_health.remove(enemies_health[enemy_index])
                break
                    
                    
# create a function to draw enemies
def draw_enemies():
    for enemy in enemies:
        screen.blit(tracks_img, (enemy.x, enemy.y - ENEMY_HEIGHT/5))
        screen.blit(enemy_img, (enemy.x, enemy.y))
        

# Colors
WHITE = (255, 255, 255)
TURQUOISE = (0, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

BULLET = RED

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Game")

# Load tank image
tank_img = pygame.image.load(f"C:/Users/ajvaz/Documents/{tank}_tank.png")
tank_img = pygame.transform.scale(tank_img, (TANK_WIDTH, TANK_HEIGHT))

# Load tracks image
tracks_img = pygame.image.load(f"C:/Users/ajvaz/Documents/tracks.png")
tracks_img = pygame.transform.scale(tracks_img, (TANK_WIDTH, TANK_HEIGHT))

# Load background image
background_img = pygame.image.load(f"C:/Users/ajvaz/Documents/snow_field.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Load bullet image
bullet_img = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
bullet_img.fill(BULLET)

# Load machine gun bullet image
machinegun_bullet_img = pygame.Surface((MACHINEGUN_BULLET_WIDTH, MACHINEGUN_BULLET_HEIGHT))
machinegun_bullet_img.fill(BULLET)

# Initial tank position
tank_x = (WIDTH - TANK_WIDTH) // 2
tank_y = HEIGHT - TANK_HEIGHT

# Create lists to store bullets
bullets = []
machinegun_bullets_left = []
machinegun_bullets_right = []
machinegun_shooting = False
machinegun_last_shot_time = 0  # Track the time of the last machine gun shot

# Timer variables
start_time = time.time()
game_time = 0  # Initialize game time to 0

# Font for displaying time
font = pygame.font.Font(None, 36)

# Game loop
running = True
last_enemy_spawn_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Fire a bullet when spacebar is pressed
                bullet_x = tank_x + (TANK_WIDTH - BULLET_WIDTH) // 2
                bullet_y = tank_y
                bullets.append([bullet_x, bullet_y])
               
                if tank_y - KNOCKBACK_DISTANCE < HEIGHT - TANK_HEIGHT - 20:
                    tank_y += KNOCKBACK_DISTANCE        
               

            if event.key == pygame.K_m:
                # Start machine gun shooting when "M" key is pressed
                machinegun_shooting = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_m:
                # Stop machine gun shooting when "M" key is released
                machinegun_shooting = False

    keys = pygame.key.get_pressed()

    # Calculate the new position
    new_x = tank_x
    new_y = tank_y
    old_x = tank_x
    old_y = tank_y
        
    if keys[pygame.K_LEFT]:
        new_x -= TANK_SPEED
    if keys[pygame.K_RIGHT]:
        new_x += TANK_SPEED
    if keys[pygame.K_UP]:
        new_y -= TANK_SPEED
    if keys[pygame.K_DOWN]:
        new_y += TANK_SPEED
       

    # Check boundaries
    if 0 <= new_x <= WIDTH - TANK_WIDTH:
        tank_x = new_x
    if 0 <= new_y <= HEIGHT - TANK_HEIGHT:
        tank_y = new_y
        
        
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time >= ENEMY_SPAWN_INTERVAL:
        spawn_enemy()
        last_enemy_spawn_time = current_time
        
    for enemy in enemies:
        if boss == 'yes':
            if int(game_time)%5 == 0:
                enemy.y += ENEMY_SPEED
                
                if tank_x > enemy.x:
                    enemy.x += ENEMY_SPEED
                else:
                    enemy.x -= ENEMY_SPEED*2
        else:
            enemy.y += ENEMY_SPEED
            
            if tank_x > enemy.x:
                enemy.x += ENEMY_SPEED
            else:
                enemy.x -= ENEMY_SPEED*2            
        
        handle_bullet_enemy_collisions(bullets, BULLET_DAMAGE)
        handle_bullet_enemy_collisions(machinegun_bullets_left, MACHINEGUN_BULLET_DAMAGE)
        handle_bullet_enemy_collisions(machinegun_bullets_right, MACHINEGUN_BULLET_DAMAGE)
    
        if enemy.y > HEIGHT:
            screen.fill(WHITE)
            pygame.display.update()
            time.sleep(5)
            sys.exit()

    # Clear the screen
    screen.fill(WHITE)
    screen.blit(background_img, (0, 0))
    
    # Draw the tracks
    if old_y > tank_y:
        screen.blit(tracks_img, (old_x, old_y+20))   
    if old_y < tank_y:
        screen.blit(tracks_img, (old_x, old_y-20))
    if old_x < tank_x:
        screen.blit(tracks_img, (old_x-10, old_y))
    if old_x > tank_x:
        screen.blit(tracks_img, (old_x+10, old_y))

    # Draw the tank
    screen.blit(tank_img, (tank_x, tank_y))
    
    # Draw the enemies
    draw_enemies()
    
    # Calculate the elapsed game time
    current_time = time.time()
    game_time = current_time - start_time
    if game_time > 180:
        ENEMY_SPEED = 0.5
        ENEMY_SPAWN_INTERVAL = 1000
        ENEMY_HEALTH = 100
        enemy_img = pygame.image.load(f"C:/Users/ajvaz/Documents/bomb_tank.png.")
        enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
        enemy_img = pygame.transform.rotate(enemy_img, 180)
        explosion_img_1 = big_explosion_img_1
        explosion_img_2 = big_explosion_img_2
        explosion_img_3 = big_explosion_img_3
        x_offshift = 650
        y_offshift = 400
        boss = 'no'  
    elif game_time > 150:
        ENEMY_SPEED = 2
        ENEMY_SPAWN_INTERVAL = 2000
        ENEMY_HEALTH = 500
        enemy_img = pygame.image.load(f"C:/Users/ajvaz/Documents/boss_tank_2.png.")
        enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
        enemy_img = pygame.transform.rotate(enemy_img, 180)
        boss = 'yes'   
    elif game_time > 120:
        ENEMY_SPEED = 2
        ENEMY_SPAWN_INTERVAL = 250
        ENEMY_HEALTH = 10
        enemy_img = pygame.image.load(f"C:/Users/ajvaz/Documents/level_4_tank.png.")
        enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
        enemy_img = pygame.transform.rotate(enemy_img, 180)  
        explosion_img_1 = blue_explosion_img_1
        explosion_img_2 = blue_explosion_img_2
        explosion_img_3 = blue_explosion_img_3                      
        boss = 'no'    
    elif game_time > 90:
        ENEMY_SPEED = 0.5
        ENEMY_SPAWN_INTERVAL = 1000
        ENEMY_HEALTH = 300
        enemy_img = pygame.image.load(f"C:/Users/ajvaz/Documents/level_3_tank.png.")
        enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
        enemy_img = pygame.transform.rotate(enemy_img, 180)
        boss = 'no'    
    elif game_time > 51:
        ENEMY_SPEED = 0.5
        ENEMY_SPAWN_INTERVAL = 10000
        ENEMY_HEALTH = 2000
        enemy_img = pygame.image.load(f"C:/Users/ajvaz/Documents/boss_tank_1.png.")
        enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
        enemy_img = pygame.transform.rotate(enemy_img, 180)
        boss = 'yes'
        explosion_img_1 = blue_explosion_img_1
        explosion_img_2 = blue_explosion_img_2
        explosion_img_3 = blue_explosion_img_3     
    elif game_time > 30:
        ENEMY_SPEED = 2
        ENEMY_HEALTH = 150
        ENEMY_SPAWN_INTERVAL = 1750
        enemy_img = pygame.image.load(f"C:/Users/ajvaz/Documents/level_2_tank.png")
        enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
        enemy_img = pygame.transform.rotate(enemy_img, 180)
        boss = 'no'

                                      
    # Render and display the game time in the top-left corner
    time_text = font.render(f"Time: {int(game_time)} seconds", True, BLACK)
    screen.blit(time_text, (10, 10))    

    # Update and draw bullets
    current_time = time.time()  # Get the current time
    for bullet in bullets:
        bullet[1] -= BULLET_SPEED
        pygame.draw.rect(screen, BULLET, (bullet[0], bullet[1], BULLET_WIDTH, BULLET_HEIGHT))

    # Update and draw machine gun bullets with a delay
    if machinegun_shooting and current_time - machinegun_last_shot_time >= MACHINEGUN_SHOT_DELAY:
        bullet_x_left = tank_x + (TANK_WIDTH - MACHINEGUN_BULLET_WIDTH) // 2 + 10
        bullet_y = tank_y
        machinegun_bullets_left.append([bullet_x_left, bullet_y])
       
        bullet_x_right = tank_x + (TANK_WIDTH - BULLET_WIDTH) // 2 - 8
        machinegun_bullets_right.append([bullet_x_right, bullet_y])
           
        machinegun_last_shot_time = current_time  # Update the last shot time

    for machinegun_bullet_left in machinegun_bullets_left:
        machinegun_bullet_left[1] -= MACHINEGUN_BULLET_SPEED
        pygame.draw.rect(screen, BULLET, (machinegun_bullet_left[0], machinegun_bullet_left[1], MACHINEGUN_BULLET_WIDTH, MACHINEGUN_BULLET_HEIGHT))
        
        if tank_y - KNOCKBACK_DISTANCE < HEIGHT - TANK_HEIGHT - 20:
            tank_y += KNOCKBACK_DISTANCE/1000

    for machinegun_bullet_right in machinegun_bullets_right:
        machinegun_bullet_right[1] -= MACHINEGUN_BULLET_SPEED
        pygame.draw.rect(screen, BULLET, (machinegun_bullet_right[0], machinegun_bullet_right[1], MACHINEGUN_BULLET_WIDTH, MACHINEGUN_BULLET_HEIGHT))

    # Remove bullets that are out of the screen
    bullets = [bullet for bullet in bullets if bullet[1] > 0]
    machinegun_bullets_right = [bullet for bullet in machinegun_bullets_right if bullet[1] > 0]
    machinegun_bullets_left = [bullet for bullet in machinegun_bullets_left if bullet[1] > 0]

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
