import requests
def task_1():
    urls = [
        "https://github.com",
        "https://binance.com",
        "https://tomtit.tomsk.ru",
        "https://typicode.com",
        "https://tomtit-tomsk.ru"
    ]
    print("URL – доступность – код ответа")
    print("-" * 50)
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            code = response.status_code
            if code == 200:
                status = "доступен"
            elif code == 403:
                status = "вход запрещен"
            elif code == 404:
                status = "не найден"
            elif code >= 500:
                status = "ошибка сервера"
            else:
                status = "не определен"
            print(f"{url} – {status} – {code}")
        except requests.exceptions.ConnectionError:
            print(f"{url} – не доступен – ошибка соединения")
        except Exception as e:
            print(f"{url} – ошибка – {type(e).__name__}")
if __name__ == "__main__":
    task_1()
