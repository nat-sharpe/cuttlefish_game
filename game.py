import pygame
import math
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

    def update(self, keys):   
        self.move_x = 0
        self.move_y = 0

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.move_x = -10
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.move_x = 10
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.move_y = -10
        if keys[pygame.K_DOWN] and self.rect.bottom < DEPTH:
            self.move_y = 10

        # changes player's position to next move spot
        self.rect.x += self.move_x
        self.rect.y += self.move_y
        
class Other(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.fatness = 1
        self.tallness = 5
        self.image = pygame.Surface([self.fatness, self.tallness])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.player = player

        self.rect.left = self.player.rect.right
        self.rect.centery = self.player.rect.centery

    def update(self, keys):
        self.rect.left += self.player.move_x
        self.rect.centery += self.player.move_y
        if keys[pygame.K_SPACE]:
            self.extend()
        else:
            self.retract()
      
    def extend(self):
        self.image = pygame.transform.scale(self.image, (100, 5))

    def retract(self):
        self.image = pygame.transform.scale(self.image, (1, 5))

#  def update(self, keys):
#         self.image = pygame.transform.scale(self.image, (5, 5))
#         self.rect.left += self.player.move_x
#         self.rect.centery += self.player.move_y
#         if keys[pygame.K_SPACE] and self.length < 500:
#             self.length += self.length
#             self.extend()
#         else:  
#             self.length = self.fatness
    
#     def extend(self):
#         self.image = pygame.transform.scale(self.image, (self.length, 5))

#     # def retract(self):
#     #     self.image = pygame.transform.scale(self.image, (1, 5))

def main():
    player = Player(40, 40, 200, 400)
    tongue = Other(player)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(tongue)


    running = True
    while running:
        
        clock.tick(60)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q]:
                running = False

        all_sprites.update(keys)

        screen.fill((0, 0, 0)) 
        all_sprites.draw(screen)
        pygame.display.update()
        
    pygame.quit()

main()