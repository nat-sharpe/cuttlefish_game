import pygame
import random

BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    swim_right = [pygame.image.load('R-W1.png'), pygame.image.load('R-W2.png'), pygame.image.load('R-W3.png'), pygame.image.load('R-W2.png')]
    swim_left = [pygame.image.load('L-W1.png'), pygame.image.load('L-W2.png'), pygame.image.load('L-W3.png'), pygame.image.load('L-W2.png')]

    grab_right = [pygame.image.load('R-G1.png'), pygame.image.load('R-G2.png'), pygame.image.load('R-G3.png')]
    grab_left = [pygame.image.load('L-G1.png'), pygame.image.load('L-G2.png'), pygame.image.load('L-G3.png')]

    def __init__(self, fat, tall, x, y, WIDTH, DEPTH):
        pygame.sprite.Sprite.__init__(self)
        self.screen_width = WIDTH
        self.screen_depth = DEPTH
        self.time = 0
        self.fatness = fat
        self.tallness = tall 
        self.image = pygame.transform.scale(self.swim_right[0], (self.fatness, self.tallness))
        self.image.set_colorkey(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_x = 0
        self.move_y = 0
        self.left = False
        self.right = True
        self.squirting = False
        self.squirt_speed = 4
        self.swim_count = 0
        self.eating = False
        self.mouth_open = False

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

    def open_mouth(self):
        self.rect.height = self.tallness
        self.mouth_open = True 

    def eat(self):
        self.mouth_open = False
        self.eating = True
        self.swim_count = 0

    def update(self):
        if self.squirting:
            self.time += 1
            if self.time <= 20:
                self.squirt_left(3, random.randrange(-1, 1))
                self.squirt_right(3, random.randrange(-1, 1))
            elif self.time <= 30:
                self.squirt_left(2, 0)
                self.squirt_right(2, 0)
            elif self.time <= 35:
                self.squirt_left(1, 0)
                self.squirt_right(1, 0)
            else:
                self.time = 0
                self.squirting = False
        

        self.rect.x += self.move_x
        self.rect.y += self.move_y
        self.move_x = 0
        self.move_y = 0

    
        if self.squirting:
            if self.right:
                self.image = pygame.transform.scale(pygame.image.load('L-S1.png'), (self.fatness, self.tallness))
            if self.left:
                self.image = pygame.transform.scale(pygame.image.load('R-S1.png'), (self.fatness, self.tallness))

        if self.mouth_open:    
            if self.right:
                self.image = pygame.transform.scale(self.grab_right[0], (self.fatness, self.tallness))
            if self.left:
                self.image = pygame.transform.scale(self.grab_left[0], (self.fatness, self.tallness))

        elif self.eating:
            if self.swim_count < 5:
                if self.left:
                    self.image = pygame.transform.scale(self.grab_left[1], (self.fatness, self.tallness))
                    self.swim_count += 1
                elif self.right:
                    self.image = pygame.transform.scale(self.grab_right[1], (self.fatness, self.tallness))
                    self.swim_count += 1

            elif self.swim_count >= 5 and self.swim_count < 9:
                if self.left:
                    self.image = pygame.transform.scale(self.grab_left[2], (self.fatness, self.tallness))
                    self.swim_count += 1
                elif self.right:
                    self.image = pygame.transform.scale(self.grab_right[2], (self.fatness, self.tallness))
                    self.swim_count += 1
            else:
                self.eating = False

        elif self.swim_count + 1 >= 32 and not self.squirting:
            self.swim_count = 0
        elif self.left and not self.squirting:
            self.image = pygame.transform.scale(self.swim_left[self.swim_count//8], (self.fatness, self.tallness))
            self.swim_count += 1
        elif self.right and not self.squirting:
            self.image = pygame.transform.scale(self.swim_right[self.swim_count//8], (self.fatness, self.tallness))
            self.swim_count += 1 
    
        
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
        self.tallness = 20
        self.length = 1
        self.image = pygame.transform.scale(pygame.image.load('TONGUE.png'), (self.length, self.tallness))
        self.rect = self.image.get_rect()
        self.player = player
        self.rect.left = self.player.rect.right
        self.rect.centery = self.player.rect.centery
        self.attacking = False
        self.time = 0
        self.speed = 2
        self.length_increment = 12
        self.dist_retract = 1 + (self.length_increment * 2)
        self.hit = False
        self.left = False
        self.right = True

    def update(self):
        if self.attacking:
            self.time += 1
            if self.time == 1:
                self.extend()
            if self.time <= 15:
                if self.hit:
                   self.retract() 
                else:
                    self.extend()
            if self.time > 15:
                self.retract()

        if self.right:
            self.rect = self.image.get_rect()
            self.rect.left = (self.player.rect.right - 30)
            self.rect.centery = self.player.rect.centery

        if self.left:
            self.rect = self.image.get_rect()
            self.rect.right = (self.player.rect.left + 30)
            self.rect.centery = self.player.rect.centery

    def attack(self):
        self.attacking = True
        
    def extend(self):
        self.length += self.length_increment
        self.image = pygame.transform.scale(pygame.image.load('TONGUE.png'), (self.length, self.tallness))            

    def retract(self):
        if self.length > self.length_increment:
            self.length -= self.length_increment
            self.image = pygame.transform.scale(pygame.image.load('TONGUE.png'), (self.length, self.tallness))
        else:
            self.player.eat()
            self.length = 1
            self.image = pygame.transform.scale(pygame.image.load('TONGUE.png'), (self.length, self.tallness))
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
    swimming = [pygame.image.load('FOOD_1.png'), pygame.image.load('FOOD_2.png'), pygame.image.load('FOOD_3.png'), pygame.image.load('FOOD_4.png')]

    def __init__(self, WIDTH, DEPTH, tongue):
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
        self.got_caught = False
        self.tongue = tongue
        self.swim_count = 0

    def respawn(self):
            self.rect.x = random.randrange(1000, 2000)
            self.rect.y = random.randrange(600)
            self.speedx = random.randrange(-2, -1)
            self.speedy = random.randrange(-1, 1)

    def update(self):
        if self.swim_count + 1 >= 32:
            self.swim_count = 0
        else:
            self.image = pygame.transform.scale(self.swimming[self.swim_count//8], (25, 20))
            self.swim_count += 1
        # elif self.right:
        #     self.image = pygame.transform.scale(self.swimming[self.swim_count//8], (25, 20))
        #     self.image = pygame.transform.flip(self.image, False, True)
        #     self.swim_count += 1 
            
        if self.got_caught and self.tongue.left:
            self.rect = self.image.get_rect()
            self.rect.centerx = self.tongue.rect.left
            self.rect.y = self.tongue.rect.y
            if self.tongue.length == 1:
                self.got_caught = False
                self.respawn()
        elif self.got_caught and self.tongue.right:
            self.rect = self.image.get_rect()
            self.rect.centerx = self.tongue.rect.right
            self.rect.y = self.tongue.rect.y
            if self.tongue.length == 1:
                self.got_caught = False
                self.respawn()

        self.time += 1
        if self.time == 3:
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if self.rect.bottom < 0 or self.rect.left > self.width or self.rect.right < 0:
                self.respawn()
            self.time = 0


    # def change_course(self):
    #     self.speedx = -self.speedx
    #     self.speedy = -self.speedy 
    
    # def got_bumped(self):
    #     self.bumped = True
    
    def caught(self):
        self.got_caught = True

# class FearZone(pygame.sprite.Sprite):
#     def __init__(self, player):
#         pygame.sprite.Sprite.__init__(self)
#         self.player = player
#         self.image = pygame.Surface((90, 60))
#         self.image.fill((255, 0, 0))
#         self.image.set_colorkey((255, 0, 0))
#         self.rect = self.image.get_rect()
#         self.rect.centerx = self.player.rect.centerx
#         self.rect.centery = self.player.rect.centery

#     def update(self):
#         self.rect.centerx = self.player.rect.centerx
#         self.rect.centery = self.player.rect.centery


def main():
    pygame.init()

    WIDTH = 1000
    DEPTH = 600

    screen = pygame.display.set_mode((WIDTH, DEPTH))
    background = pygame.transform.scale(pygame.image.load('underwater.png'), (WIDTH, DEPTH))
    background_rect = background.get_rect()

    clock = pygame.time.Clock()

    keystate = pygame.key.get_pressed()

    all_sprites = pygame.sprite.Group()
    yummies = pygame.sprite.Group()
    grabbies = pygame.sprite.Group()
    # bumpies = pygame.sprite.Group()

    player = Player(140, 80, 200, 400, WIDTH, DEPTH)
    all_sprites.add(player)

    tongue = Tongue(player)
    all_sprites.add(tongue)
    grabbies.add(tongue)

    fish_swarm = {}
    fish_count = 50

    for i in range(fish_count):
        fish_swarm[i] = Food(WIDTH, DEPTH, tongue)
        all_sprites.add(fish_swarm[i])
        yummies.add(fish_swarm[i])

    # fear_zone = FearZone(player)
    # all_sprites.add(fear_zone)
    # bumpies.add(fear_zone)

    running = True
    while running:
        
        clock.tick(60)
        player_speed = 3
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q]:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.open_mouth()
                tongue.attack() 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
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
        if keys[pygame.K_DOWN] and player.rect.bottom < (DEPTH + 30):
            player.moving_y(player_speed)             

        # if tongue.length > 1:
        #     hit = pygame.sprite.groupcollide(grabbies, yummies, False, True)
        #     if hit:
        #         tongue.bullseye()

        if tongue.length > 1:
            for i in range(fish_count):
                hit = pygame.sprite.spritecollide(fish_swarm[i], grabbies, False, False)
                if hit:
                    tongue.bullseye()
                    fish_swarm[i].caught()
    
        # for i in range(fish_count):
        #     bump = pygame.sprite.spritecollide(fish_swarm[i], bumpies, False, False)
        #     if bump:
        #         if fish_swarm[i].bumped == False:
        #             fish_swarm[i].got_bumped()
        #             fish_swarm[i].change_course()
        all_sprites.update()

        screen.fill(BLUE)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        pygame.display.update()
        
    pygame.quit()

main()