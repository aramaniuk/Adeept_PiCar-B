#!/usr/bin/python

def replace_num(filename, initial, new_num):  # Call this function to replace data in '.txt' file
    newline = ""
    str_num = str(new_num)
    with open(filename, "r") as f:
        for line in f.readlines():
            if (line.find(initial) == 0):
                line = initial + "%s" % (str_num)
            newline += line
    with open(filename, "w") as f:
        f.writelines(newline)  # Call this function to replace data in '.txt' file


def num_import(filename, initial):  # Call this function to import data from '.txt' file
    with open(filename) as f:
        for line in f.readlines():
            if (line.find(initial) == 0):
                r = line
    begin = len(list(initial))
    snum = r[begin:]
    n = snum
    return n