import psutil
def task_2():
    print("--- СИСТЕМНЫЙ МОНИТОР ---")
    cpu_load = psutil.cpu_percent(interval=1)
    print(f"Загрузка CPU: {cpu_load}%")
    ram = psutil.virtual_memory()
    print(f"Использовано RAM: {ram.used // (1024 ** 2)} МБ ({ram.percent}%)")
    disk = psutil.disk_usage('/')
    print(f"Загруженность диска: {disk.percent}%")
if __name__ == "__main__":
    task_2()
