import subprocess
from multiprocessing import Queue
def run_in_terminal(command):
    subprocess.run(command, shell=True)

if __name__ == '__main__':
    # Запуск monitoring_script.py в новом окне командной строки
    run_in_terminal("start cmd /c python monitoring_script.py")
    queue = Queue()
    # Обработка сообщений из очереди в основном процессе
    while True:
        msg = queue.get()
        if msg is None:
            break
        print("Received:", msg)
