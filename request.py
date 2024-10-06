import requests


#Crear un nuevo juego
"""response = requests.post('http://3.216.217.128:5000/games/create', data={'name': 'Terreneitor'})
print(response.text)"""

#Mostrar los juegos
"""response = requests.get('http://3.216.217.128:5000/games/show')
print(response.text)"""

#Mostrar los jugadores asociados a un juego
game_id = 594
response = requests.get(f'http://3.216.217.128:5000/games/showPlayers/{game_id}')
print(response.text)

#Agregar un jugador
"""data = {
    'name': 'LaMuñeca',
    'game_id': 443  # Reemplaza con el ID del juego al que quieres agregar el jugador
}
response = requests.post('http://3.216.217.128:5000/players/enter', data=data)
print(response.text)"""

#Iniciar un juego
"""game_id = 386  # Reemplaza con el ID del juego que quieres iniciar
response = requests.post(f'http://3.216.217.128:5000/games/start/{game_id}')
print(response.text)"""

#Eliminar un juego
"""game_id = 1159  # Reemplaza con el ID del juego que quieres eliminar
response = requests.delete(f'http://3.216.217.128:5000/games/{game_id}')
print(response.text)"""

#Actualizar mapa durante el turno
"""player_id = 488  # Reemplaza con el ID del jugador correspondiente
data = {
    'mountain': '{"2":1,"5":3,"9":1}'  # entre comillas esta el numero de la columna y el numero a la par al nivel que se
                                       #encuentra el escalador
}
response = requests.post(f'http://3.216.217.128:5000/players/duringTurn/{player_id}', data=data)
print(response.text)"""

#Finalizar turno
"""player_id = 488  # Reemplaza con el ID del jugador correspondiente
data = {
    'mountain': '{"2":1,"5":3,"9":1}'  # Reemplaza con la información del mapa al finalizar el turno
}
response = requests.post(f'http://3.216.217.128:5000/players/endTurn/{player_id}', data=data)
print(response.text)"""

#Eliminar jugador
player_id = 1171  # Reemplaza con el ID del jugador que quieres eliminar
response = requests.delete(f'http://3.216.217.128:5000/players/{player_id}')
print(response.text)

#Obtener si es el turno de un jugador
"""player_id = 717  # Reemplaza con el ID del jugador que quieres consultar
response = requests.get(f'http://3.216.217.128:5000/players/turn/{player_id}')
print(response.text)"""

#Obtener los dados de un jugador
"""player_id = 488  # Reemplaza con el ID del jugador que quieres consultar
response = requests.get(f'http://3.216.217.128:5000/players/dice/{player_id}')
print(response.text)"""
    