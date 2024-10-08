import json
import time


class GameManager:
    def __init__(self, agent):
        self.agent = agent
        self.game_status = False

    def show_menu(self):
        print("---- Menú ----")
        print("1. Create Party")
        print("2. Join Party and Play")
        print("3. Start Party")
        print("4. Players in my party")
        print("5. Exit")
    
    def create_party(self):
        game_name = input("Write a game name: ")
        self.agent.create_game(game_name)
    
    def join_party(self):
        parties = self.agent.server_connection.show_games()
        print("---- Parties Available ----")
        print(f"{'Id party':<10} {'Name party':<20}")
        print("-" * 50) 
        for party in parties:
            print(f"{party['id']:<10} {party['name']:<20}")
        
        game_id = int(input("Select id: "))
        self.agent.join_game(game_id)
        
        # Verificar el estado del juego
        self.check_game_status()

        if not self.game_status:
            print("La partida aún no ha comenzado. Puedes iniciar la partida cuando estés listo.")
            self.start_game_if_desired()  # Preguntar al jugador si desea iniciar la partida
        else:
            print("La partida ha comenzado.")
            self.run_game()  # Llama a run_game si el juego ha comenzado

    def check_game_status(self):
        try:
            response = self.agent.is_turn()
            if response == "Es su turno":
                self.game_status = True
        except Exception as e:
            print("La partida no ha iniciado.")

    def players_in_party(self):
        players = self.agent.players_in_my_party()
        
        if not players:
            print("Sorry, no players")
            return
        
        print("---- Players ----")
        print(f"{'Id player':<10} {'Name player':<20}")
        print("-" * 50)
        for player in players:
            print(f"{player['id']:<10} {player['name']:<20}")    
    
    def start_party(self):
        self.agent.start_game()
        self.game_status = True
    
    def start_game_if_desired(self):
        # Preguntar al jugador si quiere iniciar la partida
        start_game = input("¿Quieres iniciar la partida? (s/n): ")
        if start_game.lower() == 's':
            self.start_party()
            self.run_game()  # Iniciar el bucle de juego después de iniciar la partida

    def run_game(self):
        options = {
            '1': self.create_party,
            '2': self.join_party,
            '3': self.start_party,
            '4': self.players_in_party
        }
        
        while True:
            if self.game_status:
                print("La partida está en marcha")
                response = self.agent.is_turn()
                if response == "Es su turno":
                    print("Mi turno")
                    self.agent.play_turn()
                    time.sleep(0.5)
                    response = self.agent.decide_to_continue_or_stop()
                    if response == 3:
                        print("Cimas conquistadas")
                        break
                    if response == False:
                        self.agent.end_turn()
                        time.sleep(0.5)
                else:
                    print("Esperando mi turno...")
                    time.sleep(10)
            else:
                self.check_game_status()
                if self.game_status:
                    print("La partida ha comenzado, pasando al juego.")
                    self.run_game()  # Iniciar el juego si ha comenzado
                else:
                    self.show_menu()
                    choice = input("Select an option: ")
                    if choice in options:
                        options[choice]()
