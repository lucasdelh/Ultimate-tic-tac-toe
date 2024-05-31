from socket import *
import numpy as np
import hashlib
import time 

### Definition
serverPort = 12352

'''played_positions = []'''
#Matrices A(i,j,k,l) mettant 1 quand une personne a joué dans la grande case de coordonnée (i,j), et de petite coordonnee (k,l)
server_positions_array = np.zeros((3,3,3,3))
client_positions_array = np.zeros((3,3,3,3))

#Matrice A(i,j) mettant 1 quand la personne a gagné la grande case (i,j)
big_table_server = np.zeros((3,3))
big_table_client = np.zeros((3,3))

time_out = 10






'''### Connexion
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





'''
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


def big_win(big_table_client):
    # Check lines
    if np.any(big_table_client.sum(axis=1) == 3):
        return True
    # Check columns
    if np.any(big_table_client.sum(axis=0) == 3):
        return True
    # Check diagonal
    if np.trace(big_table_client) == 3:
        return True
    # Check other diagonal
    if np.trace(np.rot90(big_table_client)) == 3:
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
    print(resultat)
    m = hashlib.sha3_224()
    m.update(resultat.encode('utf-8'))
    print(m.hexdigest())
    return(m.hexdigest())







'''
### Play
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
                            break
                        else:
                            print("fatal error")
                            connectionSocket.close()
                            serverSocket.close()
                            break
                    else:
                        response = ''
                        while not response.startswith("UTTT/1.0 NEW_STATE"):
                            position_server = input("Entrez la position du coup : ")
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
                            

            num_tour+=1'''
            
















