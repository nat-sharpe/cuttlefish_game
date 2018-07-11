import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, fat, tall, x, y, WIDTH, DEPTH):
        pygame.sprite.Sprite.__init__(self)
        self.screen_width = WIDTH
        self.screen_depth = DEPTH
        self.time = 0
        self.fatness = fat
        self.tallness = tall
        self.image = pygame.Surface([self.fatness, self.tallness])
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_x = 0
        self.move_y = 0
        self.left = False
        self.right = True
        self.squirting = False
        self.squirt_speed = 4

    def going_left(self):
        self.left = True
        self.right = False

    def going_right(self):
        self.left = False
        self.right = True

    def squirt_right(self, speed, y_move):
        if self.left and self.rect.right < (self.screen_width - self.squirt_speed):
            self.rect.x += (self.squirt_speed * speed)
            self.rect.y += y_move

    def squirt_left(self, speed, y_move):
        if self.right and self.rect.left > (0 + self.squirt_speed):
            self.rect.x -= (self.squirt_speed * speed)
            self.rect.y += y_move

    def update(self):   
        if self.squirting:
            self.time += 1
            if self.time <= 25:
                self.squirt_left(2, random.randrange(-1, 1))
                self.squirt_right(2, random.randrange(-1, 1))
            elif self.time <= 35:
                self.squirt_left(1, 0)
                self.squirt_right(1, 0)
            elif self.time <= 40:
                self.squirt_left(.5, 0)
                self.squirt_right(.5, 0)
            else:
                self.time = 0
                self.squirting = False

        self.rect.x += self.move_x
        self.rect.y += self.move_y
        self.move_x = 0
        self.move_y = 0
        
        # self.time += 1
        # if self.time > 30 and self.time <= 60:
        #     self.rect.x += (self.move_x / 2)
        #     self.rect.y += (self.move_y / 2)
        # elif self.time > 60:
        #     self.move_x = 0
        #     self.move_y = 0
        #     self.time = 0

    def squirt(self):
        self.squirting = True
        
    def moving_x(self, direction):
        self.move_x = direction

    def moving_y(self, direction):
        self.move_y = direction
        
class Tongue(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.fatness = 1
        self.tallness = 20
        self.image = pygame.Surface([self.fatness, self.tallness])
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect()
        self.player = player
        self.length = 1
        self.rect.left = self.player.rect.right
        self.rect.centery = self.player.rect.centery
        self.attacking = False
        self.time = 0
        self.speed = 2
        self.tongue_length = 10
        self.dist_retract = 1 + (self.tongue_length * 2)
        self.hit = False
        self.left = False
        self.right = True

    def update(self):
        if self.right:
            self.rect = self.image.get_rect()
            self.rect.left = self.player.rect.right
            self.rect.centery = self.player.rect.centery

        if self.left:
            self.rect = self.image.get_rect()
            self.rect.right = self.player.rect.left
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
        self.length += self.tongue_length
        self.image = pygame.transform.scale(self.image, (self.length, self.tallness))            

    def retract(self):
        if self.length > self.tongue_length:
            self.length -= self.tongue_length
            self.image = pygame.transform.scale(self.image, (self.length, self.tallness))
        else:
            self.length = 1
            self.image = pygame.transform.scale(self.image, (self.length, self.tallness))
            self.attacking = False
            self.time = 0
            self.hit = False          

    def bullseye(self):
        self.hit = True

    def going_left(self):
        self.left = True
        self.right = False

    def going_right(self):
        self.left = False
        self.right = True

class Food(pygame.sprite.Sprite):
    def __init__(self, WIDTH, DEPTH):
        pygame.sprite.Sprite.__init__(self)
        self.time = 0
        self.width = WIDTH
        self.depth = DEPTH
        self.image = pygame.Surface((25, 20))
        self.image.fill((255, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1000, 2000)
        self.rect.y = random.randrange(600)
        self.speedx = random.randrange(-2, -1)
        self.speedy = random.randrange(-1, 1)
        self.bumped = False

    def update(self):
        self.time += 1
        if self.time == 3:
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if self.rect.bottom < 0 or self.rect.left > self.width or self.rect.right < 0:
                self.rect.x = random.randrange(1000, 2000)
                self.rect.y = random.randrange(600)
                self.speedx = random.randrange(-2, -1)
                self.speedy = random.randrange(-1, 1)
            self.time = 0
    
    def change_course(self):
        self.speedx = -self.speedx
        self.speedy = -self.speedy 
    
    def got_bumped(self):
        bumped = True

class FearZone(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.image = pygame.Surface((90, 60))
        self.image.fill((255, 0, 0))
        self.image.set_colorkey((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.player.rect.centerx
        self.rect.centery = self.player.rect.centery

    def update(self):
        self.rect.centerx = self.player.rect.centerx
        self.rect.centery = self.player.rect.centery

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
    bumpies = pygame.sprite.Group()

    fish_swarm = {}
    fish_count = 30
    
    for i in range(fish_count):
        fish_swarm[i] = Food(WIDTH, DEPTH)
        all_sprites.add(fish_swarm[i])
        yummies.add(fish_swarm[i])

    player = Player(80, 60, 200, 400, WIDTH, DEPTH)
    all_sprites.add(player)

    tongue = Tongue(player)
    all_sprites.add(tongue)
    grabbies.add(tongue)

    fear_zone = FearZone(player)
    all_sprites.add(fear_zone)
    bumpies.add(fear_zone)

    running = True
    while running:
        
        clock.tick(60)
        player_speed = 2
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q]:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                tongue.attack()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                player.squirt()

        if keys[pygame.K_LEFT] and player.rect.left > 0:
            player.going_left()
            tongue.going_left()
            player.moving_x(-player_speed)
        if keys[pygame.K_RIGHT] and player.rect.right < WIDTH:
            player.going_right()
            tongue.going_right()
            player.moving_x(player_speed)
        if keys[pygame.K_UP] and player.rect.top > 0:
            player.moving_y(-player_speed)
        if keys[pygame.K_DOWN] and player.rect.bottom < DEPTH:
            player.moving_y(player_speed)             

        if tongue.length > 1:
            hit = pygame.sprite.groupcollide(grabbies, yummies, False, True)
            if hit:
                tongue.bullseye()
    
        for i in range(fish_count):
            bump = pygame.sprite.spritecollide(fish_swarm[i], bumpies, False, False)
            if bump:
                if fish_swarm[i].bumped == False:
                    fish_swarm[i].got_bumped()
                    fish_swarm[i].change_course()

        all_sprites.update()

        screen.fill((0, 0, 0)) 
        all_sprites.draw(screen)
        pygame.display.update()
        
    pygame.quit()

main()