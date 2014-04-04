__author__ = 'naikymen'

ptmlist = open('../ptmlist', 'r')
#print ptmlistfile.readline()
ptmlistid = []
i = 1
for line in ptmlist:
    #print line
    lineadeID = line.count('ID   ')
    if lineadeID == 1:
        ptmlistid.append(line)
print(ptmlistid[:2])
ptmlist.close()