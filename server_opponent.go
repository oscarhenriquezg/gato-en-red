package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"math/rand"
	"net"
	"time"
)

func getComputerMove(board [3][3]string) (int, int) {
	availableMoves := []struct{ row, col int }{}
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			if board[i][j] == " " {
				availableMoves = append(availableMoves, struct{ row, col int }{i, j})
			}
		}
	}
	if len(availableMoves) == 0 {
		return -1, -1
	}
	rand.Seed(time.Now().UnixNano())
	move := availableMoves[rand.Intn(len(availableMoves))]
	return move.row, move.col
}

func main() {
	serverSocket, err := net.Listen("tcp", ":12346")
	if err != nil {
		fmt.Println("[OPPONENT] Error al iniciar el servidor:", err)
		return
	}
	defer serverSocket.Close()
	fmt.Println("[OPPONENT] Servidor oponente escuchando en localhost:12346")

	for {
		conn, err := serverSocket.Accept()
		if err != nil {
			fmt.Println("[OPPONENT] Error al aceptar conexión:", err)
			continue
		}
		fmt.Printf("[OPPONENT] Conectado con %s\n", conn.RemoteAddr().String())
		handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	scanner := bufio.NewScanner(conn)
	for scanner.Scan() {
		boardStr := scanner.Text()
		fmt.Printf("[OPPONENT] Recibido tablero: %s\n", boardStr)

		if boardStr == "exit" {
			fmt.Println("[OPPONENT] El servidor intermediario ha cerrado la conexión")
			break
		}

		// Convertir el tablero de JSON a una matriz de 3x3
		var board [3][3]string
		err := json.Unmarshal([]byte(boardStr), &board)
		if err != nil {
			fmt.Println("[OPPONENT] Error al decodificar el tablero:", err)
			continue
		}

		// Elige el movimiento de la computadora
		row, col := getComputerMove(board)
		move := fmt.Sprintf("%d %d", row, col)
		_, err = conn.Write([]byte(move + "\n"))
		if err != nil {
			fmt.Println("[OPPONENT] Error al enviar movimiento:", err)
			break
		}
		fmt.Printf("[OPPONENT] Enviado movimiento: %s\n", move)
	}

	if err := scanner.Err(); err != nil {
		fmt.Println("[OPPONENT] Error en la conexión:", err)
	}
}
