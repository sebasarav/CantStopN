Este sería el enlace del server: http://3.216.217.128:5000/

Esto son los endpoints 

route post('/games/create')         -> Crear nuevo juego ('name': name)
route.get('/games/show')        -> Muestra los juegos
route get('/games/showPlayers/<int:game_id>')    -> Muestra los jugadores asociados a un juego
route post('/games/start/<int:game_id>')    -> Iniciar juego
route post('/games/end/<int:game_id>')       -> Finalizar juego (En construccion)
route delete('/games/<int:game_id>')       -> Eliminar juego

route post('/players/enter')         -> Agregar jugador ('name': name, 'game_id': game_id) -> retorna "player_id": player_id
route post('/players/duringTurn/<int:player_id>')   -> Actualizar mapa durante turno ('mountain': '{2:1,5:3,9:1}) -> Lista de la posición de los escaladores
route post('/players/endTurn/<int:player_id>')    -> Finalizar turno ('mountain': '{2:1,5:3,9:1,11:2,12:1}) -> Lista de la posición de los campamentos
route delete('/players/<int:player_id>')     -> Eliminar jugador

route get('/players/turn/<int:player_id>')     -> Obtener si es el turno -> retorna "turn": 1 si es el turno si no se obvia
route get('/players/dice/<int:player_id>')    -> Obtener los dados -> retorna "dice": listaDadosSeparadosPorComas
