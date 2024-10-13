# Shantanu Barua, S377141

import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

### Music ###
pygame.mixer.music.load('music.mp3')  # Load background music file
pygame.mixer.music.play(-1)  # Play indefinitely
pygame.mixer.music.set_volume(0.5)  # Adjust volume to 50%


### Basic game setup ###

# Game Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Battlefield")

clock = pygame.time.Clock()

# Game Variables
score = 0 # Initial variables
lives = 2
level = 1
running = True
boss_tank_spawned = False  # Track the boss has been spawned in Level 3

# Tank, projectile, enemy tank

player_image = pygame.Surface((50, 30))  # Tank, initial fill, later image was put
player_image.fill((0, 255, 0))

projectile_image = pygame.Surface((10, 5)) # Canon projectiles
projectile_image.fill((255, 0, 0))

enemy_image = pygame.Surface((50, 30))  # Enemy tank, initial fill, later image was put
enemy_image.fill((255, 0, 0))

# Set the font for text
font = pygame.font.SysFont('Arial', 24)


#  Health bar function
max_health = 100
current_health = 100 # Initial

def draw_health_bar(screen, x, y, current_health, max_health):

    bar_width = 40  # The total width of the health bar
    bar_height = 20  # The height of the health bar
    health_ratio = current_health / max_health

    # Colors of Health bar
    health_color = (255, 0, 0)  # Red for health bar
    background_color = (100, 100, 100)  # Grey for background

    # Draw the background bar (the empty part)
    pygame.draw.rect(screen, background_color, (x, y, bar_width, bar_height))

    # Draw the filled health bar (based on the current health)
    pygame.draw.rect(screen, health_color, (x, y, bar_width * health_ratio, bar_height))

def game_over_screen():
    screen.fill(color='red')
    text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))

    # Create Restart Button
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 400, 50)  # Button dimensions
    pygame.draw.rect(screen, (200, 0, 0), restart_button)  # Draw button 
    button_text = font.render("Press Button R to  Restart", True, (255, 255, 255))  # Text on the button
    screen.blit(button_text, (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 + 60))  # Position text on the button
    pygame.display.flip()
    # pygame.time.wait(10000)  # To wait 10 seconds before closing

    # Wait for user input to restart the game
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # If the player presses 'R', restart the game
                    waiting = False
                    reopen_application()
                    

def victory_screen():
    screen.fill(color='green')
    text = font.render("Game over!!! YOU WIN!", True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
    
    # Create Restart Button
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 400, 50)  # Button dimensions
    pygame.draw.rect(screen, (0, 200, 0), restart_button)  # Draw button 
    button_text = font.render("Press Button R to  Restart", True, (255, 255, 255))  # Text on the button
    screen.blit(button_text, (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 + 60))  # Position text on the button
    pygame.display.flip()
    # pygame.time.wait(10000)  # To wait 10 seconds before closing

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # If the player presses 'R', restart the game
                    waiting = False
                    reopen_application()

def reopen_application():
    
    os.execl(sys.executable, sys.executable, 'ans2.py')

### Create projectile class ###

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = projectile_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 7

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIDTH:
            self.kill()  # Remove projectile when it goes off-screen


### Create player class ###

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 128, 255))
        self.image = pygame.image.load('plyr.jpg').convert_alpha() # Load blue tank image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 100
        self.speed = 5
        self.jump_speed = 30
        self.is_jumping = False
        self.health = 100
        self.lives = 2
        self.invincible = False  # Track if player is invincible after hit
        self.invincible_timer = 0  # Timer for invincibility frames

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT]: # Move left
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT]: # Move right
            self.rect.x += self.speed
        if keys_pressed[pygame.K_SPACE] and not self.is_jumping: # Player Jump
            self.is_jumping = True
            self.jump()
        if keys_pressed[pygame.K_UP]:  # Move up
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_DOWN]:  # Move down
            self.rect.y += self.speed
        
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False  # Turn off invincibility when timer runs out

        # Keep player on screen
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width

    def jump(self):
        if self.is_jumping:
            self.rect.y -= self.jump_speed
            self.jump_speed -= 1
            if self.jump_speed < -10:
                self.is_jumping = False
                self.jump_speed = 10

    def shoot(self):
        return Projectile(self.rect.right, self.rect.centery)

    def take_damage(self, damage):
        if not self.invincible:
            self.health -= damage  # Reduce player health
            if self.health <= 0:
                self.lives -= 1  # Reduce player lives if health is 0
                if self.lives > 0:
                    self.health = 100  # Restore health if player still has lives
            self.invincible = True  # Activate invincibility frames
            self.invincible_timer = 60  # Invincible for 60 frames (1 second if running at 60 FPS) at new life
    

### Create enemy class ###


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))  # Create a surface for the enemy
        self.image.fill((255, 0, 0))  # Fill the enemy surface with red color (RGB)
        self.image = pygame.image.load('enemy.jpg').convert_alpha() # Load red tank image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3
        self.health = 50

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.kill()

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True  # Enemy killed
        return False  # Enemy still alive
    
def spawn_enemy():
    x = SCREEN_WIDTH + 50  # Start just off the right edge of the screen
    y = random.randint(50, SCREEN_HEIGHT - 50)  # Random y position within the screen bounds
    enemy = Enemy(x, y)
    enemies.add(enemy)  # Add the enemy to the enemies group

### Boss Tank for Level 3 ###

def spawn_boss():
    x = SCREEN_WIDTH - 50  # Start just off the right edge of the screen
    y = random.randint(50, SCREEN_HEIGHT - 50)  # Random y position within the screen bounds
    boss = BossTank(x, y)
    boss_tank_group.add(boss)


class BossTank(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 60))  # Large size for the boss tank
        self.image.fill((128, 0, 0))  # Dark red initial fill color for the boss
        self.image = pygame.image.load('bosstank.jpg').convert_alpha() # Big boss tank image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH - 150
        self.rect.y = SCREEN_HEIGHT // 2
        self.shoot_timer = 0  # Timer for shooting projectiles

    def update(self):
        self.shoot_timer += 1
        if self.shoot_timer >= 60:  # Shoot every 1 seconds (60 frames at 60 FPS)
            self.shoot_projectile()
            self.shoot_timer = 0

    def shoot_projectile(self):
        boss_projectile = Projectile(self.rect.x, self.rect.centery)
        boss_projectile.speed = -7  # Shoot projectiles to the left
        projectiles.add(boss_projectile)



class BossProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))  # Define the size of the projectile
        self.image.fill(color='gold')  # Color of the projectile
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7  # Speed of the projectile

    def update(self):
        self.rect.y += self.speed  # Boss projectiles move downwards
        if self.rect.y > screen.get_height():  # Remove if it goes off-screen
            self.kill()

BOSS_SHOOT_EVENT = pygame.USEREVENT + 1  # Custom event for boss shooting
pygame.time.set_timer(BOSS_SHOOT_EVENT, 1000)  # Boss fires every 1 seconds

boss_shoot_timer = 1000  # Time interval in milliseconds for the boss to shoot (1 second)

boss_projectiles = pygame.sprite.Group()  # Group to store all boss projectiles


### Loot class ###


class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, collectible_type):
        super().__init__()
        self.image = pygame.Surface((30, 30))  # Create a surface for the collectible
        if collectible_type == "health":
            self.image.fill((0, 255, 0))  # Green color for health collectible
        elif collectible_type == "extra_life":
            self.image.fill((0, 0, 255))  # Blue color for extra life collectible
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collectible_type = collectible_type

    def update(self):
        # Optional: Add movement or behavior (e.g., falling downwards or scrolling left)
        self.rect.x -= 3  # Move left with the environment
        if self.rect.x < 0:  # Remove collectible when it goes off-screen
            self.kill()

def spawn_collectible():
    x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 100)  # Start just off the right side of the screen
    y = random.randint(50, SCREEN_HEIGHT - 50)  # Random y position within screen height
    collectible_type = random.choice(["health", "extra_life"])  # Random type of collectible
    collectible = Collectible(x, y, collectible_type)
    collectibles.add(collectible)  # Add to the collectibles group

SPAWN_COLLECTIBLE = pygame.USEREVENT + 2  # Custom event for collectible spawn
pygame.time.set_timer(SPAWN_COLLECTIBLE, 5000)  # Spawn collectible every 5 seconds


### Scoring and health ###

# Sprite groups
player = Player()
player_group = pygame.sprite.Group(player) # Group player
projectiles = pygame.sprite.Group() # Group for projectiles
enemies = pygame.sprite.Group() # Group for enemy tanks
collectibles = pygame.sprite.Group() # Group for collectibles
boss_tank_group = pygame.sprite.GroupSingle()  # Group for the boss tank
boss_projectiles = pygame.sprite.Group()  # Group for boss projectiles

def create_enemy():
    return Enemy(random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 100), random.randint(100, SCREEN_HEIGHT - 50))

for _ in range(5):
    enemies.add(create_enemy())

### Set game in loop ###

SPAWN_ENEMY = pygame.USEREVENT + 1  # Custom event for enemy spawn
pygame.time.set_timer(SPAWN_ENEMY, 2000)  # Spawn enemy every 2 seconds

SPAWN_BOSS = pygame.USEREVENT

def game_loop():
    global score, running, boss_tank_spawned, level # Declare global variables used in this function

    while running:
      
        screen.fill(WHITE)
        keys_pressed = pygame.key.get_pressed() # Get key input for the player

        ### Check level and adjust behavior ###
        if 0 <= score <= 90:
            level = 1
        elif 100 <= score <= 190:
            level = 2
        elif 200 <= score <= 300: # Testing 201 <= score <= 300
            level = 3
            if not boss_tank_spawned:
                boss_tank = BossTank()
                boss_tank_group.add(boss_tank)
                boss_tank_spawned = True
                pygame.time.set_timer(BOSS_SHOOT_EVENT, boss_shoot_timer)  # Set timer for boss shooting
            # Speed up enemies and change their appearance in level 3
            for enemy in enemies:
                enemy.speed = 5  # Speed up enemy
                enemy.image = pygame.image.load('bomb.jpg').convert_alpha() # replace red tank image with missile
            hitbomb = font.render(f"Hit the bombs! Boss does not take damage!", True, (0, 0, 0))  # level 3 info
            screen.blit(hitbomb, (200, 30))  # Mid top

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Fire projectile key "s"
                    projectiles.add(player.shoot())
            elif event.type == SPAWN_ENEMY and score < 300 and player.lives > 0:
                spawn_enemy()  # Spawn an enemy
            elif event.type == SPAWN_COLLECTIBLE:
                spawn_collectible()  # Spawn collectible
            elif event.type == BOSS_SHOOT_EVENT and level == 3 and boss_tank_spawned:
                # Make the boss fire a projectile
                boss_projectile = BossProjectile(boss_tank.rect.centerx, boss_tank.rect.bottom)
                boss_projectiles.add(boss_projectile)  # Add to projectile group


        # Draw health bar
        draw_health_bar(screen, 75, 45, player.health, max_health)

        # Update all sprites
        player_group.update(keys_pressed)
        projectiles.update()
        enemies.update()
        collectibles.update()
        boss_tank_group.update()
        boss_projectiles.update()  # Update boss projectiles


        # Check for collision between player and collectibles
        collectible_hit = pygame.sprite.spritecollideany(player, collectibles)
        if collectible_hit:
            if collectible_hit.collectible_type == "health":
                player.health = min(player.health + 25, 100)  # Boost health, cap at 100
            elif collectible_hit.collectible_type == "extra_life":
                player.lives += 1  # Add an extra life
            collectible_hit.kill()  # Remove the collectible after collection

        # Check for collisions
        for projectile in projectiles:
            enemy_hit = pygame.sprite.spritecollideany(projectile, enemies)
            if enemy_hit:
                if enemy_hit.take_damage(25):
                    score += 10  # Increase score for defeating an enemy
                projectile.kill()
        
        # Check for collisions between player and boss projectiles
        boss_proj_hit = pygame.sprite.spritecollideany(player, boss_projectiles)
        if boss_proj_hit:
            player.take_damage(50)  # Deal half damage to the player
            boss_proj_hit.kill()  # Remove the projectile after hitting the player
        
        # Check for collisions between player and enemies
        enemy_hit = pygame.sprite.spritecollideany(player, enemies)
        if enemy_hit:
            player.take_damage(50)  # Deal 50 damage to player on collision

        # Check if player dies or reaches the score limit
        if player.lives <= 0:
            running = False  # Player is dead, stop the game
            game_over_screen()  # Show Game Over screen
        elif score >= 300:
            running = False  # Player wins, stop the game
            victory_screen()  # Show Victory screen


        # Draw all sprites
        player_group.draw(screen) # Draw player
        projectiles.draw(screen) # Draw projectile
        enemies.draw(screen) # Draw lenemy
        collectibles.draw(screen) # Draw loot
        boss_tank_group.draw(screen)   # Draw boss 
        boss_projectiles.draw(screen)  # Draw boss projectiles

        # Display score and lives
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        health_text = font.render(f"Health: {player.health}", True, (0, 0, 0))
        screen.blit(health_text, (10, 40))
        lives_text = font.render(f"Lives: {player.lives}", True, (0, 0, 0))
        screen.blit(lives_text, (10, 70))

        # Display score, health, lives, info and level 
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))  # Position at the top-left corner

        health_text = font.render(f"Health: {player.health}", True, (0, 0, 0))
        screen.blit(health_text, (10, 40))  # Below score

        lives_text = font.render(f"Lives: {player.lives}", True, (0, 0, 0))
        screen.blit(lives_text, (10, 70))  # Below health

        level_text = font.render(f"Level: {level}", True, (0, 0, 0))  # Display level at the top
        screen.blit(level_text, (10, 100))  # Below lives

        control1 = font.render(f"Press S to shoot", True, (0, 0, 0))  # Control info
        screen.blit(control1, (600, 10))  # Right top

        control2 = font.render(f"Arrows to move", True, (0, 0, 0))  # Control info
        screen.blit(control2, (600, 30))  # Right top

        control3 = font.render(f"Space to jump", True, (0, 0, 0))  # Control info
        screen.blit(control3, (600, 50))  # Right top

        bossi = font.render(f"Boss at level 3, Blue box for Life, Green box for HP", True, (0, 0, 0))  # Boss and loot info
        screen.blit(bossi, (10, 570))  # Right top

        # Refresh display
        pygame.display.flip()
        clock.tick(FPS)

# Start the game loop
game_loop()

pygame.quit()

# https://github.com/Shantanu-Barua/hit137_assignment3.git