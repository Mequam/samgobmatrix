from .matrix import Matrix
import numpy as np

import unittest

def human_test()->None:
    print(Matrix([[123,2,3],[456,2,3]],dtype=np.complex64))
    print(Matrix(width=2,height=3,dtype=np.int32))
    print(Matrix(dtype=np.complex64,shape=(5,4)))

    print("multiplication test")
    print("=====")

    cube_matrix = [

            [-0.1031840443611145, -0.3494035005569458, 0.9312735199928284, 0.9684466123580933],
            [0.5947019457817078, 0.7288206815719604, 0.3393377661705017, 5.576062202453613],
            [-0.7972972989082336, 0.5888444185256958, 0.13258817791938782, 2.7450413703918457],
            [0.0, 0.0, 0.0, 1.0]

               ]



    parent_matrix = [
            
            [0.554140567779541, -0.1336411088705063, -0.8216254115104675, -3.063601016998291],
            [0.639702320098877, 0.6999386548995972, 0.31759539246559143, -2.903002977371216],
            [0.5326435565948486, -0.7015881538391113, 0.47335490584373474, 3.2721052169799805],
            [0.0, 0.0, 0.0, 1.0]

            ]

    m1 = Matrix(parent_matrix)
    m2 = Matrix(cube_matrix)

    print(m1)
    print(m2)
    print(m1*m2)
    print(m2*m1)

    print("doubling m1")
    

    print("-2*m1",-2*m1)

    print("m1*-2",m1*-2)

    print("m1-m1",m1-m1)

    print("m2-m1",m2-m1)

    print("m1-m2",m1-m2)

    print("testing the determinent!")

    print("m1.det()",m1.det())

    print("m1.transpose()",m1.transpose())

    print("m1.inv()*m1",m1.inv()*m1)
    
    try:
        Matrix([[ 0,0 ],[1,0]]).inv()
    except ArithmeticError:
        print("arithmatic error")


    print(Matrix.Identity(2))
    
    print(Matrix.Diagonal([1,2,3,4,5]))

    print(Matrix.Zero(shape=(10,10)))


    unittest.main()




if __name__ == '__main__':
    human_test()
