import pygame
import game as game
import os
from button import Button
from utils import Color, Size, Point

pygame.init()

def menu_screen():

    control = 1
    play_music('intro.mp3', 1)

    font = pygame.font.Font(os.path.join('assets', '8-bitanco.ttf'), 80)

    display = pygame.display.set_mode((640, 480))

    btn_start = Button(display, Size.DISPLAY_W//2,  Size.DISPLAY_H//2, 100, 50, Color.BTN_COLOR)
    btn_start.write('Start', Color.WHITE)

    btn_quit = Button(display, Size.DISPLAY_W//2,  Size.DISPLAY_H//2 + 70, 100, 50, Color.BTN_COLOR)
    btn_quit.write('Quit', Color.WHITE)

    btn_settings = Button(display, Size.DISPLAY_W//2,  Size.DISPLAY_H//2 + 140, 100, 50, Color.BTN_COLOR)
    btn_settings.write('Settings', Color.WHITE)

    while True:
        surface = pygame.Surface([Size.DISPLAY_W, Size.DISPLAY_H], pygame.SRCALPHA)
        pygame.draw.rect(surface, (*Color.GRAY, 150), pygame.Rect(0, 0, Size.DISPLAY_W, Size.DISPLAY_H))
        display.blit(surface, (0,0))

        pygame.display.set_caption('Snake Game')

        center = Point(Size.DISPLAY_W//2, Size.DISPLAY_H//2 - 100)
        show_text(display, font, 'Snake Game',  Color.BLACK, center)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        if btn_start.draw():
            score = game.play_game(control)
            game_over_screen(score)

            play_music('intro.mp3', 1)

        if btn_quit.draw():
            pygame.quit()

        if btn_settings.draw():
            control = settings_screen()

        pygame.display.flip()

def game_over_screen(score):

    pygame.init()

    font_game_over = pygame.font.Font(os.path.join('assets', '8-bitanco.ttf'), 50)
    font_score = pygame.font.SysFont('arial', 30)

    display = pygame.display.set_mode((640, 480))

    btn_restart = Button(display, 440, 260, 125, 50, Color.BTN_COLOR)
    btn_restart.write('Restart', Color.WHITE)

    btn_menu = Button(display, 200, 260, 125, 50, Color.BTN_COLOR)
    btn_menu.write('Menu', Color.WHITE)

    while True:
        surface = pygame.Surface([Size.DISPLAY_W, Size.DISPLAY_H], pygame.SRCALPHA)
        pygame.draw.rect(surface, (*Color.GRAY, 150), pygame.Rect(0, 0, Size.DISPLAY_W, Size.DISPLAY_H))
        display.blit(surface, (0,0))

        pygame.display.set_caption('Snake Game')

        center_game_over = Point(Size.DISPLAY_W//2, Size.DISPLAY_H//2 - 100)
        center_score = Point(Size.DISPLAY_W//2, Size.DISPLAY_H//2 - 50)

        show_text(display, font_game_over, 'GAME OVER',  Color.BLACK, center_game_over)
        show_text(display, font_score, 'Final Score: ' + str(score),  Color.BLACK, center_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        if btn_restart.draw():
            score = game.play_game()
        
        if btn_menu.draw():
            return

        pygame.display.flip()

def settings_screen():

    opt1_img = pygame.image.load(os.path.join('assets','arrows.png'))
    opt1_img = pygame.transform.scale(opt1_img, (100, 80))

    opt2_img = pygame.image.load(os.path.join('assets','wasd.png'))
    opt2_img = pygame.transform.scale(opt2_img, (100, 80))

    opt1_rect = opt1_img.get_rect()
    opt1_rect.center = (210, 200)

    opt2_rect = opt1_img.get_rect()
    opt2_rect.center = (420, 200)
    
    font = pygame.font.SysFont('arial', 30)

    display = pygame.display.set_mode((640, 480))

    btn_menu = Button(display, Size.DISPLAY_W//2, 430, 100, 50, Color.BTN_COLOR)
    btn_menu.write('Menu', Color.WHITE)

    while True:
        surface = pygame.Surface([Size.DISPLAY_W, Size.DISPLAY_H], pygame.SRCALPHA)
        pygame.draw.rect(surface, (*Color.GRAY, 150), pygame.Rect(0, 0, Size.DISPLAY_W, Size.DISPLAY_H))
        display.blit(surface, (0,0))

        pygame.display.set_caption('Snake Game')

        center_msg = Point(Size.DISPLAY_W//2, 100)

        show_text(display, font, 'Choose control system:',  Color.BLACK, center_msg)

        display.blit(opt1_img, opt1_rect.topleft)
        display.blit(opt2_img, opt2_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if opt1_rect.collidepoint(event.pos):
                    control = 1

                if opt2_rect.collidepoint(event.pos):
                    control = 2
        
        if btn_menu.draw():
            return control
        


        pygame.display.flip()
    
def show_text(display, font, text, color, center):

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    text_rect.center = center

    display.blit(text_surface, text_rect.topleft)

def play_music(music_file, volume):

    pygame.mixer.music.stop()
    pygame.mixer.music.load(os.path.join('assets', music_file))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)