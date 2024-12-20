import socket
import os
import shutil  # Para mover archivos

def manejar_cliente(conn, addr):
    print(f"Conexión desde {addr}")

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

            elif comando.lower().startswith('mv '):  # Detectar comando mv
                archivo = comando[3:].strip()
                if os.path.exists(archivo):
                    nuevo_archivo = f"moved_{archivo}"
                    shutil.move(archivo, nuevo_archivo)  # Mover archivo
                    conn.send(f"Archivo '{archivo}' movido a '{nuevo_archivo}'.".encode())
                else:
                    conn.send(f"Archivo '{archivo}' no encontrado.".encode())

            elif comando.lower() == 'ls':
                archivos = os.listdir('.')
                conn.send("\n".join(archivos).encode())

            else:
                conn.send("Comando no reconocido.".encode())

        except Exception as e:
            print(f"Error al manejar el comando: {e}")
            break

    conn.close()
    print(f"Conexión cerrada con {addr}")

def iniciar_servidor_vecino():
    host = '0.0.0.0'
    puerto = 8084  # Puerto diferente al servidor principal

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
        try:
            servidor_socket.bind((host, puerto))
            servidor_socket.listen(5)
            print(f"Servidor vecino escuchando en {host}:{puerto}...")

            while True:
                try:
                    conn, addr = servidor_socket.accept()
                    manejar_cliente(conn, addr)
                except Exception as e:
                    print(f"Error al aceptar una nueva conexión: {e}")
        except OSError as e:
            print(f"No se puede iniciar el servidor. El puerto {puerto} ya está en uso. Error: {e}")

if __name__ == "__main__":
    iniciar_servidor_vecino()
