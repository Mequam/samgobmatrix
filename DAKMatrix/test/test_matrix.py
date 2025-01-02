import unittest
from DAKMatrix import Matrix
from random import random,randint
from math import pi,cos,sin

#array of functions that the module uses to create values for testing matricies
number_generators = [
          lambda : random()*100,
          lambda : randint(0, 100),
          lambda : complex(random()*100,random()*100)
          ]

def fuzzy_test(test_amount,**kwargs):
    """
    repeats the decorated function test amount times accross each of the different number generators
    for testing functions over several different classes and many random values
    """

    def decorator(f):

        verbose = kwargs["verbose"] if "verbose" in kwargs else False

        def ret_val(*args,**kwargs):
            if verbose:
                print()
                print(f"fuzzy testing  {f.__name__} {test_amount*len(number_generators)} ({test_amount}x{len(number_generators)}) times...")

            for i in range(test_amount):
                for gen in number_generators:
                    fuzz = lambda x : (gen() for i in range(x))
                    f(*args,fuzz,**kwargs)
            
            if verbose:
                print("done!")

        return ret_val

    return decorator

class TestMatrixMethods(unittest.TestCase):
    @fuzzy_test(100)
    def test_diagonalization(self,fuzz):
        """
        determines if we are properly diagonalizing a matrix using a trivial case
        """
        a,b,c = fuzz(3)

        inv_diag_eigvec = Matrix.Diagonal([a,b,c])

        value = Matrix.Identity(3)
        for x in reversed(inv_diag_eigvec.diagonalize()):
            value = x*value

        self.assertEqual(Matrix([[a,0,0],
                                 [0,b,0],
                                 [0,0,c]]), value)

    @fuzzy_test(100)
    def test_add(self,fuzz):
        a,b,c,d = fuzz(4)
        e,f,g,h = fuzz(4)
        

        m1 = Matrix([[a,b],[c,d]])
        m2 = Matrix([[e,f],[g,h]])

        self.assertEqual(m1+m2, m2+m1)
        self.assertEqual(m1+m2, Matrix([[a+e,b+f],[c+g,d+h]]))
        self.assertEqual(m2+m1, Matrix([[a+e,b+f],[c+g,d+h]]))

    @fuzzy_test(100)
    def test_multiply(self,fuzz):
        """
        tests basic multiplication between two VALID matricies
        """

        """
        matrix naming convention for convinence
        with the first  number (X bellow) dictating the matrix that the value
        is assigned to

        X00 X10
        X01 X11
        """
        m100,m110,m101,m111 = fuzz(4)
        m200,m210,m201,m211 = fuzz(4)

        m1 = Matrix([[m100,m110],
                     [m101,m111]])

        m2 = Matrix([[m200,m210],
                     [m201,m211]])

        self.assertEqual(m1*m2,Matrix([
                                        [m100*m200+m110*m201,m210*m100+m211*m110]
                                       ,[m101*m200+m111*m201,m210*m101+m211*m111]
                                       ]))
        self.assertEqual(m2*m1, Matrix([[m100*m200+m101*m210,m110*m200+m111*m210],
                                        [m100*m201+m101*m211,m110*m201+m111*m211]]))

        self.assertEqual(2*m1, Matrix([[2*m100,2*m110],[2*m101,2*m111]]))
        self.assertEqual(m1*2, Matrix([[2*m100,2*m110],[2*m101,2*m111]]))
        self.assertEqual(m1*2, 2*m1)

        self.assertEqual(m1*-1, -1*m1)
        self.assertEqual(m1*-1, -m1)
        self.assertEqual(-1*m1, -m1)

    def test_is_vector(self):
        """test determines of a matrix is vector-like"""
        v1 = Matrix([1,2,3,4])

        v2 = Matrix([[1,2,3,4]]).transpose()

        self.assertTrue(v1.is_vector())
        self.assertTrue(v2.is_vector())

    def test_vector_dimensions(self):
        """test determines if we can verify vector dimensions"""
        v1 = Matrix([1,2,3,4,5])
        v2 = Matrix([1,2,3])
        v3 = Matrix([[1,2]]).transpose()
        v4 = Matrix([[1]]).transpose()


        self.assertTrue(v1.is_vector_dimension_n(5))
        self.assertTrue(v2.is_vector_dimension_n(3))
        self.assertTrue(v3.is_vector_dimension_n(2))
        self.assertTrue(v4.is_vector_dimension_n(1))

    @fuzzy_test(100)
    def test_invalid_multiplication(self,fuzz):
        a,b,c,d,e,f = fuzz(6)
        
        m22 = Matrix([[a,b],[c,d]])
        m21 = Matrix([[e,f]])

        self.assertRaises(ArithmeticError,  lambda : m22 * m21)

    @fuzzy_test(10)
    def test_transpose(self,fuzz):
        a,b,c,d,e,f = fuzz(6)

        m = Matrix([[a,b,c],
                    [d,e,f]])
        self.assertEqual(m.transpose(), Matrix([[a,d],[b,e],[c,f]]))

    @fuzzy_test(30)
    def test_negate(self,fuzz):
        a,b,c,d,e,f = fuzz(6)
        self.assertEqual(-Matrix([[a,b,c],[d,e,f]]), Matrix([[-a,-b,-c],[-d,-e,-f]]))

    @fuzzy_test(100)
    def test_subtract(self,fuzz):
        m100,m110,m101,m111 = fuzz(4)
        m200,m210,m201,m211 = fuzz(4)

        m1 = Matrix([[m100,m110],
                     [m101,m111]])

        m2 = Matrix([[m200,m210],
                     [m201,m211]])


        self.assertEqual(m1-m2, Matrix([[m100-m200,m110-m210],
                                        [m101-m201,m111-m211]]))


        self.assertEqual(m2-m1, Matrix([[m200-m100,m210-m110],
                                        [m201-m101,m211-m111]]))

    @fuzzy_test(100)
    def test_rotation(self,fuzz):
        m100,m110,m101,m111 = fuzz(4)
        theta = random()*4*pi - 2*pi #ranges from -2pi <> 2pi

        m1 = Matrix([[m100,m110],
                     [m101,m111]])

        self.assertEqual(m1.rotated(theta),Matrix([[cos(theta),-sin(theta)],
                                                   [sin(theta),cos(theta)]]) * m1
                         )

        v1 = Matrix([d for d in fuzz(2)])
        self.assertEqual(v1.rotated(theta),Matrix([[cos(theta),-sin(theta)],
                                                   [sin(theta),cos(theta)]]) * v1
                         )

    @fuzzy_test(100)
    def test_determinant(self,fuzz):
        m100,m110,m101,m111 = fuzz(4)

        m1 = Matrix([[m100,m110],
                     [m101,m111]])

        our_determinant = m100*m111-m101*m110
        self.assertAlmostEqual(m1.det(), our_determinant ,5)


if __name__ == '__main__':
    unittest.main()

