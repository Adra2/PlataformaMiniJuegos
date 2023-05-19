# Carola Adrados Herrero 18001
# Juan Berenguer Triana 19036
# Sergio Gómez Montes 18150

# Autor: Sergio Gómez

import pygame
import random

def snake(dif):

    pygame.init()

    ganado = False
    if dif == "Fácil":
        vel = 11
    elif dif == "Normal":
        vel = 11
    elif dif == "Difícil":
        vel = 20
    elif dif == "Imposible":
        vel = 30
    else:
        print ("ERROR: dificultad no válida")
        return ganado



    #variables
    cuadrado = 10
    Fuente_GO1 = pygame.font.SysFont("Atari Classic", 45)
    Fuente_GO2 = pygame.font.SysFont("Atari Classic", 35)
    fuente_puntos = pygame.font.SysFont("Atari Classic", 35)
    bg_music=pygame.mixer.Sound('Archivos_Snake/snake.wav')  #ruta cancion
    bg_music.set_volume(0.5) #ajustar volumen
    bg_music.play(loops=-1) #repetir infinito

   
    #ventana 
    ancho=700
    alto=500
    screen = pygame.display.set_mode((ancho+10, alto+10))
    pygame.display.set_caption("Snake Modo " +str (dif))

    #colores personalizados
    azul = (50, 153, 168) #fondo
    rojo = (175, 6, 53) #fondo 2
    dorado=(206, 214, 13)#fondo 3
    naranja = (255, 128, 0) #comida
    pared=(51, 44, 43) #muro
    morado=(136, 5, 206) #veneno
    mandarina=(255, 180, 0) #puntuacion perder
    violeta=(131, 75, 227)  #puntuacion victoria
   
 
    #clock
    clock = pygame.time.Clock()

    #clases
    class Serpiente(pygame.sprite.Sprite):
        def __init__(self):
            self.x=0
            self.y=0
            self.lista=[]
            self.puntos=0
            self.tripa=0
            self.comer_sonido=pygame.mixer.Sound('Archivos_Snake/comer.wav')
            self.veneno_sonido=pygame.mixer.Sound('Archivos_Snake/venenoso.wav')
            self.golpe_sonido=pygame.mixer.Sound('Archivos_Snake/auch.wav')
        
    class Comida(pygame.sprite.Sprite):
        def __init__(self):
            self.x=0
            self.y=0

    class Veneno(pygame.sprite.Sprite):
        def __init__(self):
            self.x=0
            self.y=0
    
    #"main"
    def bucle():
        cerrar = 0
        perder = 0
        ganado=False
        serpiente=Serpiente()
        serpiente.x=ancho/2
        serpiente.y=alto/2 
        serpiente.bloque=[]
        serpiente.lista = []
        serpiente.dir=[0,0]
        serpiente.tripa=1

        comida=Comida()
        comida.x = round(random.randrange(0, ancho) / 10.0) * 10.0
        comida.y = round(random.randrange(0, alto) / 10.0) * 10.0
        if comida.x<=10.0 or comida.x>=690.0:
            comida.x = round(random.randrange(0, ancho) / 10.0) * 10.0
        if comida.y<=10.0 or comida.y>=490.0:
            comida.y = round(random.randrange(0, alto) / 10.0) * 10.0
        veneno=Veneno()
        veneno.x = round(random.randrange(0, ancho) / 10.0) * 10.0
        veneno.y = round(random.randrange(0, alto) / 10.0) * 10.0
        if veneno.x<=10.0 or veneno.x>=690.0:
            veneno.x = round(random.randrange(0, ancho) / 10.0) * 10.0
        if veneno.y<=10.0 or veneno.y>=490.0:
            veneno.y = round(random.randrange(0, alto) / 10.0) * 10.0


        while not cerrar:
            #pantalla final
            while perder == 1:
                if ganado == False:
                    screen.fill(rojo)
                    texto1 = Fuente_GO1.render("Has perdido :(", 1, 'black')
                    screen.blit(texto1, [ancho / 3, alto / 3])
                    # texto2=Fuente_GO2.render("Pulsa R para volver a jugar y ESC para salir.", 1, 'black')
                    texto2=Fuente_GO2.render("Pulsa ESC para salir.", 1, 'black')
                    screen.blit(texto2, [ancho / 3-20, alto / 3+40])
                    ptof = fuente_puntos.render("Puntos: " + str(serpiente.tripa - 1), 1, mandarina)
                    screen.blit(ptof, [20, 20])
                    
                else:
                    screen.fill(dorado)
                    texto3 = Fuente_GO1.render("Has ganado :)", 1, 'black')
                    screen.blit(texto3, [ancho / 3, alto / 3])
                    #texto4=Fuente_GO2.render("Pulsa R para volver a jugar y ESC para salir.", 1, 'black')
                    texto4=Fuente_GO2.render("Pulsa ESC para salir.", 1, 'black')
                    screen.blit(texto4, [ancho / 3, alto / 3+40])   
                    ptof = fuente_puntos.render("Puntos: " + str(serpiente.tripa - 1), 1, violeta)
                    screen.blit(ptof, [20, 20])

                pygame.display.update()

            #salir del juego o reiniciar
                for event in pygame.event.get():
                    key = pygame.key.get_pressed()
                    if key[pygame.K_ESCAPE]:
                        cerrar = 1
                        perder = 0
                    # if key[pygame.K_r]:
                    #     bucle()   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    perder = 1
            
            #movimiento serpiente
                key = pygame.key.get_pressed()
                if (key[pygame.K_w] or (key[pygame.K_UP])) : #arriba
                    if (serpiente.dir!=[0,10]) :
                        serpiente.dir=[0,-10]
                if (key[pygame.K_a] or (key[pygame.K_LEFT])): #izda
                    if (serpiente.dir!=[10,0]) :
                        serpiente.dir=[-10,0]
                if (key[pygame.K_s] or (key[pygame.K_DOWN])): #abajo
                    if (serpiente.dir!=[0,-10]) :
                        serpiente.dir=[0,10]      
                if (key[pygame.K_d] or (key[pygame.K_RIGHT])): #dcha
                    if (serpiente.dir!=[-10,0]) :
                        serpiente.dir=[10,0]
            serpiente.x += serpiente.dir[0] 
            serpiente.y += serpiente.dir[1]
       
        #perder
            if dif=="Fácil":
                if serpiente.x >= ancho+10:
                    serpiente.x=0
                if serpiente.x < 0:
                    serpiente.x=ancho+10
                if serpiente.y >= alto+10:
                    serpiente.y=0
                if serpiente.y < 0:
                    serpiente.y=alto+10
        
                for x in serpiente.lista[:-1]:
                    if x == serpiente.bloque:
                        perder = 1

            if dif=="Normal" or dif=="Difícil" or dif=="Imposible":
                if serpiente.x >= ancho or serpiente.x < 10 or serpiente.y >= alto or serpiente.y < 10:
                    serpiente.golpe_sonido.play() 
                    perder = 1
                for x in serpiente.lista[:-1]:
                    if x == serpiente.bloque:
                        serpiente.golpe_sonido.play()
                        perder = 1

        #ganar
            if (serpiente.tripa - 1)>=10:
                ganado=True

        #pantalla principal        
            screen.fill(azul)
            pygame.draw.rect(screen, naranja, [comida.x, comida.y, cuadrado, cuadrado])

            if dif=="Normal" or dif=="Difícil" or dif=="Imposible":
                pygame.draw.rect(screen, pared, [0, 0, ancho, cuadrado])#arriba
                pygame.draw.rect(screen, pared, [0, 0, cuadrado, alto])#izquierda
                pygame.draw.rect(screen, pared, [0, alto, ancho+10, cuadrado])#abajo
                pygame.draw.rect(screen, pared, [ancho, 0, cuadrado, alto+10])#derecha
            if dif=="Imposible":
                pygame.draw.rect(screen, morado, [veneno.x, veneno.y, cuadrado, cuadrado])

            serpiente.bloque = []
            serpiente.bloque.append(serpiente.x)
            serpiente.bloque.append(serpiente.y)
            serpiente.lista.append(serpiente.bloque)
            if len(serpiente.lista) > serpiente.tripa:
                del serpiente.lista[0]

        #dibujar serpiente
            for k in serpiente.lista:
                pygame.draw.rect(screen, 'black', [k[0], k[1], cuadrado, cuadrado])

        #puntuacion
            pto1 = fuente_puntos.render("Puntos: " + str(serpiente.tripa - 1), 1, 'White')
            screen.blit(pto1, [20, 20])
            ptoM = fuente_puntos.render("Objetivo: 10", 1, 'White')
            screen.blit(ptoM, [550, 20])
            pygame.display.update()

        #colision comida 
            if serpiente.x == comida.x and serpiente.y == comida.y:
                serpiente.comer_sonido.play()
                comida.x = round(random.randrange(0, ancho) / 10.0) * 10.0
                comida.y = round(random.randrange(0, alto) / 10.0) * 10.0
                serpiente.tripa += 1
                if dif=="Imposible":
                    veneno.x = round(random.randrange(0, ancho) / 10.0) * 10.0
                    veneno.y = round(random.randrange(0, alto) / 10.0) * 10.0
                    if veneno.x == comida.x and veneno.y == comida.y:
                        veneno.x = round(random.randrange(0, ancho) / 10.0) * 10.0
                        veneno.y = round(random.randrange(0, alto) / 10.0) * 10.0

            if comida.x<=10.0 or comida.x>=690.0:
                comida.x = round(random.randrange(0, ancho) / 10.0) * 10.0
            if comida.y<=10.0 or comida.y>=490.0:
                comida.y = round(random.randrange(0, alto) / 10.0) * 10.0

            if serpiente.x == veneno.x and serpiente.y == veneno.y:
                serpiente.veneno_sonido.play() 
                perder=1 
            if veneno.x<=10.0 or veneno.x>=690.0:
                veneno.x = round(random.randrange(0, ancho) / 10.0) * 10.0
            if veneno.y<=10.0 or veneno.y>=490.0:
                veneno.y = round(random.randrange(0, alto) / 10.0) * 10.0


            clock.tick(vel) #velocidad del juego

        pygame.quit()
        
        return ganado, serpiente.tripa-1
        
        # if ganado:
        #     return ganado, serpiente.tripa-1, "Â¡Nivel superado! Puntos conseguidos: " + str(serpiente.tripa-1) 
        # else:
        #     return ganado, serpiente.tripa-1,  "Â¡Nivel no superado! Puntos conseguidos: " + str(serpiente.tripa-1)      
        quit()
 
    [g,p] = bucle()
    return g, p

def men_snake(ganado, punt):
    
    if int(ganado):
        return "Nivel superado\nPuntos conseguidos: " + str(punt)
    else:
        return "Nivel no superado\nPuntos conseguidos: " + str(punt)