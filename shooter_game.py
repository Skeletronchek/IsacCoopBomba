from pygame import *
from random import *
from time import time as timer
font.init()
font2 = font.SysFont('Arial', 40)
cd = False
score = 0
lost = 0
hp = 3
img_back = 'basement.png'
img_hero = 'bradmoi.png'
img_heroded = 'isacded.png'
img_enemy = 'Gaper.png'
img_spike = 'Poky.png'
img_heart = 'heart.png'
img_bullet = 'tear.png'
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
bullets = sprite.Group()
#класс-наследник для спрайта-игрока (управляется стрелками)
class Bullet(GameSprite):
    def update(self):
        global score
        self.rect.y -= self.speed
        collision = sprite.groupcollide(
            bullets, monsters, True, True
        )
        if collision:
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 47, 55, randint(2, 6))
            monsters.add(monster)
            score +=1
        if self.rect.y < 0:
           self.kill()
class Player(GameSprite):
    def update(self):
        global cd
        global starttime
        global lost
        global hp
        keys = key.get_pressed()
        collision = sprite.spritecollide(
            self, spikes, True
        )
        if collision:
            hp -= 1
            if hp == 2:
                heart1.kill()
            elif hp == 1:
                heart2.kill()
            hit_sound.play()
            spike = Spike(img_spike, randint(80, win_width - 80), -40, 55, 55, 3)
            spikes.add(spike)
        if keys[K_UP]:  
            if cd == False:
                starttime = timer()
                fire_sound.play()
                bullet = Bullet(img_bullet, ship.rect.x+50, ship.rect.top, 25, 25, 6)
                bullets.add(bullet)
                cd = True   
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Spike(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

      



#Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("ооой тесак ко оп имбуля репентенс")
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 120, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 47, 55, randint(2, 6))
    monsters.add(monster)

spikes = sprite.Group()
for i in range(1, 3):
    spike = Spike(img_spike, randint(80, win_width - 80), -40, 55, 55, 3)
    spikes.add(spike)



hearts = sprite.Group()
heart1 = GameSprite(img_heart, (650 - 30), 450, 30, 30, 3)
heart1.add(hearts)
heart2 = GameSprite(img_heart, (650 - 60), 450, 30, 30, 3)
heart2.add(hearts)
heart3 = GameSprite(img_heart, (650 - 90), 450, 30, 30, 3)
heart3.add(hearts)




run = True
finish = False
clock = time.Clock()
FPS = 60


#музыка
mixer.init()
mixer.music.load('isacpesnya.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
hit_sound = mixer.Sound('Hurt_grunt.wav')

starttime = 0
curtime = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
                
    
    if not finish:
        if cd == True:
            curtime = timer()
            delay = curtime - starttime
            print(delay)
            if delay > 0.4:
                cd = False
                delay = 0
                starttime = 0
                curtime = 0
        window.blit(background,(0,0))
        if lost > 2 or hp < 1:
            ship.image = transform.scale(image.load(img_heroded), (60, 45))
            ship.rect.y = win_height - 50
            textlost = font2.render('YOU LOST!', 1, (255, 0, 0))
            window.blit(textlost, (300, 200))
        if score > 19:
            textwin= font2.render('YOU WIN!', 1, (0, 255, 0))
            window.blit(textwin, (300, 200))
        text = font2.render('Счёт:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        
        if not lost > 2 and not hp < 1 and not score > 19:
            ship.update()
            bullets.update()
            bullets.draw(window)
            monsters.update()
            spikes.update()
            
            monsters.draw(window)
            spikes.draw(window)
            hearts.draw(window)
        ship.reset()
        display.update()   
           
    time.delay(30)