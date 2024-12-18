import unittest
from matrix import Matrix
import random
from typing import Callable

class TestMatrixMethods(unittest.TestCase):

    def test_diagonalization(self):
        
        inv_diag_eigvec = Matrix.Diagonal([1,2,3])

        value = Matrix.Identity(3)
        for x in reversed(inv_diag_eigvec.diagonalize()):
            value = x*value

        self.assertEqual(Matrix([[1,0,0],
                                 [0,2,0],
                                 [0,0,3]]), value)

    def test_add(self):
        #verify that we add for SEVERAL different values
        #accross several different types

        for i in range(300):
            self.verifyRandomAdd(lambda : random.random()*100)

            self.verifyRandomAdd(lambda : random.randint(0, 100))

            self.verifyRandomAdd(lambda : complex(
                                            random.random()*100,
                                            random.random()*100)
                                  )

    
    """
    generates two random matrix from the given function
    and verifies that they add properly
    """
    def verify_random_add(self,generator : Callable[[],any])->None:
        a,b,c,d = [generator() for i in range(4)]
        e,f,g,h = [generator() for i in range(4)]

        m1 = Matrix([[a,b],[c,d]])
        m2 = Matrix([[e,f],[g,h]])

        self.assertEqual(m1+m2, m2+m1)
        self.assertEqual(m1+m2, Matrix([[a+e,b+f],[c+g,d+h]]))
        self.assertEqual(m2+m1, Matrix([[a+e,b+f],[c+g,d+h]]))


    def test_multiply(self):
        m1 = Matrix([[1,1],[2,1]])
        m2 = Matrix([[1,2],[2,2]])

        self.assertEqual(m1*m2,Matrix([[3,4],[4,6]]))
        self.assertEqual(m2*m1, Matrix([[5,3],[6,4]]))

        self.assertEqual(2*m1, Matrix([[2,2],[4,2]]))
        self.assertEqual(m1*2, Matrix([[2,2],[4,2]]))
        self.assertEqual(m1*2, 2*m1)

        self.assertEqual(m1*-1, -1*m1)
        self.assertEqual(m1*-1, -m1)
        self.assertEqual(-1*m1, -m1)


        m22 = Matrix([[1,2],[3,4]])
        m21 = Matrix([1,1])

        self.assertRaises(ArithmeticError,  lambda : m22 * m21)


if __name__ == '__main__':
    unittest.main()

