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
BLUE = (0, 0, 255)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30

# Bullet settings
BULLET_WIDTH = 5
BULLET_HEIGHT = 15
bullets = []
bullet_speed = -7
bullet_timer = 0  # Timer to control automatic bullet firing

# Score
score = 0
coins = 0
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

class Enemy:
    def __init__(self, x, y, enemy_type="normal"):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.width = 40
        self.height = 30
        self.speed = 2
        self.shoot_timer = 0
        self.delta_x = random.choice([-1, 1])  # Horizontal movement direction
        self.delta_y = 1  # Start moving downward

        # Set bullet size and shoot rate based on enemy type
        if self.type == "heavy":
            self.bullet_size = (10, 30)  # Larger bullet
            self.shoot_rate = 70  # Shoots less frequently
        else:
            self.bullet_size = (5, 15)  # Normal bullet
            self.shoot_rate = 50 if self.type == "normal" else 20

        self.change_direction_timer = random.randint(30, 100)  # Time to change direction
        self.timer_counter = 0

    def move(self):
        self.timer_counter += 1

        # Randomly change direction at intervals
        if self.timer_counter >= self.change_direction_timer:
            self.delta_x = random.choice([-1, 1])
            self.delta_y = random.choice([-1, 1])  # Allow random vertical direction changes
            self.change_direction_timer = random.randint(30, 100)  # Reset direction change timer
            self.timer_counter = 0

        # Update position
        self.x += self.delta_x * self.speed
        self.y += self.delta_y * self.speed

        # Bounce at screen edges
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.delta_x *= -1  # Reverse horizontal direction

        # Allow free downward movement until fully visible
        if self.y >= 250:
            self.delta_y = -1  # Reverse direction when hitting the bottom bound
        elif self.y <= 0:
            self.delta_y = random.choice([1])  # Ensure upward movement changes back downward

    def shoot(self):
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_rate:
            self.shoot_timer = 0
            return [self.x + self.width // 2, self.y + self.height]
        return None

    def draw(self):
        # Assign color based on type
        if self.type == "normal":
            color = RED
        elif self.type == "rapid":
            color = BLUE
        elif self.type == "heavy":
            color = WHITE  
        else:
            color = RED  

        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

def draw_bullet(x, y, size):
    pygame.draw.rect(screen, WHITE, (x, y, size[0], size[1]))

def show_score_and_health(score, health, coins):
    score_text = font.render(f"Score: {score}", True, WHITE)
    health_text = font.render(f"Health: {health}", True, WHITE)
    coins_text = font.render(f"Coins: {coins}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 40))
    screen.blit(coins_text, (10, 70))

def main():
    global bullets, score, coins, bullet_timer

    # Create player object
    player = CyberSafe(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - 60)

    # Initialize enemies
    enemies = []
    enemy_bullets = []

    # Spawn 5 enemies with random types, starting above the screen
    for _ in range(5):
        enemy_type = random.choice(["normal", "heavy", "rapid"])
        enemies.append(Enemy(random.randint(0, SCREEN_WIDTH - 40), random.randint(-200, -40), enemy_type))

    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            # Pause functionality here
            pass

        # Player movement
        player.move(keys)

        # Automatic shooting
        bullet_timer += 1
        if bullet_timer >= 20:
            bullets.append([player.x + PLAYER_WIDTH // 2, player.y])
            bullet_timer = 0

        # Update bullets
        bullets = [[x, y + bullet_speed] for x, y in bullets if y + bullet_speed > 0]
        for bullet in bullets:
            draw_bullet(bullet[0], bullet[1], (BULLET_WIDTH, BULLET_HEIGHT))

        # Update enemies and their bullets
        for enemy in enemies:
            enemy.move()
            enemy.draw()

            # Enemy shooting
            new_bullet = enemy.shoot()
            if new_bullet:
                enemy_bullets.append([new_bullet[0], new_bullet[1], enemy.bullet_size])

        # Update enemy bullets
        enemy_bullets = [[x, y + 5, size] for x, y, size in enemy_bullets if y < SCREEN_HEIGHT]
        for enemy_bullet in enemy_bullets:
            draw_bullet(enemy_bullet[0], enemy_bullet[1], enemy_bullet[2])

            # Check collision with player
            if (
                player.x < enemy_bullet[0] < player.x + PLAYER_WIDTH
                and player.y < enemy_bullet[1] < player.y + PLAYER_HEIGHT
            ):
                enemy_bullets.remove(enemy_bullet)
                player.take_damage()

        # Check collisions between player bullets and enemies
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if (
                    enemy.x < bullet[0] < enemy.x + enemy.width
                    and enemy.y < bullet[1] < enemy.y + enemy.height
                ):
                    bullets.remove(bullet)
                    enemies.remove(enemy)

                    # Add different scores based on enemy type
                    if enemy.type == "normal":
                        score += 100
                    elif enemy.type == "rapid":
                        score += 150
                    elif enemy.type == "heavy":
                        score += 200

                    # Add coins based on enemy type
                    if enemy.type == "normal":
                        coins += 10
                    elif enemy.type == "rapid":
                        coins += 15
                    elif enemy.type == "heavy":
                        coins += 20

                    # Respawn a new enemy
                    enemies.append(Enemy(random.randint(0, SCREEN_WIDTH - 40), random.randint(-100, -40), random.choice(["normal", "heavy", "rapid"])))
                    break

        # Draw player
        player.draw()

        # Show score and health
        show_score_and_health(score, player.health, coins)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)


if __name__ == "__main__":
    main()
