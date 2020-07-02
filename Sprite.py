from pygame import *
from random import randint
font.init()
mixer.init()

time.set_timer(USEREVENT, 3000)
WS = WL, WH = 1280, 720
sc = display.set_mode(WS)
models = 'toilet_paper.png', 'car_black_2.png', 'car_black_3.png', 'apple.png'
enemy_surf = []
display.set_caption('Edible or not edible')
white, black, red, blue = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255)
neat = sprite.Group()
eat = sprite.Group()
player = sprite.Group()
background = image.load('background.jpg').convert()
background = transform.scale(background, WS)
back_sound = mixer.music.load('background_sound.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.035)
great = mixer.Sound('collect_sound.wav')
x_change = 0
accel_x = 0
max_speed = 20
pos = '0', '0'
game = 0
menu = 1
score = 0
best_score = 0


class Enemy(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.x = randint(31, WL - 31)
        self.turn = randint(-360, 360)
        self.filename = models[randint(0, 3)]
        self.image = image.load(self.filename).convert_alpha()

        if self.filename == 'car_black_3.png' or 'car_black_2.png':
            self.image = transform.scale(self.image, (71, 131))
            self.add(neat)
        if self.filename == 'toilet_paper.png' or self.filename == 'apple.png':
            if self.filename == 'toilet_paper.png':
                self.image = transform.scale(self.image, (71, 71))
            self.add(eat)
        
        self.image = transform.rotate(self.image, self.turn)
        self.rect = self.image.get_rect(center=(self.x, -131))
        self.speed = randint(1, 7)

    def update(self):
        if sprite.spritecollideany(self, player) is not None:
            self.kill()

        if self.rect.y < WH:
            self.rect.y += self.speed
        else:
            self.kill()


class Player(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.add(player)
        self.image = image.load('character.png').convert_alpha()
        self.image = transform.scale(self.image, (200, 185))
        self.rect = self.image.get_rect(center=(WL / 2, WH - (WH / 8)))
        self.score = 0
        self.speed = 5


font_quit = font.Font(None, 36)
text_quit = font_quit.render('Quit', 1, red)
but_quit = Surface((150, 150))
but_quit.fill(blue)

font_play = font.Font(None, 36)
text_plat = font_play.render('Play', 1, blue)
but_play = Surface((150, 150))
but_play.fill(red)

main = Player()
Enemy()

display.update()
while 1:

    while menu:
        for even in event.get():
            if even.type == QUIT:
                exit()
            elif even.type == MOUSEBUTTONDOWN:
                pos = mouse.get_pos()

        if pos[0] in range(700, 850) and pos[1] in range(300, 450):
            game = 1
            menu = 0
            pos = '0', '0'
        elif pos[0] in range(1130, 1280) and pos[1] in range(0, 150):
            exit()
            pos = '0', '0'

        sc.fill(black)
        sc.blit(background, (0, 0))
        but_quit.blit(text_quit, (50, 50))
        sc.blit(but_quit, (1130, 0))
        but_quit.fill(blue)
        but_play.blit(text_plat, (50, 50))
        sc.blit(but_play, (700, 300))
        but_play.fill(red)
        time.delay(17)
        display.update()

    while game:
        for even in event.get():
            if even.type == QUIT:
                exit()
            elif even.type == USEREVENT:
                Enemy()
            elif even.type == MOUSEBUTTONDOWN:
                pos = mouse.get_pos()

        pressed = key.get_pressed()
        if pressed[K_LEFT] and (main.rect.x > 0):
            accel_x = -0.5
        elif pressed[K_RIGHT] and (main.rect.x < WL - 200):
            accel_x = 0.5
        else:
            accel_x = 0

        x_change += accel_x
        if abs(x_change) >= max_speed:
            x_change = x_change/abs(x_change) * max_speed
        if accel_x == 0:
            x_change *= 0.5

        main.rect.x += x_change

        if sprite.spritecollideany(main, eat) is not None or sprite.spritecollideany(main, neat) is not None:
            if sprite.spritecollideany(main, eat) is not None:
                great.play()
                score += 1
            elif sprite.spritecollideany(main, neat) is not None:
                score -= 1

        if pos[0] in range(1130, 1280) and pos[1] in range(0, 150):
            menu = 1
            game = 0
            pos = '0', '0'

        file = open('data.txt', 'r')

        if score >= int(file.read()):
            file.close()
            file = open('data.txt', 'w')
            file.write(str(score))
            best_score = score
            file.close()
        else:
            file = open('data.txt', 'r')
            best_score = file.read()
            file.close()

        f1 = font.Font(None, 50)
        Score = f1.render(str(score), 1, (255, 255, 255))
        f2 = font.Font(None, 50)
        Best_score = f2.render(str(best_score), 1, (255, 255, 255))

        sc.fill(black)
        sc.blit(background, (0, 0))
        but_quit.blit(text_quit, (50, 50))
        sc.blit(but_quit, (1130, 0))
        but_quit.fill(blue)
        eat.draw(sc)
        neat.draw(sc)
        player.draw(sc)
        sc.blit(Score, (50, 50))
        sc.blit(Best_score, (50, 100))
        time.delay(17)
        display.update()
        eat.update()
        neat.update()
        player.update()
