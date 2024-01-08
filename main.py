import subprocess
import threading
from pathlib import Path
import time

def run_flask():
    subprocess.run(["python", "app.py"])

def run_udp_server():
    subprocess.run(["python", "udp_server.py"])

if __name__ == "__main__":
    # Створюємо папку "storage", якщо вона ще не існує
    Path("storage").mkdir(exist_ok=True)

    # Запускаємо Flask у окремому потоці
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Даємо трошки часу для того, щоб Flask встиг заспрацювати
    time.sleep(2)

    # Запускаємо Socket сервер у окремому потоці
    udp_thread = threading.Thread(target=run_udp_server)
    udp_thread.daemon = True
    udp_thread.start()

    # Чекаємо завершення обох потоків
    flask_thread.join()
    udp_thread.join()