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

# Enemy settings
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 30
enemy_speed = 2
enemies = [
    [random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH), random.randint(-100, -40)]
    for _ in range(6)
]

# Initialize random movement deltas for enemies
enemy_deltas = [[random.choice([-1, 1]), random.choice([1])] for _ in range(len(enemies))]

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
enemy_shoot_timer = 0  # Timer for controlling enemy firing rate

# Score
score = 0
font = pygame.font.SysFont("Arial", 24)


class CyberSafe:
    def __init__(self, x, y, health=10):
        self.x = x
        self.y = y
        self.health = health
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - PLAYER_WIDTH:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - PLAYER_HEIGHT:
            self.y += self.speed
        if self.y < 350:
            self.y = 350

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT))

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            print("Game Over!")
            pygame.quit()
            sys.exit()


def draw_enemy(x, y):
    pygame.draw.rect(screen, RED, (x, y, ENEMY_WIDTH, ENEMY_HEIGHT))


def draw_bullet(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, BULLET_WIDTH, BULLET_HEIGHT))


def draw_enemy_bullet(x, y):
    pygame.draw.rect(screen, RED, (x, y, ENEMY_BULLET_WIDTH, ENEMY_BULLET_HEIGHT))


def show_score_and_health(score, health):
    score_text = font.render(f"Score: {score}", True, WHITE)
    health_text = font.render(f"Health: {health}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 40))


def main():
    global bullets, enemy_bullets, enemies, score, bullet_timer, enemy_shoot_timer

    # Create player object
    player = CyberSafe(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - 60)

    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player movement
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Automatic shooting
        bullet_timer += 1
        if bullet_timer >= 20:
            bullets.append([player.x + PLAYER_WIDTH // 2, player.y])
            bullet_timer = 0

        # Update bullets
        bullets = [[x, y + bullet_speed] for x, y in bullets if y + bullet_speed > 0]
        for bullet in bullets:
            draw_bullet(bullet[0], bullet[1])

        # Enemy shooting
        enemy_shoot_timer += 1
        if enemy_shoot_timer >= 50:
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
                player.x < enemy_bullet[0] < player.x + PLAYER_WIDTH
                and player.y < enemy_bullet[1] < player.y + PLAYER_HEIGHT
            ):
                enemy_bullets.remove(enemy_bullet)
                player.take_damage()

        # Update enemies
        for i, enemy in enumerate(enemies):
            # Respawn logic if enemy moves off-screen from above
            if enemy[1] < 0:
                enemy[1] += 2  # Spawn from above (falling)

            # Movement after spawning
            if enemy[1] >= 0:
                enemy[0] += enemy_deltas[i][0] * enemy_speed
                enemy[1] += enemy_deltas[i][1] * enemy_speed

                # Restrict movement to the y=0 to y=200 area
                if enemy[1] >= 200:
                    enemy[1] = 200
                    enemy_deltas[i][1] *= -1
                elif enemy[1] <= 0:
                    enemy[1] = 0
                    enemy_deltas[i][1] *= -1

                # Bounce off the horizontal boundaries
                if enemy[0] <= 0 or enemy[0] >= SCREEN_WIDTH - ENEMY_WIDTH:
                    enemy_deltas[i][0] *= -1

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
                    enemy_deltas.append([random.choice([-1, 1]), random.choice([1])])
                    score += 1
                    break

        # Draw player
        player.draw()

        # Draw score and health
        show_score_and_health(score, player.health)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)


if __name__ == "__main__":
    main()
