import numpy as np

class Board:
    def __init__(self):
        # El tablero tiene 11 columnas, numeradas del 2 al 12, y 3 posiciones en cada columna (para los escaladores).
        self.board = np.full((3, 11), " ")  # Espacios vacíos representan posiciones libres.
        self.columns = list(range(2, 13))   # Las columnas están numeradas del 2 al 12.
    
    def update_board(self, mountain):
        # Actualiza la matriz según las posiciones de los escaladores en las diferentes columnas.
        for column, position in mountain.items():
            if column >= 2 and column <= 12:
                self.board[position - 1, column - 2] = 'A'  # 'A' representa el escalador en esa posición.

    def display_board(self):
        # Muestra el tablero en la consola.
        print("   ", "  ".join(map(str, self.columns)))  # Muestra los números de las columnas
        for row in range(3):
            print(f" {3 - row} ", end="")  # Muestra los números de las filas (posición del escalador)
            for col in range(11):
                print(f" {self.board[row][col]} ", end=" ")
            print("")  # Salto de línea entre filas
