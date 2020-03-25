#!/usr/bin/env python3
import os
import re
import sys

os.system("grep 'class\|def\|self.[^[:space:]]* =' "+sys.argv[1]+" > tmp_uml1")

class_regex = re.compile(r"^\s*class (.*):$")
non_init_regex = re.compile(r"^(\s*)def [^(__init__)]")
init_regex = re.compile(r"^\s*def __init__")
att_regex = re.compile(r"^\s*self.(\S+) =.*")

read_file = open("tmp_uml1", 'r')
write_file = open("tmp_uml2", 'w')
write_file.write("@startuml\n")

to_write = True
class_met = False
last_class = ""
tab_space = ''
attributes_list = []
method_list = []

for line in read_file:
    (res1, res2, res3, res4) = (class_regex.search(line), non_init_regex.search(line), init_regex.search(line), att_regex.search(line))
    if res2 != None:
        tab_space = res2.group(1)
        method_list.append(line)
        to_write = False
    elif res1 != None:
        last_class = res1.group(1)
        if class_met:
            for a in attributes_list:
                write_file.write(tab_space+'- '+a+"\n")
            for m in method_list:
                write_file.write(m)
            write_file.write("}\n\n"+line.replace(':', ' {'))
            method_list.clear()
            attributes_list.clear()
        else:
            write_file.write(line.replace(':', ' {'))
        to_write = True
        class_met = True
    elif res3 != None:
        method_list.append(line.replace('__init__', last_class))
        to_write = True
    else:
        if to_write:
            attributes_list.append(res4.group(1))
            # write_file.write(line)

for a in attributes_list:
    write_file.write(tab_space+'- '+a+"\n")
for m in method_list:
    write_file.write(m)
write_file.write("}\n\n@enduml\n")
read_file.close()
write_file.close()
os.system("rm tmp_uml1")
os.system(r"sed -i 's/^\(\s*\)def/\1+/' tmp_uml2")
os.system(r"sed -i 's/self\(, \)\?//' tmp_uml2")
