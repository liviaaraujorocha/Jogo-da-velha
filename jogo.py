import threading

# Tabuleiro do jogo
board = [[" " for _ in range(3)] for _ in range(3)]

# Semáforos para sincronização
jogador1_turn = threading.Semaphore(1)
jogador2_turn = threading.Semaphore(0)
game_over = threading.Event()  # Evento para sinalizar o fim do jogo

# Lista de threads ativas
active_threads = []

# Função para exibir o tabuleiro
def display_board():
    for row in board:
        print(" | ".join(row))
        print("---------")

# Função que representa a lógica de um jogador
def jogador(jogador_nome, marker, my_turn, other_turn):
    while not game_over.is_set():
        print(f"{jogador_nome}'s turn.")
        
        my_turn.acquire()  # Aguarda o semáforo do seu turno
        if game_over.is_set():
            break  # Verifica se o jogo terminou após adquirir o semáforo

        row = int(input("Enter row (0, 1, 2): "))
        col = int(input("Enter column (0, 1, 2): "))
        
        # Verifica se a célula está vazia
        if board[row][col] == " ":
            board[row][col] = marker
        else:
            print("Cell is already occupied. Try again.")
            my_turn.release()  # Libera o semáforo para permitir outra tentativa
            continue
        
        display_board()
        
        # Verifica se há um vencedor após a jogada
        if check_winner():
            print(f"{jogador_nome} wins!")
            game_over.set()  # Sinaliza o fim do jogo
            break

        # Verifica se o tabuleiro está cheio (empate)
        if all(cell != " " for row in board for cell in row):
            print("It's a tie!")
            game_over.set()
            break

        other_turn.release()  # Libera o semáforo do outro jogador

    # Remove a thread da lista de threads ativas ao encerrar
    active_threads.remove(threading.current_thread())

# Função para verificar se há um vencedor
def check_winner():
    # Lógica para verificar se há um vencedor
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return True  # Vencedor na linha i
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return True  # Vencedor na coluna i

    if board[0][0] == board[1][1] == board[2][2] != " ":
        return True  # Vencedor na diagonal principal

    if board[0][2] == board[1][1] == board[2][0] != " ":
        return True  # Vencedor na diagonal secundária

    return False  # Nenhum vencedor encontrado

# Inicializa as threads para os jogadores
jogador1_thread = threading.Thread(target=jogador, args=("Jogador 1", "X", jogador1_turn, jogador2_turn))
jogador2_thread = threading.Thread(target=jogador, args=("Jogador 2", "O", jogador2_turn, jogador1_turn))

# Adiciona as threads à lista de threads ativas
active_threads.append(jogador1_thread)
active_threads.append(jogador2_thread)

# Inicia as threads dos jogadores
jogador1_thread.start()
jogador2_thread.start()

# Aguarda o término de todas as threads
for thread in active_threads:
    thread.join()

# Encerra o programa
print("Game Over.")
exit()