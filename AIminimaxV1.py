import cProfile
memory={}
def Minimax(TotalGrid,indexGrid,Depth,player,memory):
    if Depth==0 or terminated(TotalGrid):
        return get_score(TotalGrid,indexGrid,memory), None
    
    if player==2:
        Maxvalue=-100000
        Best_Totalgrid=None
        pos=None
        all_moves=get_all_moves(TotalGrid,indexGrid)
        if indexGrid<0:
            for k in range(len(all_moves)):
                for i in range(len(all_moves[k])):
                    temp_TotalGrid=[[TotalGrid[n][m] for m in range(9)] for n in range(9)]
                    temp_TotalGrid[k][all_moves[k][i]]=2
                    temp_indexGrid=-1 if len(empty_cells_Grid(temp_TotalGrid[all_moves[k][i]]))==0 else all_moves[k][i]
                    value=Minimax(temp_TotalGrid,temp_indexGrid,Depth-1,1,memory)[0]
                    Maxvalue=max(Maxvalue,value)
                    if Maxvalue==value:
                        pos=(k,all_moves[k][i])
            return Maxvalue, pos

        else:
            for i in range(len(all_moves)):
                temp_TotalGrid=[[TotalGrid[n][m] for m in range(9)] for n in range(9)]
                temp_TotalGrid[indexGrid][all_moves[i]]=2
                temp_indexGrid=-1 if len(empty_cells_Grid(temp_TotalGrid[all_moves[i]]))==0 else all_moves[i]
                value=Minimax(temp_TotalGrid,temp_indexGrid,Depth-1,1,memory)[0]
                Maxvalue=max(Maxvalue,value)
                if Maxvalue==value:
                    pos=(indexGrid,all_moves[i])
            return Maxvalue, pos

    else:
        Minvalue=100000
        Best_Totalgrid=None
        pos=None
        all_moves=get_all_moves(TotalGrid,indexGrid)
        if indexGrid<0:
            for k in range(len(all_moves)):
                for i in range(len(all_moves[k])):
                    temp_TotalGrid=[[TotalGrid[n][m] for m in range(9)] for n in range(9)]
                    temp_TotalGrid[k][all_moves[k][i]]=1
                    temp_indexGrid=-1 if len(empty_cells_Grid(temp_TotalGrid[all_moves[k][i]]))==0 else all_moves[k][i]
                    value=Minimax(temp_TotalGrid,temp_indexGrid,Depth-1,2,memory)[0]
                    Minvalue=min(Minvalue,value)
                    if Minvalue==value:
                        pos=(k,all_moves[k][i])
            return Minvalue, pos

        else:
            for i in range(len(all_moves)):
                temp_TotalGrid=[[TotalGrid[n][m] for m in range(9)] for n in range(9)]
                temp_TotalGrid[indexGrid][all_moves[i]]=1
                temp_indexGrid=-1 if len(empty_cells_Grid(temp_TotalGrid[all_moves[i]]))==0 else all_moves[i]
                value=Minimax(temp_TotalGrid,temp_indexGrid,Depth-1,2,memory)[0]
                Minvalue=min(Minvalue,value)
                if Minvalue==value:
                    pos=(indexGrid,all_moves[i])
            return Minvalue, pos
            

def get_score(TotalGrid,indexGrid,memory):
    # global memory
    score = 0
    mainBd=[]
    evaluatorMul=[1.4,1,1.4,1,1.75,1,1.4,1,1.4]
    for i in range(9):
        Grid=TotalGrid[i]
        if tuple(Grid) in memory :
            grid_score=memory[tuple(Grid)]
        else:
            grid_score=eval_grid(Grid)
            memory[tuple(Grid)]=grid_score

        score += grid_score*1.5*evaluatorMul[i]
        if i == indexGrid:
            score += grid_score*evaluatorMul[i]
        tmpEv=Grid_fill(TotalGrid[i])
        if tmpEv==1:
            score-=evaluatorMul[i]
        elif tmpEv==2:
            score+=evaluatorMul[i]
        mainBd.append(tmpEv)
    #print(mainBd)
    Victory=Grid_fill(mainBd)
    if Victory==1:
        score-=50000 # or 5000
    elif Victory==2:
        score+=50000 # or 5000
    if tuple(mainBd) in memory :
        grid_score=memory[tuple(mainBd)]
    else:
        grid_score=eval_grid(mainBd)
        memory[tuple(mainBd)]=grid_score
    score+=grid_score*150

    return score



def get_all_moves(TotalGrid,indexGrid):
    if indexGrid<0:
        return empty_cells_Totalgrid(TotalGrid)
    else:
        return empty_cells_Grid(TotalGrid[indexGrid])

def eval_grid(Grid):
    score=0
    points=[0.2,0.17,0.2,0.17,0.22,0.17,0.2,0.17,0.2]
    for i in range(9):
        if Grid[i]==1:
            score-=points[i]
        elif Grid[i]==2:
            score+=points[i]
    
    L1=[Grid[k] for k in range(3)]
    L2=[Grid[3+k] for k in range(3)]
    L3=[Grid[6+k] for k in range(3)]
    C1=[Grid[3*k] for k in range(3)]
    C2=[Grid[3*k+1] for k in range(3)]
    C3=[Grid[3*k+2] for k in range(3)]
    D1=[Grid[4*k] for k in range(3)]
    D2=[Grid[2*(k+1)] for k in range(3)]

    # player
    if L1.count(1)==2 or L2.count(1)==2 or L3.count(1)==2:
        score-=6
    if C1.count(1)==2 or C2.count(1)==2 or C3.count(1)==2:
        score-=6
    if D1.count(1)==2 or D2.count(1)==2:
        score-=7
    
    if (L1.count(2)==2 and L1.count(1)==1) or (L2.count(2)==2 and L2.count(1)==1) or (L3.count(2)==2 and L3.count(1)==1) or (C1.count(2)==2 and C1.count(1)==1) or (C2.count(2)==2 and C2.count(1)==1) or (C3.count(2)==2 and C3.count(1)==1) or (D1.count(2)==2 and D1.count(1)==1) or (D2.count(2)==2 and D2.count(1)==1):
        score-=9

    # AI
    if L1.count(2)==2 or L2.count(2)==2 or L3.count(2)==2:
        score+=6
    if C1.count(2)==2 or C2.count(2)==2 or C3.count(2)==2:
        score+=6
    if D1.count(2)==2 or D2.count(2)==2:
        score+=7
    
    if (L1.count(1)==2 and L1.count(2)==1) or (L2.count(1)==2 and L2.count(2)==1) or (L3.count(1)==2 and L3.count(2)==1) or (C1.count(1)==2 and C1.count(2)==1) or (C2.count(1)==2 and C2.count(2)==1) or (C3.count(1)==2 and C3.count(2)==1) or (D1.count(1)==2 and D1.count(2)==1) or (D2.count(1)==2 and D2.count(2)==1):
        score+=9

    if Grid_fill(Grid)==1:
        score-=12
    elif Grid_fill(Grid)==2:
        score+=12
    return score


def empty_cells_Grid(Grid):
    empty_cells=[]
    if Grid_fill(Grid)!=0:
            return empty_cells
    for i in range(9):
        if Grid[i]==0:
            empty_cells.append(i)
    return empty_cells

def empty_cells_Totalgrid(TotalGrid):
    empty_cells=[]
    for i in range(9):
        empty_cells.append(empty_cells_Grid(TotalGrid[i]))
    return empty_cells

def Grid_fill(Grid):
    
    #check rows
    for x in range(0,9,3):
        if Grid[x]==Grid[x+1] and Grid[x]==Grid[x+2] and Grid[x]!=0:
            return Grid[x]
    
    #check columns
    for y in range(3):
        if Grid[y]==Grid[y+3] and Grid[y]==Grid[y+6] and Grid[y]!=0:
            return Grid[y]

    #check diagonals
    if Grid[0]==Grid[4] and Grid[0]==Grid[8] and Grid[0]!=0:
        return Grid[0]

    if Grid[2]==Grid[4] and Grid[2]==Grid[6] and Grid[2]!=0:
        return Grid[2]
    
    return 0

def terminated(TotalGrid):
    if len(empty_cells_Totalgrid(TotalGrid))==0:
        return True

    TotalGrid_simple=[]
    for Grid in TotalGrid:
        TotalGrid_simple.append(Grid_fill(Grid))
    if Grid_fill(TotalGrid_simple)!=0:
        return True

    return False

def Convertmain(Gridmain):
    TotalGrid=[[0 for i in range(9)] for j in range(9)]
    for x in range(9):
        for y in range(9):
            TotalGrid[3*(y//3)+x//3][3*(y%3)+x%3]=Gridmain[x][y]
    return TotalGrid

test_Totalgrid=[[0, 1, 2, 1, 0, 0, 0, 0, 0], [1, 2, 0, 0, 0, 0, 0, 0, 0], [1, 2, 1, 0, 2, 0, 1, 0, 0], [2, 0, 1, 2, 0, 0, 1, 0, 0], [2, 0, 0, 1, 1, 2, 0, 0, 0], [0, 0, 1, 0, 0, 1, 1, 0, 0], [2, 2, 2, 2, 0, 0, 2, 2, 2], [2, 2, 2, 0, 1, 0, 2, 2, 2], [2, 2, 2, 0, 1, 0, 2, 2, 2]]
test_indexgrid=4

def main():
    # Call the function you want to profile here
    # For example:
    global memory
    result = Minimax(Convertmain(test_Totalgrid),test_indexgrid,5,2)
    print(result[0])
if __name__ == '__main__':    
    cProfile.run('main()')