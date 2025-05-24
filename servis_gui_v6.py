import subprocess
import socket
import paramiko
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import threading

# SSH ile servisleri sorgula
def get_services_over_ssh(ip, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password, timeout=5)

        stdin, stdout, stderr = client.exec_command(
            "systemctl list-units --type=service --state=running --no-legend"
        )
        output = stdout.read().decode(errors='ignore')

        services = []
        for line in output.strip().split('\n'):
            if not line:
                continue
            service_name = line.split()[0]
            stdin2, stdout2, stderr2 = client.exec_command(
                f'systemctl show -p ActiveEnterTimestamp {service_name}'
            )
            timestamp_raw = stdout2.read().decode(errors='ignore').strip()
            timestamp = timestamp_raw.split('=')[1].strip()
            try:
                uptime_dt = datetime.strptime(timestamp, "%a %Y-%m-%d %H:%M:%S %Z")
                now = datetime.now()
                uptime_days = (now - uptime_dt).days
                services.append((service_name, uptime_days))
            except:
                services.append((service_name, "Bilinmiyor"))

        # Hostname al
        stdin3, stdout3, stderr3 = client.exec_command("hostname")
        hostname = stdout3.read().decode().strip()

        client.close()
        return hostname, services

    except Exception as e:
        return f"Hata: {e}", []

# GUI fonksiyonları
def refresh_info():
    tree.delete(*tree.get_children())
    results.clear()

    ip_list = ip_textbox.get("1.0", END).strip().split("\n")
    if ip_file_list:
        ip_list += ip_file_list
    ip_list = list(set(filter(None, [ip.strip() for ip in ip_list])))

    username = username_entry.get()
    password = password_entry.get()

    def worker():
        for ip in ip_list:
            status_label.config(text=f"Sorgulanıyor: {ip}")
            hostname, services = get_services_over_ssh(ip, username, password)
            results.append((ip, hostname, services))
            for service, days in services:
                tree.insert("", "end", values=(ip, hostname, service, days))
        status_label.config(text="Tamamlandı")

    threading.Thread(target=worker).start()

def load_ips_from_file():
    global ip_file_list
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as f:
            ip_file_list = [line.strip() for line in f.readlines() if line.strip()]
        messagebox.showinfo("Bilgi", f"{len(ip_file_list)} IP dosyadan yüklendi.")

def save_to_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                for ip, hostname, services in results:
                    f.write("="*60 + "\n")
                    f.write(f"IP Adresi : {ip}\n")
                    f.write(f"Hostname  : {hostname}\n")
                    f.write(f"Tarih     : {datetime.now()}\n")
                    f.write("Servis Adı                             - Gün\n")
                    f.write("-"*60 + "\n")
                    for service, days in services:
                        f.write(f"{service:<40} - {days}\n")
                    f.write("\n")
            messagebox.showinfo("Başarılı", "Bilgiler dosyaya kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya kaydedilemedi: {e}")

# GUI Başlat
root = Tk()
root.title("Çoklu Linux Servis İzleyici")
root.geometry("900x600")

ip_file_list = []
results = []

frame_top = Frame(root)
frame_top.pack(pady=5)

Label(frame_top, text="Kullanıcı Adı:").grid(row=0, column=0, sticky='e')
username_entry = Entry(frame_top, width=20)
username_entry.grid(row=0, column=1)

Label(frame_top, text="Şifre:").grid(row=1, column=0, sticky='e')
password_entry = Entry(frame_top, width=20, show="*")
password_entry.grid(row=1, column=1)

# IP giriş alanı
Label(frame_top, text="IP Adresleri (bir satıra bir IP):").grid(row=2, column=0, columnspan=2)
ip_textbox = Text(frame_top, height=5, width=30)
ip_textbox.grid(row=3, column=0, columnspan=2, pady=5)

Button(frame_top, text="Dosyadan IP Yükle", command=load_ips_from_file).grid(row=4, column=0, columnspan=2, pady=5)

# Tablo
frame_table = Frame(root)
frame_table.pack(pady=5)

columns = ("IP", "Hostname", "Servis Adı", "Çalışma Süresi (gün)")
tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200 if col != "Servis Adı" else 300)
tree.pack()

# Butonlar
frame_buttons = Frame(root)
frame_buttons.pack(pady=5)

Button(frame_buttons, text="Sorgula", command=refresh_info).pack(side=LEFT, padx=10)
Button(frame_buttons, text="Kaydet", command=save_to_file).pack(side=LEFT, padx=10)
Button(frame_buttons, text="Çıkış", command=root.destroy).pack(side=LEFT, padx=10)

status_label = Label(root, text="Hazır", anchor="w")
status_label.pack(fill="x")

root.mainloop()
