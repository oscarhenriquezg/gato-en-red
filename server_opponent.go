package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"math/rand"
	"net"
	"strconv"
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
	listener, err := net.Listen("tcp", ":8001")
	if err != nil {
		fmt.Println("[OPPONENT] Error al iniciar el servidor:", err)
		return
	}
	defer listener.Close()
	fmt.Println("[OPPONENT] Servidor oponente escuchando en localhost:8001")

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("[OPPONENT] Error al aceptar conexión:", err)
			continue
		}
		fmt.Printf("[OPPONENT] Conectado con %s\n", conn.RemoteAddr().String())
		go handleInitialConnection(conn)
	}
}

func handleInitialConnection(conn net.Conn) {
	defer conn.Close()
	scanner := bufio.NewScanner(conn)
	if scanner.Scan() {
		message := scanner.Text()
		fmt.Printf("[OPPONENT] Recibido mensaje: %s\n", message)

		if message == "Conexion Inicial" {
			// Seleccionar un puerto aleatorio para la conexión de juego
			rand.Seed(time.Now().UnixNano())
			newPort := rand.Intn(65535-8002) + 8002

			// Enviar el puerto aleatorio al intermediario
			response := fmt.Sprintf("Conexion Establecida:%d", newPort)
			conn.Write([]byte(response + "\n"))
			fmt.Printf("[OPPONENT] Enviando respuesta: %s\n", response)

			// Configurar un nuevo listener en el puerto aleatorio
			newListener, err := net.Listen("tcp", ":"+strconv.Itoa(newPort))
			if err != nil {
				fmt.Println("[OPPONENT] Error al iniciar el listener en el nuevo puerto:", err)
				return
			}
			defer newListener.Close()
			fmt.Printf("[OPPONENT] Escuchando en el nuevo puerto: %d\n", newPort)

			for {
				newConn, err := newListener.Accept()
				if err != nil {
					fmt.Println("[OPPONENT] Error al aceptar conexión en el nuevo puerto:", err)
					continue
				}
				fmt.Printf("[OPPONENT] Conectado en el nuevo puerto con %s\n", newConn.RemoteAddr().String())
				handleGameConnection(newConn)
			}
		}
	}
}

func handleGameConnection(conn net.Conn) {
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
