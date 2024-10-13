import socket
import threading
import json

def handle_client(client_socket, opponent_socket_addr):
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = 'X'

    def check_winner(board):
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

    # Usar UDP para la comunicación con el servidor oponente
    opponent_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"[INTERMEDIARY] Conectado al servidor oponente en {opponent_socket_addr}")

    while True:
        # Enviar el tablero al jugador humano
        board_json = json.dumps(board)
        client_socket.sendall(board_json.encode() + b'\n')
        print(f"[INTERMEDIARY] Enviado tablero al cliente: {board}")

        # Recibir movimiento del jugador humano
        move = client_socket.recv(1024).decode().strip()
        print(f"[INTERMEDIARY] Recibido movimiento del cliente: {move}")

        if move == "exit":
            print("[INTERMEDIARY] El cliente ha salido del juego")
            return

        row, col = map(int, move.split())
        board[row][col] = 'X'

        if check_winner(board):
            client_socket.sendall("Ganaste\n".encode())
            opponent_socket.sendto("Perdiste\n".encode(), opponent_socket_addr)
            print("[INTERMEDIARY] El cliente ha ganado")
            break
        elif board_full(board):
            client_socket.sendall("Empate\n".encode())
            opponent_socket.sendto("Empate\n".encode(), opponent_socket_addr)
            print("[INTERMEDIARY] El juego terminó en empate")
            break

        # Cambiar turno al oponente
        board_json = json.dumps(board)
        opponent_socket.sendto(board_json.encode(), opponent_socket_addr)
        print(f"[INTERMEDIARY] Enviado tablero al oponente: {board}")

        # Recibir movimiento del oponente
        move, _ = opponent_socket.recvfrom(1024)
        move = move.decode().strip()
        print(f"[INTERMEDIARY] Recibido movimiento del oponente: {move}")

        row, col = map(int, move.split())
        board[row][col] = 'O'

        if check_winner(board):
            client_socket.sendall("Perdiste\n".encode())
            opponent_socket.sendto("Ganaste\n".encode(), opponent_socket_addr)
            print("[INTERMEDIARY] El oponente ha ganado")
            break
        elif board_full(board):
            client_socket.sendall("Empate\n".encode())
            opponent_socket.sendto("Empate\n".encode(), opponent_socket_addr)
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

        # Conexión inicial con el servidor oponente para obtener el puerto dinámico
        initial_opponent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        initial_opponent_socket.connect(('localhost', 8001))
        initial_opponent_socket.sendall("Conexion Inicial\n".encode())
        response = initial_opponent_socket.recv(1024).decode().strip()
        print(f"[INTERMEDIARY] Respuesta del servidor oponente: {response}")

        if response.startswith("Conexion Establecida:"):
            new_port = int(response.split(":")[1])
            opponent_socket_addr = ('localhost', new_port)
            initial_opponent_socket.close()
        else:
            print("[INTERMEDIARY] Error al establecer conexión con el servidor oponente")
            client_socket.close()
            continue

        client_handler = threading.Thread(
            target=handle_client, args=(client_socket, opponent_socket_addr))
        client_handler.start()
