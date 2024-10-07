import socket

def print_board(board):
    print("\n".join([" | ".join(row) for row in board]))
    print("-" * 9)

def get_player_move():
    move = input("Ingresa tu movimiento (fila y columna): ").strip()
    row, col = move.split()
    return int(row), int(col)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))  # Conéctate al servidor intermedio

    while True:
        while True:
            # Recibe el estado del juego
            board = client_socket.recv(1024).decode()
            if board in ['Ganaste', 'Perdiste', 'Empate']:
                print_board(eval(last_board))
                print(board)
                break

            last_board = board
            board = eval(board)  # Convertir a lista
            print_board(board)

            # Elige el movimiento del jugador
            row, col = get_player_move()
            client_socket.send(f"{row} {col}".encode())

        # Preguntar si desea jugar otra partida
        play_again = input("¿Quieres jugar otra partida? (s/n): ").strip().lower()
        if play_again == 's':
            client_socket.send("restart".encode())
        else:
            client_socket.send("exit".encode())
            break

    client_socket.close()

if __name__ == "__main__":
    main()
