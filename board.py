import numpy as np

class Board:
    def __init__(self):
        self.board = np.full((13, 13),"N",object)

        row, column = self.board.shape
        middle = column // 2

        self.board[0][middle] = '7'
        self.board[2][middle - 1] = '6'
        self.board[2][middle + 1] = '8'
        self.board[4][middle - 2] = '5'
        self.board[4][middle + 2] = '9'
        self.board[6][middle - 3] = '4'
        self.board[6][middle + 3] = '10'
        self.board[8][middle - 4] = '3'
        self.board[8][middle + 4] = '11'
        self.board[10][middle - 5] = '2'
        self.board[10][middle + 5] = '12'

        for i in range(row):
            for j in range(column):
                if self.board[i][j].isdigit():
                    num_col = j
                    for k in range(i, row):
                        self.board[k, num_col] = 'V'
        self.board[0][middle] = '7'
        self.board[2][middle - 1] = '6'
        self.board[2][middle + 1] = '8'
        self.board[4][middle - 2] = '5'
        self.board[4][middle + 2] = '9'
        self.board[6][middle - 3] = '4'
        self.board[6][middle + 3] = '10'
        self.board[8][middle - 4] = '3'
        self.board[8][middle + 4] = '11'
        self.board[10][middle - 5] = '2'
        self.board[10][middle + 5] = '12'
    
    def update_board(self, mountain):
        # Actualiza la matriz según las posiciones de los escaladores en las diferentes columnas.
        for column, position in mountain.items():
            column_int = int(column)  # Convertir la clave de columna a entero
            position_int = int(position)  # Convertir la posición a entero
            self.board[position_int, column_int-1] = 'A'  # 'A' representa el escalador en esa posición

    def display_board(self):
        #Imprimir la board
        for row in self.board:
            print(" ".join(row))  # Imprime cada fila unida por espacios