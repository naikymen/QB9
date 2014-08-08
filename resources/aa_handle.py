__author__ = 'nicolas'
# coding=utf-8


def aminoacids(a):
    from os.path import expanduser
    from ordereddict import OrderedDict

    aa_file = expanduser("~") + '/QB9-git/SuperMarioQB9/resources/aminoacidos'
    result = OrderedDict()
    res = OrderedDict()

    with open(aa_file) as aminoa:
        line = aminoa.readline().replace("\n", '')
        while line != '':
            letra = line[0]
            abr = line[2:5]
            nombre = line[6:]
            result[letra] = (abr, nombre)
            line = aminoa.readline().replace("\n", '')
            for i in range(0, len(result)):
                res[result.keys()[i]] = result[result.keys()[i]][a]
        return res


# """