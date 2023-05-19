# Carola Adrados Herrero
# Juan Berenguer Triana
# Sergio Gómez Montes

# Autor: Juan Berenguer

import pygame
from pygame.locals import *

import sys
import random
import time

# Juego
def runner(dif):

    running = True
    
    clock = pygame.time.Clock()
    fps = 30
    
    # Dimensiones grada
    grada_height = 120
    
    # Dimensiones pantalla
    screen_width = 800
    screen_height = 480
    
    # Dimensiones runner
    sprite_dim = 32
    
    # Variable que indica si se ha superado el nivel
    ganado = False
    
    # Diferentes dificultades
    if dif == "Fácil":
        obs_speed = 3
        n_obs = 10
        ratio = 10
        obs_dist = 10
    elif dif == "Normal":
        obs_speed = 5
        n_obs = 20
        ratio = 5
        obs_dist = 9
    elif dif == "Difícil":
        obs_speed = 7
        n_obs = 30
        ratio = 4
        obs_dist = 8
    elif dif == "Imposible":
        obs_speed = 10
        n_obs = 50
        ratio = 3
        obs_dist = 7
    else:
        print("ERROR: Dificultad no válida")
        return ganado
        
    opening_factor = 2
    
    moving_height = 5
    
    vida = 100
    vida_flag = False
    aplastamiento_flag = False
    punt = 0
    
    obs = []
    obs_ind = []
    
    del_flag = False
    obs_del = []
    
    animationCount = 0
    
    col_prec = sprite_dim
    
    txt_height = -50
    
    # Imágenes para la animación del runner
    img1 = "Archivos_Runner/Runners_1.png"
    img2 = "Archivos_Runner/Runners_2.png"
    img3 = "Archivos_Runner/Runners_3.png"
    
    images = [img1, img3, img2, img3]
    
    x_factor = 1
    
    class Runner:
        
        def __init__(self, x_speed, y_speed):
            
            self.img = 0
            
            self.sprite = pygame.image.load(images[self.img])
            self.sprite = pygame.transform.scale(self.sprite, (x_factor*sprite_dim, sprite_dim))
            self.sprite.convert_alpha()
            
            self.abs_speed = [x_speed, y_speed]
            self.speed = self.abs_speed
            
            self.rect = self.sprite.get_rect()
            self.rect.centerx = screen_width / 2
            self.rect.centery = screen_height / 2 + grada_height
            
            self.col_flag = False
            self.aplastamiento_flag = False
        
        def update(self):
            
            if event.key == pygame.K_RIGHT:
                self.speed[0] = self.abs_speed[0]
            elif event.key == pygame.K_LEFT:
                self.speed[0] = -self.abs_speed[0]
            elif event.key == pygame.K_DOWN:
                self.speed[1] = self.abs_speed[1]
            elif event.key == pygame.K_UP:
                self.speed[1] = -self.abs_speed[1]
            
            if self.rect.left <= 0:
                self.speed[0] = 1
            elif self.rect.right >= screen_width:
                self.speed[0] = -1
            elif self.rect.top <= grada_height:
                self.speed[1] = 1
            elif self.rect.bottom >= screen_height + grada_height:
                self.speed[1] = -1
            
            self.rect.move_ip(self.speed)
        
        def collision(self, obstacle):
            
            self.speed = [0,0]
            
            if self.rect.colliderect(obstacle.rect):
                
                self.dist = [self.rect.right-obstacle.rect.left - col_prec, obstacle.rect.right-self.rect.left - col_prec, obstacle.rect.bottom-self.rect.top - col_prec, self.rect.bottom-obstacle.rect.top - col_prec]
                
                if self.dist[0] < 0:
                    self.speed[0] = -3*obs_speed
                elif self.dist[1] < 0:
                    self.speed[0] = 3*obs_speed
                elif self.dist[2] < 0:
                    self.speed[1] = 3*obs_speed
                elif self.dist[3] < 0:
                    self.speed[1] = -3*obs_speed
                
                self.col_flag = True
                self.rect.move_ip(self.speed)
                
                if self.rect.right < sprite_dim/2:
                    self.aplastamiento_flag = True
                else:
                    self.aplastamiento_flag = False
                
            else:
                
                self.col_flag = False
                
        def animation(self):
            
            self.img = (self.img + 1)%4
            self.sprite = pygame.image.load(images[self.img])
            self.sprite = pygame.transform.scale(self.sprite, (x_factor*sprite_dim, sprite_dim))
            self.sprite.convert_alpha()
                
    class BasicObstacle:
        
        def __init__(self, x_speed, left, top, bottom):
            
            self.sprite = pygame.image.load("Archivos_Runner/Log.png")
            self.sprite = pygame.transform.scale(self.sprite, (sprite_dim, bottom-top))
            self.sprite.convert()
            
            self.abs_speed = [x_speed, 0]
            self.speed = self.abs_speed
            
            self.rect = self.sprite.get_rect()
            self.rect.centerx = left + sprite_dim/2
            self.rect.centery = (top+bottom)/2 + grada_height
            
        def update(self):
            
            if self.rect.right < 0:
                obs_del.append(i)
                self.flag = True
            else:
                self.flag = False
                
            self.rect.move_ip(self.speed)
    
    class MovingObstacle:
        
        def __init__(self, x_speed, y_speed, left, pos):
            
            self.sprite = pygame.image.load("Archivos_Runner/Log.png")
            self.sprite = pygame.transform.scale(self.sprite, (sprite_dim, moving_height*sprite_dim))
            self.sprite.convert()
            
            self.abs_speed = [x_speed, y_speed]
            self.speed = self.abs_speed
            
            self.rect = self.sprite.get_rect()
            self.rect.centerx = left + sprite_dim/2
            self.rect.centery = pos + grada_height
            
        def update(self):
            
            if self.rect.right < 0:
                obs_del.append(i)
                self.flag = True
            else:
                self.flag = False
            
            if self.rect.top <= grada_height:
                self.speed[1] = -self.speed[1]
            elif self.rect.bottom >= screen_height + grada_height:
                self.speed[1] = -self.speed[1]
            
            self.rect.move_ip(self.speed)
    
    class Trofeo:
        
        def __init__(self, x_speed, left):
            
            self.sprite = pygame.image.load("Archivos_Runner/Trophy.png")
            self.sprite = pygame.transform.scale(self.sprite, (5*sprite_dim, 6*sprite_dim))
            self.sprite.convert()
            
            self.abs_speed = [x_speed, 0]
            self.speed = self.abs_speed
            
            self.rect = self.sprite.get_rect()
            self.rect.centerx = left + 5*sprite_dim/2
            self.rect.centery = screen_height/2 + grada_height
            
            self.trophy_flag = False
        
        def update(self):
            
            if self.rect.centerx < screen_width/2:
                self.rect.centerx = screen_width/2
                self.speed = [0,0]
            
            self.rect.move_ip(self.speed)
        
        def collision(self, runner):
            
            if self.rect.colliderect(runner.rect):
                self.trophy_flag = True
            else:
                self.trophy_flag = False
    
    # Inicializar el juego
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height + grada_height))
    pygame.display.set_caption("Runner")
    
    pygame.key.set_repeat(fps)
    
    # Imágenes de fondo y actualizar pantalla
    
    bg = pygame.image.load("Archivos_Runner/Grass.png")
    bg = pygame.transform.scale(bg, (screen_width, screen_height))
    bg.convert()
    screen.blit(bg, (0,grada_height))
    
    grada = pygame.image.load("Archivos_Runner/Grada.jpg")
    grada = pygame.transform.scale(grada, (screen_width, grada_height))
    grada.convert()
    screen.blit(grada, (0,0))
    
    # Fuentes usadas en todo el juego
    score_font = pygame.font.SysFont("Atari Classic", 90)
    intro_font = pygame.font.SysFont("Atari Classic", 45)
    
    # Mensaje inicial
    score = score_font.render("RUNNER",True,'Red','Black')
    scoreRect = score.get_rect()
    scoreRect.center = [screen_width/2, grada_height/2]
    screen.blit(score, scoreRect)
    
    intro1 = intro_font.render("Alcanza el trofeo para pasar el nivel",True,'White')
    intro1Rect = intro1.get_rect()
    intro1Rect.center = [screen_width/2, screen_height/2 - 120 + txt_height + grada_height]
    screen.blit(intro1, intro1Rect)
    
    intro2 = intro_font.render("Tocar los obstáculos o los límtes de",True,'White')
    intro2Rect = intro2.get_rect()
    intro2Rect.center = [screen_width/2, screen_height/2 - 60 + txt_height + grada_height]
    screen.blit(intro2, intro2Rect)
    
    intro3 = intro_font.render("la pantalla te hará perder vida",True,'White')
    intro3Rect = intro3.get_rect()
    intro3Rect.center = [screen_width/2, screen_height/2 - 30 + txt_height + grada_height]
    screen.blit(intro3, intro3Rect)
    
    intro4 = intro_font.render("Si quedas aplastado entre un",True,'White')
    intro4Rect = intro4.get_rect()
    intro4Rect.center = [screen_width/2, screen_height/2 + 30 + txt_height + grada_height]
    screen.blit(intro4, intro4Rect)
    
    intro5 = intro_font.render("obstáculo y los límites de la",True,'White')
    intro5Rect = intro5.get_rect()
    intro5Rect.center = [screen_width/2, screen_height/2 + 60 + txt_height + grada_height]
    screen.blit(intro5, intro5Rect)
    
    intro6 = intro_font.render("pantalla perderás toda tu vida",True,'White')
    intro6Rect = intro6.get_rect()
    intro6Rect.center = [screen_width/2, screen_height/2 + 90 + txt_height + grada_height]
    screen.blit(intro6, intro6Rect)
    
    intro7 = intro_font.render("Pulsa cualquier tecla para continuar",True,'White')
    intro7Rect = intro7.get_rect()
    intro7Rect.center = [screen_width/2, screen_height/2 + 210 + txt_height + grada_height]
    screen.blit(intro7, intro7Rect)
    
    pygame.display.flip()
    
    time.sleep(1)
    
    # No se pasa de pantalla hasta que no se pulse cualquier tecla
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False
    
    # Runner
    runner = Runner(5,10)
    
    # Obstáculos (dos tipos: moving y basic)
    for i in range(0, n_obs):
        
        # 0 ==> moving
        # Otra cosa ==> basic
        tipo = random.randint(0, ratio)
        
        if tipo == 0:
            
            speed_y = random.randint(1,3)
            start_pos = random.randint(moving_height*sprite_dim, screen_height-moving_height*sprite_dim)
            
            obs.append(MovingObstacle(-obs_speed, speed_y*obs_speed, screen_width + obs_dist*i*sprite_dim, start_pos))
            obs_ind.append(len(obs)-1)
            
        else:
            
            # Número de aperturas en el obstáculo
            n_openings = random.randint(1, 3)    
            openings = []
            
            for j in range(0, n_openings):
                
                # Colocación de las aperturas en el espacio
                openings.append(random.randint(opening_factor*sprite_dim/2, screen_height-opening_factor*sprite_dim/2))
                for k in range(0, j):
                    if k != j:
                        while abs(openings[j]-openings[k]) < sprite_dim*2:
                            openings[j] = random.randint(opening_factor*sprite_dim/2, screen_height-opening_factor*sprite_dim/2)
            
            openings.sort()
            
            # Creación de los obstáculos (número de aperturas + 1)
            top = 0
            for j in range(0, n_openings):
                bottom = openings[j] - opening_factor*sprite_dim/2
                if bottom - top > sprite_dim/2:
                    obs.append(BasicObstacle(-obs_speed, screen_width + obs_dist*i*sprite_dim, top, bottom))
                    obs_ind.append(len(obs)-1)
                top = bottom + opening_factor*sprite_dim
            bottom = screen_height
            obs.append(BasicObstacle(-obs_speed, screen_width + obs_dist*i*sprite_dim, top, bottom))
            obs_ind.append(len(obs)-1)
    
    # Trofeo final (condición para superar el nivel)
    trophy = Trofeo(-obs_speed, screen_width + obs_dist*(n_obs+2)*sprite_dim)
    
    # Bucle principal del juego
    
    running = True
    
    while running:
        
        # Colisiones y vida
        if n_obs - punt:
            for i in obs_ind:
                runner.collision(obs[i])
                if runner.col_flag:
                    vida_flag = True
                if runner.aplastamiento_flag:
                    aplastamiento_flag = True
            if vida_flag:
                vida = vida - 1
                vida_flag = False
            if aplastamiento_flag:
                vida = 0
                aplastamiento_flag = False
        # Condición de ganar el juego (tocar el trofeo)
        else:
            trophy.collision(runner)
            if trophy.trophy_flag:
                ganado = True
                running = False
        
        # Eliminar obstáculos
        for i in obs_ind:
            obs[i].update()
            if obs[i].flag:
                del_flag = True
        if del_flag:
            for i in range(0,len(obs_del)):
                obs_ind.remove(obs_del[i])
            obs_del = []
            del_flag = False
            punt = punt + 1

        # Actualizar pantalla, puntuación y vida
        
        screen.blit(bg, (0,grada_height))
        screen.blit(grada, (0,0))
        
        score = intro_font.render("Obstáculos restantes: " + str(n_obs-punt),True,'Red','Black')
        scoreRect = score.get_rect()
        scoreRect.center = [screen_width/4, grada_height/2]
        screen.blit(score, scoreRect)
        
        healthRect = pygame.Rect(0, 0, 310, 30)
        healthRect.center = [3*screen_width/4, grada_height/2]
        pygame.draw.rect(screen,'White',healthRect)
        
        barRect = pygame.Rect(0, 0, 3*vida, 20)
        barRect.center = [3*screen_width/4 - (300-vida*3)/2, grada_height/2]
        pygame.draw.rect(screen,((1-vida*0.01)*255,vida*0.01*255,0),barRect)
        
        trophy.update()
        
        for i in obs_ind:
            screen.blit(obs[i].sprite, obs[i].rect)
        screen.blit(runner.sprite, runner.rect)
        screen.blit(trophy.sprite, trophy.rect)
        
        pygame.display.flip()
        
        # Salir del juego y actualizar runner
        if vida == 0:
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                runner.update()
        
        # Cambiar el sprite (animación)
        animationCount = animationCount + 1
        if animationCount == 10:
            animationCount = 0
            runner.animation()
        
        clock.tick(fps)
    
    time.sleep(1)
    
    # Actualizar pantalla
    screen.blit(bg, (0,grada_height))
    screen.blit(grada, (0,0))
    
    # Mensaje final (cambio dependiendo de si se ha superado el nivel o no)
    
    score = score_font.render("RUNNER",True,'Red','Black')
    scoreRect = score.get_rect()
    scoreRect.center = [screen_width/2, grada_height/2]
    screen.blit(score, scoreRect)
    
    if ganado:
    
        intro1 = intro_font.render("Buen trabajo",True,'White')
        intro1Rect = intro1.get_rect()
        intro1Rect.center = [screen_width/2, screen_height/2 - 60 + txt_height + grada_height]
        screen.blit(intro1, intro1Rect)
        
        intro2 = intro_font.render("Nivel superado",True,'White')
        intro2Rect = intro2.get_rect()
        intro2Rect.center = [screen_width/2, screen_height/2 + txt_height + grada_height]
        screen.blit(intro2, intro2Rect)
        
        intro3 = intro_font.render("Vida restante: " + str(vida) + "%",True,'White')
        intro3Rect = intro3.get_rect()
        intro3Rect.center = [screen_width/2, screen_height/2 + 60 + txt_height + grada_height]
        screen.blit(intro3, intro3Rect)
                
    else:
        
        intro1 = intro_font.render("Mala suerte",True,'White')
        intro1Rect = intro1.get_rect()
        intro1Rect.center = [screen_width/2, screen_height/2 - 60 + txt_height + grada_height]
        screen.blit(intro1, intro1Rect)
        
        intro2 = intro_font.render("Nivel no superado",True,'White')
        intro2Rect = intro2.get_rect()
        intro2Rect.center = [screen_width/2, screen_height/2 + txt_height + grada_height]
        screen.blit(intro2, intro2Rect)
        
        intro3 = intro_font.render("Obstáculos superados: " + str(punt) + "/" + str(n_obs),True,'White')
        intro3Rect = intro3.get_rect()
        intro3Rect.center = [screen_width/2, screen_height/2 + 60 + txt_height + grada_height]
        screen.blit(intro3, intro3Rect)
    
    intro4 = intro_font.render("Pulsa cualquier tecla para continuar",True,'White')
    intro4Rect = intro4.get_rect()
    intro4Rect.center = [screen_width/2, screen_height/2 + 180 + txt_height + grada_height]
    screen.blit(intro4, intro4Rect)
    
    pygame.display.flip()
    
    time.sleep(1)
    
    # No se sale del juego hasta que no se pulse cualquier tecla
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False
    
    pygame.quit()
    
    # La función devuelve el parámetro ganado
    # En caso de superar el nivel, también se devuelve la vida restante
    if ganado:
        return ganado, vida
    # En caso de no superar el nivel, también se devuelve la puntuación (número de obstáculos superados)
    else:
        return ganado, punt

# Mensaje del resultado en el menú
def men_runner(ganado, punt):
    
    if int(ganado):
        return "Nivel superado\n" + str(punt) + "% de vida restante"
    else:
        return "Nivel no superado\n" + str(punt) + " obstáculos superados"
