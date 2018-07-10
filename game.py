import pygame
pygame.init()
WIDTH = 1000
DEPTH = 600
screen = pygame.display.set_mode((WIDTH, DEPTH))
clock = pygame.time.Clock()
keystate = pygame.key.get_pressed()

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

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.left = self.player.rect.right
        self.rect.centery = self.player.rect.centery

        if self.attacking:
            self.time += 1
            if self.time == 1:
                self.extend()
            elif self.time % self.speed == 0 and self.time <= (self.speed * self.dist_extend):
                self.extend()
            elif self.time % self.speed == 0 and self.time > (self.speed * self.dist_extend) and self.time <= (self.speed * self.dist_retract):
                self.retract()
            elif self.time > (self.speed * self.dist_retract):
                self.attacking = False
                self.time = 0


    def attack(self):
        self.attacking = True
        
    def extend(self):
        self.length += 10
        self.image = pygame.transform.scale(self.image, (self.length, 5))

    def retract(self):
        self.length -= 10
        self.image = pygame.transform.scale(self.image, (self.length, 5))

class Food(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.fatness = 25
        self.tallness = 20
        self.image = pygame.Surface([self.fatness, self.tallness])
        self.image.fill((255, 200, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 300

    def update(self):   
        pass

def main():

    player = Player(40, 40, 200, 400)
    tongue = Tongue(player)
    fish = Food()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(tongue)
    all_sprites.add(fish)

    yummies = pygame.sprite.Group()
    yummies.add(fish)

    grabbies = pygame.sprite.Group()
    grabbies.add(tongue)


    running = True
    while running:
        
        clock.tick(60)
        speed = 2

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q]:
                running = False

        hits = pygame.sprite.groupcollide(grabbies, yummies, False, False)

        if hits:
            fish.kill()

        if keys[pygame.K_LEFT] and player.rect.left > 0:
            player.moving_x(-speed)
        if keys[pygame.K_RIGHT] and player.rect.right < WIDTH:
            player.moving_x(speed)
        if keys[pygame.K_UP] and player.rect.top > 0:
            player.moving_y(-speed)
        if keys[pygame.K_DOWN] and player.rect.bottom < DEPTH:
            player.moving_y(speed)

        if keys[pygame.K_SPACE]:
            tongue.attack()             

        all_sprites.update()

        screen.fill((0, 0, 0)) 
        all_sprites.draw(screen)
        pygame.display.update()
        
    pygame.quit()

main()