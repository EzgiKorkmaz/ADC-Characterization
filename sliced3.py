import matplotlib.pyplot as plt
import binascii
import numpy
import struct

array = []

a=int(input("Enter the first value:"))
b=int(input("Enter the second value:"))

with open("thefile.bin", "rb") as f:
    
    i=0 
    for i in range(0, a):
        byte = f.read(2)
    
    i=0
    for i in range(a,b):
        byte = f.read(2)
        value = struct.unpack("H", byte)[0]
        array.append(value)


plt.plot(array)
plt.ylabel('Value')
plt.show()
