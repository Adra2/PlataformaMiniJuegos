# Carola Adrados Herrero 18001
# Juan Berenguer Triana 19036
# Sergio Gómez Montes 18150

from tkinter import *

# Snake
import pygame
import random
from snake_funcion import *
# print("Snake OK")

# Pong
# import pygame
# import random
import time
from pygame.locals import *
from pong_funcion import *
# print("Pong OK")

# Runner
# import pygame
# from pygame.locals import *
import sys
# import random
# import time
from runner_funcion import *
# print("Runner OK")

# Catch
# import pygame
# from pygame.locals import *
# import sys
# import random
# import time
import math
from catch_funcion import *
# print("Catch OK")

def update_highscores(i_juego, i_dif, ganado, score):
    
    record = False
    
    if ganado:
        ganado = 1
    else:
        ganado = 0
    
    with open("highscores.txt") as file:
        hs = [line.rstrip() for line in file]
    
    i_juego = hs.index(nombre_juegos[i_juego])
    
    # Partidas jugadas
    hs[i_juego+3*i_dif+1] = str(int(hs[i_juego+3*i_dif+1])+1)
    
    # Partidas ganadas
    if ganado:
        hs[i_juego+3*i_dif+2] = str(int(hs[i_juego+3*i_dif+2])+1)
    
    # Actualizar record
    if ganado > int(hs[i_juego+3*i_dif+2]):
        hs[i_juego+4*i_dif+3] = str(score)
        record = True
    elif score > int(hs[i_juego+3*i_dif+3]):
        hs[i_juego+3*i_dif+3] = str(score)
        record = True

    hs = "\n".join(hs)

    txt = open("highscores.txt","w")
    txt.writelines(hs)
    txt.close()
    
    return record

def read_highscores(i_juego, i_dif):
    
    with open("highscores.txt") as file:
        hs = [line.rstrip() for line in file]
    
    i_juego = hs.index(nombre_juegos[i_juego])
    
    return hs[i_juego+3*i_dif+1], hs[i_juego+3*i_dif+2], hs[i_juego+3*i_dif+3]

def reset_highscores():
    
    hs = ["0"]*(l_juegos*(l_dif*3+1))
    
    for i in range(0,l_juegos):
        hs[i*(l_dif*3+1)] = nombre_juegos[i]
    
    hs = "\n".join(hs)

    txt = open("highscores.txt","w")
    txt.writelines(hs)
    txt.close()

nombre_juegos = ["Snake","Pong","Runner","Catch"]
juegos = [snake, pong, runner, catch]
men_juegos = [men_snake, men_pong, men_runner, men_catch]
l_juegos = len(juegos)

dificultades = ["Fácil","Normal","Difícil","Imposible"]
l_dif = len(dificultades)

l = max(l_juegos, l_dif)


#colores
negro=("#000000")
blanco=("#ffffff")
azul_c=("#03f4fc")#azul cian brillante fondo?
azul_o=("#291866")
amarillo=("#ffff00")
rosa=("#d305fc")
rojo=("#ff001e")
verde=("#4ced07")
naranja_c=("#ffa600")
naranja_o=("#ff5e00")

class VentanaDificultad:
    
    dif = ""
    flagDif = 0
    indDif = l_dif + 1
    
    flagGanado = 0
    punt = 0
    
    recordFlag = 0
    
    men = ""
    
    def __init__(self):
        
        self.ventanaDificultad = Toplevel()
        self.ventanaDificultad.title("Party: Dificultad")
        self.ventanaDificultad.configure(bg=azul_c)
        
        self.etiqueta = Label(self.ventanaDificultad, text="Elegir dificultad",font=("Fixedsys",10),bg=azul_c,fg=rosa)
        self.etiqueta.grid(columnspan = l_dif, row = 0)
        
        for i in range(0,l_dif):
            self.botonJuegos = Button(self.ventanaDificultad, text=dificultades[i], command = lambda j = i: self.regDif(j),font=("System",10),bg=azul_o,fg=amarillo)
            self.botonJuegos.grid(column = i, row = 1)
        
        self.mensajeDif = StringVar()
        self.mensajeDif.set("Ninguna dificultad seleccionada")
        self.etiqueta = Label(self.ventanaDificultad, textvariable = self.mensajeDif,bg=azul_c,fg=rojo)
        self.etiqueta.grid(columnspan = l, row = 2)
        
        self.botonJugar = Button(self.ventanaDificultad, text="Jugar", command=self.jugar,font=("System",10),bg=azul_o,fg=amarillo)
        self.botonJugar.grid(columnspan = l, row = 3)
        
        self.mensajeJugar = StringVar()
        self.mensajeJugar.set("")
        self.etiqueta = Label(self.ventanaDificultad, textvariable = self.mensajeJugar,bg=azul_c,fg=naranja_o)
        self.etiqueta.grid(columnspan = l, row = 4)
        
        self.botonSalir = Button(self.ventanaDificultad, text="Salir", command = self.ventanaDificultad.destroy,font=("System",10),bg=azul_o,fg=rosa)
        self.botonSalir.grid(columnspan = l, row = 5)
        
        self.ventanaDificultad.grab_set()
    
    def regDif(self, j):
        self.dif = dificultades[j]
        self.indDif = j
        self.flagDif = 1
        self.mensajeDif.set("Dificultad seleccionada: " + dificultades[j])
    
    def jugar(self):
        
        if self.flagDif:
            
           self.mensajeJugar.set("Juego en progreso")
           
           names = nombre_juegos.copy()
           random.shuffle(names)
           
           for game in names:
               
               ind = nombre_juegos.index(game)
               
               [self.flagGanado, self.punt] = juegos[ind](self.dif)
               self.recordFlag = update_highscores(ind, self.indDif, self.flagGanado, self.punt)
               
               self.men = men_juegos[ind](self.flagGanado,self.punt) + self.recordFlag*("\n¡¡NUEVO RÉCORD!!")
               
               if self.flagGanado:
                   self.men = self.men + "\nBien hecho\nPasas a la siguiente dificultad"
                   self.mensajeJugar.set(self.men)
                   self.ventanaDificultad.update()
               else:
                   self.men = self.men + "\nMala suerte\nNo has podido superar esta dificultad"
                   self.mensajeJugar.set(self.men)
                   self.ventanaDificultad.update()
                   break

            
        else:
            self.mensajeJugar.set("Ninguna dificultad seleccionada")

class VentanaJuego:
    
    juego = ""
    flagJuego = 0
    indJuego = l_juegos + 1
    
    flagGanado = 0
    punt = 0
    
    recordFlag = 0
    
    men = ""
    
    def __init__(self):
        
        self.ventanaJuego = Toplevel()
        self.ventanaJuego.title("Party: Juego")
        self.ventanaJuego.configure(bg=azul_c)
        
        self.etiqueta = Label(self.ventanaJuego, text="Elegir juego",font=("Fixedsys",10),bg=azul_c,fg=rosa)
        self.etiqueta.grid(columnspan = l, row = 0)
        
        for i in range(0,l_juegos):
            self.botonJuegos = Button(self.ventanaJuego, text=nombre_juegos[i], command = lambda j = i: self.regJuego(j),font=("System",10),bg=azul_o,fg=amarillo)
            self.botonJuegos.grid(column = i, row = 1)
        
        self.mensajeJuego = StringVar()
        self.mensajeJuego.set("Ningún juego seleccionado")
        self.etiqueta = Label(self.ventanaJuego, textvariable = self.mensajeJuego,bg=azul_c,fg=rojo)
        self.etiqueta.grid(columnspan = l, row = 2)
        
        self.botonJugar = Button(self.ventanaJuego, text="Jugar", command=self.jugar,font=("System",10),bg=azul_o,fg=amarillo)
        self.botonJugar.grid(columnspan = l, row = 3)
        
        self.mensajeJugar = StringVar()
        self.mensajeJugar.set("")
        self.etiqueta = Label(self.ventanaJuego, textvariable = self.mensajeJugar,bg=azul_c,fg=naranja_o)
        self.etiqueta.grid(columnspan = l, row = 4)
        
        self.botonSalir = Button(self.ventanaJuego, text="Salir", command = self.ventanaJuego.destroy,font=("System",10),bg=azul_o,fg=rosa)
        self.botonSalir.grid(columnspan = l, row = 5)
        
        self.ventanaJuego.grab_set()
    
    def regJuego(self, j):
        self.juego = juegos[j]
        self.indJuego = j
        self.flagJuego = 1
        self.mensajeJuego.set("Juego seleccionado: " + nombre_juegos[j])
    
    def jugar(self):
        
        if self.flagJuego:
            
            self.mensajeJugar.set("Juego en progreso")
            
            for dif in dificultades:
                            
                ind = dificultades.index(dif)
                
                [self.flagGanado, self.punt] = juegos[self.indJuego](dif)
                self.recordFlag = update_highscores(self.indJuego, ind, self.flagGanado, self.punt)
                
                self.men = men_juegos[self.indJuego](self.flagGanado,self.punt) + self.recordFlag*("\n¡¡NUEVO RÉCORD!!")
                
                if self.flagGanado:
                    self.men = self.men + "\nBien hecho\nPasas a la siguiente dificultad"
                    self.mensajeJugar.set(self.men)
                    self.ventanaJuego.update()
                else:
                    self.men = self.men + "\nMala suerte\nNo has podido superar esta dificultad"
                    self.mensajeJugar.set(self.men)
                    self.ventanaJuego.update()
                    break
                
        else:
            self.mensajeJugar.set("Ningún juego seleccionado")

class VentanaParty:
    
    def __init__(self):
        
        self.ventanaParty = Tk()
        self.ventanaParty.title("Super Party")
        self.ventanaParty.configure(bg=azul_c)
        
        self.etiqueta = Label(self.ventanaParty, text="Elige un modo de juego\nTendrás que intentar superar todos los niveles del modo seleccionado",font="Fixedsys",bg=azul_c,fg=rosa)
        self.etiqueta.grid(columnspan = 2, row = 0)
        
        self.botonJuego = Button(self.ventanaParty, text="Juego", command=self.juego,font=("System",10),bg=azul_o,fg=amarillo)
        self.botonJuego.grid(column = 0, row = 1)
        
        self.botonDificultad = Button(self.ventanaParty, text="Dificultad", command=self.dificultad,font=("System",10),bg=azul_o,fg=amarillo)
        self.botonDificultad.grid(column = 1, row = 1)
        
        self.botonSalir = Button(self.ventanaParty, text="Salir", command=self.ventanaParty.destroy,font=("System",10),bg=azul_o,fg=rosa)
        self.botonSalir.grid(columnspan = 2, row = 2)
        
        self.ventanaParty.mainloop()
    
    def juego(self):
        self.ventanaJuego = VentanaJuego()
        
    def dificultad(self):
        self.ventanaDificultad = VentanaDificultad()


class VentanaReset:
    
    def __init__(self):
        
        self.ventanaReset = Toplevel()
        self.ventanaReset.title("Confirmación")
        self.ventanaReset.configure(bg=azul_c)
        
        self.etiqueta = Label(self.ventanaReset, text="Una vez hayas reseteado tu historial, no podrás recuperarlo.\n¿Resetear historial?",font="Fixedsys",bg=azul_c,fg=rojo)
        self.etiqueta.grid(columnspan = 2, row = 0)
        
        self.botonReset = Button(self.ventanaReset, text="Resetear historial",font=("System",10), command=self.reset,bg=azul_o,fg=verde)
        self.botonReset.grid(column = 0, row = 1)
        
        self.botonCancelar = Button(self.ventanaReset, text="Cancelar",font=("System",10), command = self.ventanaReset.destroy,bg=azul_o,fg=rosa)
        self.botonCancelar.grid(column = 1, row = 1)
        
        self.ventanaReset.grab_set()
    
    def reset(self):
        reset_highscores()
        self.botonReset.destroy()
        self.botonCancelar.destroy()
        self.etiqueta = Label(self.ventanaReset, text="Historial reseteado",font="Fixedsys",bg=azul_c,fg=negro)
        self.etiqueta.grid(columnspan = 2, row = 1)
        self.botonSalir = Button(self.ventanaReset, text="Salir",font=("System",10), command = self.ventanaReset.destroy,bg=azul_o,fg=rosa)
        self.botonSalir.grid(columnspan = 2, row = 2)

class VentanaRecords:
    
    juego = ""
    flagJuego = 0
    indJuego = l_juegos + 1
    
    dif = ""
    flagDif = 0
    indDif = l_dif + 1
    
    partJugadas = 0
    partGanadas = 0
    highscore = 0
    
    def __init__(self):
        
        self.ventanaIndividual = Toplevel()
        self.ventanaIndividual.title("Historial")
        self.ventanaIndividual.geometry("300x420")
        self.ventanaIndividual.configure(bg=azul_c)
        
        self.etiqueta = Label(self.ventanaIndividual, text="Elegir juego",font=("Fixedsys",20),bg=azul_c,fg=rosa)
        self.etiqueta.place(x=45,y=5)

        

        self.botonsnake = Button(self.ventanaIndividual, text=nombre_juegos[0],font=("System",10), command = lambda j = 0: self.regJuego(j),bg=azul_o,fg=amarillo)
        self.botonsnake.place(x=25,y=45)
        self.botonpong = Button(self.ventanaIndividual, text=nombre_juegos[1],font=("System",10), command = lambda j = 1: self.regJuego(j),bg=azul_o,fg=amarillo)
        self.botonpong.place(x=90,y=45)
        self.botonrunner = Button(self.ventanaIndividual, text=nombre_juegos[2],font=("System",10), command = lambda j = 2: self.regJuego(j),bg=azul_o,fg=amarillo)
        self.botonrunner.place(x=155,y=45)
        self.botoncatch = Button(self.ventanaIndividual, text=nombre_juegos[3],font=("System",10), command = lambda j = 3: self.regJuego(j),bg=azul_o,fg=amarillo)
        self.botoncatch.place(x=230,y=45)   

        self.mensajeJuego = StringVar()
        self.mensajeJuego.set("Ningún juego seleccionado")
        self.etiqueta = Label(self.ventanaIndividual, textvariable = self.mensajeJuego,font="Fixedsys",bg=azul_c,fg=negro)
        self.etiqueta.place(x=50,y=73)

        
        self.etiqueta = Label(self.ventanaIndividual, text="Elegir\ndificultad",font=("Fixedsys",17),bg=azul_c,fg=rosa)
        self.etiqueta.place(x=70,y=93)


        self.botonfacil= Button(self.ventanaIndividual, text=dificultades[0],font=("System",10), command = lambda j = 0: self.regDif(j),bg=azul_o,fg=amarillo)
        self.botonfacil.place(x=20,y=163)
        self.botonnormal= Button(self.ventanaIndividual, text=dificultades[1],font=("System",10), command = lambda j = 1: self.regDif(j),bg=azul_o,fg=amarillo)
        self.botonnormal.place(x=75,y=163)
        self.botondificil= Button(self.ventanaIndividual, text=dificultades[2],font=("System",10), command = lambda j = 2: self.regDif(j),bg=azul_o,fg=amarillo)
        self.botondificil.place(x=145,y=163)
        self.botonimposible= Button(self.ventanaIndividual, text=dificultades[3],font=("System",10), command = lambda j = 3: self.regDif(j),bg=azul_o,fg=amarillo)
        self.botonimposible.place(x=205,y=163)    

        self.mensajeDif = StringVar()
        self.mensajeDif.set("Ninguna dificultad seleccionada")
        self.etiqueta = Label(self.ventanaIndividual, textvariable = self.mensajeDif,font="Fixedsys",bg=azul_c,fg=negro)
        self.etiqueta.place(x=20,y=193)

        
        self.botonRecord = Button(self.ventanaIndividual, text="Ver historial",font=("System",10), command=self.record,bg=azul_o,fg=amarillo)
        self.botonRecord.place(x=100,y=215)

        
        self.mensajeRecord = StringVar()
        self.mensajeRecord.set("")
        self.etiqueta = Label(self.ventanaIndividual, textvariable = self.mensajeRecord,font="Fixedsys",bg=azul_c,fg=naranja_o)
        self.etiqueta.place(x=65,y=243)

        
        self.botonReset = Button(self.ventanaIndividual, text="Resetear historial",font=("System",10), command=self.reset,bg=azul_o,fg=blanco)
        self.botonReset.place(x=90,y=350)

        
        self.botonSalir = Button(self.ventanaIndividual, text="Salir",font=("System",10), command = self.ventanaIndividual.destroy,bg=azul_o,fg=rosa)
        self.botonSalir.place(x=130,y=380)

        
        self.ventanaIndividual.grab_set()
    
    def regJuego(self, j):
        self.juego = juegos[j]
        self.indJuego = j
        self.flagJuego = 1
        self.mensajeJuego.set("Juego seleccionado: " + nombre_juegos[j])
    
    def regDif(self, j):
        self.dif = dificultades[j]
        self.indDif = j
        self.flagDif = 1
        self.mensajeDif.set("Dificultad seleccionada: " + dificultades[j])
    
    def record(self):
        if self.flagJuego * self.flagDif:
            [self.partJugadas, self.partGanadas, self.highscore] = read_highscores(self.indJuego, self.indDif)
            
            if int(self.partJugadas):
                self.mensajeRecord.set(self.partJugadas + " partidas jugadas\n" + self.partGanadas + " partidas ganadas\nMejor partida:\n" + men_juegos[self.indJuego](self.partGanadas,self.highscore))
            else:
                self.mensajeRecord.set("Ninguna partida jugada")
            
        elif (self.flagJuego == 0) and (self.flagDif == 0):
            self.mensajeRecord.set("Ni juego ni\ndificultad seleccionados")
        elif self.flagJuego == 0:
            self.mensajeRecord.set("Juego no seleccionado")
        elif self.flagDif == 0:
            self.mensajeRecord.set("Dificultad no seleccionada")
    
    def reset(self):
        self.ventanaReset = VentanaReset()

class VentanaIndividual:
    
    juego = ""
    flagJuego = 0
    indJuego = l_juegos + 1
    
    dif = ""
    flagDif = 0
    indDif = l_dif + 1
    
    flagGanado = 0
    punt = 0
    
    recordFlag = 0
    
    def __init__(self):
        
        self.ventanaIndividual = Toplevel()
        self.ventanaIndividual.title("Juego individual")
        self.ventanaIndividual.geometry("300x420")
        self.ventanaIndividual.configure(bg=azul_c)
        
        self.etiqueta = Label(self.ventanaIndividual, text="Elegir juego",font=("Fixedsys",20),bg=azul_c,fg=rosa)
        self.etiqueta.place(x=45,y=20)

        self.botonsnake = Button(self.ventanaIndividual, text=nombre_juegos[0],font=("System",10), command = lambda j = 0: self.regJuego(j),bg=azul_o,fg=amarillo)
        self.botonsnake.place(x=25,y=70)
        self.botonpong = Button(self.ventanaIndividual, text=nombre_juegos[1],font=("System",10), command = lambda j = 1: self.regJuego(j),bg=azul_o,fg=amarillo)
        self.botonpong.place(x=90,y=70)
        self.botonrunner = Button(self.ventanaIndividual, text=nombre_juegos[2],font=("System",10), command = lambda j = 2: self.regJuego(j),bg=azul_o,fg=amarillo)
        self.botonrunner.place(x=155,y=70)
        self.botoncatch = Button(self.ventanaIndividual, text=nombre_juegos[3],font=("System",10), command = lambda j = 3: self.regJuego(j),bg=azul_o,fg=amarillo)
        self.botoncatch.place(x=230,y=70)

        self.mensajeJuego = StringVar()
        self.mensajeJuego.set("Ningún juego seleccionado")
        self.etiqueta = Label(self.ventanaIndividual, textvariable = self.mensajeJuego,font="Fixedsys",bg=azul_c,fg=negro)
        self.etiqueta.place(x=50,y=105)

        
        self.etiqueta = Label(self.ventanaIndividual, text="Elegir\ndificultad",font=("Fixedsys",17),bg=azul_c,fg=rosa)
        self.etiqueta.place(x=70,y=145)

        

        self.botonfacil= Button(self.ventanaIndividual, text=dificultades[0],font=("System",10), command = lambda j = 0: self.regDif(j),bg=azul_o,fg=amarillo)
        self.botonfacil.place(x=20,y=220)
        self.botonnormal= Button(self.ventanaIndividual, text=dificultades[1],font=("System",10), command = lambda j = 1: self.regDif(j),bg=azul_o,fg=amarillo)
        self.botonnormal.place(x=75,y=220)
        self.botondificil= Button(self.ventanaIndividual, text=dificultades[2],font=("System",10), command = lambda j = 2: self.regDif(j),bg=azul_o,fg=amarillo)
        self.botondificil.place(x=145,y=220)
        self.botonimposible= Button(self.ventanaIndividual, text=dificultades[3],font=("System",10), command = lambda j = 3: self.regDif(j),bg=azul_o,fg=amarillo)
        self.botonimposible.place(x=205,y=220)



        self.mensajeDif = StringVar()
        self.mensajeDif.set("Ninguna dificultad seleccionada")
        self.etiqueta = Label(self.ventanaIndividual, textvariable = self.mensajeDif,font="Fixedsys",bg=azul_c,fg=negro)
        self.etiqueta.place(x=20,y=250)

        
        self.botonJugar = Button(self.ventanaIndividual, text="Jugar",font=("System",10), command=self.jugar,bg=azul_o,fg=amarillo)
        self.botonJugar.place(x=127,y=350)

        
        self.mensajeJugar = StringVar()
        self.mensajeJugar.set("")
        self.etiqueta = Label(self.ventanaIndividual, textvariable = self.mensajeJugar,font="Fixedsys",bg=azul_c,fg=naranja_o)
        self.etiqueta.place(x=50,y=275)

        
        self.botonSalir = Button(self.ventanaIndividual, text="Salir",font=("System",10), command = self.ventanaIndividual.destroy,bg=azul_o,fg=rosa)
        self.botonSalir.place(x=130,y=380)

        
        self.ventanaIndividual.grab_set()
    
    def regJuego(self, j):
        self.juego = juegos[j]
        self.indJuego = j
        self.flagJuego = 1
        self.mensajeJuego.set("Juego seleccionado: " + nombre_juegos[j])
    
    def regDif(self, j):
        self.dif = dificultades[j]
        self.indDif = j
        self.flagDif = 1
        self.mensajeDif.set("Dificultad seleccionada: " + dificultades[j])
    
    def jugar(self):
        if self.flagJuego * self.flagDif:
            
            self.mensajeJugar.set("Juego en progreso")
            [self.flagGanado, self.punt] = juegos[self.indJuego](self.dif)
            self.recordFlag = update_highscores(self.indJuego, self.indDif, self.flagGanado, self.punt)
            self.mensajeJugar.set(men_juegos[self.indJuego](self.flagGanado,self.punt) + self.recordFlag*("\n¡¡NUEVO RÉCORD!!"))
            
        elif (self.flagJuego == 0) and (self.flagDif == 0):
            self.mensajeJugar.set("Ni juego ni \ndificultad seleccionados")
        elif self.flagJuego == 0:
            self.mensajeJugar.set("Juego no seleccionado")
        elif self.flagDif == 0:
            self.mensajeJugar.set("Dificultad no seleccionada")
            
class VentanaPrincipal: 
    
    def __init__(self):
        
        self.master = Tk()
        self.master.geometry("400x225")
        self.master.title("Inicio")
        self.master.configure(bg=azul_c)
        
        self.etiqueta = Label(self.master, text="Modos de juego",font=("Fixedsys",17),bg=azul_c,fg=rosa)
        self.etiqueta.place(x=80,y=10)

        
        self.botonIndividual = Button(self.master, text="Juego\nindividual",font="Terminal", command=self.individual,bg=azul_o,fg=amarillo)
        self.botonIndividual.place(x=40,y=60)

        
        self.botonAleatorio = Button(self.master, text="Modo\nSuper Party",font="Terminal", command=self.aleatorio,bg=azul_o,fg=amarillo)
        self.botonAleatorio.place(x=230,y=60)
  
        
        self.botonRecords = Button(self.master, text="Historial",font="Terminal", command=self.records,bg=azul_o,fg=naranja_c)
        self.botonRecords.place(x=125,y=125)

        
        self.botonSalir = Button(self.master, text="Salir",font="Terminal", command=self.master.destroy,bg=azul_o,fg=rosa)
        self.botonSalir.place(x=150,y=170)

        
        self.master.mainloop()
    
    def individual(self):
        self.ventanaIndividual = VentanaIndividual()
        
    def aleatorio(self):
        self.ventanaAleatorio = VentanaParty()
    
    def records(self):
        self.ventanaRecords = VentanaRecords()

ventana = VentanaPrincipal()