import unittest
from matrix import Matrix

class TestMatrixMethods(unittest.TestCase):

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


    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()

