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
        self.active_columns = []  # Columnas activas en el turno actual
    
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

        # Dividir los dados en dos pares de sumas
        pairs = self._generate_pairs(dice)
        print(f"Pares de dados: {pairs}")

        # Actualizar la montaña con las decisiones del agente
        for pair in pairs:
            column = sum(pair)
            if column in self.mountain:
                self.mountain[column] += 1
            else:
                self.mountain[column] = 1
                self.active_columns.append(column)  # Marcar la columna como activa

        # Enviar actualización al servidor
        self.server_connection.update_turn(self.player_id, self.mountain)
        self.board.update_board(self.mountain)
        self.board.display_board()

    def end_turn(self):
        # Finalizar turno y acampar
        self.server_connection.end_turn(self.player_id, self.mountain)

    def _generate_pairs(self, dice):
        # Generar todas las combinaciones de pares de dados
        return [(dice[i], dice[j]) for i in range(len(dice)) for j in range(i+1, len(dice))]

    def decide_to_continue_or_stop(self):
        """
        Decisión estratégica basada en el progreso y las probabilidades.
        """
        # Estrategia 1: Si hay menos de 3 columnas activas, continuar.
        if len(self.active_columns) < 3:
            print("No hay suficientes columnas activas, continuaré.")
            return True
        
        # Estrategia 2: Basado en el progreso acumulado. Si he avanzado suficiente, detenerme.
        if all(self.mountain[column] >= 2 for column in self.active_columns):
            print("He avanzado lo suficiente en las columnas activas. Acamparé para no arriesgarme.")
            return False
        
        # Estrategia 3: Si hay posibilidades de avanzar en las columnas activas, continuar.
        dice = self.server_connection.get_dice(self.player_id)
        possible_sums = [sum(pair) for pair in self._generate_pairs(dice)]
        for column in self.active_columns:
            if column in possible_sums:
                print(f"Aún puedo avanzar en la columna {column}. Continuaré.")
                return True

        # Si no hay más posibilidades de avanzar, detenerse.
        print("No hay posibilidades de avanzar. Acamparé.")
        return False
