from CPU.registers import *

a = Register()
a.add_10(3)
print(a.value)
b = a.add_10(-5)
print(a.value)
print(b)
