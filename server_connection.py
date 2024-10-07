import requests

class ServerConnection:
    def __init__(self, server_url):
        self.server_url = server_url

    def create_game(self, game_name):
        response = requests.post(f'{self.server_url}/games/create', data={'name': game_name})

    def join_game(self, player_name, game_id):
        response = requests.post(f'{self.server_url}/players/enter', data={'name': player_name, 'game_id': game_id})
        return response.json()['player_id']

    def start_game(self, game_id):
        requests.post(f'{self.server_url}/games/start/{game_id}')

    def get_dice(self, player_id):
        response = requests.get(f'{self.server_url}/players/dice/{player_id}')
        return response.json()['dice']

    def update_turn(self, player_id, mountain):
        response = requests.post(f'{self.server_url}/players/duringTurn/{player_id}', data={"mountain": mountain})
        print(response.text)
        

    def end_turn(self, player_id, mountain):
        requests.post(f'{self.server_url}/players/endTurn/{player_id}', data={"mountain": mountain})

    def delete_game(self, game_id):
        requests.delete(f'{self.server_url}/games/{game_id}')

    def delete_player(self, player_id):
        requests.delete(f'{self.server_url}/players/{player_id}')
        
    def show_games(self):
        response = requests.get(f'{self.server_url}/games/show')
        return response.json()
    
    def player_in_party(self, game_id):
        response = requests.get(f'{self.server_url}/games/showPlayers/{game_id}')
        return response.json()
    
    def play_turn(self, player_id):
        response = requests.get(f'{self.server_url}/players/turn/{player_id}')
        return response.json()['msg']