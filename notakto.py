from termcolor import colored
from copy import deepcopy
from globals import *
import time

# min(max(node))
# max(min(node))

def can_place(square,i,j):
    if square[i][j] == 'X':
        return False

    if square[i].count('X') == 2:
        return False

    if [square[j][num] for num in range(len(square))].count('X') == 2:
        return False
    
    if i == j or abs(i-j) == 2:
        if [square[num][num] for num in range(len(square))].count('X') == 2:
            return False
        
        if [square[len(square) -1 -num][num] for num in range(len(square))].count('X') == 2:
            return False
    return True

def is_red(end_state,i,j):
    if end_state[i][j] != 'X':
        return False

    if end_state[i].count('X') == 3:
        return True

    if [end_state[num][j] for num in range(3)].count('X') == 3:
        return True
    
    if i == j or abs(i-j) == 2:
        if [end_state[num][num] for num in range(3)].count('X') == 3:
            return True
        
        if [end_state[2 -num][num] for num in range(3)].count('X') == 3:
            return True
            
    return False


class Board:
    def __init__(self, square = [['_' for _ in range(3)] for _ in range(3)]) -> None:
        self.size = 3
        self.square = square
        self.value = 0

    def get(self, i, j):
        return self.square[i][j]

    def place(self, i, j):
        self.square[i][j] = 'X'

    def get_empty_spaces(self):
        return sum([row.count('_') for row in self.square])


    def is_blocked(self):
        for row in self.square:
            if row.count('X') == 3:
                return True

        for i in range(self.size):
            if [row[i] for row in self.square].count('X') == 3:
                return True

        if [self.square[i][i] for i in range(self.size)].count('X') == 3:
            return True

        if [self.square[self.size -1 - i][i] for i in range(self.size)].count('X') == 3:
            return True
        
        return False

    def get_childs(self) -> list:
        childs = []
        for i in range(self.size):
            for j in range(self.size):
                if self.square[i][j] == '_':
                    _square = deepcopy(self.square)
                    _square [i][j] = 'X'
                    childs.append(Board(_square))
        return childs
                    
    def __sub__(self, other):
        for i in range(self.size):
            for j in range(self.size):
                if self.square[i][j] != other.square[i][j]:
                    return self.size*i + j +1
        return 0

    def __str__(self) -> str:
        string = '\n\n'
        for i in range(len(self.square)):
            for j in range(len(self.square)):
                    string += '\t'+colored(str(self.square[i][j]),'green' if self.square[i][j] == 'X' else 'yellow')
                
            string +='\n\n\n'
        return string


def min_func(state: Board, depth):
    if state.is_blocked():
        state.value = -1 * state.get_empty_spaces()
        return state

    tmp_state = None
    value = 9

    for child in state.get_childs():
        child.value = max_func(child, depth+1).value
        if depth == 1:
            win_or_lose = "wins" if child.value > 0 else "loses"
            print(f'PC {win_or_lose} with {abs(child.value)} blanks', child.square)
        if value > child.value:
            value = child.value
            tmp_state = child
    
    if depth == 1:
        print('PC picked',tmp_state - state)
    return tmp_state


def max_func(state: Board, depth):
    if state.is_blocked():
        state.value = 1 * state.get_empty_spaces()
        return state

    tmp_state = None
    value = -9

    for child in state.get_childs():
        child.value = min_func(child, depth+1).value
        if depth == 1:
            win_or_lose = "wins" if child.value > 0 else "loses"
            print(f'You {win_or_lose} with {abs(child.value)} blanks', child.square)
        if value < child.value:
            value = child.value
            tmp_state = child
    if depth == 1:
        print('I suggest',tmp_state - state)
    return tmp_state


# Notakto misere mode
class Notakto:
    def __init__(self, init_state: Board) -> None:
        self.state = init_state

  
    def get_best_move(self):
        state = self.state
        return max_func(state) if state.player == 2 else min_func(state)

def main():
    board = Board([
    ['_','_','_'],
    ['_','_','_'],
    ['_','_','_']
    ])


    game = Notakto(board)

    print(NOTAKTO)

    print('init state :\n', game.state)

    turn = 1 if input('Wanna start the game ? [y/n] ').lower() == 'y' else 2
    print('\n')

    for row in [[1,2,3],[4,5,6],[7,8,9]]:
        for num in row:
            print('\t'+colored(str(num),'yellow'),end='')
        print('\n\n')
    
    while (not game.state.is_blocked()):
        
        if turn == 1:
            print('Hints : ')
            max_func(game.state,1)
            i = int(input('1 --> 9 : '))-1
            if i not in [0,1,2,3,4,5,6,7,8]:
                print('Invalid Input')
                continue
            if game.state.get(i//3, i % 3) == 'X':
                print('Occupied Cell')
                continue
            game.state.place(i//3, i % 3)
            print('You Played :\n', game.state)
            turn = 2

        else:
            game.state = min_func(game.state, 1)
            print('PC Played :\n', game.state)
            turn = 1
        

    win = True if game.state.value > 0 else False
    
    for i,row in enumerate(game.state.square):
        for j,x in enumerate(row):
            print('\t'+colored(str(x),'red') if is_red(game.state.square,i,j) else '\t'+colored(str(x),'green') ,end='')
        print('\n\n')

    if not win:
        print(GAMEOVER)
    else:
        print(YOUWIN)
    
if __name__ == "__main__":
    main()