🔍 Linux Multi-Host Service Monitor (SSH + GUI)

Bu Python tabanlı uygulama, birden fazla Linux makineye SSH ile bağlanarak her bir cihazın çalışan servis bilgilerini alır, GUI (Tkinter) arayüzü ile görüntüler ve tüm sonuçları düzenli bir şekilde tek bir rapor dosyasına aktarır.

🚀 Özellikler

•	🌐 SSH üzerinden bağlantı ile uzaktaki Linux makinelerde servis bilgisi toplama

•	👥 Çoklu IP desteği:

o	GUI ekranından elle IP girişi

o	.txt dosyasından toplu IP yükleme

•	📊 Servis listesi, hostname ve uptime (gün cinsinden) bilgilerini toplar

•	💾 Tüm sonuçları tek bir not defteri (TXT) dosyasına sıralı şekilde kaydeder

•	🧩 Her IP için çıktı ayrı bloklarda tutulur (IP ve hostname başlıklarıyla)

•	🖥️ Basit ve kullanıcı dostu Tkinter arayüzü

•	🔐 Kullanıcı adı ve şifre ile bağlantı kontrolü

🖼️ Ekran Görüntüsü


 ![image](https://github.com/user-attachments/assets/40690d63-78a2-49b5-a7a8-a674f36a81b8)

🛠️ Gereksinimler

•	Python 3.6+

•	paramiko (SSH bağlantısı için)

•	Tkinter (standart olarak Python içinde gelir)

Kurulum:

pip install paramiko

⚙️ Kullanım

1.	Uygulamayı başlatın.
3.	IP, kullanıcı adı ve şifreyi GUI'den girin veya ip_list.txt dosyasından toplu IP alın.
4.	“Sorgula” butonuna basın, sonuçlar ekranda görüntülenecek.
5.	“Kaydet” butonu ile tüm sonuçları bir .txt dosyasına aktarabilirsiniz.	
📁 Rapor Yapısı
--------------------------------------------------
IP: 10.10.10.10
Hostname: ubuntu-server-1
Tarih: 2025-05-22 15:00:12
--------------------------------------------------
Servis Adı                                             - Gün
--------------------------------------------------
cron.service                                          - 12
ssh.service                                           - 45
...
--------------------------------------------------
📌 Katkıda Bulunmak
Katkı sağlamak isterseniz Pull Request gönderebilir veya Issues kısmına geri bildirim bırakabilirsiniz.
________________________________________
📫 İletişim: https://github.com/ramazan-turkmen
