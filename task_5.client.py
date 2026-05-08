import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
import psutil
import json
import os
import socket
import threading
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class PracticeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Учебная практика 2.2 — Настольное приложение")
        self.root.geometry("900x750")
        self.fayl_sohraneniya = 'save.json'
        self.gruppy_valyut = self.zagruzit_gruppy()
        self.bazoviy_url = "https://github.com"
        self.gh_headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        self.create_task1_tab()
        self.create_task2_tab()
        self.create_task3_tab()
        self.create_task4_tab()
        self.create_task5_tab()
    def create_task1_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Сайты")
        ttk.Button(tab, text="Проверить доступность сайтов", command=self.check_sites).pack(pady=10)
        self.txt_sites = tk.Text(tab, height=15, font=("Consolas", 10))
        self.txt_sites.pack(padx=10, pady=10, fill="both", expand=True)
    def check_sites(self):
        urls = ["https://github.com", "https://binance.com", "https://tomtit.tomsk.ru",
                "https://typicode.com", "https://tomtit-tomsk.ru"]
        self.txt_sites.delete("1.0", tk.END)
        self.txt_sites.insert(tk.END, "URL – статус – код ответа\n" + "-" * 40 + "\n")
        for url in urls:
            try:
                r = requests.get(url, timeout=5, verify=False)
                codes = {200: "доступен", 403: "вход запрещен", 404: "не найден"}
                status = codes.get(r.status_code, "ошибка сервера" if r.status_code >= 500 else "не определен")
                self.txt_sites.insert(tk.END, f"{url} – {status} – {r.status_code}\n")
            except:
                self.txt_sites.insert(tk.END, f"{url} – не доступен – ошибка соединения\n")
    def create_task2_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Система")
        self.lbl_cpu = ttk.Label(tab, text="Загрузка CPU: --%", font=("Arial", 14))
        self.lbl_cpu.pack(pady=15)
        self.lbl_ram = ttk.Label(tab, text="RAM: --%", font=("Arial", 14))
        self.lbl_ram.pack(pady=15)
        self.lbl_disk = ttk.Label(tab, text="Диск: --%", font=("Arial", 14))
        self.lbl_disk.pack(pady=15)
        ttk.Button(tab, text="Обновить монитор", command=self.update_monitor).pack(pady=10)

    def update_monitor(self):
        self.lbl_cpu.config(text=f"Загрузка CPU: {psutil.cpu_percent()}%")
        ram = psutil.virtual_memory()
        self.lbl_ram.config(text=f"RAM: {ram.percent}% ({ram.used // 1024 ** 2} МБ)")
        self.lbl_disk.config(text=f"Загруженность диска: {psutil.disk_usage('/').percent}%")


    def zagruzit_gruppy(self):
        if os.path.exists(self.fayl_sohraneniya):
            try:
                with open(self.fayl_sohraneniya, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def create_task3_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Валюты")
        btns = ttk.Frame(tab);
        btns.pack(pady=5)
        ttk.Button(btns, text="Все курсы", command=self.show_all_valute).pack(side="left", padx=5)
        ttk.Button(btns, text="Мои группы", command=self.show_currency_groups).pack(side="left", padx=5)
        self.tree_v = ttk.Treeview(tab, columns=("C", "N", "V"), show="headings")
        self.tree_v.heading("C", text="Код");
        self.tree_v.heading("N", text="Валюта");
        self.tree_v.heading("V", text="Курс (руб)")
        self.tree_v.pack(fill="both", expand=True, padx=10)

    def show_all_valute(self):
        try:
            data = requests.get("https://cbr-xml-daily.ru", verify=False).json()['Valute']
            self.tree_v.delete(*self.tree_v.get_children())
            for c, i in data.items(): self.tree_v.insert("", "end", values=(c, i['Name'], i['Value']))
        except:
            messagebox.showerror("Ошибка", "Ошибка загрузки данных ЦБ")

    def show_currency_groups(self):
        self.tree_v.delete(*self.tree_v.get_children())
        for g, codes in self.gruppy_valyut.items():
            self.tree_v.insert("", "end", values=(f"ГРУППА: {g}", "", ""), tags=('gray',))
            for c in codes: self.tree_v.insert("", "end", values=(f"  {c}", "в группе", ""))
        self.tree_v.tag_configure('gray', background='#ececec')


    def create_task4_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="GitHub")
        ttk.Label(tab, text="Введите никнейм или поисковый запрос:").pack(pady=5)
        self.gh_ent = ttk.Entry(tab, width=40);
        self.gh_ent.pack(pady=5)

        btns = ttk.Frame(tab);
        btns.pack(pady=5)
        ttk.Button(btns, text="Профиль", command=self.gh_profile).pack(side="left", padx=5)
        ttk.Button(btns, text="Репозитории", command=self.gh_repos).pack(side="left", padx=5)
        ttk.Button(btns, text="Поиск репо", command=self.gh_search).pack(side="left", padx=5)

        self.gh_txt = tk.Text(tab, height=15, font=("Consolas", 10), bg="#fcfcfc")
        self.gh_txt.pack(fill="both", expand=True, padx=10, pady=10)

    def gh_profile(self):
        u = self.gh_ent.get().strip()
        r = requests.get(f"{self.bazoviy_url}/users/{u}", headers=self.gh_headers)
        self.gh_txt.delete(1.0, tk.END)
        if r.status_code == 200:
            d = r.json()
            res = f"Профиль: {u}\nИмя: {d.get('name') or 'Не указано'}\nURL: {d['html_url']}\nРепо: {d['public_repos']}\nПодписчики: {d['followers']}"
            self.gh_txt.insert(tk.END, res)
        else:
            self.gh_txt.insert(tk.END, f"Ошибка: {r.status_code}")

    def gh_repos(self):
        u = self.gh_ent.get().strip()
        r = requests.get(f"{self.bazoviy_url}/users/{u}/repos", headers=self.gh_headers)
        self.gh_txt.delete(1.0, tk.END)
        if r.status_code == 200:
            for repo in r.json():
                self.gh_txt.insert(tk.END, f"• {repo['name']} (Язык: {repo['language'] or 'N/A'})\n")

    def gh_search(self):
        q = self.gh_ent.get().strip()
        r = requests.get(f"{self.bazoviy_url}/search/repositories?q={q}", headers=self.gh_headers)
        self.gh_txt.delete(1.0, tk.END)
        if r.status_code == 200:
            for i in r.json().get('items', [])[:5]:
                self.gh_txt.insert(tk.END, f"Название: {i['full_name']} | Звезды: {i['stargazers_count']}\n")


    def create_task5_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="TCP Связь")

        self.srv_btn = ttk.Button(tab, text="1. Запустить сервер", command=self.start_server_thread)
        self.srv_btn.pack(pady=10)
        self.cli_btn = ttk.Button(tab, text="2. Отправить тестовый файл (Клиент)", command=self.run_client_logic,
                                  state="disabled")
        self.cli_btn.pack(pady=10)

        self.srv_txt = tk.Text(tab, height=10, font=("Consolas", 10), bg="#f0f0f0")
        self.srv_txt.pack(padx=10, pady=10, fill="both")

    def encrypt_data(self, data, key=123):
        res = bytearray()
        for b in data:
            shifted = ((b << 2) & 0xFF) | (b >> 6)
            res.append(shifted ^ key)
        return res

    def start_server_thread(self):
        threading.Thread(target=self.run_server, daemon=True).start()
        self.srv_btn.config(state="disabled")
        self.cli_btn.config(state="normal")
        self.srv_txt.insert(tk.END, "Сервер запущен на 127.0.0.1:5555...\n")

    def run_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 5555))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            header = conn.recv(1024).decode()
            if header:
                data = conn.recv(4096)
                with open("received_file.bin", "wb") as f:
                    f.write(self.encrypt_data(data))
                conn.send("Файл зашифрован на сервере".encode())
            conn.close()

    def run_client_logic(self):
        test_file = "test.json"
        if not os.path.exists(test_file):
            with open(test_file, "w") as f: f.write('{"status": "ok", "message": "hello server"}')

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('127.0.0.1', 5555))
            client.send(test_file.encode())
            with open(test_file, "rb") as f:
                client.send(f.read())
            resp = client.recv(1024).decode()
            self.srv_txt.insert(tk.END, f"Клиент: файл отправлен. Ответ сервера: {resp}\n")
            client.close()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Клиент: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PracticeApp(root)
    root.mainloop()
