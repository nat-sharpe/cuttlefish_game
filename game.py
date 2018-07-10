import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, fat, tall, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.fatness = fat
        self.tallness = tall
        self.image = pygame.Surface([self.fatness, self.tallness])
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_x = 0
        self.move_y = 0

    def update(self):   
        self.rect.x += self.move_x
        self.rect.y += self.move_y
        self.move_x = 0
        self.move_y = 0

    def moving_x(self, direction):
        self.move_x = direction

    def moving_y(self, direction):
        self.move_y = direction
        
class Tongue(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.fatness = 1
        self.tallness = 5
        self.image = pygame.Surface([self.fatness, self.tallness])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.player = player
        self.length = 1
        self.rect.left = self.player.rect.right
        self.rect.centery = self.player.rect.centery
        self.attacking = False
        self.time = 0
        self.speed = 2
        self.dist_extend = 10
        self.dist_retract = 1 + (self.dist_extend * 2)
        self.hit = False

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.left = self.player.rect.right
        self.rect.centery = self.player.rect.centery

        if self.attacking:
            self.time += 1
            if self.time == 1:
                self.extend()
            if self.time <= 10:
                if self.hit:
                   self.retract() 
                else:
                    self.extend()
            if self.time > 10:
                self.retract()

    def attack(self):
        self.attacking = True
        
    def extend(self):
        self.length += 10
        self.image = pygame.transform.scale(self.image, (self.length, 5))            

    def retract(self):
        if self.length > 10:
            self.length -= 10
            self.image = pygame.transform.scale(self.image, (self.length, 5))
        else:
            self.length = 1
            self.image = pygame.transform.scale(self.image, (self.length, 5))
            self.attacking = False
            self.time = 0
            self.hit = False          

    def bullseye(self):
        self.hit = True

class Food(pygame.sprite.Sprite):
    def __init__(self, WIDTH, DEPTH):
        pygame.sprite.Sprite.__init__(self)
        self.width = WIDTH
        self.depth = DEPTH
        self.image = pygame.Surface((25, 20))
        self.image.fill((255, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1000)
        self.rect.y = random.randrange(600, 1200)
        self.speedx = 0
        self.speedy = random.randrange(-2, -1)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom < 0 or self.rect.left > self.width or self.rect.right < 0:
            self.rect.x = random.randrange(1000)
            self.rect.y = random.randrange(600, 800)
            self.speedx = 0
            self.speedy = random.randrange(-3, -1)
            
def main():
    pygame.init()

    WIDTH = 1000
    DEPTH = 600

    screen = pygame.display.set_mode((WIDTH, DEPTH))
    clock = pygame.time.Clock()

    keystate = pygame.key.get_pressed()

    all_sprites = pygame.sprite.Group()
    yummies = pygame.sprite.Group()
    grabbies = pygame.sprite.Group()

    for i in range(60):
        fish = Food(WIDTH, DEPTH)
        all_sprites.add(fish)
        yummies.add(fish)

    player = Player(40, 40, 200, 400)
    tongue = Tongue(player)

    all_sprites.add(tongue)
    all_sprites.add(player)

    grabbies.add(tongue)

    running = True
    while running:
        
        clock.tick(60)
        speed = 8

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q]:
                running = False
            if event.type == pygame.KEYDOWN and event.key == 32:
                tongue.attack()

        if keys[pygame.K_LEFT] and player.rect.left > 0:
            player.moving_x(-speed)
        if keys[pygame.K_RIGHT] and player.rect.right < WIDTH:
            player.moving_x(speed)
        if keys[pygame.K_UP] and player.rect.top > 0:
            player.moving_y(-speed)
        if keys[pygame.K_DOWN] and player.rect.bottom < DEPTH:
            player.moving_y(speed)             

        all_sprites.update()

        if tongue.length > 1:
            hit = pygame.sprite.groupcollide(grabbies, yummies, False, True)
            if hit:
                tongue.bullseye()

        screen.fill((0, 0, 0)) 
        all_sprites.draw(screen)
        pygame.display.update()
        
    pygame.quit()

main()