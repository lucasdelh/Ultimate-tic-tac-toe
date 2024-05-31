import pygame
import pygame_gui
import tictactoe
import tictactoe_online_guest
import tictactoe_online_host
import tictactoe_online_guest_AI
import tictactoe_online_host_AI
import mainAI
from socket import *
import numpy as np
import hashlib
import time


# Initialize Pygame
pygame.init()

def load_image(image_path):
    return pygame.transform.scale(pygame.image.load(image_path), (SCREEN_WIDTH, SCREEN_HEIGHT))

def create_button(position, text, manager):
    button_width, button_height = 270, 90
    return pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (button_width, button_height)),
                                        text=text,
                                        manager=manager)

SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

pygame.mixer.music.load('music/StayInsideMe.wav')
pygame.mixer.music.play(-1)
button_sound = pygame.mixer.Sound("music/click.wav")
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
ui_manager = pygame_gui.UIManager(WINDOW_SIZE, 'theme.json')
tic = load_image("image/background.png")

def create_text_entry(position, manager):
    text_entry_width, text_entry_height = 280, 50
    return pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(position, (text_entry_width, text_entry_height)), 
                                               manager=manager)

def menu(a):
    pygame.display.set_caption("Main Menu")
    
    play_button = create_button((SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT / 3), 'Play Game', ui_manager)
    settings_button = create_button((SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT / 2), 'Settings', ui_manager)
    quit_button = create_button((SCREEN_WIDTH / 2 - 125, 3 * SCREEN_HEIGHT / 4.5), 'Quit', ui_manager)
    win_button = create_button((50, SCREEN_HEIGHT - 100), 'Win Page', ui_manager)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                pygame.mixer.Sound.play(button_sound)
                if event.ui_element == play_button:
                    ui_manager.clear_and_reset()
                    local_online(a)
                elif event.ui_element == settings_button:
                    ui_manager.clear_and_reset()
                    settings()
                elif event.ui_element == quit_button:
                    pygame.quit()
                elif event.ui_element == win_button:
                    ui_manager.clear_and_reset()
                    win("Draw")

            ui_manager.process_events(event)

        ui_manager.update(1.0 / 60.0)
        screen.blit(tic, (0, 0))
        ui_manager.draw_ui(screen)
        pygame.display.flip()
    
    pygame.quit()

def local_online(a):
    pygame.display.set_caption("Server/Client Menu")
    
    button_y = SCREEN_HEIGHT / 2 - 40
    server_button = create_button((SCREEN_WIDTH / 2 - 300, button_y), 'Local', ui_manager)
    client_button = create_button((SCREEN_WIDTH / 2 + 20, button_y), 'Online', ui_manager)
    return_button = create_button((50, SCREEN_HEIGHT - 100), 'Return Back', ui_manager)
    text_entry = None
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                pygame.mixer.Sound.play(button_sound)
                if event.ui_element == server_button:
                    print("Server button clicked")
                    ui_manager.clear_and_reset()
                    local(a)
                elif event.ui_element == client_button:
                    ui_manager.clear_and_reset()
                    online(1)
                elif event.ui_element == return_button:
                    ui_manager.clear_and_reset()
                    menu(1)

            ui_manager.process_events(event)

        ui_manager.update(1.0 / 60.0)
        screen.blit(tic, (0, 0))
        ui_manager.draw_ui(screen)
        pygame.display.flip()
    
    pygame.quit()

def local(a):
    pygame.display.set_caption("Server/Client Menu")
    
    button_y = SCREEN_HEIGHT / 2 - 40
    ai_button = create_button((SCREEN_WIDTH / 2 - 300, button_y), 'Player VS AI', ui_manager)
    player_button = create_button((SCREEN_WIDTH / 2 + 20, button_y), 'Player VS Player', ui_manager)
    return_button = create_button((50, SCREEN_HEIGHT - 100), 'Return Back', ui_manager)
    text_entry = None
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                pygame.mixer.Sound.play(button_sound)
                if event.ui_element == ai_button:
                    print("AI button clicked")
                    ui_manager.clear_and_reset()
                    winner=mainAI.main(a)
                    win(winner)
                elif event.ui_element == player_button:
                    ui_manager.clear_and_reset()
                    winner=tictactoe.main(a)
                    win(winner)
                elif event.ui_element == return_button:
                    ui_manager.clear_and_reset()
                    local_online(1)

            ui_manager.process_events(event)

        ui_manager.update(1.0 / 60.0)
        screen.blit(tic, (0, 0))
        ui_manager.draw_ui(screen)
        pygame.display.flip()
    
    pygame.quit()

def online(a):
    pygame.display.set_caption("Server/Client Menu")
    
    button_y = SCREEN_HEIGHT / 2 - 40
    ai_button = create_button((SCREEN_WIDTH / 2 - 300, button_y), 'AI is playing', ui_manager)
    player_button = create_button((SCREEN_WIDTH / 2 + 20, button_y), 'Player is playing', ui_manager)
    return_button = create_button((50, SCREEN_HEIGHT - 100), 'Return Back', ui_manager)
    text_entry = None
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                pygame.mixer.Sound.play(button_sound)
                if event.ui_element == ai_button:
                    print("AI button clicked")
                    ui_manager.clear_and_reset()
                    server_client(a,True)
                elif event.ui_element == player_button:
                    ui_manager.clear_and_reset()
                    server_client(a,False)
                elif event.ui_element == return_button:
                    ui_manager.clear_and_reset()
                    local_online(1)

            ui_manager.process_events(event)

        ui_manager.update(1.0 / 60.0)
        screen.blit(tic, (0, 0))
        ui_manager.draw_ui(screen)
        pygame.display.flip()
    
    pygame.quit()

def server_client(a,AI):
    pygame.display.set_caption("Server/Client Menu")
    
    button_y = SCREEN_HEIGHT / 2 - 40
    server_button = create_button((SCREEN_WIDTH / 2 - 300, button_y), 'Host', ui_manager)
    client_button = create_button((SCREEN_WIDTH / 2 + 20, button_y), 'Guest', ui_manager)
    return_button = create_button((50, SCREEN_HEIGHT - 100), 'Return Back', ui_manager)
    play_button = None
    text_entry = None
    port_entry = None
    police = pygame.font.Font('police/Futured.TTF',30)
    text1=police.render("",1,(255,255,255))
    text2=police.render("",1,(255,255,255))
    pygame.display.flip()

    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                pygame.mixer.Sound.play(button_sound)
                if event.ui_element == server_button:
                    print("Server button clicked")
                    ui_manager.clear_and_reset()
                    pygame.display.set_caption("Main Menu")
                    ui_manager.update(1.0 / 60.0)
                    screen.blit(tic, (0, 0))
                    ui_manager.draw_ui(screen)
                    police1=pygame.font.Font('police/Futured.TTF',60)
                    text3=police1.render("Waiting for opponent ...",1,(255,255,255))
                    screen.blit(text3,(SCREEN_WIDTH / 2 - 300,SCREEN_HEIGHT / 2 - 30))
                    s = socket(AF_INET, SOCK_DGRAM)
                    s.connect(("8.8.8.8", 80))
                    print(s.getsockname()[0])
                    police2=pygame.font.Font('police/Futured.TTF',30)
                    text4=police2.render("IP adress : "+s.getsockname()[0]+"\nPORT : 2020" ,1,(255,255,255))
                    screen.blit(text4,(SCREEN_WIDTH / 2 - 180,SCREEN_HEIGHT / 2 + 70))
                    pygame.display.flip()
                    if AI:
                        winner=tictactoe_online_host_AI.main(a)
                        win(winner)
                    else:
                        winner=tictactoe_online_host.main(a)
                        win(winner)
                elif event.ui_element == client_button:
                    if text_entry == None:
                        print("Client button clicked")
                        text_entry = create_text_entry((SCREEN_WIDTH / 2 - 140, SCREEN_HEIGHT / 2 + 100), ui_manager)
                        port_entry = create_text_entry((SCREEN_WIDTH / 2 - 140, SCREEN_HEIGHT / 2 + 160), ui_manager)
                        text1=police.render("IP adress : ",1,(255,255,255))
                        text2=police.render("Port : ",1,(255,255,255))
                        screen.blit(text1,(SCREEN_WIDTH / 2 - 300,SCREEN_HEIGHT / 2 + 110))
                        screen.blit(text2,(SCREEN_WIDTH / 2 - 230,SCREEN_HEIGHT / 2 + 170))
                        play_button = create_button((SCREEN_WIDTH / 2 - 140 , SCREEN_HEIGHT/2 +230), 'OK', ui_manager)
                        pygame.display.flip()
                elif event.ui_element == play_button:
                    serverName= text_entry.get_text()
                    serverPort = int(port_entry.get_text())
                    print(serverName,serverPort)
                    ui_manager.clear_and_reset()
                    if AI:
                        winner=tictactoe_online_guest_AI.main(a,serverPort,serverName)
                        win(winner)
                    else:
                        winner=tictactoe_online_guest.main(a,serverPort,serverName)
                        win(winner)
                elif event.ui_element == return_button:
                    ui_manager.clear_and_reset()
                    online(1)

            ui_manager.process_events(event)

        ui_manager.update(1.0 / 60.0)
        screen.blit(tic, (0, 0))
        ui_manager.draw_ui(screen)
        screen.blit(text1,(SCREEN_WIDTH / 2 - 295,SCREEN_HEIGHT / 2 + 110))
        screen.blit(text2,(SCREEN_WIDTH / 2 - 230,SCREEN_HEIGHT / 2 + 170))
        pygame.display.flip()
    
    pygame.quit()

def win(winner):
    WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
    pygame.display.set_caption("Server/Client Menu")
    
    button_y = SCREEN_HEIGHT / 2 - 40
    return_button = create_button((SCREEN_WIDTH / 2 - 115, 3 * SCREEN_HEIGHT / 4.5), 'Return Menu', ui_manager)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                pygame.mixer.Sound.play(button_sound)
                if event.ui_element == return_button:
                    ui_manager.clear_and_reset()
                    menu(1)

            ui_manager.process_events(event)

        ui_manager.update(1.0 / 60.0)
        screen.blit(tic, (0, 0))
        ui_manager.draw_ui(screen)
        police=pygame.font.Font('police/Futured.TTF',100)
        if winner!="Draw":
            text1=police.render("Winner :",1,(255,255,255))
            screen.blit(text1,(SCREEN_WIDTH / 2 - 180,SCREEN_HEIGHT / 2 - 120))
            text2=police.render(winner,1,(255,51,153))
            screen.blit(text2,((SCREEN_WIDTH - police.size(winner)[0])/ 2 ,SCREEN_HEIGHT / 2 -20 ))
        else:
            text2=police.render(winner,1,(255,51,153))
            screen.blit(text2,((SCREEN_WIDTH - police.size(winner)[0])/ 2 ,SCREEN_HEIGHT / 2 -70 ))
        pygame.display.flip()
    
    pygame.quit()


def settings():
    pygame.display.set_caption("Extras")
    
    icon_button = create_button((SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT / 4), 'Choose Icon', ui_manager)
    music_button = create_button((SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT / 2), 'Choose Music', ui_manager)
    return_button = create_button((SCREEN_WIDTH / 2 - 125, 3 * SCREEN_HEIGHT / 4), 'Return Back', ui_manager)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                pygame.mixer.Sound.play(button_sound)
                if event.ui_element == icon_button:
                    ui_manager.clear_and_reset()
                    icon()
                elif event.ui_element == return_button:
                    ui_manager.clear_and_reset()
                    menu(1)
                elif event.ui_element == music_button:
                    ui_manager.clear_and_reset()
                    music_interface()

            ui_manager.process_events(event)

        ui_manager.update(1.0 / 60.0)
        screen.blit(tic, (0, 0))
        ui_manager.draw_ui(screen)
        pygame.display.flip()
    
    pygame.quit()

def icon():
    pygame.display.set_caption("Icon")
    
    Image1 = create_button((SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT / 4), 'Image 1', ui_manager)
    Image2 = create_button((SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT / 2), 'Image 2', ui_manager)
    Image3 = create_button((SCREEN_WIDTH / 2 - 125, 3 * SCREEN_HEIGHT / 4), 'Image 3', ui_manager)
    return_button = create_button((50, SCREEN_HEIGHT - 100), 'Return Back', ui_manager)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == Image1:
                    ui_manager.clear_and_reset()
                    menu(1)
                elif event.ui_element == Image2:
                    ui_manager.clear_and_reset()
                    menu(2)
                elif event.ui_element == return_button:
                    ui_manager.clear_and_reset()
                    menu(1)

            ui_manager.process_events(event)

        ui_manager.update(1.0 / 60.0)
        screen.blit(tic, (0, 0))
        ui_manager.draw_ui(screen)
        pygame.display.flip()
    
    pygame.quit()

def music_interface():
    pygame.display.set_caption("Choose Music")
    
    music1_button = create_button((SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT / 4), 'Music 1', ui_manager)
    music2_button = create_button((SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT / 2), 'Music 2', ui_manager)
    music3_button = create_button((SCREEN_WIDTH / 2 - 125, 3 * SCREEN_HEIGHT / 4), 'Music 3', ui_manager)
    return_button = create_button((50, SCREEN_HEIGHT - 100), 'Return Back', ui_manager)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == music1_button:
                    pass
                elif event.ui_element == music2_button:
                    pass
                elif event.ui_element == music3_button:
                    pass
                elif event.ui_element == return_button:
                    ui_manager.clear_and_reset()
                    menu(1)

            ui_manager.process_events(event)

        ui_manager.update(1.0 / 60.0)
        screen.blit(tic, (0, 0))
        ui_manager.draw_ui(screen)
        pygame.display.flip()
    
    pygame.quit()

menu(1)
