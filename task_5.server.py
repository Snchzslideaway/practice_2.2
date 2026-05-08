import socket
import json
import os



def encrypt_data(data, key=123):
    res = bytearray()
    for b in data:
        shifted = ((b << 2) & 0xFF) | (b >> 6)
        res.append(shifted ^ key)
    return res


def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen(1)
    print("Сервер запущен и ждет клиента...")

    while True:
        conn, addr = server.accept()
        print(f"Подключен: {addr}")

        try:

            header = conn.recv(1024).decode()
            if not header: continue

            filename = "received_file.bin"

            with open(filename, "wb") as f:
                data = conn.recv(4096)
                encrypted = encrypt_data(data)
                f.write(encrypted)

            print(f"Файл получен, зашифрован и сохранен как {filename}")
            conn.send("Файл успешно обработан на сервере".encode())
        except Exception as e:
            print(f"Ошибка сервера: {e}")
        finally:
            conn.close()


if __name__ == "__main__":
    run_server()
