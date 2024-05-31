import pygame
import os
from server import *
def main(a):
    serverPort = 2020

    '''played_positions = []'''
    #Matrices A(i,j,k,l) mettant 1 quand une personne a joué dans la grande case de coordonnée (i,j), et de petite coordonnee (k,l)
    server_positions_array = np.zeros((3,3,3,3))
    client_positions_array = np.zeros((3,3,3,3))

    #Matrice A(i,j) mettant 1 quand la personne a gagné la grande case (i,j)
    big_table_server = np.zeros((3,3))
    big_table_client = np.zeros((3,3))

    time_out = 10

    ### Connexion
    serverSocket = socket(AF_INET, SOCK_STREAM)  
    serverSocket.bind(('', serverPort))  
    serverSocket.listen(1)  
    print("Waiting for guest player to connect...")


    interfacePort = 12310
    interfaceSocket = socket(AF_INET, SOCK_STREAM)  
    interfaceSocket.bind(('', interfacePort))  
    interfaceSocket.listen(1)


    connectionSocket, addr = serverSocket.accept()
    message_client = connectionSocket.recv(1024).decode()

    starting_message = f"UTTT/1.0 CONNECTION [PSEUDO_HOTE]\n"
    connectionSocket.send(starting_message.encode())
    print(starting_message)

    # Load player images
    print("a is", a)
    if a == 1:
        PNL = pygame.image.load("image/pnl.png") 
        PNL2 = pygame.image.load("image/pnl2.jpg") 
    elif a == 2:
        PNL = pygame.image.load("image/pnl.png") #à modifier
        PNL2 = pygame.image.load("image/pnl.png")



    darkmode = "n"
    if "y" in darkmode:
        BLACK = (255, 255, 255)
        WHITE = (0, 0, 0)
        GREEN = (255, 0, 255)
        RED = (0, 255, 255)
        BLUE = (255,255,0)
    else:
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        BLUE = (0,255,0)


    amtrow =9
    amtcol =9
    # HEIGHT AND WIDTH NEED TO BE LARGER THAN MARGIN !!!
    HEIGHT = 75
    WIDTH = 75
    MARGIN = 5
    playcolour = [25, 250, 100]
    grid = []
    TotalGrid = []
    totxsize = ((WIDTH + MARGIN) * amtrow)+5*MARGIN
    totysize = ((HEIGHT + MARGIN) * amtcol)+5*MARGIN


    def ResizePlayBox(playrect,allowedx,allowedy):
        if allowedx == -1 and allowedy == -1:
            playrect[0] = MARGIN
            playrect[1] = MARGIN
            playrect[2] = (3*WIDTH + 4*MARGIN)*3
            playrect[3] = (3*HEIGHT + 4*MARGIN)*3
        else:

            playrect[1]=allowedy*(MARGIN+HEIGHT) + 2*MARGIN + ((allowedy//3 -1)*MARGIN)
            playrect[0]=allowedx*(MARGIN+WIDTH) + 2*MARGIN + ((allowedx//3 -1) *MARGIN)
            playrect[2]=(MARGIN+WIDTH)*3 + MARGIN
            playrect[3]=(MARGIN+HEIGHT)*3 + MARGIN


    def NextBox(Ccords,TotalGrid):
        boxFull = False
        if TotalGrid[Ccords[0]%3][Ccords[1]%3] != 0:
            return (-1,-1)
        else:
            return((Ccords[0]%3)*3,(Ccords[1]%3)*3)
    def SetWin(Grid,Team,TotalGrid):
        for x in range(amtrow):
            for y in range(amtcol):
                Grid[x][y] = Team
        for x in TotalGrid:
            for y in x:
                y = Team

    def winSetter(OC,Team,Grid,TotalGrid):
        TotalGrid[OC[0]//3][OC[1]//3] = Team
        for x in range((OC[0]//3) * 3,(OC[0]//3) *3 + 3):
            for y in range((OC[1]//3) * 3,(OC[1]//3) *3 + 3):
                grid[x][y] = Team
        for x in range(0,3):
            if TotalGrid[x][0] == Team and TotalGrid[x][1] == Team and TotalGrid[x][2] == Team:
                print("Win detected on",x)
                if Team == 1:
                    SetWin(Grid,1,TotalGrid)
                else:
                    SetWin(Grid,2,TotalGrid)
        for y in range(0,3):
            if TotalGrid[0][y] == Team and TotalGrid[1][y] == Team and TotalGrid[2][y] == Team:
                print("Win detected on ",y)
                if Team == 1:
                    SetWin(Grid,1,TotalGrid)
                else:
                    SetWin(Grid,2,TotalGrid)
        if (TotalGrid[0][0] ==Team and TotalGrid[1][1] == Team and TotalGrid[2][2] == Team) or (TotalGrid[2][0] == Team and TotalGrid[1][1] == Team and TotalGrid[0][2] == Team ):
            print("Win here detected")
            if Team == 1:
                SetWin(Grid,1,TotalGrid)
            else:
                SetWin(Grid,2,TotalGrid)
        print(TotalGrid)

    def winCalc(OuterCords,Grid,TotalGrid):
        OC = OuterCords
        IC = (OC[0]%3,OC[1]%3)
        thisTileTeam = Grid[OC[0]][OC[1]]
        Team = thisTileTeam
        if thisTileTeam == 0:
            return "Invaild Team"
        if IC == (0,0):

            if Grid[OC[0]+1][OC[1]] == thisTileTeam and Grid[OC[0]+2][OC[1]] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
            elif Grid[OC[0]][OC[1]+1] == thisTileTeam and Grid[OC[0]][OC[1]+2] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
            elif Grid[OC[0]+1][OC[1]+1] == thisTileTeam and Grid[OC[0]+2][OC[1]+2] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif IC == (1,0):
            if Grid[OC[0]+1][OC[1]] == thisTileTeam and Grid[OC[0]-1][OC[1]] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
            elif Grid[OC[0]][OC[1]+1] == thisTileTeam and Grid[OC[0]][OC[1]+2] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif IC == (2,0):
            if Grid[OC[0]-1][OC[1]] == thisTileTeam and Grid[OC[0]-2][OC[1]] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
            elif Grid[OC[0]][OC[1]+1] == thisTileTeam and Grid[OC[0]][OC[1]+2] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
            elif Grid[OC[0]-1][OC[1]+1] == thisTileTeam and Grid[OC[0]-2][OC[1]+2] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif IC == (0,1):
            if Grid[OC[0]][OC[1]+1] == thisTileTeam and Grid[OC[0]][OC[1]-1] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
            elif Grid[OC[0]+1][OC[1]] == thisTileTeam and Grid[OC[0]+2][OC[1]] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif IC == (1,1):
            if Grid[OC[0]][OC[1]+1] == thisTileTeam and Grid[OC[0]][OC[1]-1] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
            elif Grid[OC[0]+1][OC[1]] == thisTileTeam and Grid[OC[0]-1][OC[1]] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
            elif Grid[OC[0]-1][OC[1]-1] == thisTileTeam and Grid[OC[0]+1][OC[1]+1] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
            elif Grid[OC[0]-1][OC[1]+1] == thisTileTeam and Grid[OC[0]+1][OC[1]-1] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)

        elif IC == (2,1):
            if Grid[OC[0]][OC[1]+1] == thisTileTeam and Grid[OC[0]][OC[1]-1] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
            elif Grid[OC[0]-1][OC[1]] == thisTileTeam and Grid[OC[0]-2][OC[1]] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)

        elif IC == (0,2):
            if Grid[OC[0]+1][OC[1]] == thisTileTeam and Grid[OC[0]+2][OC[1]] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
            elif Grid[OC[0]][OC[1]-1] == thisTileTeam and Grid[OC[0]][OC[1]-2] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
            elif Grid[OC[0]+1][OC[1]-1] == thisTileTeam and Grid[OC[0]+2][OC[1]-2] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif IC == (1,2):
            if Grid[OC[0]+1][OC[1]] == thisTileTeam and Grid[OC[0]-1][OC[1]] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
            elif Grid[OC[0]][OC[1]-1] == thisTileTeam and Grid[OC[0]][OC[1]-2] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)

        elif IC == (2,2):
            if (Grid[OC[0]][OC[1]-1] == thisTileTeam and Grid[OC[0]][OC[1]-2] == thisTileTeam) :
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
            elif (Grid[OC[0]-1][OC[1]] == thisTileTeam and Grid[OC[0]-2][OC[1]] == thisTileTeam):
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
            elif Grid[OC[0]-1][OC[1]-1] == thisTileTeam and Grid[OC[0]-2][OC[1]-2] == thisTileTeam:
                winSetter(OC,thisTileTeam,Grid,TotalGrid)
        amtused = 0
        #print(OC[0],IC[0],OC[1],IC[1])
        for x in range(OC[0]-IC[0],OC[0]-IC[0]+3):
            for y in range(OC[1]-IC[1],OC[1]-IC[1]+3):
                if Grid[x][y] != 0:
                    amtused = amtused + 1
        if amtused == 9:
            if TotalGrid[OC[0]//3][OC[1]//3] == 0:
                TotalGrid[OC[0]//3][OC[1]//3] = -1
                print("Box tied!!")

        #print(TiedBox)






    for row in range(3):

        TotalGrid.append([])
        for column in range(3):
            TotalGrid[row].append(0)



    for row in range(amtrow):

        grid.append([])
        for column in range(amtcol):
            grid[row].append(0)


    print(grid)
    # Initialize pygame
    pygame.init()
    #video.preview()

    WINDOW_SIZE = [totxsize, totysize]
    screen = pygame.display.set_mode(WINDOW_SIZE)





    pygame.display.set_caption("Ulimate Tic tac toe")
    try:
        gameIcon = pygame.image.load('image/pnl.png')
        pygame.display.set_icon(gameIcon)
    except:
        print("No logo found starting anyway")
    allowedx = -1
    allowedy = -1
    playablex = MARGIN
    playabley = MARGIN
    playsizex = (3*WIDTH + 4*MARGIN)*3
    playsizey = (3*HEIGHT + 4*MARGIN)*3
    playrect = [playablex,playabley,playsizex,playsizex]
    playwidth = int(WIDTH//20)
    if playwidth == 0:
        playwidth = 1
    done = False
    redPlaying = True
    clock = pygame.time.Clock()
    tot3by3 = (3*WIDTH+MARGIN)
    screen.fill(BLACK)
    extramarginx = 0
    extramarginy = 0
    for row in range(amtrow):
        if row%3 == 0:
            extramarginy = extramarginy +MARGIN
        for column in range(amtcol):
            color = WHITE
            if column%3 == 0:
                extramarginx = extramarginx + MARGIN
            if grid[column][row] == 1:
                color = RED
            if grid[column][row] == 2:
                color = BLUE
            pygame.draw.rect(screen,
                            color,
                            [((MARGIN + WIDTH) * column) + MARGIN + extramarginx,
                            ((MARGIN + HEIGHT) * row) + MARGIN+ extramarginy,
                            WIDTH,
                            HEIGHT])
            pygame.draw.rect(screen, playcolour, playrect,playwidth)
        extramarginx =0
    clock.tick(60)
    pygame.display.flip()
    num_tour = 1
    while True:
        play_message_client = connectionSocket.recv(1024).decode()
        time1 = time.time()
        if play_message_client == "UTTT/1.0 406 FATAL_ERROR\n":
            print("fatal error")
            connectionSocket.close()
            serverSocket.close()
            break
        elif play_message_client == "UTTT/1.0 WIN HOST\n":
            if big_win(big_table_server) == True:
                connectionSocket.send("UTTT/1.0 END\n".encode())
                print("Le host a gagné")
                connectionSocket.close()
                serverSocket.close()
                return "Host"
                break
            else:
                connectionSocket.send("UTTT/1.0 FATAL_ERROR\n".encode())
                print("fatal error")
                connectionSocket.close()
                break
        elif play_message_client == "UTTT/1.0 WIN\n":
            if draw(big_table_server, big_table_client) == True:
                connectionSocket.send("UTTT/1.0 END\n".encode())
                print("Draw")
                connectionSocket.close()
                serverSocket.close()
                return "Draw"
                break
            else:
                connectionSocket.send("UTTT/1.0 FATAL_ERROR\n".encode())
                print("fatal error")
                connectionSocket.close()
                break
        else:
            position_client = play_message_client.split()[-2]
            client_indices = get_indices(position_client)
            
            if not position_client.isdigit() or len(position_client) != 2 or '9' in position_client:
                connectionSocket.send("UTTT/1.0 405 BAD_REQUEST\n".encode())
            elif server_positions_array[client_indices] == 1 or client_positions_array[client_indices] == 1:
                connectionSocket.send("UTTT/1.0 405 BAD_REQUEST\n".encode())
            elif (num_tour != 1) and (position_client[0] != play_message_server.split()[-2][1]) and (big_table_server[server_indices[2:]]==0) and (big_table_client[server_indices[2:]]==0):
                connectionSocket.send("UTTT/1.0 405 BAD_REQUEST\n".encode())
            elif big_table_server[client_indices[0:2]]==1 or big_table_client[client_indices[0:2]]==1:
                connectionSocket.send("UTTT/1.0 405 BAD_REQUEST\n".encode())

            else:
                client_positions_array[client_indices] = 1 
                sub_win(client_positions_array,client_indices,big_table_client, "GUEST") 
                state_of_play_server = construction_state_of_play(server_positions_array, client_positions_array)
                xcord,ycord=client_indices[1]*3+client_indices[3],client_indices[0]*3+client_indices[2]
                grid[xcord][ycord]=2
                redPlaying=True
                playcolour=RED
                winCalc([xcord,ycord],grid,TotalGrid)
                allowedx ,allowedy = NextBox([xcord,ycord],TotalGrid)
                ResizePlayBox(playrect,allowedx,allowedy)
                screen.fill(BLACK)
                extramarginx = 0
                extramarginy = 0
                for row in range(amtrow):
                    if row%3 == 0:
                        extramarginy = extramarginy +MARGIN
                    for column in range(amtcol):
                        color = WHITE
                        if column%3 == 0:
                            extramarginx = extramarginx + MARGIN
                        if grid[column][row] == 1:
                            color = RED
                        if grid[column][row] == 2:
                            color = BLUE
                        pygame.draw.rect(screen,
                                        color,
                                        [((MARGIN + WIDTH) * column) + MARGIN + extramarginx,
                                        ((MARGIN + HEIGHT) * row) + MARGIN+ extramarginy,
                                        WIDTH,
                                        HEIGHT])
                        pygame.draw.rect(screen, playcolour, playrect,playwidth)
                    extramarginx =0
                clock.tick(60)
                pygame.display.flip()
                connectionSocket.send(f"UTTT/1.0 NEW_STATE {state_of_play_server}\n".encode())
                confirmation_state = connectionSocket.recv(1024).decode()
                time2 = time.time()
                if confirmation_state != "UTTT/1.0 ACK\n":
                    print('pas le mm state 1')
                    #continuez ce cas
                else:
                    #time out
                    if time2 - time1 > time_out:
                        clientSocket.send("UTTT/1.0 406 FATAL_ERROR\n".encode())
                        clientSocket.close()
                        exit = True
                        break
                    else:
                        if big_win(big_table_client)==True:
                            connectionSocket.send("UTTT/1.0 WIN GUEST\n".encode())
                            response = connectionSocket.recv(1024).decode()
                            if response == "UTTT/1.0 END\n":
                                print("Le guest a gagné")
                                connectionSocket.close()
                                serverSocket.close()
                                return "Guest"
                                break
                            else:
                                print("fatal error")
                                connectionSocket.close()
                                serverSocket.close()
                                break
                        elif draw(big_table_server, big_table_client)==True:
                            connectionSocket.send("UTTT/1.0 WIN\n".encode())
                            response = connectionSocket.recv(1024).decode()
                            if response == "UTTT/1.0 END\n":
                                print("Draw")
                                connectionSocket.close()
                                serverSocket.close()
                                return "Draw"
                                break
                            else:
                                print("fatal error")
                                connectionSocket.close()
                                serverSocket.close()
                                break
                        else:
                            response = ''
                            while not response.startswith("UTTT/1.0 NEW_STATE"):
                                done=False
                                while not done:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            done = True
                                        elif event.type == pygame.K_q:
                                            print ("hiii")
                                            done = True
                                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                            pos = pygame.mouse.get_pos()
                                            xcord = ((pos[0] - ((pos[0]//tot3by3)-1)*MARGIN) - 2*MARGIN) // (MARGIN+WIDTH)
                                            ycord = ((pos[1] - ((pos[1]//tot3by3)-1)*MARGIN) - 2*MARGIN)// (MARGIN+HEIGHT)
                                            print("Click ", pos, "Grid coordinates: ", xcord, ycord , "Inner cords",xcord%3,ycord%3)
                                            if xcord /8 <= 1 and ycord /8 <= 1:
                                                if grid[xcord][ycord] == 0:
                                                    if allowedx == -1 and allowedy == -1: #move anywhere
                                                        if redPlaying == True:
                                                            grid[xcord][ycord] = 1
                                                            redPlaying = False
                                                            playcolour = BLUE
                                                        else:
                                                            grid[xcord][ycord] = 2
                                                            redPlaying = True
                                                            playcolour = RED
                                                        winCalc([xcord,ycord],grid,TotalGrid)
                                                        allowedx ,allowedy = NextBox([xcord,ycord],TotalGrid)
                                                        ResizePlayBox(playrect,allowedx,allowedy)
                                                        done = True
                                                    elif allowedx <= xcord <= allowedx+2 and allowedy <= ycord <= allowedy+2:
                                                        if redPlaying == True:
                                                            grid[xcord][ycord] = 1
                                                            redPlaying = False
                                                            playcolour = BLUE
                                                        else:
                                                            grid[xcord][ycord] = 2
                                                            redPlaying = True
                                                            playcolour = RED
                                                        winCalc([xcord,ycord],grid,TotalGrid)
                                                        allowedx ,allowedy = NextBox([xcord,ycord],TotalGrid)
                                                        ResizePlayBox(playrect,allowedx,allowedy)
                                                        done = True
                                screen.fill(BLACK)
                                extramarginx = 0
                                extramarginy = 0
                                for row in range(amtrow):
                                    if row%3 == 0:
                                        extramarginy = extramarginy +MARGIN
                                    for column in range(amtcol):
                                        color = WHITE
                                        if column%3 == 0:
                                            extramarginx = extramarginx + MARGIN
                                        if grid[column][row] == 1:
                                            color = RED
                                        if grid[column][row] == 2:
                                            color = BLUE
                                        pygame.draw.rect(screen,
                                                        color,
                                                        [((MARGIN + WIDTH) * column) + MARGIN + extramarginx,
                                                        ((MARGIN + HEIGHT) * row) + MARGIN+ extramarginy,
                                                        WIDTH,
                                                        HEIGHT])
                                        pygame.draw.rect(screen, playcolour, playrect,playwidth)
                                    extramarginx =0
                                clock.tick(60)
                                pygame.display.flip()
                                position_server = str(xcord//3+(ycord//3)*3)+str(xcord%3+(ycord%3)*3)
                                play_message_server = f"UTTT/1.0 PLAY {position_server} {state_of_play_server}\n"
                                connectionSocket.send(play_message_server.encode())
                                response = connectionSocket.recv(1024).decode()

                            state_of_play_client = response.split()[-1]
                            server_indices = get_indices(position_server)
                            server_positions_array[server_indices] = 1
                            sub_win(server_positions_array,server_indices,big_table_server, "HOST")
                            state_of_play_server = construction_state_of_play(server_positions_array, client_positions_array)
                            if state_of_play_server != state_of_play_client:
                                print('pas le mm state 2')
                            else:
                                connectionSocket.send("UTTT/1.0 ACK\n".encode())
                                

                num_tour+=1



    pygame.quit()
position=''
#InterfaceSocket.send(position.encode())