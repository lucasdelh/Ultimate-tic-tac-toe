from socket import *
import numpy as np
import hashlib
import time

### Definition
serverPort = 12345
serverName = '172.24.11.107'
'''
interfacePort = 12310
interfaceName = 'localhost'
'''
played_positions = []
#Matrices A(i,j,k,l) mettant 1 quand une personne a joué dans la grande case de coordonnée (i,j), et de petite coordonnee (k,l)
server_positions_array = np.zeros((3,3,3,3))
client_positions_array = np.zeros((3,3,3,3))

#Matrice A(i,j) mettant 1 quand la personne a gagné la grande case (i,j)
big_table_server = np.zeros((3,3))
big_table_client = np.zeros((3,3))

time_out = 10







'''### Connexion
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))'''

'''
interfaceSocket = socket(AF_INET, SOCK_STREAM)  
interfaceSocket.bind(('', interfacePort))  
interfaceSocket.listen(1) 
'''

# Envoie du message de connexion
'''starting_message = "UTTT/1.0 CONNECTION [PSEUDO_GUEST]\n"
clientSocket.send(starting_message.encode())
send_time = time.time()
print(starting_message)
response = clientSocket.recv(1024).decode()
recv_time = time.time()
#time out connexion
if recv_time - send_time > time_out:
    clientSocket.send("UTTT/1.0 406 FATAL_ERROR\n".encode())
    clientSocket.close()'''














### Fonctions
def get_indices(position):
    big_case = int(position[0])
    sub_case = int(position[1])
    bigline, bigcolumn = divmod(big_case, 3)
    subline, subcolumn = divmod(sub_case,3)
    return (bigline, bigcolumn, subline, subcolumn)

def sub_win(positions_array, indices, big_table, person):
    i,j = indices[0:2]
    small_case = positions_array[i,j,:,:]
    played_line = indices[2]
    played_column = indices[3]
    #check if line is won
    if small_case.sum(axis=1)[played_line] == 3:
        big_table[indices[0:2]] = 1
        print(f"une case est gagnée pour le {person} : \n {big_table}")
    #check if column is won
    elif small_case.sum(axis=0)[played_column] == 3:
        big_table[indices[0:2]] = 1
        print(f"une case est gagnée pour le {person} : \n {big_table}")
    #check if diagonal is won
    elif played_line == played_column and np.trace(small_case) == 3:
        big_table[indices[0:2]] = 1
        print(f"une case est gagnée pour le {person} : \n {big_table}")
    #check other diagonal 
    elif played_line == 2 - played_column and np.trace(np.rot90(small_case)) == 3:
        big_table[indices[0:2]] = 1
        print(f"une case est gagnée pour le {person} : \n {big_table}")

def big_win(big_table_server):
    # Check lines
    if np.any(big_table_server.sum(axis=1) == 3):
        return True
    # Check columns
    if np.any(big_table_server.sum(axis=0) == 3):
        return True
    # Check diagonal
    if np.trace(big_table_server) == 3:
        return True
    # Check other diagonal
    if np.trace(np.rot90(big_table_server)) == 3:
        return True
    return False

def draw(big_table_server, big_table_client):
   matrix = np.zeros((3,3))
   for i in range(3):
       for j in range(3):
           if big_table_server[i, j] == 1 or big_table_client[i, j] == 1:
               matrix[i, j] = 1
   if np.array_equal(matrix, np.ones((3,3))):
       return True 
   return False


def construction_state_of_play(server_positions_array, client_positions_array):
    chaine_server = ''.join(server_positions_array.flatten().astype(int).astype(str))
    chaine_client = ''.join(client_positions_array.flatten().astype(int).astype(str))
    chaine = ""
    
    for i in range(len(chaine_server)):
        if chaine_server[i] == '0' and chaine_client[i] == '0':
            chaine += '.'
        elif chaine_server[i] == '1':
            chaine += '0'
        else:
            chaine += '1'
    resultat = chaine[0:9] + '-' + chaine[9:18] + '-' + chaine[18:27] + '/' + chaine[27:36] + '-' + chaine[36:45] + '-' + chaine[45:54] + '/' + chaine[54:63] + '-' + chaine[63:72] + '-' + chaine[72:]
    m = hashlib.sha3_224()
    m.update(resultat.encode('utf-8'))
    print(m.hexdigest())
    return(m.hexdigest())







### Play
'''validite_coup_server = True
exit = False
while True: 
    if validite_coup_server == True:
            state_of_play_client = construction_state_of_play(server_positions_array, client_positions_array)
            position_client = input("Entrez la position du coup : ")
            position_client = interfaceSocket.recv(1024).decode()
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
                                        exit = True
                                        break
                                    else:
                                        print("fatal error")
                                        clientSocket.close()
                                        exit = True
                                        break
            if exit == True:
                break'''


   












