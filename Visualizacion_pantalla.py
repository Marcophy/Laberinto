# coding=utf-8

import pygame, math, os

# os.chdir('d:\')

# ****** Crear ventana ******
screen_size = (2490, 1248)

black = (0, 0, 0)
red = (255, 0 , 0)
white = (255, 255, 255)
brown = (139, 69, 19)
yellow = (255, 238, 0)

# ****** Variables ******
FPS = 90
sprite_ratio = 15
# control_llave = True    # Llave no encontrada

# Muros
pointer = 0
muros = []
puertas = []
keys = []
ghosts = []
archivo = open('pantalla.txt', 'r')
for linea in archivo.readlines():
    if linea == 'WALLS\n':
        pointer += 1
    elif linea == 'DOOR\n':
        pointer += 1
    elif linea == 'KEY\n':
        pointer += 1
    elif linea == 'PLAYER\n':
        pointer += 1
    elif linea == 'GHOST\n':
        pointer += 1
    elif linea == 'HOUSE\n':
        pointer += 1
    else:
        if pointer == 1: # Muros
            linea = tuple(map(int, linea.split(', ')))
            muros.append(pygame.Rect(linea))
        elif pointer == 2: # Puerta
            linea = tuple(map(int, linea.split(', ')))
            puertas.append(pygame.Rect(linea))
        elif pointer == 3: # Llave
            linea = tuple(map(int, linea.split(', ')))
            keys.append(linea)
        elif pointer == 4: # player
            player_pos = tuple(map(int, linea.split(', ')))
        elif pointer == 5: # ghost
            linea = tuple(map(int, linea.split(', ')))
            ghosts.append(linea)
        elif pointer == 6: # house
            house_pos = tuple(map(int, linea.split(', ')))

archivo.close()

# Variables de desarrollo
developer = True        # Muestra opciones extra para desarrollo


# ****** Funciones ******
def Muro(superficie, rectangulo):
    pygame.draw.rect(superficie, white, rectangulo)

def Puerta(superficie, rectangulo):
    pygame.draw.rect(superficie, brown, rectangulo)

# ****** Clases ******
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Player_front_30x30.png').convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.pos_player_old_x = 0
        self.pos_player_old_y = 0
        self.player_speed_x = 0
        self.player_speed_y = 0

    def update (self):
        self.pos_player_old_x = self.rect.x
        self.pos_player_old_y = self.rect.y
        self.rect.x += self.player_speed_x
        self.rect.y += self.player_speed_y

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > screen_size[0] - 2*sprite_ratio:
            self.rect.x = screen_size[0] - 2*sprite_ratio
        
        if self.rect.y < 48:
            self.rect.y = 48
        elif self.rect.y > screen_size[1] - 2*sprite_ratio:
            self.rect.y = screen_size[1] - 2*sprite_ratio

class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Fantasma_left_30x30.png').convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = screen_size[0] - 2*sprite_ratio
        self.rect.y = screen_size[1] - 2*sprite_ratio
        self.pos_ghost_old_x = 0
        self.pos_ghost_old_y = 0
        self.ghost_speed_x = 0
        self.ghost_speed_y = 0
        self.vista = 250

    def __Distance__(self, obj1, obj2):
        return math.sqrt((obj2.rect.x - obj1.rect.x)**2 + (obj2.rect.y - obj1.rect.y)**2)

    def __Speed__(self, obj1, obj2):
        if (obj2.rect.x - obj1.rect.x) < 0:
            ghost_speed_x = -1
        elif (obj2.rect.x - obj1.rect.x) == 0:
            ghost_speed_x = 0
        else:
            ghost_speed_x = 1

        if (obj2.rect.y - obj1.rect.y) < 0:
            ghost_speed_y = -1
        elif (obj2.rect.y - obj1.rect.y) == 0:
            ghost_speed_y = 0
        else:
            ghost_speed_y = 1

        return ghost_speed_x, ghost_speed_y

    def update (self, player):
        if self.__Distance__(self, player) < self.vista + 2*sprite_ratio:
            self.pos_ghost_old_x = self.rect.x
            self.pos_ghost_old_y = self.rect.y

            tempo = self.__Speed__(self, player)
            self.rect.x += tempo[0]
            self.rect.y += tempo[1]
        else:
            self.ghost_speed_x = 0
            self.ghost_speed_y = 0

class Llave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Llave_30x30.png').convert()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = screen_size[1] - 2*sprite_ratio

class Casa(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Casa_30x60.png').convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = screen_size[0] - 4*sprite_ratio
        self.rect.y = 48


class Game(object):
    def __init__(self):
        self.muros = muros
        self.puertas = puertas
        self.keys = keys
        self.ghosts = ghosts
        self.player_pos = player_pos

        # ****** Variables del juego
        self.game_over = False
        self.game_win = False
        self.control_llave = False      # False/True = No/Si tengo llave
        self.control_puerta = True      # True/False = Puerta Cerrada/Abierta
        self.vidas = 3                  # Vidas iniciales

        # ****** Definición de objetos
        self.player = Player()
        self.player_vidas = Player()
        self.ghost = Ghost()
        self.llave = Llave()
        self.casa = Casa()

        # ****** Variables de objetos
        self.player.rect.x = player_pos[0]
        self.player.rect.y = player_pos[1]
     
        self.player_vidas.rect.x = 5
        self.player_vidas.rect.y = 5

        self.ghost.rect.x = ghosts[0][0]
        self.ghost.rect.y = ghosts[0][1]

        self.llave.rect.x = keys[0][0]
        self.llave.rect.y = keys[0][1]

        self.casa.rect.x = house_pos[0]
        self.casa.rect.y = house_pos[1]

    def process_events(self):
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                # Cierra el programa al presionar la X de la esquina
                return True

            # Evento teclado
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_LEFT:
                    self.player.player_speed_x = -3
                if events.key == pygame.K_RIGHT:
                    self.player.player_speed_x = 3
                if events.key == pygame.K_UP:
                    self.player.player_speed_y = -3
                if events.key == pygame.K_DOWN:
                    self.player.player_speed_y = 3

            if events.type == pygame.KEYUP:
                if events.key == pygame.K_LEFT:
                    self.player.player_speed_x = 0
                if events.key == pygame.K_RIGHT:
                    self.player.player_speed_x = 0
                if events.key == pygame.K_UP:
                    self.player.player_speed_y = 0
                if events.key == pygame.K_DOWN:
                    self.player.player_speed_y = 0

        return False

    def run_logic(self):
        # Recarga de pantalla
        pointer = 0
        self.muros = []
        self.puertas = []
        self.keys = []
        self.ghosts = []
        archivo = open('pantalla.txt', 'r')
        for linea in archivo.readlines():
            if linea == 'WALLS\n':
                pointer += 1
            elif linea == 'DOOR\n':
                pointer += 1
            elif linea == 'KEY\n':
                pointer += 1
            elif linea == 'PLAYER\n':
                pointer += 1
            elif linea == 'GHOST\n':
                pointer += 1
            elif linea == 'HOUSE\n':
                pointer += 1
            else:
                if pointer == 1: # Muros
                    linea = tuple(map(int, linea.split(', ')))
                    self.muros.append(pygame.Rect(linea))
                elif pointer == 2: # Puerta
                    linea = tuple(map(int, linea.split(', ')))
                    self.puertas.append(pygame.Rect(linea))
                elif pointer == 3: # Llave
                    linea = tuple(map(int, linea.split(', ')))
                    self.keys.append(linea)
                elif pointer == 4: # player
                    self.player_pos = tuple(map(int, linea.split(', ')))
                elif pointer == 5: # ghost
                    linea = tuple(map(int, linea.split(', ')))
                    self.ghosts.append(linea)
                elif pointer == 6: # house
                    self.house_pos = tuple(map(int, linea.split(', ')))

        archivo.close()

        # self.player.rect.x = self.player_pos[0]
        # self.player.rect.y = self.player_pos[1]

        self.ghost.rect.x = self.ghosts[0][0]
        self.ghost.rect.y = self.ghosts[0][1]

        self.llave.rect.x = self.keys[0][0]
        self.llave.rect.y = self.keys[0][1]

        self.casa.rect.x = self.house_pos[0]
        self.casa.rect.y = self.house_pos[1]

        # ****** Colisiones
        for muro in self.muros:
            if self.player.rect.colliderect(muro):
                self.player_speed_x = 0
                self.player_speed_y = 0
                self.player.rect.x = self.player.pos_player_old_x
                self.player.rect.y = self.player.pos_player_old_y

        self.player.update()


    def display_frame(self, screen):
        screen.fill(black)
        # Dibujar linea superior
        pygame.draw.rect(screen, white, (0, 40, screen_size[0], 5))

        # Dibujar vidas
        screen.blit(self.player_vidas.image, self.player_vidas.rect)
        font = pygame.font.SysFont("serif", 25, bold=False, italic=False)                         # Fuente
        text = font.render("x "+str(self.vidas), True, white) # Texto
        center_x = self.player_vidas.rect.x + 2*sprite_ratio + 5        # posicion text
        center_y = 5
        screen.blit(text, [center_x, center_y])                         # ponerlo en pantalla

        # Dibujar muro
        for muro in self.muros:
            Muro(screen, muro)  # Pinta todo los muros definidos

        # Dibujar puerta
        if self.control_puerta:
            for puerta in self.puertas:
                 Puerta(screen, puerta)

        # Dibujar llave
        screen.blit(self.llave.image, self.llave.rect)

        # ****** Dibujo de personajes

        # Dibujar jugador
        screen.blit(self.player.image, self.player.rect)

        # Dibujo fantasma
        screen.blit(self.ghost.image, self.ghost.rect)

        if developer:
            pygame.draw.circle(screen, red, (self.ghost.rect.x, self.ghost.rect.y), self.ghost.vista, 1)

        # Dibujo casa
        screen.blit(self.casa.image, self.casa.rect)
    
        pygame.display.flip()


# ******************************************************
# ****************** BUCLE PRINCIPAL *******************
# ******************************************************

def main():
    # ****** Centra la ventana
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()

    # ****** Inicializa ventala
    screen = pygame.display.set_mode(screen_size)#, pygame.FULLSCREEN)
    pygame.display.set_caption(u'Laberinto')

    # ****** Oculta el ratón
    pygame.mouse.set_visible(1)

    done = False
    clock = pygame.time.Clock()

    game = Game()

    while not done:
        done = game.process_events() # Sale del bucle while para cerrar el programa
        game.run_logic()
        game.display_frame(screen)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
