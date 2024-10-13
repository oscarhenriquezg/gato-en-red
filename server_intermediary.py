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
            return all(cell != " " for row in board for cell in row)

        while True:
            # Enviar el tablero al jugador humano
            client_socket.send(str(board).encode())
            print(f"[INTERMEDIARY] Enviado tablero al cliente: {board}")

            # Recibir movimiento del jugador humano
            move = client_socket.recv(1024).decode()
            print(f"[INTERMEDIARY] Recibido movimiento del cliente: {move}")

            if move == "exit":
                print("[INTERMEDIARY] El cliente ha salido del juego")
                return

            row, col = map(int, move.split())
            board[row][col] = 'X'

            # Verificar si el jugador humano ha ganado
            if check_winner(board):
                client_socket.send("Ganaste".encode())
                opponent_socket.send("Perdiste".encode())
                print("[INTERMEDIARY] El cliente ha ganado")
                break
            elif board_full(board):
                client_socket.send("Empate".encode())
                opponent_socket.send("Empate".encode())
                print("[INTERMEDIARY] El juego terminó en empate")
                break

            # Cambiar turno al oponente
            opponent_socket.send(str(board).encode())
            print(f"[INTERMEDIARY] Enviado tablero al oponente: {board}")

            # Recibir movimiento del oponente
            move = opponent_socket.recv(1024).decode()
            print(f"[INTERMEDIARY] Recibido movimiento del oponente: {move}")

            row, col = map(int, move.split())
            board[row][col] = 'O'

            # Verificar si la computadora ha ganado
            if check_winner(board):
                client_socket.send("Perdiste".encode())
                opponent_socket.send("Ganaste".encode())
                print("[INTERMEDIARY] El oponente ha ganado")
                break
            elif board_full(board):
                client_socket.send("Empate".encode())
                opponent_socket.send("Empate".encode())
                print("[INTERMEDIARY] El juego terminó en empate")
                break

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("[INTERMEDIARY] Servidor escuchando en localhost:12345")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[INTERMEDIARY] Conectado con cliente {addr}")

        opponent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        opponent_socket.connect(('localhost', 12346))  # Conéctate al servidor oponente
        print("[INTERMEDIARY] Conectado al servidor oponente en localhost:12346")

        client_handler = threading.Thread(
            target=handle_client, args=(client_socket, opponent_socket))
        client_handler.start()
