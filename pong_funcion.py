# Carola Adrados Herrero 18001
# Juan Berenguer Triana 19036
# Sergio Gómez Montes 18150

# Autor: Carola Adrados

import pygame
import random
import time
from pygame.locals import *

def pong(dif):
    
    pygame.init()
    
    run = True
    clock = pygame.time.Clock()
    fps = 30
    
    #return función juego
    ganado = False
    
    if dif == "Fácil":
        vel_palas = 15
        vel_pala2 = 10
        vel_bola = 10
        limpunt = 10
        dificultad = 0.4
    elif dif == "Normal":
        vel_palas = 15
        vel_pala2 = 15
        vel_bola = 15
        limpunt = 10
        dificultad = 0.2
    elif dif == "Difícil":
        vel_palas = 10
        vel_pala2 = 15
        vel_bola = 15
        limpunt = 10
        dificultad = 0.1
    elif dif == "Imposible":
        vel_palas = 10
        vel_pala2 = 15
        vel_bola = 15
        limpunt = 10
        dificultad = 0.05
    else:
        print ("ERROR: dificultad no válida")
        return ganado


    # Colores
    white = (255, 255, 255)
    black = (0, 0, 0)

    #Fuente
    font_game = pygame.font.SysFont("Atari Classic", 30)

    

    # clases objetos juego
    class pala(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([10, 50])
            self.image.fill(white)
            self.rect = self.image.get_rect()
            self.points = 0





    class bola(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([10, 10])
            self.image.fill(white)
            self.rect = self.image.get_rect()
            self.speed = 15 
            self.dx = 1
            self.dy = 1

    

    # Refresh de la pantalla
    def redraw():
    
        # invocación del vacío -- ventana negra
        vent.fill(black)
    
        # título
        text = font_game.render('PONG', False, white)
        textRect = text.get_rect()
        textRect.center = (750 // 2, 25)
        vent.blit(text, textRect)
    
        # puntuación de jugador
        p1_score = font_game.render(str(pala1.points), False, white)
        p1Rect = p1_score.get_rect()
        p1Rect.center = (50, 50)
        vent.blit(p1_score, p1Rect)
    
        # puntuación de la computadora
        p2_score = font_game.render(str(pala2.points), False, white)
        p2Rect = p2_score.get_rect()
        p2Rect.center = (700, 50)
        vent.blit(p2_score, p2Rect)
    
        # actualizar los objetos
        all_sprites.draw(vent)
    
        # dibujar las actualizaciones
        pygame.display.update()
        




    # Ventana
    vent = pygame.display.set_mode((750, 500))
    pygame.display.set_caption('Pong')

    # creación de objetos
    pala1 = pala()
    pala1.rect.x = 25
    pala1.rect.y = 225

    pala2 = pala()
    pala2.rect.x = 715
    pala2.rect.y = 225

    pong = bola()
    pong.rect.x = 375
    pong.rect.y = 250
    pong.speed = vel_bola
    
    # agrupar objetos
    all_sprites = pygame.sprite.Group()
    all_sprites.add(pala1, pala2, pong)

    run = True
    # Loop del juego
    while run:
    
        clock.tick(fps)
    
        # salir del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False     
          
        # movimiento del jugador
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            pala1.rect.y += -vel_palas
        if key[pygame.K_s]:
            pala1.rect.y += vel_palas
            
        #movimiento de la computadora
        if random.random() < dificultad:
            if pala2.rect.y < pong.rect.y:
                pala2.rect.y += (vel_pala2 - 5)
            if pala2.rect.y > pong.rect.y:
                pala2.rect.y -= (vel_pala2 - 5)
        else:
            if pala2.rect.y < pong.rect.y:
                pala2.rect.y += vel_pala2 + 5
            if pala2.rect.y > pong.rect.y:
                pala2.rect.y -= vel_pala2 + 5
                 
        # mover la pelota
        pong.rect.x += pong.speed * pong.dx
        pong.rect.y += pong.speed * pong.dy
    
        # rebotes contra pared y palas
        if pong.rect.y > 490:
            pong.dy = -1
    
        if pong.rect.y < 1:
            pong.dy = 1
    
        if pong.rect.x > 740:
            pong.rect.x, pong.rect.y = 375, 250
            pong.dx = -1
            pala1.points += 1
    
        if pong.rect.x < 1:
            pong.rect.x, pong.rect.y = 375, 250
            pong.dx = 1
            pala2.points += 1
    
        if pala1.rect.colliderect(pong.rect):
            pong.dx = 1
    
        if pala2.rect.colliderect(pong.rect):
            pong.dx = -1
    
        # ganar el juego
        if pala1.points == limpunt:
            ganado = True
            run = False

        # actualización con redraw
        redraw()
        
        #si pierdes salir del juego
        if pala2.points == limpunt:
            run = False

        clock.tick(fps)
        
    time.sleep(1)
    
    if ganado:
        vent.fill(black)
        texto1 = font_game.render("Has ganado :)", 1, white)
        vent.blit(texto1, [750 / 3+40,500 / 3])
        texto2=font_game.render("Pulsa cualquier tecla para continuar.", 1, white)
        vent.blit(texto2, [750 / 4, 500 / 3+40])
    else:
        vent.fill(black)
        texto1 = font_game.render("Has perdido :(", 1, white)
        vent.blit(texto1, [750 / 3+40,500 / 3])
        texto2=font_game.render("Pulsa cualquier tecla para continuar.", 1, white)
        vent.blit(texto2, [750 / 4, 500 / 3+40])
        
    pygame.display.update()   
                
    time.sleep(1)
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                run = False
    
    pygame.quit()
    
    # if ganado:
    #     return ganado, pala1.points, "Nivel superado ( Puntos Player 1: " + str(pala1.points) + " Puntos Player 2: " + str(pala2.points)
    # else:
    #     return ganado, pala1.points,  "Nivel no superado ( Puntos Player 1: " + str(pala1.points) + " Puntos Player 2: " + str(pala2.points) 
    
    return ganado, pala1.points

def men_pong(ganado, punt):
    
    if int(ganado):
        return "Nivel superado\nPuntos conseguidos: " + str(punt)
    else:
        return "Nivel no superado\nPuntos conseguidos: " + str(punt)

# [a,b] = pong("Fácil")
# print(str(a) + " " + str(b))