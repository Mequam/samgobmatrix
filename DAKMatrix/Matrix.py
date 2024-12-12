import numpy as np

"""
Matrix class that wraps numpy arrays. Constructed with Dimensions or whatever ig.
"""
class Matrix:
    def __init__(self,*args,**kwargs):
        
        #smallest absolute value concidered 0 when computing the determinent
        self.epsilon = 1.0e-6

        if "width" in kwargs or "height" in kwargs:
            
            width = 1 if not "width" in kwargs else kwargs["width"]
            height = 1 if not "height" in kwargs else kwargs["height"]

            kwargs.pop("width")
            kwargs.pop("height")

            self._matrix = np.matrix(np.ones(*args,shape=(width,height),**kwargs))
        elif "shape" in kwargs:
            self._matrix = np.matrix(np.ones(*args,**kwargs))
        else:
            self._matrix = np.matrix(*args,**kwargs)
    
    #NOTE: just use numpy :)
    @staticmethod
    def Identity(*args,**kwargs)->"Matrix":
        return Matrix(np.identity(*args,**kwargs))
    
    @staticmethod
    def Zero(*args,**kwargs)->"Matrix":
        return Matrix(np.zeros(*args,**kwargs))


    @staticmethod
    def Diagonal(diag : [float])->"Matrix":
        #glorious numpy oneline, who needs for loops
        return Matrix(np.tile(diag,(len(diag),1))*np.identity(len(diag)))


    
    @property
    def value(self)->np.matrix:
        return self._matrix

    #nupmpy has a matrix class, note the redundency for requirements :)
    #and also the elegence of numpy matricies

    def __eq__(self,other)->bool:
        if not isinstance(other, Matrix) or other.value.shape != self.value.shape:
            return False

        #yapo - yet another python oneliner
        return np.all(abs(other.value - self.value) < self.epsilon)

    def __str__(self)->str:
        return str(self._matrix) #let numpy do the str work :p
    
    def __mul__(self,other)->"Matrix":
        if isinstance((other), Matrix):
            return Matrix(self._matrix * other.value)
        return Matrix(self._matrix * other)
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
        return other+-self
    
    def det(self)->float:
        return np.linalg.det(self.value)

    def inv(self)->"Matrix":

        if abs(self.det()) < self.epsilon: #account for floating point errors
            raise ArithmeticError("matrix has no inverse")

        return Matrix(np.linalg.inv(self.value))

    def transpose(self)->"Matrix":
        return Matrix(self._matrix.transpose())




