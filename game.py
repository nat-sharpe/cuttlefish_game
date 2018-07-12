import pygame
import random


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
        self.length_increment = 18
        self.dist_retract = 1 + (self.length_increment * 2)
        self.hit = False
        self.left = False
        self.right = True
        self.killed = False


    def update(self):
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

    def kill_count(self):
        self.killed = True

    def kill_reset(self):
        self.killed = False

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
        self.dead = False

    def respawn(self):
        self.rect.x = random.randrange(1000, 2000)
        self.rect.y = random.randrange(600)
        self.speedx = random.randrange(-3, -1)
        self.speedy = random.randrange(-2, 2)

    def reset(self):
        self.dead = False

    def update(self):
        if self.swim_count + 1 >= 32:
            self.swim_count = 0
        else:
            self.image = pygame.transform.scale(self.swimming[self.swim_count//8], (45, 30))
            self.swim_count += 1
            
        if self.got_caught and self.tongue.left:
            self.rect = self.image.get_rect()
            self.rect.centerx = self.tongue.rect.left
            self.rect.centery = self.tongue.rect.centery
            if self.tongue.length > 1 and self.tongue.length < 5:
                point_score.play()
            if self.tongue.length == 1:
                self.got_caught = False
                self.respawn()
                self.tongue.kill_count()
        elif self.got_caught and self.tongue.right:
            self.rect = self.image.get_rect()
            self.rect.centerx = self.tongue.rect.right
            self.rect.centery = self.tongue.rect.centery
            if self.tongue.length > 1 and self.tongue.length < 5:
                point_score.play()
            if self.tongue.length == 1:
                self.got_caught = False
                self.respawn()
                self.tongue.kill_count()

        self.time += 1
        if self.time == 2:
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if self.rect.bottom < 0 or self.rect.left > self.width or self.rect.right < 0:
                self.respawn()
            self.time = 0

    def caught(self):
        self.got_caught = True

def main():
    pygame.init()

    WIDTH = 1000
    DEPTH = 600

    screen = pygame.display.set_mode((WIDTH, DEPTH))
    background = pygame.transform.scale(pygame.image.load('underwater.png'), (WIDTH, DEPTH))
    background_rect = background.get_rect()

    pygame.mixer.init()
    slurp = pygame.mixer.Sound('impactsplat08.ogg')
    music = pygame.mixer.Sound('mushroom dance_0.ogg')
    point_score = pygame.mixer.Sound('Coin01.ogg')
    eat_noises = [pygame.mixer.Sound('eat_01.ogg'), pygame.mixer.Sound('eat_02.ogg'), pygame.mixer.Sound('eat_03.ogg'), pygame.mixer.Sound('eat_04.ogg')]
    squirt_noise = pygame.mixer.Sound('impactsplat07.ogg')
    lose_noise = pygame.mixer.Sound('Jingle_Lose_00.ogg')
    win_noise = pygame.mixer.Sound('Jingle_Win_00.ogg')
    countdown = pygame.mixer.Sound('Menu_Navigate_03.ogg')

    clock = pygame.time.Clock()

    time = 0

    keystate = pygame.key.get_pressed()

    font_name = pygame.font.match_font('arial')
    
    def text_draw(surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, ((150, 230, 255)))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def show_start_screen():
        screen.blit(background, background_rect)
        text_draw(screen, 'CUTTLEFISH DO', 80, WIDTH / 2, DEPTH / 4)
        text_draw(screen, 'Arrows to move - Space to eat - Enter to splurt', 40, WIDTH / 2, DEPTH / 2)
        text_draw(screen, 'Press a key to begin', 30, WIDTH / 2, DEPTH * 3/4)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_q]:
                    pygame.quit()
                if event.type  == pygame.KEYUP:
                    waiting = False

    def show_lose_screen():
        lose_noise.play()
        screen.blit(background, background_rect)
        text_draw(screen, 'GAME OVER', 80, WIDTH / 2, DEPTH / 4)
        text_draw(screen, 'Press C to continue', 30, WIDTH / 2, DEPTH * 3/4)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_q]:
                    pygame.quit()
                if event.type == pygame.KEYUP and event.key == pygame.K_c:
                    waiting = False
       

    def show_win_screen():
        win_noise.play()
        screen.blit(background, background_rect)
        text_draw(screen, 'LEVEL COMPLETED', 80, WIDTH / 2, DEPTH / 4)
        text_draw(screen, '%s fish eaten with %s seconds left' % (win_score, time_second), 50, WIDTH / 2, DEPTH / 2)
        text_draw(screen, 'Press C to continue', 30, WIDTH / 2, DEPTH * 3/4)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_q]:
                    pygame.quit()
                if event.type == pygame.KEYUP and event.key == pygame.K_c:
                    waiting = False

    running = True
    game_start = True

    while running:
        player_speed = 3
        keys = pygame.key.get_pressed()

        if game_start:
            show_start_screen()
            game_start = False
            time = 3000
            win_score = 50
            current_score = 0
            time_second = 50
            
            music.play()

            all_sprites = pygame.sprite.Group()
            yummies = pygame.sprite.Group()
            grabbies = pygame.sprite.Group()

            player = Player(140, 80, 100, 500, WIDTH, DEPTH)
            all_sprites.add(player)

            tongue = Tongue(player)
            all_sprites.add(tongue)
            grabbies.add(tongue)

            fish_swarm = {}
            fish_count = 40

            for i in range(fish_count):
                fish_swarm[i] = Food(WIDTH, DEPTH, tongue)
                all_sprites.add(fish_swarm[i])
                yummies.add(fish_swarm[i])
        
        if time == 0:
            show_lose_screen()
            game_start = True


        if current_score == win_score:
            show_win_screen()
            game_start = True

        clock.tick(60)
        
        time -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q]:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not player.mouth_open:
                    slurp.play()
                player.open_mouth()
                tongue.attack() 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                player.squirt()
                squirt_noise.play()

        if keys[pygame.K_LEFT] and player.rect.left > 0:
            player.going_left()
            tongue.going_left()
            player.moving_x(-player_speed)
        if keys[pygame.K_RIGHT] and player.rect.right < WIDTH:
            player.going_right()
            tongue.going_right()
            player.moving_x(player_speed)
        if keys[pygame.K_UP] and player.rect.top > -30:
            player.moving_y(-player_speed)
        if keys[pygame.K_DOWN] and player.rect.bottom < (DEPTH + 30):
            player.moving_y(player_speed)             

        if tongue.length > 1:
            for i in range(fish_count):
                hit = pygame.sprite.spritecollide(fish_swarm[i], grabbies, False, False)
                if hit:
                    tongue.bullseye()
                    fish_swarm[i].caught()
                    if fish_swarm[i].dead:
                        fish_swarm[i].reset()

        if tongue.killed:
            current_score += 1
            tongue.kill_reset()
            eat_noises[random.randrange(0, 4)].play()
            point_score.play()
    

        all_sprites.update()

        screen.blit(background, background_rect)
        all_sprites.draw(screen)

        # text_draw(screen, '%s of %s' % (current_score, win_score), 100, WIDTH / 2, 10)
        # if time > 2939:
        #     text_draw(screen, '1:00', 60, 80, 20)
        # else:
        #     if time % 60 == 0:
        #         time_second -= 1
        #     if time_second > 9:
        #         text_draw(screen, '0:%s' % time_second, 60, 80, 20)
        #     else:
        #         text_draw(screen, '0:0%s' % time_second, 60, 80, 20)

        text_draw(screen, '%s of %s' % (current_score, win_score), 100, WIDTH / 2, 10)
    
        if time % 60 == 0:
            time_second -= 1
            if time_second < 11:
                countdown.play()

        if time_second > 9:
            text_draw(screen, '0:%s' % time_second, 60, 80, 20)
         
        else:
            text_draw(screen, '0:0%s' % time_second, 60, 80, 20)
        
        pygame.display.update()
        
    pygame.quit()

main()