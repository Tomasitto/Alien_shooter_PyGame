import pygame
import random
from os import path


img_dir = path.join(path.dirname(__file__), 'image')
snd_dir = path.join(path.dirname(__file__), 'sound')


HEIGHT = 600
WIDTH = 480
FPS = 60

BLACK = (0, 0, 0)




pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.randomsize = random.randint(20,60)
        self.image_orig = pygame.transform.scale(sp[random.randint(0,3)  ], (self.randomsize, self.randomsize))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(100 * 0.85 /2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center 

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx 
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20: 
            self.rect.x = random.randrange(WIDTH - self.rect.width )
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
        self.rotate()



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 30))
        self.rect = self.image.get_rect()
        self.radius = 20
        self.image.set_colorkey(BLACK)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
  

    def update(self):

        self.speedx = 0

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
               
        self.rect.x += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (5, 10))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        

    def update(self):
        self.rect.y += self.speedy
        if  self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


sp = []
meteor_name = ['meteorBrown_big1.png',
               'meteorBrown_big2.png',
               'meteorBrown_big3.png',
               'meteorBrown_big4.png']

#Звуки
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
expl_sound = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sound.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
#pygame.mixer.music.set_volume(0.4)
#pygame.mixer.music.load(path.join(snd_dir, 'earth.wav'))

# Объекты
background = pygame.image.load(path.join(img_dir, 'purple.png')).convert()
background  = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir,'playerShip2_blue.png')).convert()
#Взрыв метеора
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)


# Генерация рандомных метеоров
for i in range(4):
    meteor_img = pygame.image.load(path.join(img_dir, meteor_name[random.randint(0,3)])).convert()
    sp.append(meteor_img)
bullet_img = pygame.image.load(path.join(img_dir,'laserBlue03.png')).convert()



all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
all_sprites.add(player)


score = 0
#pygame.mixer.music.play(loops=-1)
running = True

font_name = pygame.font.match_font('arial')

def draw_text(surf  , text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, 'white')
    text_rect = text_surface.get_rect()
    text_rect.midleft = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, 'green', fill_rect)
    pygame.draw.rect(surf, 'white', outline_rect, 2)

for i in range(8):
    newmob()




'_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ '                 
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        # Обновление
    all_sprites.update()

    hits = pygame.sprite.spritecollide(player, mobs, True , pygame.sprite.collide_circle)     
    for hit in hits:
        player.shield -= hit.radius
        newmob()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if player.shield <= 0:
            running = False

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True) 
    for hit in hits: 
        score += 50 - hit.radius
        random.choice(expl_sound).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()
    # Рендеринг
    screen.fill('black')
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5 ,5, player.shield)   
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()


pygame.quit()