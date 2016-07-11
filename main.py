#!/usr/bin/python
import sys
import copy
import time

columns = ('A','B','C','D','E')
rows = ('1','2','3','4','5')
player = ''
opponent = ''

def writeNextState(file, currState):
    for i in range(0,5):
        for j in range(0,5):
            file.write(currState[i][j])
        file.write('\n')

def updateRaid(currState,i,j,currPlayer,currOpponent):
    if(i-1 >= 0 and currState[i-1][j] == currOpponent):
        currState[i-1][j] = currPlayer
    if(i+1 <= 4 and currState[i+1][j] == currOpponent):
        currState[i+1][j] = currPlayer
    if(j-1 >= 0 and currState[i][j-1] == currOpponent):
        currState[i][j-1] = currPlayer
    if(j+1 <= 4 and currState[i][j+1] == currOpponent):
        currState[i][j+1] = currPlayer
    return currState
        
    
def checkForPlayer(currState,i,j, currPlayer, currOpponent):
    if((i-1 >= 0 and currState[i-1][j] == currPlayer) or (j-1 >= 0 and currState[i][j-1] == currPlayer) or (i+1 <= 4 and currState[i+1][j] == currPlayer) or (j+1 <= 4 and currState[i][j+1] == currPlayer)):
        currState = updateRaid(currState,i,j, currPlayer, currOpponent)
    return currState
        
    
def calculateScore(currState):
    score = 0
    if(data[0] == '4'):
        offset = 7
    else:
        offset = 3
    for i in range(0,5):
        for j in range(0,5):
            if(currState[i][j] == player):
                score += int(data[i+offset][j])
            elif(currState[i][j] == opponent):
                score -= int(data[i+offset][j])
    return score


def endofgame(currState):
    for i in range(0,5):
        for j in range(0,5):
            if(currState[i][j] == '*'):
                return False
    return True


def gbfs(currState, currPlayer, currOpponent):
    flag = 0
    nextmove = [-1,-1,-1]
    if(data[0] == '4'):
        offset = 7
    else:
        offset = 3
    print currPlayer, currOpponent    
    for i in range(0,5):
        for j in range(0,5):
            max = 0
            if(currState[i][j] == '*'):
                max += int(data[i+offset][j])
                if((i-1 >= 0 and currState[i-1][j] == currPlayer) or (j-1 >= 0 and currState[i][j-1] == currPlayer) or (i+1 <= 4 and currState[i+1][j] == currPlayer) or (j+1 <= 4 and currState[i][j+1] == currPlayer)):
                    if(i-1 >= 0 and currState[i-1][j] == currOpponent):
                        max += int(data[i+offset-1][j])
                    if(i+1 <= 4 and currState[i+1][j] == currOpponent):
                        max += int(data[i+offset+1][j])
                    if(j-1 >= 0 and currState[i][j-1] == currOpponent):
                        max += int(data[i+offset][j-1])
                    if(j+1 <= 4 and currState[i][j+1] == currOpponent):
                        max += int(data[i+offset][j+1])
                    if(max > nextmove[2]):
                        nextmove = [i,j,max]
                        flag = 1
            if(max > nextmove[2]):
                nextmove = [i,j,max]
                flag = 0
    
    if(nextmove[0] != -1):
        print nextmove
        currState[nextmove[0]][nextmove[1]] = currPlayer
        i = nextmove[0]
        j = nextmove[1]
        if(flag == 1):
            if(i-1 >= 0 and currState[i-1][j] == currOpponent):
                currState[i-1][j] = currPlayer
            if(i+1 <= 4 and currState[i+1][j] == currOpponent):
                currState[i+1][j] = currPlayer
            if(j-1 >= 0 and currState[i][j-1] == currOpponent):
                currState[i][j-1] = currPlayer
            if(j+1 <= 4 and currState[i][j+1] == currOpponent):
                currState[i][j+1] = currPlayer
    
def print_log(logData, flag):
    log.write(str(logData[0])+","+str(logData[1])+",")
    if(logData[2] == float("-inf")):
        log.write("-Infinity")
    elif(logData[2] == float("inf")):
        log.write("Infinity")
    else:
        log.write(str(logData[2]))
    if(flag):
        log.write(",")
        if(logData[3] == float("-inf")):
            log.write("-Infinity")
        elif(logData[3] == float("inf")):
            log.write("Infinity")
        else:
            log.write(str(logData[3]))
            
        log.write(",")
        if(logData[4] == float("-inf")):
            log.write("-Infinity")
        elif(logData[4] == float("inf")):
            log.write("Infinity")
        else:
            log.write(str(logData[4]))    
    log.write("\n")
        
def minimax(cutoff, currState, currPlayer, currOpponent, logData):
    scores = []
    if(cutoff == 0 or endofgame(currState)):
        logData[2]=calculateScore(currState)
        if(data[0] != '4'):
            print_log(logData, False)
        return logData[2]     
    else:
        if(currPlayer==player):
            logData[2]=float("-inf")
            scores.append(float("-inf"))
        else:
            logData[2]=float("inf")
            scores.append(float("inf"))
        if(data[0] != '4'):    
            print_log(logData, False)
           
    for i in range(0,5):
        for j in range(0,5):
            if(currState[i][j] == '*'):
                temp=logData[0]
                temp2=logData[2]
                logData[0]=columns[j]+rows[i]
                cutoff -= 1
                nextState = copy.deepcopy(currState)
                nextState[i][j] = currPlayer
                nextState = checkForPlayer(nextState, i, j, currPlayer, currOpponent)
                logData[1]+=1
                scores.append(minimax(cutoff, nextState, currOpponent, currPlayer, logData))
                if(currPlayer==player):
                    if(logData[2] > temp2 and logData[1] == 1):
                        loc[0] = i
                        loc[1] = j
                    logData[2]=max(logData[2],temp2)
                else:
                    logData[2]=min(logData[2],temp2)
                logData[1]-=1
                logData[0]=temp
                if(data[0] != '4'):
                    print_log(logData, False)
                cutoff+=1
                
    if(currPlayer == opponent):
        logData[2]=min(scores)
        return logData[2]
    else:
        logData[2]=max(scores)
        return logData[2]
        
def alphabeta(cutoff, currState, currPlayer, currOpponent, node, depth, value, alpha, beta):
    v = maxalphabeta(cutoff, currState, currPlayer, currOpponent, node, depth, value, alpha, beta)

def maxalphabeta(cutoff, currState, currPlayer, currOpponent, node, depth, value, alpha, beta):
    if(cutoff == 0 or endofgame(currState)):
        if(data[0] != '4'):
            print_log([node, depth, calculateScore(currState), alpha, beta], True)
        return calculateScore(currState)
    v = float("-inf")
    if(data[0] != '4'):
        print_log([node, depth, v, alpha, beta], True)
    for i in range(0,5):
        for j in range(0,5):
            if(currState[i][j] == '*'):
                nextState = copy.deepcopy(currState)
                nextState[i][j] = currPlayer
                nextState = checkForPlayer(nextState, i, j, currPlayer, currOpponent)
                returnFromMin = minalphabeta(cutoff - 1, nextState, currOpponent, currPlayer, columns[j]+rows[i], depth + 1, v, alpha, beta)
                if(returnFromMin > v and depth == 0):
                    loc[0] = i
                    loc[1] = j
                v = max(v, returnFromMin)
                if(v >= beta):
                    if(data[0] != '4'):
                        print_log([node, depth, v, alpha, beta], True)
                    return v
                alpha = max(alpha, v)
                if(data[0] != '4'):
                    print_log([node, depth, v, alpha, beta], True)
    return v
    
def minalphabeta(cutoff, currState, currPlayer, currOpponent, node, depth, value, alpha, beta):
    if(cutoff == 0 or endofgame(currState)):
        if(data[0] != '4'):
            print_log([node, depth, calculateScore(currState), alpha, beta], True)
        return calculateScore(currState)
    v = float("inf")
    if(data[0] != '4'):
        print_log([node, depth, v, alpha, beta], True)
    for i in range(0,5):
        for j in range(0,5):
            if(currState[i][j] == '*'):
                nextState = copy.deepcopy(currState)
                nextState[i][j] = currPlayer
                nextState = checkForPlayer(nextState, i, j, currPlayer, currOpponent)
                returnFromMax = maxalphabeta(cutoff - 1, nextState, currOpponent, currPlayer, columns[j]+rows[i], depth + 1, v, alpha, beta)
                v = min(v, returnFromMax)
                if(v <= alpha):
                    if(data[0] != '4'):
                        print_log([node, depth, v, alpha, beta], True)
                    return v
                beta = min(beta, v)
                if(data[0] != '4'):
                    print_log([node, depth, v, alpha, beta], True)
    return v
        
def simulation():
    player = data[1]
    playerAlgo = int(data[2])
    playerCutoff = int(data[3])
    opponent = data[4]
    opponentAlgo = int(data[5])
    opponentCutoff = int(data[6])
    
    for i in range(7,12):
        data[i] = data[i].split(' ')
    for i in range(12,17):
        data[i] = list(data[i]) 
    
    while(not endofgame(data[12:17])):
        if(playerAlgo == 1):
            gbfs(data[12:17],player,opponent)
            
        elif(playerAlgo == 2):
            node = "root"
            depth = 0
            value = float("-inf")
            logData = [node,depth,value]
            minimax(playerCutoff,data[12:17],player,opponent,logData)
            data[loc[0]+12][loc[1]] = player
            
            data[12:17] = checkForPlayer(data[12:17], loc[0], loc[1], player, opponent)
            
        else:
            alpha = float("-inf")
            beta = float("inf")
            alphabeta(playerCutoff, data[12:17], player, opponent, "root", 0, float("-inf"), alpha, beta)
            data[loc[0]+12][loc[1]] = player
            
            data[12:17] = checkForPlayer(data[12:17], loc[0], loc[1], player, opponent) 
            
        writeNextState(trace, data[12:17])
        
        if(not endofgame(data[12:17])):
            global player
            global opponent
            player, opponent = opponent, player
            if(opponentAlgo == 1):
                gbfs(data[12:17],player,opponent)
                
            elif(opponentAlgo == 2):
                node = "root"
                depth = 0
                value = float("-inf")
                logData = [node,depth,value]
                minimax(opponentCutoff,data[12:17],player,opponent,logData)
                data[loc[0]+12][loc[1]] = player
                
                data[12:17] = checkForPlayer(data[12:17], loc[0], loc[1], player, opponent) 
                
            else:
                alpha = float("-inf")
                beta = float("inf")
                alphabeta(opponentCutoff, data[12:17], player, opponent, "root", 0, float("-inf"), alpha, beta)
                data[loc[0]+12][loc[1]] = player
                data[12:17] = checkForPlayer(data[12:17], loc[0], loc[1], player, opponent)
            player,opponent = opponent,player
            writeNextState(trace, data[12:17])
    
data = open(sys.argv[1], "r").read().splitlines()
if(data[0] != '4'):
    for i in range(3,8):
        data[i] = data[i].split(' ')
    for i in range(8,13):
        data[i] = list(data[i])
    player = data[1]
    if(player == 'X'):
        opponent = 'O'
    else:
        opponent = 'X'
    cutoff = int(data[2])

loc = [-1,-1]
if(data[0] == '1'):
    gbfs(data[8:13],player,opponent)
    file = open("next_state.txt","w+")
    writeNextState(file, data[8:13])
    file.close()
elif(data[0] == '2'):
    log = open("traverse_log.txt","w+")
    log.write("Node,Depth,Value\n")
    node = "root"
    depth = 0
    value = float("-inf")
    logData = [node,depth,value]
    minimaxScore = minimax(cutoff, data[8:13], player, opponent, logData)
    data[loc[0]+8][loc[1]] = player
    data[8:13] = checkForPlayer(data[8:13], loc[0], loc[1], player, opponent)
    file = open("next_state.txt","w+")
    writeNextState(file, data[8:13])
    file.close()
elif(data[0] == '3'):
    log = open("traverse_log.txt","w+")
    log.write("Node,Depth,Value,Alpha,Beta\n")
    alphabeta(cutoff, data[8:13], player, opponent, "root", 0, float("-inf"), float("-inf"), float("inf"))
    data[loc[0]+8][loc[1]] = player
    data[8:13] = checkForPlayer(data[8:13], loc[0], loc[1], player, opponent)
    file = open("next_state.txt","w+")
    writeNextState(file, data[8:13])
    file.close()
else:
    trace = open("trace_state.txt","w+")
    simulation()
    trace.close()

    