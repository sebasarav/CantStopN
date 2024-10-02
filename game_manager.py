import json

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
        game_name = input("Write a game name:")
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
    
    def run_game(self):
        options = {
            '1' : self.create_party,
            '2' : self.join_party,
            '3' : self.start_party,
            '4' : self.players_in_party
        }
        while True:
            if self.game_status:
                print("The party is comming")
                while True:
                    response = self.agent.is_turn()
                    if response == 1:
                        print("My turn")
            self.show_menu()
            choice = input("Select an option: ")
            if choice in options:
                options[choice]()

