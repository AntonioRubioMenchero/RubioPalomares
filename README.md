
## Nombre de la Practica
Youtube Music Downloader

## Integrantes
 Antonio Rubio Menchero
 Javier Palomares Garrido

## Link del repositorio
[Repositorio aquí](https://github.com/4Paloms/RubioPalomares.git)

## Enunciado
El objetivo principal del proyecto es diseñar un sistema cliente-servidor que permita la descarga
de ficheros a partir de URIs. El ejemplo típico será la descarga de clips de audio de YouTube. La
implementación de este proyecto permitirá al alumno trabajar, mediante ZeroC Ice, los siguientes
aspectos:
- Comunicación asíncrona
- Manejo de canales de eventos
- Despliegue de servidores de forma dinámica
- Gestión de un grid

## Arquitectura
Esta formado por 5 componentes:
- Downloaders: encargados de las descargas de ficheros.
- Orchestrators: para la gestión de los downloaders.
- Transfers: empleados para la transferencia de archivos.
- Clientes: que solicitaran ficheros.
- Canales de eventos: para mantener un estado coherente entre componentes.

La arquitectura se desarrollara en tres fases.
* Fase 1: Introduccion de los actores
* Fase 2: Descarga y sincronización de componentes
* Fase 3: El sistema final

### Fase 1: Introduccion de los actores
* Objetivo
En la primera fase el sistema se compondrá de un cliente, un orchestrator y un downloader. El
cliente tendrá que mandar un URL en forma de string al orchestrator que, a su vez, redirigirá la
petición al downloader. Orchestrator y downloader mostrarán que se ha recibido la petición
imprimiendo por línea de comandos

* Diagrama de la Arquitectura
 <p align="center">
  <img width="700" height="450" src="https://github.com/4Paloms/RubioPalomares/blob/master/Fase1.png">
</p>

### Fase 2: Descarga y sincronización de componentes
* Objetivo
En la segunda fase el sistema se compondrá de un cliente, uno o varios orchestrators y uno o varios
downloaders. El cliente tendrá que mandar un URL en forma de string a uno de los orchestrators
que, a su vez, redirigirá la petición a uno de sus downloader si el fichero de audio no ha sido
descargado previamente en el sistema. El downloader descargará el archivo y notificará que se ha
descargado correctamente en un canal de eventos para que todos los orchestrators sepan que el
fichero existe, mandando la información de ese fichero. Los orchestrators se anunciarán al resto de
orchestrators en su creación, que se anunciarán a su vez al nuevo orchestrator para actualizar las
listas de orchestrators existentes de cada objeto

* Diagrama de la Arquitectura
 <p align="center">
  <img width="450" height="450" src="https://github.com/4Paloms/RubioPalomares/blob/master/Fase2.png">
</p>

### Fase 3: El sistema final
En paso sera la continuación de los anteriores por lo tanto todos los componentes de las anteriores Fases estaran presentes en la fase 3.
  * Diagrama de la Arquitectura
 <p align="center">
  <img width="450" height="450" src="https://github.com/4Paloms/RubioPalomares/blob/master/Fase.png">
</p>
En la tercera fase el sistema se compondra de un cliente, tres orchestrators, una factoria de
downloaders y una factoria de transfers. 
  
El cliente tendra que mandar un URL en forma de string a
uno de los orchestrators que, a su vez, redirigira la peticion a un downloader creado a tal efecto
siempre que el fichero de audio no haya sido descargado previamente en el sistema.
  
El downloader descargara el archivo y notificara que se ha descargado correctamente en un canal de eventos para
que todos los orchestrators sepan que el fichero existe, mandando la informacion de ese fichero. Al
terminar se destruira.

El cliente podra solicitar la lista de ficheros descargados a uno de los orchestrators.

El cliente tambien tendra la opcion de pedir la transferencia de un archivo de audio. Hara
la peticion a uno de los orchestrators que, a su vez, redirigira la petición a un transfer creado a tal
efecto siempre que el fichero de audio haya sido descargado previamente en el sistema. El transfer
le mandara directamente al cliente el archivo. Al terminar se destruira.

Los orchestrators se anunciaran al resto de orchestrators en su creacion, que se anunciaran a su vez
al nuevo orchestrator para actualizar las listas de orchestrators existentes de cada objeto. Ademas,
un nuevo orchestrator ha de ser consciente de los ficheros de audio que ya han sido descargados en
el sistema.

-Transfer: El transfer es el componente encargado de la transferencia de ficheros, y son creados bajo
demanda mediante una factoria de objetos. Es creado por una factoria de objetos para poder recibir nuevas peticiones de transferencia, recibe peticiones de transferencia, Es destruido al finalizar la descarga.

-Orchestrator: El orchestrator es el componente del sistema que se encarga de la gestion de los downloaders
haciendo de intermediario entre estos y el cliente. Pueden existir uno o varios. Esta siempre a la espera de recibir nuevas    peticiones por parte del cliente.

Recibe peticiones de descarga que son asignadas a downloaders, despues de haber solicitado
su creación, mediante la función pertinente.
Recibe peticiones de transferencia que son asignadas a transfers, despues de haber solicitado
su creación, mediante la función pertinente.
Mantiene listas actualizadas de los ficheros ya descargados en el sistema controlando los eventos del canal de actualizaciones.
Cuando se arranca un nuevo orchestrator saluda al resto de orchestrators, que se anuncian al nuevo objeto.
	
-Cliente:El cliente es el componente del sistema que se conecta a cualquiera de los orchestrators para
solicitar informacion o la descarga de ficheros. En esta fase solicitara descargas, transferencias o
la lista de ficheros a cualquiera de los orchestrators: recibe una URL como argumento para
descargar, el nombre de un fichero para una transferencia y si no recibe nada lista los ficheros que
hay en el sistema.
   
### Ejecucion de la practica
* Paso 1 Ejecutar make run 

``make run 
``
En su defecto tendremos la posibilidad de ejecutar el run_server
``
./run_server.sh
``
* Paso 2 Ejecutar icegridgui. Introducimos en el terminal el siguiente comando.

``
icegridgui
``
* Paso 3

Creamos una Conexion, siguiendo los pasos.

<p align="center">
  <img width="450" height="450" src="https://github.com/4Paloms/RubioPalomares/blob/master/IceGrid.png">
</p>

<p align="center">
  <img width="450" height="450" src="https://github.com/4Paloms/RubioPalomares/blob/master/New Connection.png">
</p>




 


