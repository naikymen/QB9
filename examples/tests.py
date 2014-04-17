# coding=utf-8
__author__ = 'nicolas'
ptmlist = open('../ptmlist', 'r')

line = ptmlist.readline()

while line:
    line = ptmlist.readline()
    print line
