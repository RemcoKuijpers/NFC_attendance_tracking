import subprocess
import time

process = subprocess.Popen("florence")
time.sleep(4)

process.terminate()