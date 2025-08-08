import http.server
import ssl
import socketserver
import os

# Создаем простой HTTPS сервер
PORT = 8443

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="static", **kwargs)

# Создаем самоподписанный сертификат
print("Создание самоподписанного сертификата...")
os.system("openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj \"/C=RU/ST=Moscow/L=Moscow/O=FoodDelivery/CN=localhost\"")

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"HTTPS сервер запущен на порту {PORT}")
    print(f"Веб-приложение доступно по адресу: https://localhost:{PORT}/webapp.html")
    
    # Настраиваем SSL
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   certfile="cert.pem",
                                   keyfile="key.pem",
                                   server_side=True)
    
    httpd.serve_forever()
