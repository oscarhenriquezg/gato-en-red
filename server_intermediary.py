import socket
import threading

def handle_client(client_socket, opponent_socket):
    while True:
        board = [[" " for _ in range(3)] for _ in range(3)]
        current_player = 'X'

        def check_winner(board):
            # Comprobar filas, columnas y diagonales
            for i in range(3):
                if board[i][0] == board[i][1] == board[i][2] != " ":
                    return True
                if board[0][i] == board[1][i] == board[2][i] != " ":
                    return True
            if board[0][0] == board[1][1] == board[2][2] != " ":
                return True
            if board[0][2] == board[1][1] == board[2][0] != " ":
                return True
            return False

        def board_full(board):
            return all(all(cell != " " for cell in row) for row in board)

        while True:
            # Enviar tablero al cliente humano
            client_socket.send(str(board).encode())

            # Recibir movimiento del cliente humano
            move = client_socket.recv(1024).decode()
            if move == "restart" or move == "exit":
                break
            row, col = map(int, move.split())
            if board[row][col] == " ":
                board[row][col] = current_player

            if check_winner(board):
                client_socket.send("Ganaste".encode())
                opponent_socket.send("Perdiste".encode())
                break
            elif board_full(board):
                client_socket.send("Empate".encode())
                opponent_socket.send("Empate".encode())
                break

            # Turno del oponente (jugador computadora)
            current_player = 'O'
            opponent_socket.send(str(board).encode())
            move = opponent_socket.recv(1024).decode()
            row, col = map(int, move.split())
            if board[row][col] == " ":
                board[row][col] = current_player

            if check_winner(board):
                client_socket.send("Perdiste".encode())
                opponent_socket.send("Ganaste".encode())
                break
            elif board_full(board):
                client_socket.send("Empate".encode())
                opponent_socket.send("Empate".encode())
                break

            # Cambiar turno al jugador humano
            current_player = 'X'

        if move == "exit":
            break

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Esperando conexiones...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conectado con {addr}")

        opponent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        opponent_socket.connect(('localhost', 12346))  # Conéctate al servidor oponente

        client_handler = threading.Thread(
            target=handle_client, args=(client_socket, opponent_socket))
        client_handler.start()
