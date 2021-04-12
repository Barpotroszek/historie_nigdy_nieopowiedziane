import os, time, requests

def kill_process():
    '''Restarts program'''
    with open("pid.txt", "r") as f:
        pid = f.read()
        f.close()
    os.system(f"kill {pid}")
    time.sleep(3)
    os.system("python3 main.py")