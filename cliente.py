import socket

def iniciar_cliente():
    servidor = '127.0.0.1'
    puerto = 8083  # Puerto del servidor principal

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
        cliente_socket.connect((servidor, puerto))
        while True:
            comando = input("Ingrese un comando (echo, ls, mv, cat, up, tree, bye): ")
            cliente_socket.sendall(comando.encode())
            respuesta = cliente_socket.recv(1024).decode()
            print(f"Respuesta del servidor: {respuesta}")
            if comando.lower() == 'bye':
                break

if __name__ == "__main__":
    iniciar_cliente()

