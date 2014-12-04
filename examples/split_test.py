# coding=utf-8
__author__ = 'nicolas'

ptm1 = "S-Lysyl-methionine sulfilimine (Met-Lys) (integrasa) (wiath zanahoria)"
with_split = ptm1.split(" with ")
ptm = ptm1.split(" (with")[0].split(" (int")[0]
print(ptm)

"""
print(with_split[0])
print(with_split[0].split(" (int")[0]+"a")


with_index = ptm1.find(" with ")

print(with_split)
print(with_index)
print(ptm1[:with_index])

ptm2 = ptm1[:with_index]

print(ptm2.find(" (intr"))
print(ptm2[:ptm2.find(" (intr")] + "#")
"""