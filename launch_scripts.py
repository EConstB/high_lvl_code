import subprocess

def run_in_terminal(command):
    subprocess.run(command, shell=True)

if __name__ == '__main__':
    # Запуск monitoring_script.py в новом окне командной строки
    run_in_terminal("start cmd /c python monitoring_script.py")
    
    # Запуск teleop_script.py в новом окне командной строки
    run_in_terminal("python teleop_script.py")
