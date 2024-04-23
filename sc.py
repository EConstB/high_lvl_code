import subprocess

def run_in_terminal(command):
    subprocess.run(command, shell=True)

if __name__ == '__main__':
    # Запуск main_script.py в новом окне командной строки
    run_in_terminal("start cmd /c python Controller.py")
    
    # Запуск teleop_script.py в новом окне командной строки
    run_in_terminal("start cmd /c python teleop_script.py")
