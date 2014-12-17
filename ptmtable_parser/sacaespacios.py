# coding=utf-8
__author__ = 'nicolas'

from os.path import expanduser
csv_file = open(expanduser("~") + '/QB9-git/QB9/resources/dataframe.csv')
output_file = expanduser("~") + '/QB9-git/QB9/resources/output.txt'
output = open(output_file, 'w')

line = csv_file.readline()
i = 0
while line != '':
    line = line.replace(" ","")
    output.write(str(line))
    line = csv_file.readline()
