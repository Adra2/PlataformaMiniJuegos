# Carola Adrados Herrero 18001
# Juan Berenguer Triana 19036
# Sergio Gómez Montes 18150

# Autor: Juan Berenguer

import pygame
from pygame.locals import *

import sys
import random
import time
import math

# Juego
def catch(dif):

    running = True
    
    clock = pygame.time.Clock()
    fps = 30
    
    # Dimensiones de la ventana
    screen_width = 600
    screen_height = 700
    
    # Número de nubes en la parte superior
    big_clouds = 4
    small_clouds = 10
    
    top_height = 100
    bot_height = 100
    
    # Dimensiones leprechaun
    leprechaun_dim = [80,120]
    
    # Dimensiones nubes
    cloud_dim_x = 200
    cloud_dim_y = 75
    
    # Dimensiones monedas
    coin_dim = 50
    
    # Variable que indica si se ha superado el nivel
    ganado = False
    
    # Diferentes dificultades
    if dif == "Fácil":
        obj_speed = 3
        n_obj = 20
        max_speed = 2
        ratio = 4
    elif dif == "Normal":
        obj_speed = 4
        n_obj = 30
        max_speed = 3
        ratio = 3
    elif dif == "Difícil":
        obj_speed = 5
        n_obj = 40
        max_speed = 4
        ratio = 2
    elif dif == "Imposible":
        obj_speed = 10
        n_obj = 50
        max_speed = 4
        ratio = 1
    else:
        print("ERROR: Dificultad no válida")
        return ganado
    
    obj = []
    obj_ind = []
    
    del_flag = False
    obj_del = []
    
    txt_height = -50
    
    # Diferentes imágenes para los tipos de objetos
    gold = "Archivos_Catch/Gold.png"
    silver = "Archivos_Catch/Silver.png"
    bronze = "Archivos_Catch/Bronze.png"
    rock = "Archivos_Catch/Rock.png"
    
    img = [rock, bronze, silver, gold]
    
    # Controlar el ratio de aparición de rocas
    tipos = [0]
    tipos.extend([1]*ratio)
    tipos.extend([2]*ratio)
    tipos.extend([3]*ratio)
    
    # Puntuaciones
    puntuacion = 0
    puntuacion_total = 0
    puntuacion_objetivo = 0
    
    # Diferentes imágenes para el leprechaun
    img1 = "Archivos_Catch/Leprechaun_1.png"
    img2 = "Archivos_Catch/Leprechaun_2.png"
    
    class Leprechaun:
        
        def __init__(self, x_speed):
            
            self.img = 0
            
            self.sprite = pygame.image.load(img1)
            self.sprite = pygame.transform.scale(self.sprite, leprechaun_dim)
            self.sprite.convert_alpha()
            
            self.abs_speed = x_speed
            self.speed = self.abs_speed
            
            self.rect = self.sprite.get_rect()
            self.rect.centerx = screen_width / 2
            self.rect.bottom = screen_height - bot_height + leprechaun_dim[1]/3
            
            self.col_flag = False
        
        def update(self):
            
            if event.key == pygame.K_RIGHT:
                self.speed = self.abs_speed
            elif event.key == pygame.K_LEFT:
                self.speed = -self.abs_speed
            
            if self.rect.left <= 0:
                self.rect.right = screen_width
            elif self.rect.right >= screen_width:
                self.rect.left = 0
            
            self.rect.move_ip([self.speed, 0])
        
        def collision(self, obstacle):
            if self.rect.colliderect(obstacle.rect):
                self.col_flag = True
            else:
                self.col_flag = False
                
        def animation(self):
            if self.speed > 0:
                self.sprite = pygame.image.load(img2)
                self.sprite = pygame.transform.scale(self.sprite, leprechaun_dim)
                self.sprite.convert_alpha()
            else:
                self.sprite = pygame.image.load(img1)
                self.sprite = pygame.transform.scale(self.sprite, leprechaun_dim)
                self.sprite.convert_alpha()
    
    class BasicCoin:
        
        def __init__(self, y_speed, pos, value):
            
            self.sprite = pygame.image.load(img[value])
            self.sprite = pygame.transform.scale(self.sprite, (coin_dim, coin_dim))
            self.sprite.convert()
            
            self.abs_speed = y_speed
            self.speed = self.abs_speed
            
            self.rect = self.sprite.get_rect()
            self.rect.center = pos
            
            self.punt = value
            if self.punt == 0:
                self.punt = -3
            
        def update(self):
            
            if self.rect.bottom > screen_height:
                self.flag = True
            else:
                self.flag = False
                
            self.rect.move_ip([0, self.speed])
    
    # Inicializar el juego
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Catch")
    
    pygame.key.set_repeat(fps)
    
    # Imágenes de fondo
    
    bg1 = pygame.image.load("Archivos_Catch/Sky.png")
    bg1 = pygame.transform.scale(bg1, (screen_width, screen_height-top_height/2-bot_height))
    bg1.convert()
    
    bg2 = pygame.image.load("Archivos_Catch/Grass.png")
    bg2 = pygame.transform.scale(bg2, (screen_width, screen_height))
    bg2.convert()
    
    bg3 = pygame.image.load("Archivos_Catch/Cloud.png")
    bg3 = pygame.transform.scale(bg3, (cloud_dim_x, cloud_dim_y))
    bg3.convert()
    bg4 = pygame.transform.scale(bg3, (3*cloud_dim_x, 3*cloud_dim_y))
    bg4.convert()
    
    # Actualizar pantalla
    screen.blit(bg1, (0,top_height/2))
    screen.blit(bg2, (0,screen_height-bot_height))
    
    # Colocar las nubes aleatoriamente en la parte de arriba
    order_big = [*range(0,big_clouds)]
    random.shuffle(order_big)
    l_big = screen_width/(big_clouds-1)
    for i in order_big:
        cloudRect = bg4.get_rect()
        cloudRect.center = [l_big*i, 0]
        screen.blit(bg4, cloudRect)
    
    order_small = [*range(0,small_clouds)]
    random.shuffle(order_small)
    l_small = screen_width/(small_clouds-1)
    rdm_y = random.sample(range(-40,10), small_clouds)
    for i in order_small:
        cloudRect = bg3.get_rect()
        cloudRect.center = [l_small*i, top_height + rdm_y[i]]
        screen.blit(bg3, cloudRect)
    
    # Fuentes usadas en todo el juego
    score_font = pygame.font.SysFont("Atari Classic", 90)
    intro_font = pygame.font.SysFont("Atari Classic", 45)
    
    # Mensaje inicial
    score = score_font.render("CATCH",True,'Blue')
    scoreRect = score.get_rect()
    scoreRect.center = [screen_width/2, top_height/2]
    screen.blit(score, scoreRect)
    
    intro1 = intro_font.render("Alcanza la puntuación objetivo",True,'White')
    intro1Rect = intro1.get_rect()
    intro1Rect.center = [screen_width/2, screen_height/2 - 120 + txt_height]
    screen.blit(intro1, intro1Rect)
    
    intro2 = intro_font.render("para pasar el nivel",True,'White')
    intro2Rect = intro2.get_rect()
    intro2Rect.center = [screen_width/2, screen_height/2 - 90 + txt_height]
    screen.blit(intro2, intro2Rect)
    
    intro3 = intro_font.render("Las monedas de oro te darán 3 puntos",True,'White')
    intro3Rect = intro3.get_rect()
    intro3Rect.center = [screen_width/2, screen_height/2 - 15 + txt_height]
    screen.blit(intro3, intro3Rect)
    
    intro4 = intro_font.render("Las monedas de plata te darán 2 puntos",True,'White')
    intro4Rect = intro4.get_rect()
    intro4Rect.center = [screen_width/2, screen_height/2 + 30 + txt_height]
    screen.blit(intro4, intro4Rect)
    
    intro5 = intro_font.render("Las monedas de bronce te darán 1 punto",True,'White')
    intro5Rect = intro5.get_rect()
    intro5Rect.center = [screen_width/2, screen_height/2 + 75 + txt_height]
    screen.blit(intro5, intro5Rect)
    
    intro6 = intro_font.render("Las rocas te restarán 3 puntos",True,'White')
    intro6Rect = intro6.get_rect()
    intro6Rect.center = [screen_width/2, screen_height/2 + 120 + txt_height]
    screen.blit(intro6, intro6Rect)
    
    intro7 = intro_font.render("Pulsa cualquier tecla para continuar",True,'White')
    intro7Rect = intro7.get_rect()
    intro7Rect.center = [screen_width/2, screen_height/2 + 210 + txt_height]
    screen.blit(intro7, intro7Rect)
    
    pygame.display.flip()
    
    time.sleep(1)
    
    # No se pasa de pantalla hasta que no se pulse cualquier tecla
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False
    
    # Leprechaun
    lp = Leprechaun(10)
    
    # Objetos que caen (monedas y rocas)
    for i in range(0, n_obj):
        
        j = random.randint(0, len(tipos)-1)
        tipo = tipos[j]
        puntuacion_total = puntuacion_total + tipo
        
        speed_y = random.randint(1, max_speed)
        pos_x = random.randint(coin_dim/2, screen_width-coin_dim/2)
        pos_y = random.randint(-n_obj*200, -100)
        
        obj.append(BasicCoin(speed_y*obj_speed, [pos_x, pos_y], tipo))
        obj_ind.append(len(obj)-1)
    
    # Cálculo de la puntuación objetivo (la mitad de la puntuación total disponible)
    puntuacion_objetivo = math.floor(puntuacion_total/2)
    
    # Bucle principal del juego
    
    running = True
    
    while running:
        
        # Colisiones y puntuación (eliminando objetos)
        if len(obj_ind):
            for i in obj_ind:
                lp.collision(obj[i])
                if lp.col_flag:
                    obj_del.append(i)
                    puntuacion = puntuacion + obj[i].punt
                    del_flag = True
        if del_flag:
            for i in range(0,len(obj_del)):
                obj_ind.remove(obj_del[i])
            obj_del = []
            del_flag = False
        
        # Actualizar y eliminar objetos
        for i in obj_ind:
            obj[i].update()
            if obj[i].flag:
                obj_del.append(i)
                del_flag = True
        if del_flag:
            for i in range(0,len(obj_del)):
                obj_ind.remove(obj_del[i])
            obj_del = []
            del_flag = False
        
        # Actualizar pantalla y puntuación
        screen.blit(bg1, (0,top_height/2))
        screen.blit(bg2, (0,screen_height-bot_height))
        
        for i in obj_ind:
            screen.blit(obj[i].sprite, obj[i].rect)
        screen.blit(lp.sprite, lp.rect)
        
        for i in order_big:
            cloudRect = bg4.get_rect()
            cloudRect.center = [l_big*i, 0]
            screen.blit(bg4, cloudRect)

        for i in order_small:
            cloudRect = bg3.get_rect()
            cloudRect.center = [l_small*i, top_height + rdm_y[i]]
            screen.blit(bg3, cloudRect)
            
        score = intro_font.render("Puntuación: " + str(puntuacion),True,'Blue')
        scoreRect = score.get_rect()
        scoreRect.center = [screen_width/4, top_height/2]
        screen.blit(score, scoreRect)
        
        objetivo = intro_font.render("Objetivo: " + str(puntuacion_objetivo),True,'Blue')
        objetivoRect = objetivo.get_rect()
        objetivoRect.center = [3*screen_width/4, top_height/2]
        screen.blit(objetivo, objetivoRect)
        
        pygame.display.flip()
        
        # Salir del juego y actualizar leprechaun
        if len(obj_ind) == 0:
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                lp.update()
        
        # Cambiar el sprite (la dirección en la que mira)
        lp.animation()
        
        clock.tick(fps)
    
    # Condición de superar el nivel
    ganado = puntuacion >= puntuacion_objetivo
    
    time.sleep(1)
    
    # Actualizar pantalla
    
    screen.blit(bg1, (0,top_height/2))
    screen.blit(bg2, (0,screen_height-bot_height))
        
    for i in order_big:
        cloudRect = bg4.get_rect()
        cloudRect.center = [l_big*i, 0]
        screen.blit(bg4, cloudRect)
    
    for i in order_small:
        cloudRect = bg3.get_rect()
        cloudRect.center = [l_small*i, top_height + rdm_y[i]]
        screen.blit(bg3, cloudRect)
    
    # Mensaje final (cambio dependiendo de si se ha superado el nivel o no)
    
    score = score_font.render("CATCH",True,'Blue')
    scoreRect = score.get_rect()
    scoreRect.center = [screen_width/2, top_height/2]
    screen.blit(score, scoreRect)
    
    if ganado:
    
        intro1 = intro_font.render("Buen trabajo",True,'White')
        intro1Rect = intro1.get_rect()
        intro1Rect.center = [screen_width/2, screen_height/2 - 60 + txt_height]
        screen.blit(intro1, intro1Rect)
        
        intro2 = intro_font.render("Nivel superado",True,'White')
        intro2Rect = intro2.get_rect()
        intro2Rect.center = [screen_width/2, screen_height/2 + txt_height]
        screen.blit(intro2, intro2Rect)
                
    else:
        
        intro1 = intro_font.render("Mala suerte",True,'White')
        intro1Rect = intro1.get_rect()
        intro1Rect.center = [screen_width/2, screen_height/2 - 60 + txt_height]
        screen.blit(intro1, intro1Rect)
        
        intro2 = intro_font.render("Nivel no superado",True,'White')
        intro2Rect = intro2.get_rect()
        intro2Rect.center = [screen_width/2, screen_height/2 + txt_height]
        screen.blit(intro2, intro2Rect)
    
    # La puntuación final se calcula como el porcentaje de puntos obtenidos (de todos los disponibles)
    porc = math.ceil(puntuacion/puntuacion_total*100)
    
    intro3 = intro_font.render("Porcentaje de puntos obtenidos: " + str(porc) + "%",True,'White')
    intro3Rect = intro3.get_rect()
    intro3Rect.center = [screen_width/2, screen_height/2 + 60 + txt_height]
    screen.blit(intro3, intro3Rect)
        
    intro4 = intro_font.render("Pulsa cualquier tecla para continuar",True,'White')
    intro4Rect = intro4.get_rect()
    intro4Rect.center = [screen_width/2, screen_height/2 + 180 + txt_height]
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
    
    # La función devuelve el parámetro ganado y la puntuación final
    return ganado, porc

# Mensaje del resultado en el menú
def men_catch(ganado, punt):
    
    if int(ganado):
        return "Nivel superado\nPorcentaje de \npuntos obtenidos: " + str(punt) + "%"
    else:
        return "Nivel no superado\nPorcentaje \nde puntos obtenidos: " + str(punt) + "%"