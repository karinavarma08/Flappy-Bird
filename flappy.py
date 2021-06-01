import pygame
import sys
import random

def draw_ground():
    screen.blit (ground,(ground_x_pos, 560))
    screen.blit (ground,(ground_x_pos + 576, 560))


def create_pipe():       #for creating a new pipe
    random_pipe_position = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_position))
    bottom_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_position-285))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 450:
            screen.blit (pipe_surface, pipe)

        else:
            flip_surface = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_surface,pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False   #game_Active which is set to true will return now flase if collided

        if bird_rect.top <= -100 or  bird_rect.bottom >= 580:
            return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement* 3,1)
    return new_bird



def animation_bird():
    new_bird= bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect (center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(f'Score : {int (score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (288,120))
        screen.blit(score_surface,score_rect)

    if game_state == "game_over":
        high_score_surface = game_font.render (f'Score : {int (score)}', True, (255, 255, 255))
        high_score_rect =   high_score_surface.get_rect (center=(288, 150))
        screen.blit (  high_score_surface, high_score_rect)

        high_score_surface = game_font.render (f'High Score : {int (high_score)}', True, (255, 255, 255))
        high_score_rect =   high_score_surface.get_rect (center=(288, 390))
        screen.blit (  high_score_surface, high_score_rect)

def score_update(score,high_score):
    if score> high_score:
        high_score = score

    return high_score

# pygame.mixer.pre_init(frequency=44100, size= 16, channels= 2, buffer = 256)
pygame.init()
# game variable
gravity = 0.15
bird_movement = 0
screen_width=576
screen_height=650
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
bg_screen = pygame.image.load('Sprites/Gallery/light.jpg').convert()
ground= pygame.image.load('Sprites/Gallery/mudy.png').convert()
ground = pygame.transform.scale2x(ground)
ground_x_pos = 0

game_font = pygame.font.Font("04b19.ttf", 40)
score=0
high_score=0

bird_downflap = pygame.transform.scale2x(pygame.image.load('Sprites/Gallery/redbird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('Sprites/Gallery/redbird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('Sprites/Gallery/redbird-upflap.png').convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,325))


# birds  = pygame.image.load('Sprites/Gallery/yellowbird-midflap.png').convert_alpha()
# birds = pygame.transform.scale2x(birds)
# bird_rect = birds.get_rect(center=(100,325))
pipe_surface = pygame.image.load('Sprites/Gallery/pipe-green_50.png').convert()
pipe_surface  = pygame.transform.scale2x(pipe_surface)
pipe_height = (330,350,380)

pipe_list = []
PIPING = pygame.USEREVENT
pygame.time.set_timer(PIPING,1300)
game_active = True

BIRDING = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDING,300)

game_over_surface = pygame.image.load("Sprites/Gallery/gameover.png").convert_alpha()
game_over_surface_rect  = game_over_surface.get_rect(center = (288,325))

flap_sound = pygame.mixer.Sound("Sprites/Audio/Swoosh.mp3")
die_sound = pygame.mixer.Sound("Sprites/Audio/hit.mp3")


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and game_active == False:
                game_active = True
                bird_rect.center = (100,325)
                pipe_list.clear()
                bird_movement = 0
                score = 0



        if event.type == PIPING:
            pipe_list.extend(create_pipe())

        if event.type == BIRDING:
           if bird_index < 2:
                bird_index += 1

           else:
                bird_index = 0

           bird_surface,bird_rect = animation_bird()


#background
    screen.blit(bg_screen,(0,0))

#bird
    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active  = check_collision(pipe_list)

    #pipes

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display("main_game")

    else:
        high_score = score_update(score,high_score)
        score_display("game_over")
        screen.blit(game_over_surface,game_over_surface_rect)
        die_sound.play()
#ground
    screen.blit (ground, (ground_x_pos, 560))
    ground_x_pos -= 1
    draw_ground ()
    if ground_x_pos <= -576:
        ground_x_pos = 0

    pygame.display.update()
    clock.tick(120)