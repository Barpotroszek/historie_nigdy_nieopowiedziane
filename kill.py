import os, time

def kill_process():
    '''Restarts program'''
    with open("pid.txt", "r") as f:
        pids = f.read().split('\n')
        f.close()
    for pid in pids:
        os.system(f"kill {pid}")
    time.sleep(3)
    os.system("python3 main.py")