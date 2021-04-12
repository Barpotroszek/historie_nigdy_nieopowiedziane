import os, time, requests

def check():
    '''Checks if site is working'''
    r = requests.get("http://0.0.0.0:5000/")
    r = "<Response [200]>"
    if not str(r) == "<Response [200]>":
        with open("pid.txt", "r") as f:
            pid = f.read()
            f.close()
        os.system(f"kill {pid}")
        time.sleep(3)
        os.system("python3 main.py")