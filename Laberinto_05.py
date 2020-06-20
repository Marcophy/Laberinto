# coding=utf-8

import pygame, math, os

os.chdir('d:\Marco\Documentos\8 - Python\Gusanillo\Pygame')

version = "Version 0.5"

# ****** Crear ventana ******
screen_size = (2500, 1250)

black = (0, 0, 0)
red = (255, 0 , 0)
white = (255, 255, 255)
brown = (139, 69, 19)
yellow = (255, 238, 0)

# ****** Variables ******
FPS = 60
sprite_ratio = 15
# control_llave = True    # Llave no encontrada

# Muros
paso = True
pointer = 1
muros = []
puertas = []
archivo = open('pantalla.txt', 'r')
for linea in archivo.readlines():
    if linea == 'DOOR\n':
        pointer += 1
        paso = False

    if paso:
        if pointer == 1:
            linea = tuple(map(int, linea.split(', ')))
            muros.append(pygame.Rect(linea))
        elif pointer == 2:
            linea = tuple(map(int, linea.split(', ')))
            puertas.append(pygame.Rect(linea))

    paso = True

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
        self.image = pygame.image.load('Fantasma_left_30x30_2.png').convert()
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
        # ****** Variables del menú principal
        self.menu = True                # Menú principal
        self.menu_option = 1
        self.menu_text_list = ["Jugar","Salir"] # IDs = [1, 2]

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
        self.player.rect.y = 48

        self.player_vidas.rect.x = 5
        self.player_vidas.rect.y = 5

    def restart(self):
        # ****** Variables
        self.game_over = False      # Juego no perdido
        self.control_llave = False  # Llave no encontrada
        self.control_puerta = True  # Puerta cerrada

        # ****** Jugador
        self.player.rect.x = 0
        self.player.rect.y = 48

        # ****** Llave
        self.llave.rect.x = 0
        self.llave.rect.y = screen_size[1] - 2*sprite_ratio

        # ****** Fantasmas
        self.ghost.rect.x = screen_size[0] - 2*sprite_ratio
        self.ghost.rect.y = screen_size[1] - 2*sprite_ratio

    def process_events(self):
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                # Cierra el programa al presionar la X de la esquina
                return True

            # Evento teclado
            if events.type == pygame.KEYDOWN:
                if self.menu: # Eventos del menú principal
                        if events.key == pygame.K_UP:
                            if self.menu_option > 1:
                                self.menu_option -= 1
                        if events.key == pygame.K_DOWN:
                            if self.menu_option < len(self.menu_text_list):
                                self.menu_option += 1
                        if events.key == pygame.K_RETURN:
                            if self.menu_option == 1:
                                self.menu = False
                            else:
                                return True

                else: # Eventos del juego
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
                if events.key == pygame.K_SPACE:
                    # Reinicia el juego despues de Game over pulsando la barra espaciadora
                    if self.game_over or self.game_win:
                        self.__init__()

        return False

    def run_logic(self):
        # regogida de llave
        if pygame.sprite.collide_rect(self.player, self.llave):
            self.llave.rect.x = screen_size[0] - 2*sprite_ratio
            self.llave.rect.y = 3
            self.control_llave = True

        # ****** Colisiones
        for muro in muros:
            if self.player.rect.colliderect(muro):
                self.player_speed_x = 0
                self.player_speed_y = 0
                self.player.rect.x = self.player.pos_player_old_x
                self.player.rect.y = self.player.pos_player_old_y

            if self.ghost.rect.colliderect(muro): # MEJORAR CHOQUES DE FANTASMAS CON LOS MUROS PARA QUE SIGAN AL JUGADOR
                self.ghost_speed_x = 0
                self.ghost_speed_y = 0
                self.ghost.rect.x = self.ghost.pos_ghost_old_x
                self.ghost.rect.y = self.ghost.pos_ghost_old_y

        for puerta in puertas:
            if self.player.rect.colliderect(puerta):
                if self.control_llave == True:
                    self.control_puerta = False
                else:
                    self.player_speed_x = 0
                    self.player_speed_y = 0
                    self.player.rect.x = self.player.pos_player_old_x
                    self.player.rect.y = self.player.pos_player_old_y

            if self.ghost.rect.colliderect(puerta):
                if self.control_puerta == True:
                    self.ghost_speed_x = 0
                    self.ghost_speed_y = 0
                    self.ghost.rect.x = self.ghost.pos_ghost_old_x
                    self.ghost.rect.y = self.ghost.pos_ghost_old_y
        
        if self.ghost.rect.colliderect(self.casa):
            self.ghost_speed_x = 0
            self.ghost_speed_y = 0
            self.ghost.rect.x = self.ghost.pos_ghost_old_x
            self.ghost.rect.y = self.ghost.pos_ghost_old_y

        if self.player.rect.colliderect(self.ghost):
            self.restart()
            if self.vidas == 1:
                self.game_over = True
            else:
                self.vidas -= 1

        if self.player.rect.colliderect(self.casa):
            self.game_win = True

        self.player.update()
        self.ghost.update(self.player)
        

    def display_frame(self, screen):
        screen.fill(black)
        if self.menu: # ****** PANTALLA DE MENÚ
            font = pygame.font.SysFont("serif", 120, bold=True, italic=True)
            title_text = font.render("LABERINTO", True, white)
            title_pos_x = (screen_size[0] // 2) - (title_text.get_width() // 2)
            title_pos_y = (screen_size[1] // 2) - (title_text.get_height() // 2) - 250
            screen.blit(title_text, [title_pos_x, title_pos_y])

            font = pygame.font.SysFont("serif", 30, bold=False, italic=False)
            version_text = font.render(version, True, white)
            version_pos_x = screen_size[0] - version_text.get_width() - 25
            version_pos_y = screen_size[1] - version_text.get_height() - 25
            screen.blit(version_text, [version_pos_x, version_pos_y])

            font = pygame.font.SysFont("serif", 60, bold=True, italic=True)
            menu_pos_y = (screen_size[1] //2) - 100
            cnt = 0
            for text in self.menu_text_list:
                cnt += 1
                if cnt == self.menu_option:
                    color = yellow
                else:
                    color = white

                menu_text = font.render(text, True, color)
                menu_pos_x = (screen_size[0] //2) - (menu_text.get_width() // 2)
                menu_pos_y += 120
                screen.blit(menu_text, [menu_pos_x, menu_pos_y])

        else: # ****** PANTALLA DEL JUEGO
            if self.game_over:
                font = pygame.font.SysFont("serif", 60, bold=False, italic=False)
                game_over_text = font.render("GAME OVER, Click to continue", True, white)
                game_over_pos_x = (screen_size[0] //2) - (game_over_text.get_width() // 2)
                game_over_pos_y = (screen_size[1] //2) - (game_over_text.get_height() // 2)
                screen.blit(game_over_text, [game_over_pos_x, game_over_pos_y])
            elif self.game_win:
                font = pygame.font.SysFont("serif", 60, bold=False, italic=False)
                game_over_text = font.render("WINNER!, Click to continue", True, white)
                game_over_pos_x = (screen_size[0] //2) - (game_over_text.get_width() // 2)
                game_over_pos_y = (screen_size[1] //2) - (game_over_text.get_height() // 2)
                screen.blit(game_over_text, [game_over_pos_x, game_over_pos_y])
            else:
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
                for muro in muros:
                    Muro(screen, muro)  # Pinta todo los muros definidos

                # Dibujar puerta
                if self.control_puerta:
                    for puerta in puertas:
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
    pygame.mouse.set_visible(0)

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
