import socket
import random

def get_computer_move(board):
    available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    return random.choice(available_moves)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12346))
    server_socket.listen(1)
    print("[OPPONENT] Servidor oponente escuchando en localhost:12346")

    while True:
        conn, addr = server_socket.accept()
        print(f"[OPPONENT] Conectado con {addr}")

        while True:
            # Recibir tablero del servidor intermedio
            board = conn.recv(1024).decode()
            print(f"[OPPONENT] Recibido tablero: {board}")

            if board == "exit":
                print("[OPPONENT] El servidor intermediario ha cerrado la conexión")
                break

            board = eval(board)  # Convertir a lista

            # Elige el movimiento de la computadora
            row, col = get_computer_move(board)
            conn.send(f"{row} {col}".encode())
            print(f"[OPPONENT] Enviado movimiento: {row} {col}")

if __name__ == "__main__":
    main()
