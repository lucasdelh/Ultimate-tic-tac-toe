import pygame
from client import *
from AIminimaxV1 import *
def main(a,serverPort,serverName):
    played_positions = []
    #Matrices A(i,j,k,l) mettant 1 quand une personne a joué dans la grande case de coordonnée (i,j), et de petite coordonnee (k,l)
    server_positions_array = np.zeros((3,3,3,3))
    client_positions_array = np.zeros((3,3,3,3))

    #Matrice A(i,j) mettant 1 quand la personne a gagné la grande case (i,j)
    big_table_server = np.zeros((3,3))
    big_table_client = np.zeros((3,3))

    time_out = 10

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    print('OK')
    starting_message = "UTTT/1.0 CONNECTION [PSEUDO_GUEST]\n"
    clientSocket.send(starting_message.encode())
    send_time = time.time()
    print(starting_message)
    response = clientSocket.recv(1024).decode()
    recv_time = time.time()
    #time out connexion
    if recv_time - send_time > time_out:
        clientSocket.send("UTTT/1.0 406 FATAL_ERROR\n".encode())
        clientSocket.close()

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
        global done
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
                done=True
        for y in range(0,3):
            if TotalGrid[0][y] == Team and TotalGrid[1][y] == Team and TotalGrid[2][y] == Team:
                print("Win detected on ",y)
                if Team == 1:
                    SetWin(Grid,1,TotalGrid)
                else:
                    SetWin(Grid,2,TotalGrid)
                done=True
        if (TotalGrid[0][0] ==Team and TotalGrid[1][1] == Team and TotalGrid[2][2] == Team) or (TotalGrid[2][0] == Team and TotalGrid[1][1] == Team and TotalGrid[0][2] == Team ):
            print("Win here detected")
            if Team == 1:
                SetWin(Grid,1,TotalGrid)
            else:
                SetWin(Grid,2,TotalGrid)
            done=True
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

    WINDOW_SIZE = [totxsize, totysize]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_caption("Ulimate Tic tac toe")
    try:
        gameIcon = pygame.image.load('Logo2.png')
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
    memory={}
    clock = pygame.time.Clock()
    tot3by3 = (3*WIDTH+MARGIN)
    validite_coup_server = True
    exit = False
    # Draw the grid
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
    while True: 
        if validite_coup_server == True:
                state_of_play_client = construction_state_of_play(server_positions_array, client_positions_array)
                TotalGrid_AI=Convertmain(grid)
                indexGrid=3*(allowedy//3)+allowedx//3
                pos=Minimax(TotalGrid_AI,indexGrid,5,2,memory)[1]
                print(pos)
                xcord=3*(pos[0]%3)+pos[1]%3
                ycord=3*(pos[0]//3)+pos[1]//3
                grid[xcord][ycord]=1
                redPlaying = False
                playcolour = BLUE
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
                position_client = str(xcord//3+(ycord//3)*3)+str(xcord%3+(ycord%3)*3)
                print(xcord,ycord)
                print(position_client)
                '''position_client = interfaceSocket.recv(1024).decode()'''
                play_message_client = f"UTTT/1.0 PLAY {position_client} {state_of_play_client}\n"
                clientSocket.send(play_message_client.encode())

        confirmation_server = clientSocket.recv(1024).decode()
        if confirmation_server.startswith("UTTT/1.0 405 BAD_REQUEST\n"):
            print("La position que vous avez jouée n'est pas valide ou mal formatée.")
            continue

        else:
            client_indices = get_indices(position_client)
            client_positions_array[client_indices] = 1
            sub_win(client_positions_array,client_indices,big_table_client, "GUEST")
            state_of_play_client = construction_state_of_play(server_positions_array, client_positions_array)
            state_of_play_server = confirmation_server.split()[-1]
            if state_of_play_client != state_of_play_server: 
                print("pas meme state 1")
                #continuez ce cas 
            else:
                clientSocket.send("UTTT/1.0 ACK\n".encode())
                validite_coup_server = ''
                while validite_coup_server != True:
                    play_message_server = clientSocket.recv(1024).decode()
                    print(play_message_server)
                    time1 = time.time()
                    if play_message_server == "UTTT/1.0 406 FATAL_ERROR\n":
                        print("fatal error")
                        clientSocket.close()
                        exit = True
                        break
                    elif play_message_server == "UTTT/1.0 WIN GUEST\n":
                        if big_win(big_table_client)==True:
                            clientSocket.send("UTTT/1.0 END\n".encode())
                            print("Le guest a gagné")
                            clientSocket.close()
                            return "Guest"
                            exit = True
                            break
                        else:
                            clientSocket.send("UTTT/1.0 FATAL_ERROR\n".encode())
                            print("fatal error")
                            clientSocket.close()
                            exit = True
                            break
                    elif play_message_server == "UTTT/1.0 WIN\n":
                        if draw(big_table_server, big_table_client)==True:
                            clientSocket.send("UTTT/1.0 END\n".encode())
                            print("Draw")
                            clientSocket.close()
                            return "Draw"
                            exit = True
                            break
                        else:
                            clientSocket.send("UTTT/1.0 FATAL_ERROR\n".encode())
                            print("fatal error")
                            clientSocket.close()
                            exit = True
                            break
                    else:
                        position_server = play_message_server.split()[-2]
                        server_indices = get_indices(position_server)
                        print(server_indices)
                        if not position_server.isdigit() or len(position_server) != 2 or '9' in position_server:
                            validite_coup_server = False
                            clientSocket.send("UTTT/1.0 405 BAD_REQUEST\n".encode())
                        elif client_positions_array[server_indices] == 1 or server_positions_array[server_indices] == 1:
                            validite_coup_server = False
                            clientSocket.send("UTTT/1.0 405 BAD_REQUEST\n".encode())
                        elif (position_server[0] != play_message_client.split()[-2][1]) and (big_table_client[client_indices[2:]]==0) and (big_table_server[client_indices[2:]]==0):
                            validite_coup_server = False
                            clientSocket.send("UTTT/1.0 405 BAD_REQUEST\n".encode())
                        elif big_table_client[server_indices[0:2]]==1 or big_table_server[server_indices[0:2]]==1:
                            validite_coup_server = False
                            clientSocket.send("UTTT/1.0 405 BAD_REQUEST\n".encode())
                        else:
                            validite_coup_server = True
                            server_positions_array[server_indices] = 1                    
                            #Ajoute 1 dans la big_table_server si la subcase est gagné
                            sub_win(server_positions_array,server_indices,big_table_server, "HOST")

                            state_of_play_client = construction_state_of_play(server_positions_array, client_positions_array)
                            xcord,ycord=server_indices[1]*3+server_indices[3],server_indices[0]*3+server_indices[2]
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
                            clientSocket.send(f"UTTT/1.0 NEW_STATE {state_of_play_client}\n".encode())
                            confirmation = clientSocket.recv(1024).decode()
                            time2 = time.time()
                            if confirmation != "UTTT/1.0 ACK\n":
                                print('pas meme state 2')
                            else:
                                #time out
                                if time2 - time1 > time_out:
                                    clientSocket.send("UTTT/1.0 406 FATAL_ERROR\n".encode())
                                    clientSocket.close()
                                    exit = True
                                    break
                                else:
                                    #Regarde si 3 cases alignés dans la big_table_server
                                    if big_win(big_table_server)==True:
                                        clientSocket.send("UTTT/1.0 WIN HOST\n".encode())
                                        response = clientSocket.recv(1024).decode()
                                        if response == "UTTT/1.0 END\n":
                                            print("Le host a gagné")
                                            clientSocket.close()
                                            return "Host"
                                            exit = True
                                            break
                                        else:
                                            print("fatal error")
                                            clientSocket.close()
                                            exit = True
                                            break
                                    elif draw(big_table_server,big_table_client)==True:
                                        clientSocket.send("UTTT/1.0 WIN\n".encode())
                                        response = clientSocket.recv(1024).decode()
                                        if response == "UTTT/1.0 END\n":
                                            print("Draw")
                                            clientSocket.close()
                                            return "Draw"
                                            exit = True
                                            break
                                        else:
                                            print("fatal error")
                                            clientSocket.close()
                                            exit = True
                                            break
                if exit == True:
                    break

    
                            




    

    pygame.quit()
