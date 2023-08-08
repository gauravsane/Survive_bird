import pygame
from pygame.locals import *
import random

pygame.init()   #initialize pygame

clock = pygame.time.Clock()
fps = 30


screen_x = 870  #width
screen_y = 600  #height

screen = pygame.display.set_mode((screen_x, screen_y))   #display the screen of game
pygame.display.set_caption('Survive Bird')   #title of game

new_icon = pygame.image.load('D:/Python/Hw/Project1/bird1.png')
pygame.display.set_icon(new_icon)


#define font
font = pygame.font.SysFont('Bauhaus 93', 60)
title_font = pygame.font.SysFont('Nordic Light', 80)

#define colors
white = (255, 255, 255)
green = (65, 255, 1)
red = (255, 0, 0)
orange = (235, 103, 1)

#variable of game
ground_scroll = 0
scroll_speed = 5
flying = False
game_over = False
pipe_gap = 180
pipe_frequency = 2000 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
title = "Score: "


#load images
bg_img = pygame.image.load('D:/Python/Hw/Project1/bg1.png')
ground_img = pygame.image.load('D:/Python/Hw/Project1/ground2.png')
button_img = pygame.image.load('D:/Python/Hw/Project1/restartBtn.png')





#display score
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 200
    flappy.rect.y = 260
    score = 0
    return score
    
class Bird(pygame.sprite.Sprite):      #pygame sprite class we used
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)   #inherite some properties of sprite class ex: update,draw
        
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,3):
            img = pygame.image.load(f'D:/Python/Hw/Project1/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() #create rectangle on boundry's of img
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
        


    def update(self):

        #gravity
        if flying == True:
            self.vel += 0.4
            if self.vel > 7:
                self.vel = 7
            if self.rect.bottom < 515:
                self.rect.y += int(self.vel)
                

        if game_over == False:
            #jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                path = 'D:/Python/Hw/Project1/wingsSound.mp3'
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()
                self.vel = -8
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
                
            
            
            
            #handling animations
            self.counter += 1
            flap_cooldown = 6

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotation of bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1.5) #(image , rotating aniticlockwise)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -70)
            
           


#for obstacles
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('D:/Python/Hw/Project1/pipe2.png')
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]


    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


#Restart button
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
                
        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action
        

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(200, 260)
bird_group.add(flappy)

#instance restart button
#button = Button(screen_x // 2 - 50, screen_y //2 - 100, button_img)
button = Button(380, 260, button_img)




run = True
while run:
    clock.tick(fps)
    
    screen.blit(bg_img,(0, 0))    #blit func is used to draw the image with co-ordinates(0,0)


    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    

    #draw ground
    screen.blit(ground_img,(ground_scroll, 515))

    #check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
           and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
           and pass_pipe == False:
           pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False


    #draw and display score
    draw_text(str(score), font, green, 500, 529)
    draw_text(title, font, green, 330, 525)



    #look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
        sound = 'D:/Python/Hw/Project1/die.mp3'
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        
        
        
        


        
    #if bird hits the ground
    if flappy.rect.bottom >= 515:
        game_over = True
        flying = False
        
        
        
        

    if game_over == False and flying == True:
        #new pipes generates
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100,100)
            btm_pipe = Pipe(screen_x, 235 + pipe_height, -1)  
            pipe_group.add(btm_pipe)
            top_pipe = Pipe(screen_x, 280 + pipe_height, 1)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        #draw and scroll ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 30:
            ground_scroll = 0

        pipe_group.update()

    #check for game over and reset
    if game_over == True:
        if button.draw() == True:
            game_over = False
            pygame.mixer.music.stop()
            score = reset_game()
            
    
    
    for event in pygame.event.get():    #this is used for if you click close the window is closed 
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
            
    pygame.display.update()   #this is used for update everything you put in this while loop



pygame.quit()
