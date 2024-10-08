import itertools
import random
from board import Board
from server_connection import ServerConnection
import json

class Agent:
    def __init__(self, player_name, server_connection):
        self.player_name = player_name
        self.game_name = None
        self.server_connection = server_connection
        self.game_id = None
        self.player_id = None
        self.mountain = {}
        self.board = Board()
        self.pairs = []
        self.top = {
            2: 11,  
            3: 9,  
            4: 7,   
            5: 5,   
            6: 3,   
            7: 1,   
            8: 3,   
            9: 5,   
            10: 7,  
            11: 9,  
            12: 11  
        }

    
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

        
        if len(mis_columnas) == 3:
            # Dividir los dados en pares priorizando las sumas según las columnas activas
            columnas_conquistadas = self.board.buscar_top(self.top)

            pairs = self._generate_pairs2(dice, mis_columnas)
            print(f"Pares de sumas de dados seleccionados: {pairs}")
            
            for pair in pairs:
                columna1, columna2 = map(int, pair)  # Convertir a entero

                # Verificar que columna1 no esté en ninguna de las columnas conquistadas
                if columna1 not in columnas_conquistadas:
                    if columna1 in mis_columnas:
                        self.mountain[columna1] -= 1

                # Verificar que columna2 no esté en ninguna de las columnas conquistadas
                if columna2 not in columnas_conquistadas:
                    if columna2 in mis_columnas:
                        self.mountain[columna2] -= 1


        # Enviar actualización al servidor
        self.board.update_board(self.mountain)
        self.board.display_board()
        new_mountain = self.revert_list(self.mountain)
        mountain_server = {str(key): value for key, value in new_mountain.items()}
        mountain_json = json.dumps(mountain_server)
        print("Montaña JSON: ",  mountain_json)
        print("Imprimiendo actualización de la montaña: ", self.mountain)
        self.server_connection.update_turn(self.player_id, mountain_json)

    def end_turn(self):
        mountain_server = {str(key): value for key, value in self.mountain.items()}
        mountain_json = json.dumps(mountain_server)
        # Finalizar turno y acampar
        self.server_connection.end_turn(self.player_id, mountain_json)

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
        self.pairs = [sorted_pairs[0][1]]
        return [sorted_pairs[0][1]]  # Devolvemos la mejor combinación de pares

    def _generate_pairs2(self, dice, preferred_sums):
        # Generar todas las combinaciones posibles de 2 pares de dados
        columnas_conquistadas = self.board.buscar_top(self.top)
        pair_sums = []

        for pair1 in itertools.combinations(dice, 2):
            remaining_dice = list(dice)  # Crear una copia de la lista de dados
            for die in pair1:
                remaining_dice.remove(die)

            pair2 = tuple(remaining_dice)
            sum1 = sum(pair1)
            sum2 = sum(pair2)
            pair_sums.append(((pair1, pair2), (sum1, sum2)))

        # Filtrar las sumas preferidas para excluir las que están en columnas conquistadas
        preferred_sums = [suma for suma in preferred_sums if suma not in columnas_conquistadas]

        # Ordenar los pares de dados según las sumas priorizadas
        sorted_pairs = sorted(pair_sums, key=lambda x: (
            x[1][0] not in preferred_sums, abs(x[1][0] - 7),
            x[1][1] not in preferred_sums, abs(x[1][1] - 7)
        ))
        
        # Guardar y devolver el mejor par de sumas
        self.pairs = [sorted_pairs[0][1]]
        return [sorted_pairs[0][1]]  # Devolver la mejor combinación de pares



    def decide_to_continue_or_stop(self):
        
        """
        Decisión estratégica basada en el progreso, probabilidades y riesgo.
        """
        # Calcula las columnas activas donde ya hay progreso
        columnas_activas = [columna for columna, fila in self.mountain.items() if fila > 0]
        mis_columnas = self.board.mis_columnas_activas(columnas_activas)
        columnas_conquistadas = self.board.buscar_top(self.top)

        # Si tenemos menos de 3 columnas activas, siempre es mejor continuar.
        if len(mis_columnas) < 3:
            print(f"No hay suficientes columnas activas ({len(mis_columnas)} activas). Continuaré.")
            return True

        # Calcular un puntaje de riesgo basado en la posición de las columnas activas
        puntaje_riesgo = sum(self.mountain[columna] for columna in mis_columnas)

        # Umbral de riesgo dinámico basado en el progreso y la proximidad a la cima
        umbral_riesgo_base = 6  # Umbral base ajustable
        umbral_riesgo = umbral_riesgo_base + 2 * len([d for d in mis_columnas if (self.top[d] - self.mountain[d]) <= 2])

        repeit_numbers = any(number in mis_columnas for pair in self.pairs for number in pair)
        
        if repeit_numbers:
            # Si el puntaje de riesgo supera el umbral, detenerse para conservar el progreso
            if puntaje_riesgo >= umbral_riesgo:
                print(f"El puntaje de riesgo es alto ({puntaje_riesgo}). Acamparé para no arriesgarme.")
                return False

            # Basarse en la proximidad a la cima para decidir
            distancia_a_la_cima = [self.top[columna] - self.mountain[columna] for columna in mis_columnas]
            if any(distancia < 3 for distancia in distancia_a_la_cima):
                print("Estoy cerca de la cima en una columna. Continuaré escalando.")
                return True
            
            # Si tenemos menos de 3 columnas activas, siempre es mejor continuar.
            if len(columnas_conquistadas) == 3:
                print("Hemos conquistado las sumas")
                print("Falta finalizar el juego de parte del servidor")
                return 3
            
        else:
            self.mountain = {}
            self.board.__init__()
            #self.server_connection.update_turn(self.player_id, self.mountain)
            # Si todas las demás estrategias fallan, detenerse para no perder el progreso
            print("Escaladores cayendo")
            print("Sus pares",self.pairs )
            print("Mis columnas",mis_columnas )
            return False
    
    def revert_list(self, mountain):
        # Definir el mapeo de las filas
        row_map = {
            12: 1, 11: 2, 10: 3, 9: 4, 8: 5, 7: 6,
            6: 7, 5: 8, 4: 9, 3: 10, 2: 11, 1: 12
        }
        
        # Crear una nueva montaña con las filas modificadas según el mapeo
        new_mountain = {columna: row_map[fila] for columna, fila in mountain.items()}

        return new_mountain