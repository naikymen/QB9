__author__ = 'naikymen'

ptmlistfile = open('ptmlist.txt', 'r')
#print ptmlistfile.readline()
ptmlistid = []
i = 1
for line in ptmlistfile:
    #print line
    esta = line.count('ID   ')
    if esta == 1:
        print('ocurrencia ', i)
        i += 1

ptmlistfile.close()