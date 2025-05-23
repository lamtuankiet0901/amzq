import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Clock for controlling game speed
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('laser_cannon.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0
        self.cooldown = 0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        
        self.rect.x += self.speed_x
        
        # Keep player on the screen
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
        # Cooldown for shooting
        if self.cooldown > 0:
            self.cooldown -= 1

    def shoot(self):
        if self.cooldown == 0:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.cooldown = 15

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('alien.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 1
        self.move_down = 0

    def update(self):
        self.rect.x += self.speed_x
        
        # Move down when reaching screen edge
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.speed_x *= -1
            self.rect.y += 20
            
        # Random chance to shoot
        if random.random() < 0.001:
            alien_bullet = AlienBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(alien_bullet)
            alien_bullets.add(alien_bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        # Kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed_y = 7

    def update(self):
        self.rect.y += self.speed_y
        # Kill if it moves off the bottom of the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Function to create a new wave of aliens
def create_aliens():
    aliens.empty()
    for row in range(5):
        for column in range(10):
            alien = Alien(column * 70 + 50, row * 50 + 50)
            aliens.add(alien)
            all_sprites.add(alien)

# Game variables
score = 0
lives = 3
game_over = False
font = pygame.font.SysFont(None, 36)

# Sprite groups
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()
alien_bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create initial aliens
create_aliens()

# Game loop
running = True
while running:
    # Keep loop running at the right speed
    clock.tick(60)
    
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_r and game_over:
                # Reset game
                game_over = False
                score = 0
                lives = 3
                create_aliens()
                player.rect.centerx = SCREEN_WIDTH // 2
    
    if not game_over:
        # Update
        all_sprites.update()
        
        # Check for bullet-alien collisions
        hits = pygame.sprite.groupcollide(bullets, aliens, True, True)
        for hit in hits:
            score += 10
        
        # Check for alien-player collisions
        if pygame.sprite.spritecollide(player, aliens, True):
            lives -= 1
            if lives <= 0:
                game_over = True
        
        # Check for alien bullet-player collisions
        if pygame.sprite.spritecollide(player, alien_bullets, True):
            lives -= 1
            if lives <= 0:
                game_over = True
        
        # Check if all aliens are gone
        if len(aliens) == 0:
            create_aliens()
        
        # Check if aliens reached the bottom
        for alien in aliens:
            if alien.rect.bottom > SCREEN_HEIGHT - 50:
                game_over = True
    
    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Draw lives
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))
    
    # Game over message
    if game_over:
        game_over_text = font.render("GAME OVER - Press R to restart", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))
    
    # Flip the display
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()