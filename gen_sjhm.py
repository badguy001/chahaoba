# -*- coding: UTF-8 -*-
import os

read_file = open('sjhm.csv', 'r')
sf = u'广东'
out_file_list = {}

one_line = read_file.readline()
while '' != one_line:
    one_line = one_line.decode('utf-8').strip()
    spl = one_line.split(',')
    if one_line == '' or len(spl) != 4 or spl[3] != sf:
        one_line = read_file.readline()
        continue
    if spl[2] == 'Y':
        yys = u'移动'
    elif spl[2] == 'L':
        yys = u'联通'
    elif spl[2] == 'D':
        yys = u'电信'
    else:
        yys = spl[2]
    file_name = 'output/' + spl[3] + '/' + spl[1] + '/' + yys + '.txt'
    if file_name not in out_file_list:
        if not os.path.exists('output/' + spl[3] + '/' + spl[1]):
            os.makedirs('output/' + spl[3] + '/' + spl[1])
        file_tmp = open(file_name, 'a')
        out_file_list[file_name] = file_tmp
    this_file = out_file_list[file_name]
    for i in range(0, 9999):
        this_file.write(spl[0] + str(i).zfill(4) + '\n')
    one_line = read_file.readline()

for file_tmp in out_file_list.values():
    file_tmp.close()

read_file.close()
