# Gato en RED

Este documento detalla los pre requisitos, ejecución y contexto de proyecto "Gato en RED", un juego desarrollado para ser ejecutado en una red local con paso de mensajería entre sus distintas capas. El proyecto ha sido desarrollado con fines meramente académicos.

## Pre-requisitos

La siguiente implementación del ***juego del gato en línea ** utiliza los lenguajes *GoLang* y *Python3*, por lo que es necesario que su equipo cuente con estos lenguajes previamente instalados y configurados para poder se ejecutados desde una interfaz de línea de comandos.

 Sitio oficial para descarga de Golang: *https://go.dev/*
  Sitio oficial para descarga de Python3: *https://www.python.org/*

## Instrucciones de ejecución

1) Ejecutar ***Servidor Oponente*** en una interfaz de línea de comandos:
`go run server_oponent.go`

2) Ejecutar ***Servidor intermediario*** en otra interfaz de línea de comandos:
`python3 server_intermediary.py`

3) Ejecutar ***Cliente*** en otra interfaz de línea de comandos:
`python3 client.py`

4) Seguir instrucciones en pantalla para jugar.

*Se recomienda dejar en ejecución y a la vista las distintas consolas para ver el paso de mensajes entre los distintos componentes.*

### Acerca del proyecto
Proyecto desarrollado por:
Oscar Henríquez: oscar.henriquez.g@usach.cl
Pablo Olmos: pablo.olmos@usach.cl 
Para la asignatura de *Redes computaciones* de la *Universidad de Santiago de Chile* (**USACH**).
