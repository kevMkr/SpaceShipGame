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
pygame.display.set_caption("CyberSafe")

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
bullet_timer = 0

# Score and coins
score = 0
coins = 0
font = pygame.font.SysFont("Arial", 24)

class CyberSafe:
    def __init__(self, x, y, health=100, damage=10):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.damage = damage
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
        # Display health bar
        pygame.draw.rect(screen, RED, (self.x, self.y - 10, PLAYER_WIDTH, 5))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, PLAYER_WIDTH * (self.health / self.max_health), 5))

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            print("Game Over!")
            pygame.quit()
            sys.exit()

    def upgrade_health(self):
        self.max_health += 5
        self.health = self.max_health  # Restore full health when upgraded

    def upgrade_damage(self):
        self.damage += 1


def show_upgrade_menu(player, coins):
    #Displays the upgrade menu and allows upgrades
    upgrade_text = font.render("Upgrade Menu: Press 1 to Increase Health (50 Coins), 2 to Increase Damage (30 Coins)", True, WHITE)
    coins_text = font.render(f"Coins: {coins}", True, WHITE)

    screen.blit(upgrade_text, (10, SCREEN_HEIGHT - 80))
    screen.blit(coins_text, (10, SCREEN_HEIGHT - 50))

class Enemy:
    def __init__(self, x, y, enemy_type="normal", wave=1):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.width = 40
        self.height = 30
        self.speed = 2
        self.shoot_timer = 0
        self.delta_x = random.choice([-1, 1])
        self.delta_y = 1

        # Scale health with wave progression
        health_multiplier = 1 + (wave - 1) * 0.2  # Increase health by 20% per wave
        if self.type == "heavy":
            self.health = int(5 * health_multiplier)
            self.bullet_size = (10, 30)
            self.shoot_rate = 70
        elif self.type == "rapid":
            self.health = int(2 * health_multiplier)
            self.bullet_size = (5, 15)
            self.shoot_rate = 20
        else:
            self.health = int(3 * health_multiplier)
            self.bullet_size = (5, 15)
            self.shoot_rate = 50

        self.change_direction_timer = random.randint(30, 100)
        self.timer_counter = 0

    def move(self):
        self.timer_counter += 1

        if self.timer_counter >= self.change_direction_timer:
            self.delta_x = random.choice([-1, 1])
            self.delta_y = random.choice([-1, 1])
            self.change_direction_timer = random.randint(30, 100)
            self.timer_counter = 0

        self.x += self.delta_x * self.speed
        self.y += self.delta_y * self.speed

        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.delta_x *= -1
        if self.y >= 250:
            self.delta_y = -1
        elif self.y <= 0:
            self.delta_y = random.choice([1])

    def shoot(self):
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_rate:
            self.shoot_timer = 0
            return [self.x + self.width // 2, self.y + self.height]
        return None

    def draw(self):
        if self.type == "normal":
            color = RED
        elif self.type == "rapid":
            color = BLUE
        elif self.type == "heavy":
            color = WHITE
        else:
            color = RED
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True  # Return True if the enemy is dead
        return False  # Return False if the enemy is still alive

class Boss:
    def __init__(self, x, y, wave):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 80
        self.health = 50 + wave * 5  # Increase boss health with each boss wave
        self.speed = 2
        self.shoot_timer = 0
        self.move_timer = 0
        self.delta_x = 1
        self.delta_y = 1
        self.max_health = self.health  # Store max health for the health bar

    def move(self):
        self.move_timer += 1

        # Horizontal movement
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.delta_x *= -1
        self.x += self.delta_x * self.speed

        # Vertical movement
        if self.move_timer % 100 == 0:  # Change vertical direction periodically
            self.delta_y *= -1
        self.y += self.delta_y * self.speed

    def shoot(self):
        self.shoot_timer += 1
        if self.shoot_timer >= 50:  # Shoots every 50 frames
            self.shoot_timer = 0
            # Center the bullet relative to the boss's position
            return [self.x + self.width // 2 - 5, self.y + self.height]
        return None


    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, WHITE, (self.x, self.y - 10, self.width, 5))  # Health bar background
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, self.width * (self.health / self.max_health), 5))

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True
        return False

def draw_bullet(x, y, size):
    pygame.draw.rect(screen, WHITE, (x, y, size[0], size[1]))

def show_score_and_health(score, health, coins, wave):
    score_text = font.render(f"Score: {score}", True, WHITE)
    health_text = font.render(f"Health: {health}", True, WHITE)
    coins_text = font.render(f"Coins: {coins}", True, WHITE)
    wave_text = font.render(f"Wave: {wave}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 40))
    screen.blit(coins_text, (10, 70))
    screen.blit(wave_text, (10, 100))

def spawn_wave(wave):
    enemies = []
    for _ in range(wave * 1):  # Increase the number of enemies each wave
        enemy_type = random.choice(["normal", "heavy", "rapid"])
        enemies.append(Enemy(random.randint(0, SCREEN_WIDTH - 40), random.randint(-200, -40), enemy_type, wave))
    return enemies

def main():
    global bullets, score, coins, bullet_timer

    player = CyberSafe(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - 60)

    enemies = []
    enemy_bullets = []
    boss = None
    boss_active = False

    wave = 1
    wave_in_progress = False

    running = True
    show_upgrades = False  # Whether to display the upgrade menu

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Toggle upgrade menu with the "U" key
        if keys[pygame.K_u]:
            show_upgrades = True
        elif keys[pygame.K_ESCAPE]:
            show_upgrades = False

        if show_upgrades:
            show_upgrade_menu(player, coins)
            # Handle upgrades
            if keys[pygame.K_1] and coins >= 50:
                player.upgrade_health()
                coins -= 50
            if keys[pygame.K_2] and coins >= 30:
                player.upgrade_damage()
                coins -= 30
            pygame.display.flip()
            continue  # Skip the rest of the game loop while in upgrade menu

        player.move(keys)

        # Bullet logic
        bullet_timer += 1
        if bullet_timer >= 20:
            bullets.append([player.x + PLAYER_WIDTH // 2, player.y])
            bullet_timer = 0

        bullets = [[x, y + bullet_speed] for x, y in bullets if y + bullet_speed > 0]
        for bullet in bullets:
            draw_bullet(bullet[0], bullet[1], (BULLET_WIDTH, BULLET_HEIGHT))

        if not wave_in_progress and not boss_active:
            if wave % 5 == 0:  # Boss level every 5 waves
                boss = Boss(SCREEN_WIDTH // 2 - 50, 50, wave)
                boss_active = True
            else:
                enemies = spawn_wave(wave)
                wave_in_progress = True

        if boss_active:
            boss.move()
            boss.draw()

            new_bullet = boss.shoot()
            if new_bullet:
                enemy_bullets.append([new_bullet[0], new_bullet[1], (10, 30)])  # Boss bullets are larger

            for bullet in bullets[:]:
                if boss.x < bullet[0] < boss.x + boss.width and boss.y < bullet[1] < boss.y + boss.height:
                    bullets.remove(bullet)
                    if boss.take_damage(player.damage):  # Use player damage
                        boss_active = False
                        score += 1000  # Reward for defeating the boss
                        coins += 100
                        wave += 1
                        wave_in_progress = False

        if not boss_active:
            for enemy in enemies:
                enemy.move()
                enemy.draw()

                new_bullet = enemy.shoot()
                if new_bullet:
                    enemy_bullets.append([new_bullet[0], new_bullet[1], enemy.bullet_size])

            enemy_bullets = [[x, y + 5, size] for x, y, size in enemy_bullets if y < SCREEN_HEIGHT]
            for enemy_bullet in enemy_bullets:
                draw_bullet(enemy_bullet[0], enemy_bullet[1], enemy_bullet[2])
                if player.x < enemy_bullet[0] < player.x + PLAYER_WIDTH and player.y < enemy_bullet[1] < player.y + PLAYER_HEIGHT:
                    enemy_bullets.remove(enemy_bullet)
                    player.take_damage()

            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if enemy.x < bullet[0] < enemy.x + enemy.width and enemy.y < bullet[1] < enemy.y + enemy.height:
                        bullets.remove(bullet)
                        if enemy.take_damage(player.damage):  # Use player damage
                            enemies.remove(enemy)

                            if enemy.type == "normal":
                                score += 100
                                coins += 10
                            elif enemy.type == "rapid":
                                score += 150
                                coins += 15
                            elif enemy.type == "heavy":
                                score += 200
                                coins += 20
                            break

            if not enemies:  # If all enemies are defeated, start the next wave
                wave += 1
                wave_in_progress = False

        player.draw()
        show_score_and_health(score, player.health, coins, wave)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
