import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30
player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
player_y = SCREEN_HEIGHT - 60
player_speed = 5

# Enemy settings
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 30
enemy_speed = 2
enemies = [
    [random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH), random.randint(-100, -40)]
    for _ in range(6)
]

# Bullet settings
BULLET_WIDTH = 5
BULLET_HEIGHT = 15
bullets = []
bullet_speed = -7
bullet_timer = 0  # Timer to control automatic bullet firing

# Enemy bullet settings
ENEMY_BULLET_WIDTH = 5
ENEMY_BULLET_HEIGHT = 15
enemy_bullets = []
enemy_bullet_speed = 5
enemy_shoot_timer = 2  # Timer for controlling enemy firing rate

# Score
score = 0
font = pygame.font.SysFont("Arial", 24)

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()

def draw_player(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, PLAYER_WIDTH, PLAYER_HEIGHT))

def draw_enemy(x, y):
    pygame.draw.rect(screen, RED, (x, y, ENEMY_WIDTH, ENEMY_HEIGHT))

def draw_bullet(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, BULLET_WIDTH, BULLET_HEIGHT))

def draw_enemy_bullet(x, y):
    pygame.draw.rect(screen, RED, (x, y, ENEMY_BULLET_WIDTH, ENEMY_BULLET_HEIGHT))

def show_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def main():
    global player_x, player_y, bullets, enemy_bullets, enemies, score, bullet_timer, enemy_shoot_timer

    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - PLAYER_WIDTH:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - PLAYER_HEIGHT:
            player_y += player_speed
        if keys[pygame.K_ESCAPE]:
            pause()

        if player_y <= 350:
            player_y = 350

        # Automatic shooting
        bullet_timer += 1
        if bullet_timer >= 20:  # Adjust this value to change the firing rate
            bullets.append([player_x + PLAYER_WIDTH // 2, player_y])
            bullet_timer = 0

        # Update bullets
        bullets = [[x, y + bullet_speed] for x, y in bullets if y + bullet_speed > 0]
        for bullet in bullets:
            draw_bullet(bullet[0], bullet[1])

        # Enemy shooting
        enemy_shoot_timer += 1
        if enemy_shoot_timer >= 50:  # Adjust to change enemy firing frequency
            for enemy in enemies:
                enemy_bullets.append([enemy[0] + ENEMY_WIDTH // 2, enemy[1] + ENEMY_HEIGHT])
            enemy_shoot_timer = 0

        # Update enemy bullets
        enemy_bullets = [[x, y + enemy_bullet_speed] for x, y in enemy_bullets if y < SCREEN_HEIGHT]
        for enemy_bullet in enemy_bullets:
            draw_enemy_bullet(enemy_bullet[0], enemy_bullet[1])

        # Check for collisions with the player
        for enemy_bullet in enemy_bullets:
            if (
                player_x < enemy_bullet[0] < player_x + PLAYER_WIDTH
                and player_y < enemy_bullet[1] < player_y + PLAYER_HEIGHT
            ):
                print("Player hit!")  # Replace with game-over logic or health reduction

        # Update enemies
        for enemy in enemies:
            enemy[1] += enemy_speed
            if enemy[1] > SCREEN_HEIGHT:  # Respawn enemy at the top
                enemy[0] = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
                enemy[1] = random.randint(-100, -40)
            draw_enemy(enemy[0], enemy[1])

        # Check collisions
        for bullet in bullets:
            for enemy in enemies:
                if (
                    enemy[0] < bullet[0] < enemy[0] + ENEMY_WIDTH
                    and enemy[1] < bullet[1] < enemy[1] + ENEMY_HEIGHT
                ):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    enemies.append(
                        [random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH), random.randint(-100, -40)]
                    )
                    score += 1
                    break

        # Draw player
        draw_player(player_x, player_y)

        # Draw score
        show_score()

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()
