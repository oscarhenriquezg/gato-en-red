import socket
import json

def print_board(board):
    print("\n".join([" | ".join(row) for row in board]))
    print("-" * 9)

def get_player_move():
    move = input("Player X, Ingresa tu movimiento (Fila [espacio] Columna): ").strip()
    row, col = move.split()
    return int(row), int(col)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))  # Conéctate al servidor intermedio
    print("[CLIENT] Conectado al servidor intermediario en localhost:12345")

    while True:
        while True:
            # Recibe el estado del juego
            board = client_socket.recv(1024).decode()
            print(f"[CLIENT] Recibido del servidor: {board}")

            if board in ['Ganaste', 'Perdiste', 'Empate']:
                print_board(last_board)
                print(board)
                break

            last_board = json.loads(board)  # Convertir de JSON a lista
            print_board(last_board)

            # Elige el movimiento del jugador
            row, col = get_player_move()
            client_socket.send(f"{row} {col}".encode())
            print(f"[CLIENT] Enviado movimiento: {row} {col}")

        # Preguntar si desea jugar otra partida
        play_again = input("¿Quieres jugar otra partida? (s/n): ").strip().lower()
        if play_again == 's':
            client_socket.send("restart".encode())
            print("[CLIENT] Enviado: restart")
        else:
            client_socket.send("exit".encode())
            print("[CLIENT] Enviado: exit")
            break

    client_socket.close()
    print("[CLIENT] Conexión cerrada")

if __name__ == "__main__":
    main()