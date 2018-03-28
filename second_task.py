import subprocess
import re
from collections import Counter

args = ['netstat.exe', '-a', '-o']
file_pid = re.compile(r'(\d*)\r')
process = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)
dict = []
while True:
 line_data = process.stdout.readline()
 try:
    line = line_data.decode()
    pid = file_pid.findall(line)
    dict.append(pid)
 except Exception:
     continue
 if line == '' and process.poll() is not None:
    break
dict_without_empty_elements = [x for x in dict if x != [''] or []]
counter = Counter()
for elem in dict_without_empty_elements:
    for x in set(elem):
        counter[x] +=1

def printed(counter):
    print("PID Connections")
    for key, value in counter.items():
        print(key, value)
printed(counter)


