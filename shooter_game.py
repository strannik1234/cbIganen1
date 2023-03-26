#Создай собственный Шутер!

from pygame import *
from random import randint
#подгружаем отдельно функции для работы со шрифтом
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))


font2 = font.SysFont('Arial', 36)


#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


#нам нужны такие картинки:
img_back = "galaxy.jpg" #фон игры
img_bullet = "bullet.png" #пуля
img_hero = "rocket.png" #герой
img_enemy = "ufo2.png" #враг
img_asteroid = "asteroid.png"
score = 0 #сбито кораблей
goal = 30 #столько кораблей нужно сбить для победы
lost = 0 #пропущено кораблей
max_lost = 5 #проиграли, если пропустили столько
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)


       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed


       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))


#класс главного игрока
class Player(GameSprite):
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       super(Player, self).__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
       self.health = 3
   #мет од для управления спрайтом стрелками клавиатуры
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)
   def hit(self):
       self.health = self.health - 1
       return True if self.isAlive() == False else False
   def isAlive(self):
       return self.health > 0
   def getHealth(self):
       return self.health


#класс спрайта-врага  
class Enemy(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       global lost
       #исчезает, если дойдёт до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1
#класс спрайта-пули  
class Bullet(GameSprite):
   # движение врага
   def update(self):
       self.rect.y += self.speed
       # исчезает, если дойдет до края экрана
       if self.rect.y < 0:
           self.kill()

class asteroid(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       global lost
       #исчезает, если дойдёт до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           

#создаём окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
#создаём спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
#создание группы спрайтов-врагов
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 6):
   item = asteroid(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
   asteroids.add(item)

bullets = sprite.Group()
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
while run:
   #событие нажатия на кнопку Закрыть
   for e in event.get():
       if e.type == QUIT:
           run = False
       #событие нажатия на пробел - спрайт стреляет
       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               fire_sound.play()
               ship.fire()
 #сама игра: действия спрайтов, проверка правил игры, перерисовка
   if not finish:
       #обновляем фон
       window.blit(background,(0,0))


       #производим движения спрайтов
       ship.update()
       monsters.update()
       bullets.update()
       asteroids.update()


       #обновляем их в новом местоположении при каждой итерации цикла
       ship.reset()
       monsters.draw(window)
       bullets.draw(window)
       asteroids.draw(window)
       #проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
       collides = sprite.groupcollide(monsters, bullets, True, True)
       for c in collides:
           #этот цикл повторится столько раз, сколько монстров подбито
           score = score + 1
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)
       

       shipGroup = sprite.Group()
       shipGroup.add(ship)
       #возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
       if sprite.spritecollide(ship, monsters,  False) or lost >= max_lost:
           sprite.groupcollide(monsters, shipGroup, True, False)
           finish = ship.hit()

       if sprite.spritecollide(ship, asteroids, False):
           sprite.groupcollide(asteroids, shipGroup, True, False)
           finish = ship.hit()
        
       #проиграли, ставим фон и больше не управляем спрайтами.  
       if (finish == True):
           window.blit(lose, (200, 200))

       #проверка выигрыша: сколько очков набрали?
       if score >= goal:
           finish = True
           window.blit(win, (200, 200))


       #пишем текст на экране
       text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))


       text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 50))

       text_health = font2.render("Прочность: " + str(ship.getHealth()), 1, (255, 255, 255))
       window.blit(text_health, (10, 80))


       display.update()


   time.delay(50)













































































































































































































































































































































































































































