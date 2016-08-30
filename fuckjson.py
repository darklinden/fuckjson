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

def cmd_getargs():
    arg_dict = {}

    tmp_key = ""
    tmp_value = ""

    for single_arg in sys.argv:

        if single_arg[0] == '-':
            tmp_key = single_arg[1:]
        else:
            tmp_value = single_arg.decode("utf-8")

        if tmp_key == "":
            tmp_value = ""
            continue

        if len(tmp_key) > 0 and len(tmp_value) > 0:
            arg_dict[tmp_key] = tmp_value
            tmp_key = ""
            tmp_value = ""

    return arg_dict

def isDict(obj):
    if isinstance(obj, dict):
        return True
    else:
        return False

def isList(obj):
    if isinstance(obj, list):
        return True
    else:
        return False

def merge_list_into_list(base_list, other_list):
    result = list(base_list).extend(other_list)
    return result

def merge_dict_into_dict(base_dict, other_dict):
    result = base_dict.copy()
    if isDict(base_dict) and isDict(other_dict):
        for key in other_dict.keys():
            other_value = other_dict.get(key, None)
            base_value = base_dict.get(key, None)

            if isDict(base_value):
                # print("merge dict")
                # print(base_value)
                # print(other_value)
                result[key] = merge_dict_into_dict(base_value, other_value)
            elif isList(base_value):
                result[key] = merge_list_into_list(base_value, other_value)
            else:
                # print("set data")
                # print("key ")
                # print(key)
                # print("value ")
                # print(other_value)
                result[key] = other_value
    else:
        print("data type not match error")
        result = other_dict

    return result

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
        print("using fuckjson [path] -k key -v value to set json")
        return
        
    arg_dict = cmd_getargs()

    f = open(path, "rb")
    json_obj = json.load(f)
    f.close()

    print("get json obj")
    print(json_obj)

    if arg_dict.has_key("f"):

        other_path = arg_dict["f"]
        # if path[0] != "/":
        #     path = os.path.join(os.getcwd(), path)
        f = open(other_path, "rb")
        other_json_obj = json.load(f)
        f.close()

        if isDict(json_obj) and isDict(other_json_obj):
            json_obj = merge_dict_into_dict(json_obj, other_json_obj)
        elif isList(json_obj) and isList(other_json_obj):
            json_obj = merge_list_into_list(json_obj, other_json_obj)

    elif arg_dict.has_key("k") and arg_dict.has_key("v"):
        json_obj[arg_dict["k"]] = arg_dict["v"]

    print("work end json obj")
    print(json_obj)
    new_content = json.dumps(json_obj, indent=4, sort_keys=True)

    f = open(path, "wb")
    f.write(new_content)
    f.close()

    print("Done")

__main__()