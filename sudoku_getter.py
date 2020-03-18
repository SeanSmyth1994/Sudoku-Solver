import requests
from bs4 import BeautifulSoup
import sudoku_solver
class scrape:
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def create_puzzle(self, puzzle):
        # set up 2d 9x9 array (there's probably a much easier way to do this
        board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        counter = 0
        # scrapes in by column, so we need to switch row and col
        for i in range(len(board)):
            for j in range(len(board[0])):
                board[i][j] = puzzle[counter]
                counter +=1

        return board

def get_sudoku(p_link):
    req = requests.get(p_link)
    c = req.content
    soup = BeautifulSoup(c, 'html.parser')

    rows = soup.find_all('tr', {'class': 'grid'})
    puzzle = []
    for row in rows:
        cols = row.find_all('td')
        for col in cols:
            txt = col.text
            if txt != '\xa0':
                puzzle.append(int(txt))
            else:
                 puzzle.append(0)

    return puzzle






def find_empty(bo,l):
    for i in range(9):
        for j in range(9):
            if(bo[i][j] == 0):
                l[0] = i
                l[1] = j
                return True
    return False



def used_in_row(bo,row,num):
    for i in range(9):
        if(bo[row][i] == num):
            return True
    return False


def used_in_col(bo,col,num):
    for i in range(9):
        if(bo[i][col] == num):
            return True
    return False


def used_in_box(bo,row,col,num):
    for i in range(3):
        for j in range(3):
            if(bo[row + i][col + j] == num):
                return True
    return False


def safe(bo, row, col, num):
    return not used_in_box(bo, row - row % 3, col - col % 3, num) and not used_in_row(bo, row, num) and not used_in_col(
        bo, col, num)


def solve(bo):
    l = [0, 0]

    if (not find_empty(bo, l)):
        return True

    row = l[0]
    col = l[1]

    for num in range(1, 10):

        if (safe(bo, row, col, num)):

            bo[row][col] = num

            if (solve(bo)):
                return True
            bo[row][col] = 0
    return False



def print_grid(board):
    for i in range(len(board)):
        if i % 3  == 0 and i != 0:
            print('----------------------')
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print('|', end = "")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end ="")


def main():

    board = scrape(get_sudoku('http://www.menneske.no/sudoku/eng/'))
   
    bo = board.create_puzzle(board.puzzle)
    #print(bo)
    if(solve(bo)):
        print_grid(bo)
    else:
        print('No Solution Found')

if __name__ == '__main__':
    main()