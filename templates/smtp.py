import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

# BREVO BİLGİLERİ (LÜTFEN KENDİ BİLGİLERİNİZLE GÜNCELLEYİN!)
SMTP_SERVER = "smtp-relay.brevo.com" # Brevo'nun Sunucusu
SMTP_PORT = 587                   # TLS Portu (En Kararlı Port)
SENDER_EMAIL = "halimhudis@gmail.com" # Brevo'da onaylı gönderen e-posta adresi
PASSWORD = "zQSmXqfFapNyxPUd" # Brevo panelinden aldığınız SMTP Şifresi
RECEIVER_EMAIL = "muhammetemin53535353@gmail.com"
SUBJECT = "Brevo Testi Başarılı" 
BODY = "Bu mesaj Brevo SMTP servisi ile gönderilmiştir. Artık kısıtlama yok!"


# E-posta içeriğini oluşturma
msg = MIMEMultipart()
msg['Subject'] = Header(SUBJECT, 'utf-8')
# Gönderen adını ayarlama
msg['From'] = formataddr((str(Header('Halim Test', 'utf-8')), SENDER_EMAIL))
msg['To'] = RECEIVER_EMAIL
# BODY içeriğini UTF-8 kodlamasıyla ekle
msg.attach(MIMEText(BODY, 'plain', 'utf-8'))


try:
    # 1. SMTP sunucusuna bağlan (Port 587 için)
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.ehlo()
    server.starttls() # Güvenli bağlantıyı başlat

    # 2. Oturum aç
    server.login(SENDER_EMAIL, PASSWORD)

    # 3. E-postayı gönder
    text = msg.as_string()
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)

    # 4. Bağlantıyı kapat
    server.quit()

    print("E-posta Brevo ile başarıyla gönderildi!")

except smtplib.SMTPAuthenticationError:
    print("Hata: Brevo Kullanıcı Adı veya Şifre hatalı. Lütfen Brevo panelinizdeki SMTP kimlik bilgilerini kontrol edin.")
except Exception as e:
    print(f"E-posta gönderilirken başka bir hata oluştu: {e}")
    try:
        server.quit()
    except:
        pass