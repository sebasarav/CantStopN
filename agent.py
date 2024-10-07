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

        # Dividir los dados en dos pares
        pairs = self._generate_pairs(dice)
        print(f"Pares de sumas de dados: {pairs}")

        # Obtener las columnas activas actuales (donde el valor es mayor que 0)
        columnas_activas = [columna for columna, fila in self.mountain.items() if fila > 0]
        print(f"Columnas activas actuales: {columnas_activas}")

        # Actualizar la montaña con las decisiones del agente
        for pair in pairs:
            columna1, columna2 = map(int, pair)  # Convertir cada valor a entero

            # Solo permitir modificar columnas activas si ya hay 3 columnas activas
            if len(columnas_activas) < 3 or columna1 in columnas_activas:
                if columna1 not in self.mountain or self.mountain[columna1] == 0:
                    self.mountain[columna1] = 12
                    if columna1 not in columnas_activas:  # Agregar a activas si no lo estaba
                        columnas_activas.append(columna1)
                else:
                    self.mountain[columna1] -= 1

            if len(columnas_activas) < 3 or columna2 in columnas_activas:
                if columna2 not in self.mountain or self.mountain[columna2] == 0:
                    self.mountain[columna2] = 12
                    if columna2 not in columnas_activas:  # Agregar a activas si no lo estaba
                        columnas_activas.append(columna2)
                else:
                    self.mountain[columna2] -= 1

        # Enviar actualización al servidor
        self.board.update_board(self.mountain)
        self.board.display_board()
        print("Imprimiendo actualización de la montaña: ", self.mountain)
        self.server_connection.update_turn(self.player_id, self.mountain)

    def end_turn(self):
        # Finalizar turno y acampar
        self.server_connection.end_turn(self.player_id, self.mountain)

    def _generate_pairs(self, dice):
        # Generar todas las combinaciones posibles de 2 pares de dados
        pair_sums = []

        # Iterar sobre las combinaciones para generar pares
        for pair1 in itertools.combinations(dice, 2):
            # Hacer una copia de los dados para trabajar con ellos
            remaining_dice = dice[:]
            
            # Eliminar solo los elementos del primer par, manejando duplicados
            for die in pair1:
                remaining_dice.remove(die)

            # Crear el segundo par con los dados restantes
            pair2 = tuple(remaining_dice)

            # Obtener la suma de ambos pares
            sum1 = sum(pair1)
            sum2 = sum(pair2)

            # Almacenar los pares y sus sumas
            pair_sums.append(((pair1, pair2), (sum1, sum2)))
            print("Pares y sumas: ", pair_sums)

        # Definir las sumas de mayor prioridad
        preferred_sums = [7, 6, 8]

        # Ordenar los pares de dados según las sumas priorizadas
        sorted_pairs = sorted(pair_sums, key=lambda x: (
            x[1][0] not in preferred_sums, abs(x[1][0] - 7),
            x[1][1] not in preferred_sums, abs(x[1][1] - 7)
        ))

        # Devolver las sumas de los dos pares
        return [sorted_pairs[0][1]]  # Devolvemos la mejor combinación de pares con sus respectivas sumas

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
