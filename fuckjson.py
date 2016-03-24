#!/usr/bin/env python
#coding: utf8

import sys
import os
import json
import shutil
import subprocess

def run_cmd(cmd):
    # print("run cmd: " + " ".join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        print(err)
    return out

def self_install(file, des):
    file_path = os.path.realpath(file)

    filename = file_path

    pos = filename.rfind("/")
    if pos:
        filename = filename[pos + 1:]

    pos = filename.find(".")
    if pos:
        filename = filename[:pos]

    to_path = os.path.join(des, filename)

    print("installing [" + file_path + "] \n\tto [" + to_path + "]")
    if os.path.isfile(to_path):
        os.remove(to_path)

    shutil.copy(file_path, to_path)
    run_cmd(['chmod', 'a+x', to_path])

def json_sort_key(name):
    key_num = 0
    try:
        key_num = int(name)
    except ValueError:
        key_num = 0

    return key_num

def __main__():

    # self_install
    if len(sys.argv) > 1 and sys.argv[1] == 'install':
        self_install("fuckjson.py", "/usr/local/bin")
        return

    path = ""
    if len(sys.argv) > 1:
        path = sys.argv[1]

    if len(path) == 0:
        print("using fuckjson [path] to sort json")
        return

    f = open(path, "rb")
    content = f.read()
    f.close()

    json_obj = json.loads(content)

    new_content = json.dumps(json_obj, indent=4, sort_keys=True)

    f = open(path, "wb")
    f.write(new_content)
    f.close()

__main__()