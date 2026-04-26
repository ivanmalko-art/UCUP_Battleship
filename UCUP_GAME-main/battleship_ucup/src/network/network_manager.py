# src/network/network_manager.py
import socket
import threading
import json


class NetworkManager:
    def __init__(self):
        self.socket = None
        self.conn = None
        self.is_host = False
        self.connected = False
        self.on_message = None  # callback функція
        self.listen_thread = None

    def host_game(self, port=8080):
        """Хост запускає сервер"""
        self.is_host = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.socket.bind(('', port))
            self.socket.listen(1)

            local_ip = socket.gethostbyname(socket.gethostname())
            print(f"\n🔥 СЕРВЕР ЗАПУЩЕНО!")
            print(f"   IP: {local_ip}")
            print(f"   Порт: {port}")
            print(f"   Очікуємо гравця 2...\n")

            self.conn, addr = self.socket.accept()
            print(f"✅ Гравець 2 підключився! ({addr})")
            self.connected = True
            self.start_listening()
            return True
        except Exception as e:
            print(f"Помилка запуску сервера: {e}")
            return False

    def join_game(self, ip, port=8080):
        """Гравець 2 підключається"""
        self.is_host = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print(f"Підключення до {ip}:{port}...")
            self.socket.connect((ip, port))
            print("✅ Успішно підключено до гри!")
            self.connected = True
            self.start_listening()
            return True
        except Exception as e:
            print(f"Не вдалося підключитися: {e}")
            return False

    def start_listening(self):
        def listen():
            while self.connected:
                try:
                    data = self.conn.recv(4096) if self.is_host else self.socket.recv(4096)
                    if not data:
                        break
                    message = json.loads(data.decode('utf-8'))
                    if self.on_message:
                        self.on_message(message)
                except:
                    break
            print("З'єднання закрито")
            self.connected = False

        self.listen_thread = threading.Thread(target=listen, daemon=True)
        self.listen_thread.start()

    def send(self, data: dict):
        """Відправити повідомлення"""
        if not self.connected:
            return
        try:
            msg = json.dumps(data).encode('utf-8')
            if self.is_host and self.conn:
                self.conn.send(msg)
            elif self.socket:
                self.socket.send(msg)
        except:
            pass

    def close(self):
        self.connected = False
        if self.conn:
            self.conn.close()
        if self.socket:
            self.socket.close()