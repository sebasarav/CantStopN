import itertools
import random
from board import Board
from server_connection import ServerConnection

class Agent:
    def __init__(self, player_name, server_connection):
        self.player_name = player_name
        self.game_name = None
        self.server_connection = server_connection
        self.game_id = None
        self.player_id = None
        self.mountain = {}
        self.board = Board()
    
    def create_game(self, game_name):
        self.game_name = game_name
        self.server_connection.create_game(self.game_name)
    
    def join_game(self, game_id):
        self.game_id = game_id
        self.player_id = self.server_connection.join_game(self.player_name, self.game_id)
        
    def start_game(self):
        self.server_connection.start_game(self.game_id)
        
    def is_turn(self):
        response = self.server_connection.play_turn(self.player_id)
        return response

    def players_in_my_party(self):
        response = self.server_connection.player_in_party(self.game_id)
        return response
    
    
    def play_turn(self):
        # Obtener los dados
        dice = self.server_connection.get_dice(self.player_id)
        print(f"Dados obtenidos: {dice}")

        # Separar los valores por comas y convertir a enteros
        dice = list(map(int, dice.split(',')))

        # Obtener las columnas activas actuales
        columnas_activas = [columna for columna, fila in self.mountain.items() if fila > 0]
        print(f"Columnas activas actuales: {columnas_activas}")
        
                # Obtener las columnas activas actuales que son nuestras
        mis_columnas = self.board.mis_columnas_activas(columnas_activas)
        print("Mis columnas: ", mis_columnas)



        if len(mis_columnas) < 3:

            # Dividir los dados en pares priorizando las sumas según las columnas activas
            pairs = self._generate_pairs(dice, columnas_activas)
            print(f"Pares de sumas de dados seleccionados: {pairs}")

            # Actualizar la montaña
            for pair in pairs:
                columna1, columna2 = map(int, pair)  # Convertir a entero

                # Verificar y actualizar la montaña según las reglas
                if len(columnas_activas) < 3 or columna1 in columnas_activas:
                    if columna1 not in self.mountain or self.mountain[columna1] == 0:
                        self.mountain[columna1] = 12
                        if columna1 not in columnas_activas:
                            columnas_activas.append(columna1)

                if len(columnas_activas) < 3 or columna2 in columnas_activas:
                    if columna2 not in self.mountain or self.mountain[columna2] == 0:
                        self.mountain[columna2] = 12
                        if columna2 not in columnas_activas:
                            columnas_activas.append(columna2)

            # Enviar actualización al servidor
            self.board.update_board(self.mountain)
            self.board.display_board()
            print("Imprimiendo actualización de la montaña: ", self.mountain)
            self.server_connection.update_turn(self.player_id, self.mountain)
        
        if len(mis_columnas) <= 3:
                        # Dividir los dados en pares priorizando las sumas según las columnas activas
            pairs = self._generate_pairs2(dice, mis_columnas)
            print(f"Pares de sumas de dados seleccionados: {pairs}")
            for pair in pairs:
                columna1, columna2 = map(int, pair)  # Convertir a entero

                # Verificar y actualizar la montaña según las reglas
                if columna1 in mis_columnas:
                    self.mountain[columna1] -= 1

                if columna2 in mis_columnas:
                    self.mountain[columna2] -= 1

            # Enviar actualización al servidor
            self.board.update_board(self.mountain)
            self.board.display_board()
            print("Imprimiendo actualización de la montaña: ", self.mountain)
            self.server_connection.update_turn(self.player_id, self.mountain)

    def end_turn(self):
        # Finalizar turno y acampar
        self.server_connection.end_turn(self.player_id, self.mountain)

    def _generate_pairs(self, dice, columnas_activas):
        # Generar todas las combinaciones posibles de 2 pares de dados
        pair_sums = []

        for pair1 in itertools.combinations(dice, 2):
            remaining_dice = dice[:]
            for die in pair1:
                remaining_dice.remove(die)

            pair2 = tuple(remaining_dice)
            sum1 = sum(pair1)
            sum2 = sum(pair2)
            pair_sums.append(((pair1, pair2), (sum1, sum2)))

        # Definir las sumas de mayor prioridad, excluyendo las columnas activas
        preferred_sums = [7, 8, 6, 5, 9, 4, 10, 3, 11, 2, 12]
        preferred_sums = [suma for suma in preferred_sums if suma not in columnas_activas]

        # Ordenar los pares de dados según las sumas priorizadas
        sorted_pairs = sorted(pair_sums, key=lambda x: (
            x[1][0] not in preferred_sums, abs(x[1][0] - 7),
            x[1][1] not in preferred_sums, abs(x[1][1] - 7)
        ))

        return [sorted_pairs[0][1]]  # Devolvemos la mejor combinación de pares

    def _generate_pairs2(self, dice, preferred_sums):
        # Generar todas las combinaciones posibles de 2 pares de dados
        pair_sums = []

        for pair1 in itertools.combinations(dice, 2):
            remaining_dice = list(dice)  # Crear una copia de la lista de dados
            for die in pair1:
                remaining_dice.remove(die)

            pair2 = tuple(remaining_dice)
            sum1 = sum(pair1)
            sum2 = sum(pair2)
            pair_sums.append(((pair1, pair2), (sum1, sum2)))

        # Filtrar las sumas preferidas para excluir las que están en columnas activas
        # Aquí se asume que 'self.columnas_activas' es una lista de columnas activas
        preferred_sums = [suma for suma in preferred_sums if suma not in preferred_sums]

        # Ordenar los pares de dados según las sumas priorizadas
        sorted_pairs = sorted(pair_sums, key=lambda x: (
            x[1][0] not in preferred_sums, abs(x[1][0] - 7),
            x[1][1] not in preferred_sums, abs(x[1][1] - 7)
        ))

        return [sorted_pairs[0][1]]  # Devolvemos la mejor combinación de pares


    def decide_to_continue_or_stop(self):
        """
        Decisión estratégica basada en el progreso y las probabilidades.
        """
        # Estrategia 1: Si hay menos de 3 columnas activas en la montaña, continuar.
        columnas_activas = [columna for columna, fila in self.mountain.items() if fila > 0]
        
        if len(columnas_activas) < 3:
            print(f"No hay suficientes columnas activas ({len(columnas_activas)} activas). Continuaré.")
            return True
        
        # Estrategia 2: Basado en el progreso acumulado. Si he avanzado suficiente, detenerme.
        if all(self.mountain[columna] >= 2 for columna in columnas_activas):
            print("He avanzado lo suficiente en las columnas activas. Acamparé para no arriesgarme.")
            return False
        
        # Estrategia 3: Si hay posibilidades de avanzar en las columnas activas, continuar.
        if all(self.mountain[columna] < 2 for columna in columnas_activas):
            print("No he avanzado lo suficiente en las columnas activas. Seguiremos escalando.")
            return True

        # Si no hay más posibilidades de avanzar, detenerse.
        print("No hay posibilidades de avanzar. Voy a detenerme.")
        return False
