from DAKMatrix import Matrix
from math import pi


print(Matrix.Rotation(pi/2) * Matrix([1,0]).transpose())

value = Matrix.Identity(3)
for x in reversed(Matrix.Diagonal([1,2,3]).diagonalize()):
    print(x)
    value = x*value

print(value)
