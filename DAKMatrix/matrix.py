import numpy as np


#nupmpy has a matrix class, note the redundency for requirements :)
#and also the elegence of numpy matricies

"""
Matrix class that wraps numpy arrays.
"""
class Matrix:
    def __init__(self,*args,**kwargs):
        
        #smallest absolute value concidered 0 when computing the determinent
        self.epsilon = 1.0e-6

        if "width" in kwargs or "height" in kwargs:
            #custom width and height keyword arguments
            
            width = 1 if not "width" in kwargs else kwargs["width"]
            height = 1 if not "height" in kwargs else kwargs["height"]

            #remove width and height so as not to burden numpy with
            #our syntax
            kwargs.pop("width")
            kwargs.pop("height")

            self._matrix = np.ones(*args,shape=(width,height),**kwargs)
        elif "shape" in kwargs:
            #the reason we don't just pass this down to the numpy args,
            #is because we need to choose a default for our shaped object
            self._matrix = np.ones(*args,**kwargs)
        else:
            self._matrix = np.array(*args,**kwargs)

    @property
    def shape(self)->[float]:
        return self._matrix.shape
    
    #returns a string that samgob can parse out
    #to a matrix
    def samgob_string(self)->str:
        return ':'.join([','.join([str(round(v,2)) for v in row]) for row in self.value])

    def eig(self):
        return np.linalg.eig(self._matrix)

    """
        returns the Eigen Decomposition of a matrix
        
        see
            https://mathworld.wolfram.com/EigenDecomposition.html
            https://en.wikipedia.org/wiki/Eigendecomposition_of_a_matrix
            https://www.youtube.com/watch?v=PFDu9oVAE-g
        for more info on the math as of Wed Dec 18 04:56:14 PM EST 2024
    """
    def diagonalize(self)->["Matrix"]:
        eigenvalues,eigenvectors = self.eig()

        return [Matrix(eigenvectors).inv(),
                Matrix.Diagonal(eigenvalues),
                Matrix(eigenvectors)]


    """returns an identity matrix of the given sizes"""
    @staticmethod
    def Identity(*args,**kwargs)->"Matrix":
        return Matrix(np.identity(*args,**kwargs))

    """returns a 2d rotation matrix about theta angles"""
    @staticmethod
    def Rotation(theta : float)->"Matrix":
        return Matrix.Identity(2).rotated(theta)
    
    @staticmethod
    def Zero(*args,**kwargs)->"Matrix":
        return Matrix(np.zeros(*args,**kwargs))


    @staticmethod
    def Diagonal(diag : [float | complex | int])->"Matrix":
        #glorious numpy oneline, who needs for loops
        return Matrix(np.tile(diag,(len(diag),1))*np.identity(len(diag)))


    
    @property
    def value(self)->np.matrix:
        return self._matrix


    def __eq__(self,other)->bool:
        if not isinstance(other, Matrix) or other.value.shape != self.value.shape:
            return False

        #yapo - yet another python oneliner
        return np.all(abs(other.value - self.value) < self.epsilon)

    def __str__(self)->str:
        return str(self._matrix) #let numpy do the str work :p
    
    def __mul__(self,other)->"Matrix":
        if isinstance((other), Matrix):
            if self.shape[1] != other.shape[0]:
                raise ArithmeticError("invalid matrix shapes")
            return Matrix(self._matrix @ other.value)

        if isinstance(other, (int,float,complex)):
            return Matrix(self._matrix * other)

        #seperating this call off this way allows numpy to try one last
        #attempt to multiply with their library,
        #which allows us to do matrix vector multiplication this way
        #among other things
        return Matrix(self._matrix @ other)

    def __rmul__(self,other)->"Matrix":
        if isinstance((other), Matrix):
            return other.__mul__(self)
        return Matrix(other*self.value)

    def __neg__(self)->"Matrix":
        return Matrix(-self.value)
    
    def __add__(self,other)->"Matrix":
        if isinstance((other), Matrix):
            return Matrix(self._matrix + other.value)
        return Matrix(self._matrix + other)

    def __sub__(self,other)->"Matrix":
        return self + -other
    
    def det(self)->float | complex:
        val = (np.linalg.det(self.value))
        return val

    def inv(self)->"Matrix":

        if abs(self.det()) < self.epsilon: #account for floating point errors / complex det
            raise ArithmeticError("matrix has no singular inverse")

        return Matrix(np.linalg.inv(self.value))

    def transpose(self)->"Matrix":
        return Matrix(np.transpose(self._matrix))

    def is_vector(self)->bool:
        return len(self.shape) == 1 or self.shape[1] == 1
    
    def is_vector_dimension_n(self,dimension : int)->bool:
        """returns true if we are a vector of the given dimension"""
        if not self.is_vector(): return False
        return self.shape[0] == dimension

    """
    return a copy of the current matrix, but rotated
    by theta degrees in radians, only works on a 2d matrix
    """
    def rotated(self,theta)->"Matrix":
        
        if not self.is_vector_dimension_n(2): #we don't need to check for dimensions if we are a vector
            
            #ensure that the matrix has compatible rotation dimensions
            width,height = self.shape
            if not ( width == 2 and height == 2 or width == 1 and height == 2):
                raise ArithmeticError("only a 2x2 matrix or 2d vector (1x2) may be rotated")


        return Matrix([
                       [np.cos(theta),-np.sin(theta)],
                       [np.sin(theta),np.cos(theta)]
                       ]) * self
