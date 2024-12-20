import socket
import os
import threading

# Lista de nodos vecinos para conectar
nodos_vecinos = ['127.0.0.1']  # Direcciones de los servidores vecinos

def manejar_cliente(conn, addr):
    print(f"Conexión con {addr}")

    while True:
        try:
            data = conn.recv(1024)  # Recibir comando
            if not data:
                break

            comando = data.decode().strip()
            print(f"Comando recibido: {comando}")

            if comando.lower() == 'bye':
                conn.send("Cerrando conexión.".encode())
                break

            elif comando.lower().startswith('echo '):  # Comando echo
                mensaje = comando[5:].strip()
                conn.send(mensaje.encode())  # Enviar el mensaje de vuelta

            elif comando.lower() == 'ls':  # Comando ls
                archivos = os.listdir('.')
                conn.send("\n".join(archivos).encode())

            elif comando.lower().startswith('cat '):  # Comando cat
                archivo = comando[4:].strip()
                if os.path.exists(archivo) and os.path.isfile(archivo):
                    with open(archivo, 'r') as f:
                        contenido = f.read()
                        conn.send(contenido.encode())
                else:
                    conn.send(f"Archivo '{archivo}' no encontrado.".encode())

            elif comando.lower().startswith('tree'):  # Comando tree
                conn.send("Estructura de red no implementada.".encode())

            elif comando.startswith('mv'):  # Comando mv
                # Lógica para mover archivos o contactar servidores vecinos
                conn.send(f"Comando mv recibido: {comando}".encode())

            else:
                conn.send("Comando no reconocido.".encode())

        except Exception as e:
            print(f"Error al manejar el comando: {e}")
            conn.send(f"Error al procesar el comando: {e}".encode())
            break

    conn.close()
    print(f"Conexión cerrada con {addr}")

def iniciar_servidor():
    host = '0.0.0.0'
    puerto = 8083

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
        try:
            servidor_socket.bind((host, puerto))
            servidor_socket.listen(5)
            print(f"Servidor principal escuchando en {host}:{puerto}...")

            while True:
                try:
                    conn, addr = servidor_socket.accept()
                    threading.Thread(target=manejar_cliente, args=(conn, addr)).start()
                except Exception as e:
                    print(f"Error al aceptar una nueva conexión: {e}")
        except OSError as e:
            print(f"No se puede iniciar el servidor. Error: {e}")

if __name__ == "__main__":
    iniciar_servidor()
