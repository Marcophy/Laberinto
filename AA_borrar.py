# coding=utf-8

import pygame, os

# Muros
pointer = 0
muros = []
puertas = []
keys = []
ghosts = []
archivo = open('pantalla.txt', 'r')
for linea in archivo.readlines():
    if linea == 'WALLS\n':
        print('Muros')
        pointer += 1
    elif linea == 'DOOR\n':
        print('door')
        pointer += 1
    elif linea == 'KEY\n':
        print('llave')
        pointer += 1
    elif linea == 'PLAYER\n':
        print('Player')
        pointer += 1
    elif linea == 'GHOST\n':
        print('Fantasma')
        pointer += 1
    else:
        if pointer == 1: # Muros
            print('Leyendo walls_list')
            linea = tuple(map(int, linea.split(', ')))
            muros.append(pygame.Rect(linea))
        elif pointer == 2: # Puerta
            print('Leyendo Puerta')
            linea = tuple(map(int, linea.split(', ')))
            puertas.append(pygame.Rect(linea))
        elif pointer == 3: # Llave
            print('Leyendo Llave',linea)
            linea = tuple(map(int, linea.split(', ')))
            keys.append(linea)
        elif pointer == 4: # player
            print('Leyendo player')
            player_pos = tuple(map(int, linea.split(', ')))
        elif pointer == 5: # ghost
            print('Leyendo fantasmas')
            linea = tuple(map(int, linea.split(', ')))
            ghosts.append(linea)

archivo.close()
print('Muros =',muros)
print('Puertas = ',puertas)
print('Llaves =',keys)
print('Player = ',player_pos)
print('Ghosts = ',ghosts)

print("\n",type(ghosts))
print(ghosts[0][0])