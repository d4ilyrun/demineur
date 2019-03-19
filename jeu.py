import pygame, math, itertools
from menu import *

musique=0
loop=True

def magnitude(v):
    return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))

def sub(u, v):
    return [u[i]-v[i] for i in range(len(u))]

def normalize(v):
    return [v[i]/magnitude(v)  for i in range(len(v))]

pygame.init()
screen = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

path = itertools.cycle([(26, 43), (105, 110), (45, 225), (145, 295), (266, 211), (178, 134), (250, 56), (147, 12)])
target = next(path)
ball, speed = pygame.rect.Rect(target[0], target[1], 10, 10), 3.6
pause_text = pygame.font.SysFont('Consolas', 32).render('Pause', True, pygame.color.Color('White'))

RUNNING, PAUSE = 0, 1
state = RUNNING

background=pygame.image.load("images\\background.jpg").convert()

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: break

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a:                                             quit()
            if e.key == pygame.K_r:                                             retry()
            if e.key == pygame.K_RETURN:                                        state = click(e, state)
            if e.key == pygame.K_p or e.key == pygame.K_ESCAPE:                 state = PAUSE
            if e.key == pygame.K_s and state == PAUSE:                          state = continuer(state)
            if e.key == pygame.K_UP and state==PAUSE:                           menu_touches(e, state, screen)
            if e.key == pygame.K_DOWN and state==PAUSE:                         menu_touches(e, state, screen)

        if e.type == pygame.MOUSEBUTTONDOWN and state==PAUSE:
            state = click(e, state)
        if e.type == pygame.MOUSEMOTION and state==PAUSE:
            curseur(e, state, screen)



    else:
        screen.blit(background, background.get_rect())

        if state == RUNNING:
            target_vector = sub(target, ball.center)
            musique=0

            if magnitude(target_vector) < 2:
                target = next(path)
            else:
                ball.move_ip([c * speed for c in normalize(target_vector)])

            pygame.draw.rect(screen, pygame.color.Color('Yellow'), ball)

        elif state == PAUSE:
                pause(screen, musique)
                musique=1


        pygame.display.flip()
        clock.tick(60)
        continue
    break
    pygame.quit()