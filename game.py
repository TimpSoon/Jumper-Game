from pygame import *
from random import randint

font.init()
window = display.set_mode((450, 800))
display.set_caption('Jumper')
background = transform.scale(image.load('background.jpg'), (450, 800))
win_width = 450
win_height = 800
game = True
FPS = 60
clock = time.Clock()

GRAVITY = 0.1
JUMP_POWER = 5


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (75, 75))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.y_velocity = 0

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.on_ground = False

    def move(self):
        keys_pressed = key.get_pressed()
        self.y_velocity += GRAVITY

        if keys_pressed[K_SPACE] and self.on_ground:
            self.y_velocity = -JUMP_POWER
            self.on_ground = False

        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 70:
            self.rect.x += self.speed

        self.rect.y += self.y_velocity

        if self.rect.y >= win_height - self.rect.height:
            self.rect.y = win_height - self.rect.height
            self.y_velocity = 0
            self.on_ground = True

    def update(self):
        if self.on_ground:
            window.blit(self.image, (self.rect.x, self.rect.y))


platform_x = 50
platform_y = 650
platforms = sprite.Group()
player = Player('star.png', 200, 750, 5)

for i in range(10):
    platform = GameSprite('platform.png', randint(0, 400), platform_y, 0)
    platforms.add(platform)
    platform_y -= 150

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background, (0, 0))
    platforms.draw(window)

    player.reset()
    player.move()
    player.update()


    for platform in platforms:
        if player.rect.colliderect(platform.rect) and player.y_velocity >= 0:
            player.rect.bottom = platform.rect.top
            player.y_velocity = 0
            player.on_ground = True


    if player.rect.y > win_height:
        game = False
        text_font = font.Font(None, 36)
        game_over_text = text_font.render("Game Over", True, (255, 255, 255))
        window.blit(game_over_text, (win_width // 2 - game_over_text.get_width() // 2, win_height // 2 - game_over_text.get_height() // 2))


    if player.rect.y <= 0:
        game = False
        text_font = font.Font(None, 36)
        you_win_text = text_font.render("You Win", True, (255, 255, 255))
        window.blit(you_win_text, (win_width // 2 - you_win_text.get_width() // 2, win_height // 2 - you_win_text.get_height() // 2))

    clock.tick(FPS)
    display.update()

time.wait(2000)
