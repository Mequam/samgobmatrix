import unittest
from matrix import Matrix

class TestMatrixMethods(unittest.TestCase):

    def test_diagonalization(self):
        
        inv_diag_eigvec = Matrix.Diagonal([1,2,3])

        value = Matrix.Identity(3)
        for x in reversed(inv_diag_eigvec.diagonalize()):
            print(x)
            value = x*value

        self.assertEqual(Matrix([[1,0,0],
                                 [0,2,0],
                                 [0,0,3]]), value)

    def test_add(self):
        m1 = Matrix([[1,1],[1,1]])
        m2 = Matrix([[2,2],[2,2]])

        self.assertEqual(m1+m2, m2+m1)

        self.assertEqual(m1+m2, Matrix([[3,3],[3,3]]))

        self.assertEqual(m2+m1, Matrix([[3,3],[3,3]]))

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

