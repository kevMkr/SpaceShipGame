import pygame
import random
import sys
import pyodbc
import MainMenu as MM
import LoginPage as LP

conn = pyodbc.connect(
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=./CyberSafeDatabase.accdb;'
)
cursor = conn.cursor()


# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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

def actual_game():
    # Initialize Pygame
    pygame.init()
    # Setup the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("CyberSafe")
    background_image = pygame.image.load("background.jpg")  # Replace with your background image path
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to fit screen

    # Clock for controlling frame rate
    clock = pygame.time.Clock()


    font = pygame.font.SysFont("Arial", 24)

    #Sound effect Explosions
    explosion_sound = pygame.mixer.Sound("explosion.wav")
    explosion_sound.set_volume(0.5) #Volume to 50%

    def game_over_screen(score):
            while True:
                screen.fill(BLACK)
                game_over_text = font.render("GAME OVER", True, RED)
                score_text = font.render(f"Your Score: {score}", True, WHITE)
                save_text = font.render("Press S to Save", True, WHITE)
                restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)

                # Center the text
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
                screen.blit(save_text,(SCREEN_WIDTH // 2 - save_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
                screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
                screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        MM.MainMenu()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_s]:
                    cursor.execute('INSERT into Leaderboard(UserID,Username,Score) values(?,?,?)', LP.User().UserID,
                                        LP.User().Username, score)
                    conn.commit()
                    pygame.quit()
                    MM.MainMenu()
                if keys[pygame.K_r]:  
                    mainGame()  
                elif keys[pygame.K_q]:
                    pygame.quit()
                    sys.exit()
                    MM.MainMenu()

    def pause_menu():   
        paused = True
        while paused:
            screen.fill(BLACK)
            pause_text = font.render("PAUSED", True, RED)
            resume_text = font.render("Press R to Resume", True, WHITE)
            quit_text = font.render("Press Q to Quit", True, WHITE)

            # Center the text
            screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 3))
            screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, SCREEN_HEIGHT // 2))
            screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    MM.MainMenu()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:  # Resume game
                paused = False
            elif keys[pygame.K_q]:  # Quit game
                pygame.quit()
                sys.exit()
                MM.MainMenu()


    class CyberSafe:
        def __init__(self, x, y, health=10, damage=1):
            self.x = x
            self.y = y
            self.health = health
            self.max_health = health
            self.damage = damage
            self.speed = 5
            self.image = pygame.image.load("player.png")  # Replace with your player image path
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))  # Scale to fit

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
            screen.blit(self.image, (self.x, self.y))

        def take_damage(self):
            self.health -= 1
            if self.health <= 0:
                pygame.time.delay(500)  
                game_over_screen(score)

        def upgrade_health(self):
            self.max_health += 5
            self.health = self.max_health  # Restore full health when upgraded

        def upgrade_damage(self):
            self.damage += 2


    def show_upgrade_menu(player, coins):
        # Display the upgrade options in the bottom-right corner
        upgrade_text = font.render("UPGRADES: 1-Health (50 Coins), 2-Damage (30 Coins)", True, WHITE)

        # Positioning the text
        screen.blit(upgrade_text, (SCREEN_WIDTH - upgrade_text.get_width() - 10, SCREEN_HEIGHT - 35))

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
                self.shoot_rate = 100
            elif self.type == "rapid":
                self.health = int(2 * health_multiplier)
                self.bullet_size = (5, 15)
                self.shoot_rate = 20
            else:
                self.health = int(3 * health_multiplier)
                self.bullet_size = (5, 15)
                self.shoot_rate = 70

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
                self.image = pygame.image.load("enemy_normal.jpeg")  # Replace with the path to your normal enemy image
            elif self.type == "heavy":
                self.image = pygame.image.load("enemy_heavy.png")  # Replace with heavy enemy image
            elif self.type == "rapid":
                self.image = pygame.image.load("enemy_rapid.jpeg")  # Replace with rapid enemy image
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            screen.blit(self.image, (self.x, self.y))

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
            self.health = 100 + wave * 10  # Increase boss health with each boss wave
            self.speed = 2
            self.shoot_timer = 0
            self.move_timer = 0
            self.delta_x = 1
            self.delta_y = 1
            self.max_health = self.health  # Store max health for the health bar
            self.attack_type = "normal"  # Default attack type
            self.image = pygame.image.load("boss.png")  # Replace with your boss image path
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        def move(self):
            self.move_timer += 1
            if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
                self.delta_x *= -1
            self.x += self.delta_x * self.speed

            if self.move_timer % 100 == 0:
                self.delta_y *= -1
            self.y += self.delta_y * self.speed

        def choose_attack(self):
            # Choose attack based on boss's current health or wave
            if self.health < self.max_health * 0.70:
                self.attack_type = "rapid_fire"
            elif self.health < self.max_health * 0.30:
                self.attack_type = "bullet_spray"
            else:
                self.attack_type = "normal"

        def shoot(self):
            self.shoot_timer += 1
            self.choose_attack()  # Choose the attack type

            if self.shoot_timer >= 50:
                self.shoot_timer = 0
                if self.attack_type == "normal":
                    return [self.x + self.width // 2 - 5, self.y + self.height]
                elif self.attack_type == "rapid_fire":
                    return [self.x + self.width // 2 - 5, self.y + self.height, "rapid"]
                elif self.attack_type == "bullet_spray":
                    return [
                        [self.x + self.width // 2 - 5, self.y + self.height, "left"],
                        [self.x + self.width // 2 - 5, self.y + self.height, "right"]
                    ]
            return None

        def draw(self):
            screen.blit(self.image, (self.x, self.y))
            pygame.draw.rect(screen, WHITE, (self.x, self.y - 10, self.width, 5))
            pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, self.width * (self.health / self.max_health), 5))

        def take_damage(self, damage):
            self.health -= damage
            if self.health <= 0:
                return True
            return False

    def draw_bullet(x, y, size):
        pygame.draw.rect(screen, WHITE, (x, y, size[0], size[1]))

    def show_score_and_health(score, health, coins, wave, player):
        # Top-left corner: Score, Coins, and Wave
        score_text = font.render(f"Score: {score}", True, WHITE)
        coins_text = font.render(f"Coins: {coins}", True, WHITE)
        wave_text = font.render(f"Wave: {wave}", True, WHITE)

        # Top-right corner: Health and Damage
        health_text = font.render(f"Health: {health}/{player.max_health}", True, WHITE)
        damage_text = font.render(f"Damage: {player.damage}", True, WHITE)

        screen.blit(score_text, (10, 10))
        screen.blit(coins_text, (10, 40))
        screen.blit(wave_text, (10, 70))

        # Right-align health and damage statistics
        health_x = SCREEN_WIDTH - health_text.get_width() - 10
        damage_x = SCREEN_WIDTH - damage_text.get_width() - 10
        health_bar_width = 200
        health_bar_height = 20

        # Draw health bar
        pygame.draw.rect(screen, RED, (health_x - health_bar_width - 10, 10, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, GREEN, (health_x - health_bar_width - 10, 10, health_bar_width * (player.health / player.max_health), health_bar_height))

        # Render health and damage text
        screen.blit(health_text, (health_x, 10))
        screen.blit(damage_text, (damage_x, 40))

    def spawn_wave(wave):
        enemies = []
        for _ in range(wave * 1):  # Increase the number of enemies each wave
            enemy_type = random.choice(["normal", "heavy", "rapid"])
            enemies.append(Enemy(random.randint(0, SCREEN_WIDTH - 40), random.randint(-200, -40), enemy_type, wave))
        return enemies

    def mainGame():
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

        #Flags to avoid multiple key press
        key_u_pressed = False
        key_1_pressed = False
        key_2_pressed = False

        while running:
            screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    MM.MainMenu()

            keys = pygame.key.get_pressed()
            screen.blit(background_image, (0, 0))

            #Toggle pause menu
            if keys[pygame.K_ESCAPE]:
                pause_menu()

            # Toggle upgrade menu with the "U" key
            if keys[pygame.K_u] and not key_u_pressed:
                key_u_pressed = True
                show_upgrades = not show_upgrades
            if not keys[pygame.K_u]:
                key_u_pressed = False

            # Show upgrade options in the bottom-right corner
            if show_upgrades:
                show_upgrade_menu(player, coins)
            
            if keys[pygame.K_1] and not key_1_pressed:
                key_1_pressed = True
                if coins >= 50:
                    player.upgrade_health()
                    coins -= 50
            if not keys[pygame.K_1]:
                key_1_pressed = False

            if keys[pygame.K_2] and not key_2_pressed:
                key_2_pressed = True
                if coins >= 30:
                    player.upgrade_damage()
                    coins -= 30
            if not keys[pygame.K_2]:
                key_2_pressed = False

            player.move(keys)

            # Bullet logic
            bullet_timer += 1
            if bullet_timer >= 20:
                bullets.append([player.x + PLAYER_WIDTH // 2, player.y])
                bullet_timer = 0
                
            # Update player bullets: move them upward and remove any bullets that move off-screen
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

                bullets_to_add = boss.shoot()
                new_bullet = boss.shoot()
                if new_bullet:
                    enemy_bullets.append([new_bullet[0], new_bullet[1], (10, 30)])

                if bullets_to_add:
                    # For normal attacks
                    if isinstance(bullets_to_add[0], list):  # Bullet spray (multiple bullets)
                        for bullet in bullets_to_add:
                            direction = bullet[2]
                            if direction == "left":
                                enemy_bullets.append([bullet[0] - 10, bullet[1], (10, 20)])  # Left diagonal
                            elif direction == "right":
                                enemy_bullets.append([bullet[0] + 10, bullet[1], (10, 20)])  # Right diagonal
                    elif bullets_to_add[2] == "rapid":  # Rapid fire
                        enemy_bullets.append([bullets_to_add[0], bullets_to_add[1], (5, 10)])
                    else:
                        enemy_bullets.append([bullets_to_add[0], bullets_to_add[1], (10, 30)])

                enemy_bullets = [[x, y + 5, size] for x, y, size in enemy_bullets if y < SCREEN_HEIGHT]
                for enemy_bullet in enemy_bullets[:]:  # Iterate over a copy of the list to avoid modification issues
                    draw_bullet(enemy_bullet[0], enemy_bullet[1], enemy_bullet[2])
                    if player.x < enemy_bullet[0] < player.x + PLAYER_WIDTH and player.y < enemy_bullet[1] < player.y + PLAYER_HEIGHT:
                        enemy_bullets.remove(enemy_bullet)  # Remove the bullet after the collision
                        player.take_damage()
                    
                for bullet in bullets[:]:  # Iterate over a copy of the list for safe removal
                    if boss.x < bullet[0] < boss.x + boss.width and boss.y < bullet[1] < boss.y + boss.height:
                        bullets.remove(bullet)
                        if boss.take_damage(player.damage):  # Use player damage
                            boss_active = False
                            score += 1000  # Reward for defeating the boss
                            coins += 100
                            explosion_sound.play()  # Play explosion sound
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
                                explosion_sound.play()

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
            show_score_and_health(score, player.health, coins, wave, player)

            pygame.display.flip()
            clock.tick(60)
    mainGame()
if __name__ == "__main__":
    actual_game()
