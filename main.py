import random
import pygame

pygame.init()

game_win = pygame.display.set_mode(size=(900, 600))
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(pygame.image.load("images/icon.png"))

background = pygame.image.load("images/background.png")

pygame.mixer.music.load("music/background_music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.35)

sound_effect = pygame.mixer.Sound('music/asteroid_explosion.mp3')
sound_effect.set_volume(0.175)


class Spaceship(pygame.sprite.Sprite):

    def __init__(self, x_pos: int, y_pos: int, image_path):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = 0
        self.image = pygame.image.load(image_path)
        self.rect = pygame.Rect(self.x_pos, self.y_pos, 64, 64)

    def draw(self, surface):
        surface.blit(self.image, (self.x_pos, self.y_pos))

    def update(self):
        self.x_pos += self.speed
        if self.x_pos >= 836:
            self.x_pos = 836
        elif self.x_pos <= 0:
            self.x_pos = 0

        # updating the rectangle position represented by the rect object
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos


class Asteroid(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos, image_path):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed_x = random.randint(6, 8)
        self.speed_y = random.uniform(0.9, 1.5)
        self.image = pygame.image.load(image_path)
        self.rect = pygame.Rect(self.x_pos, self.y_pos, 64, 64)

    def draw(self, surface):
        surface.blit(self.image, (self.x_pos, self.y_pos))

    def update(self):
        self.x_pos += self.speed_x
        self.y_pos += self.speed_y
        if self.x_pos >= 836:
            self.speed_x = -self.speed_x
        elif self.x_pos <= 0:
            self.speed_x = -self.speed_x

        if self.y_pos >= 600:
            self.y_pos = 0
            self.x_pos = random.randint(0, 836)
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos, image_path):
        super().__init__()
        self.x_pos = (x_pos + 16)
        self.y_pos = (y_pos + 16)
        self.speed_y = 0
        self.image = pygame.image.load(image_path)
        self.rect = pygame.Rect(self.x_pos, self.y_pos, 16, 32)

    def draw(self, surface):
        surface.blit(self.image, (self.x_pos, self.y_pos))

    def update(self):
        self.y_pos += self.speed_y

        if self.y_pos < 552:
            self.x_pos += 0
        else:
            self.x_pos += spaceship.speed

        if self.x_pos >= 852:
            self.x_pos = 852
        elif self.x_pos <= 16:
            self.x_pos = 16
        if self.y_pos <= 0:
            self.y_pos = 552
            self.x_pos = spaceship.x_pos + 16
            self.speed_y = 0

        self.rect.x = self.x_pos + 8
        self.rect.y = self.y_pos


spaceship = Spaceship(418, 536, "images/spaceship.png")

asteroid_1 = Asteroid(random.randint(0, 836), random.randint(0, 86), "images/asteroid.png")
asteroid_2 = Asteroid(random.randint(0, 836), random.randint(0, 86), "images/asteroid2.png")
asteroid_3 = Asteroid(random.randint(0, 836), random.randint(0, 86), "images/asteroid3.png")
asteroid_4 = Asteroid(random.randint(0, 836), random.randint(0, 86), "images/asteroids4.png")

bullet = Bullet(418, 536, "images/bullet.png")
shoot = False

asteroids = pygame.sprite.Group()
asteroids.add(asteroid_1, asteroid_2, asteroid_3, asteroid_4)
score_counter = 0
font = pygame.font.SysFont('calibri', 20, bold=False, italic=False)
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Event Handling
    clock.tick(90)
    for event in pygame.event.get():
        # Exiting the game when the user closes the game window and triggers a QUIT type event.
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                spaceship.speed = -7

            elif event.key == pygame.K_RIGHT:
                spaceship.speed = 7

            if event.key == pygame.K_SPACE:
                shoot = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                spaceship.speed = 0

            if event.key == pygame.K_SPACE:
                shoot = False

    # Designing the game logic
    if shoot:
        bullet.speed_y = -30
    spaceship.update()
    asteroids.update()
    bullet.update()

    asteroids_and_bullet = pygame.sprite.spritecollide(bullet, asteroids, dokill=True)

    for i in asteroids_and_bullet:
        score_counter += 1
        sound_effect.play()

    asteroids_and_spaceship_collide = pygame.sprite.spritecollide(spaceship, asteroids, dokill=False)

    for i in asteroids_and_spaceship_collide:
        if pygame.sprite.collide_rect(spaceship, i):
            pygame.mixer.music.stop()
            running = False

    if len(asteroids.sprites()) == 0:
        asteroid_1.x_pos, asteroid_1.y_pos = random.randint(0, 836), random.randint(0, 86)
        asteroid_2.x_pos, asteroid_2.y_pos = random.randint(0, 836), random.randint(0, 86)
        asteroid_3.x_pos, asteroid_3.y_pos = random.randint(0, 836), random.randint(0, 86)
        asteroid_4.x_pos, asteroid_4.y_pos = random.randint(0, 836), random.randint(0, 86)
        asteroids.add(asteroid_1, asteroid_2, asteroid_3, asteroid_4)

    # Rendering the game graphics
    game_win.blit(background, (0, 0))
    bullet.draw(game_win)
    spaceship.draw(game_win)
    asteroids.draw(game_win)
    text = font.render(f"Score - {score_counter}", True, (200, 100, 150), None)
    game_win.blit(text, (816, 20))

    # Updating the game window
    pygame.display.flip()

pygame.quit()
