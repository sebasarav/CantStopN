from agent import Agent
from server_connection import ServerConnection
from game_manager import GameManager



if __name__ == "__main__":
    server_url = "http://3.216.217.128:5000"
    server = ServerConnection(server_url)
    player_name = input("Write a player name: ")
    agent = Agent(player_name=player_name, server_connection=server)
    game = GameManager(agent)
    game.run_game()