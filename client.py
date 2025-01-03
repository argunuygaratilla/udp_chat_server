import socket
import threading
import random
import pygame  # pygame kütüphanesini kullanacağız

# pygame'i başlat
pygame.mixer.init()

# UDP soketi oluştur
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", random.randint(8000, 9000)))

# Kullanıcı adı girişi
name = input("Nickname: ")

# Ses dosyasını yükle (ses dosyanızı buraya koymanız gerekiyor)
# Örnek olarak notification_sound.wav dosyasını kullanalım.
notification_sound = pygame.mixer.Sound("notification_sound.mp3")

# Mesajları almak için çalışan thread fonksiyonu
def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            message_decoded = message.decode()

            # Eğer mesaj kendi kullanıcı adınızdan geldiyse, mesajı yazdırma
            if not message_decoded.startswith(f"{name}:"):
                print(message_decoded)
                notification_sound.play()  # Yeni bir mesaj alındığında ses çal

        except Exception as e:
            pass

# Mesajları almak için ayrı bir thread başlat
t = threading.Thread(target=receive)
t.start()

# Sunucuya giriş mesajı gönder
client.sendto(f"SIGNUP_TAG:{name}".encode(), ("localhost", 9999))

while True:
    message = input("")
    if message == "!q":
        exit()
    else:
        # Gönderilen mesajı yalnızca başkalarına gönder, ekrana basma
        client.sendto(f"{name}: {message}".encode(), ("localhost", 9999))
