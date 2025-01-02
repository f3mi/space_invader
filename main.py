import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 5
ENEMY_SPEED = 2
BULLET_SPEED = 7
ENEMY_DROP_SPEED = 10
MAX_ENEMIES = 6

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images
player_img = pygame.image.load('img/player.png')  # Make sure you have this image or replace it with your own
player_img = pygame.transform.scale(player_img, (50, 50))

enemy_img = pygame.image.load('img/enemy.png')  # Make sure you have this image or replace it with your own
enemy_img = pygame.transform.scale(enemy_img, (50, 50))

bullet_img = pygame.image.load('img/bullet.png')  # Make sure you have this image or replace it with your own
bullet_img = pygame.transform.scale(bullet_img, (5, 10))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)

    def update(self, *args, **kwargs):  # Accept additional arguments
        keys = pygame.key.get_pressed()  # Check for key presses
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED

    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 50)
        self.rect.y = random.randint(50, 150)
        self.direction = random.choice([-1, 1])

    def update(self):
        self.rect.x += self.direction * ENEMY_SPEED
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1
            self.rect.y += ENEMY_DROP_SPEED

# Initialize sprites and groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Create enemies
for _ in range(MAX_ENEMIES):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Game loop
score = 0
running = True
while running:
    # Ensure game runs at the correct speed
    pygame.time.Clock().tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()

    # Update game objects
    keys = pygame.key.get_pressed()  # Get all key states
    player.update(keys)  # Pass the keys to the Player update method
    all_sprites.update()

    # Check for collisions
    for bullet in bullets:
        enemy_hits = pygame.sprite.spritecollide(bullet, enemies, True)
        if enemy_hits:
            bullet.kill()
            score += 1
            for enemy in enemy_hits:
                new_enemy = Enemy()
                all_sprites.add(new_enemy)
                enemies.add(new_enemy)

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Display score
    font = pygame.font.SysFont("Arial", 30)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
