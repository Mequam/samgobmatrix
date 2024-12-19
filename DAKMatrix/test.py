import unittest
from matrix import Matrix
import random
from typing import Callable

#array of functions that the module uses to create values for testing matricies
number_generators = [
          lambda : random.random()*100,
          lambda : random.randint(0, 100),
          lambda : complex(random.random()*100,random.random()*100)
          ]

"""
repeats the decorated function test amount times accross each of the different number generators
for testing functions over several different classes and many random values
"""
def fuzzy_test(test_amount,**kwargs):
    def decorator(f):

        verbose = kwargs["verbose"] if "verbose" in kwargs else False

        def ret_val(*args,**kwargs):
            
            if verbose:
                print()
                print(f"fuzzy testing  {f.__name__} {test_amount*len(number_generators)} ({test_amount}x{len(number_generators)}) times...")

            for i in range(test_amount):
                for gen in number_generators:
                    creator = lambda x : (gen() for i in range(x))
                    f(*args,creator,**kwargs)
            
            if verbose:
                print("done!")

        return ret_val

    return decorator

class TestMatrixMethods(unittest.TestCase):
    @fuzzy_test(100,verbose=True)
    def test_diagonalization(self,gen):
        a,b,c = gen(3)

        inv_diag_eigvec = Matrix.Diagonal([a,b,c])

        value = Matrix.Identity(3)
        for x in reversed(inv_diag_eigvec.diagonalize()):
            value = x*value

        self.assertEqual(Matrix([[a,0,0],
                                 [0,b,0],
                                 [0,0,c]]), value)

    @fuzzy_test(100,verbose=True)
    def test_add(self,gen):
        a,b,c,d = gen(4)
        e,f,g,h = gen(4)
        

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

