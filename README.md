# Proyecto Descarga de Archivos
Proyecto para la Asignatura de Sistema Distribuidos de la Escuela Superior de Informatica de Ciudad Real, convocatoria extraordinaria
---
## Integrantes
 Antonio Rubio Menchero
 Javier Palomares Garrido
---
## Link del repositorio
[Repositorio aquí](https://github.com/4Paloms/RubioPalomares.git)

## Tabla de Contenidos
- [Enunciado](#enunciado)
- [Requisitos](#requisitos)
- [Ejecución](#ejecución)

----
## Enunciado

----
## Requisitos
1. Descargar e instalar `zeroc-ice-utils v.3.7.1-1`
1. Librerias necesarias para el funcionamiento de la practica:
    * `python3-zeroc-ice 3.7.1.1`

## Ejecucion

1. Lanzar en el primer terminal la parte de servidora donde vamos a encontrar tanto la factoria de envios como el manager de transferencias, toda la configuracion y creacion de archivos pertinentes para el correcto funciomaniento del programa:`./run_server.sh`
    * Icegrid (Registry)
    * IceStorm
    * Sender_Factory
    * Transfers_Manager
1. Lanzar en el segundo terminal la parte del cliente del sistema de tal manera que

Para ejecutar el cliente:

``
./run_client.sh archivo1 archivo2
``
En este caso archivo1 y archivo2 representas los nombres de los archivos para descargar.
