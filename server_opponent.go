package main

import (
	"fmt"
	"math/rand"
	"net"
	"os"
	"strconv"
	"strings"
	"time"
)

func main() {
	// Configuración inicial para escuchar conexiones TCP en el puerto 8001
	tcpAddr, err := net.ResolveTCPAddr("tcp", "localhost:8001")
	if err != nil {
		fmt.Println("Error al resolver la dirección TCP:", err)
		os.Exit(1)
	}

	tcpListener, err := net.ListenTCP("tcp", tcpAddr)
	if err != nil {
		fmt.Println("Error al iniciar el listener TCP:", err)
		os.Exit(1)
	}
	fmt.Println("[OPPONENT] Escuchando en puerto TCP 8001")

	for {
		conn, err := tcpListener.Accept()
		if err != nil {
			fmt.Println("Error al aceptar conexión TCP:", err)
			continue
		}

		go handleTCPConnection(conn)
	}
}

func handleTCPConnection(conn net.Conn) {
	defer conn.Close()

	// Generar un puerto aleatorio entre 8001 y 65535
	rand.Seed(time.Now().UnixNano())
	randomPort := rand.Intn(65535-8001) + 8001

	// Enviar el puerto aleatorio al servidor intermediario
	conn.Write([]byte("Conexion Establecida:" + strconv.Itoa(randomPort) + "\n"))

	// Iniciar listener UDP en el puerto aleatorio generado
	udpAddr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("localhost:%d", randomPort))
	if err != nil {
		fmt.Println("[OPPONENT] Error al resolver dirección UDP:", err)
		return
	}

	udpConn, err := net.ListenUDP("udp", udpAddr)
	if err != nil {
		fmt.Println("[OPPONENT] Error al iniciar listener UDP:", err)
		return
	}
	defer udpConn.Close()

	fmt.Printf("[OPPONENT] Escuchando en puerto UDP %d\n", randomPort)

	for {
		handleUDPConnection(udpConn)
	}
}

func handleUDPConnection(conn *net.UDPConn) {
	buffer := make([]byte, 1024)

	// Recibir datos del servidor intermediario
	n, addr, err := conn.ReadFromUDP(buffer)
	if err != nil {
		fmt.Println("[OPPONENT] Error al recibir datos UDP:", err)
		return
	}
	message := strings.TrimSpace(string(buffer[:n]))
	fmt.Printf("[OPPONENT] Recibido: %s desde %v\n", message, addr)

	if message == "Perdiste" || message == "Empate" || message == "Ganaste" {
		fmt.Println("[OPPONENT] Fin del juego:", message)
		return
	}

	// Simular un movimiento del oponente
	row, col := simulateMove()
	response := fmt.Sprintf("%d %d", row, col)

	// Enviar movimiento al servidor intermediario
	_, err = conn.WriteToUDP([]byte(response), addr)
	if err != nil {
		fmt.Println("[OPPONENT] Error al enviar respuesta UDP:", err)
		return
	}
	fmt.Printf("[OPPONENT] Enviado movimiento: %s\n", response)
}

func simulateMove() (int, int) {
	// Simulación básica de un movimiento del oponente
	return 1, 1 // Ejemplo de movimiento en la posición (1,1)
}
