"""
Module used to provide the helper classes
`Matrix` and `Vector` for important functions
such as lstsq and llsq. In turn, these functions
will be helpful for stuff like balancing chemical
equations and such.
"""

from _util import coerce
from .exception import *

# Save local copies of errors
LinalgException = LinalgException
UninvertibleMatrixError = UninvertibleMatrixError
LinalgOPError = LinalgOPError
VectorOPError = VectorOPError
MatrixOPError = MatrixOPError
LSTSQNonconvergenceError = LSTSQNonconvergenceError

NumericType = int | float | complex

class Vector:
    def __init__(self, vecv: list[list[NumericType]]) -> None:
        if not all(len(vecv[i]) == len(vecv[0]) for i in range(1, len(vecv))):
            raise ValueError(
                "Vector must have rows of length 1 "
                "if it has more than one row."
            )
        
        self.vecv = vecv
        return
    
    def __coerce__(self, other):
        if not isinstance(other, Vector):
            other = Vector(other)
        pass

    def conjugate(self):
        ret = self.vecv[:]
        for i in range(len(ret)):
            for j in range(len(ret[0])):
                ret[i][j] = ret[i][j].conjugate()
        
        return Vector(ret)
    
    @property
    def T(self):
        """
        Transposes the vector
        """
        return Vector(list(map(list, zip(*self.vecv))))
    
    @property
    def H(self):
        return self.conjugate().T
    
    def __add__(self, other):
        coerce(self, other)
        
        if len(self.vecv) != len(other.vecv) or len(self.vecv[0]) != len(other.vecv[0]):
            raise VectorOPError(
                "Cannot add vectors with incompatible dimensions.")
        
        ret = self.vecv[:]
        for idx in range(len(self.vecv)):
            for jdx in range(len(self.vecv[0])):
                ret[idx][jdx] += other.vecv[idx][jdx]
        
        return Vector(ret)
    
    def __sub__(self, other):
        coerce(self, other)

        if len(self.vecv) != len(other.vecv) or len(self.vecv[0]) != len(other.vecv[0]):
            raise VectorOPError(
                "Cannot subtract vectors with incompatible dimensions.")
        
        ret = self.vecv[:]
        for idx in range(len(self.vecv)):
            for jdx in range(len(self.vecv[0])):
                ret[idx][jdx] -= other.vecv[idx][jdx]
        
        return Vector(ret)
    
    def __mul__(self, other):
        ret = self.vecv[:]
        if isinstance(type(other), NumericType):
            for idx in range(len(self.vecv)):
                for jdx in range(len(self.vecv[0])):
                    ret[idx][jdx] *= other
            
            return Vector(ret)
        
        return NotImplemented
        
    def __iadd__(self, other):
        self = self + other
        return self
    
    def __isub__(self, other):
        self = self - other
        return self
    
    def __imul__(self, other):
        self = self * other
        return self

    def __radd__(self, other):
        return self.__add__(other)
    
    def __rsub__(self, other):
        return self.__sub__(other)
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return f"Vector({self.vecv})"
    
    __str__ = __repr__

class Matrix:
    def __init__(self, matv: list[list[NumericType]]) -> None:
        if not all(len(matv[i]) == len(matv[0]) for i in range(1, len(matv))):
            raise ValueError(
                "Matrix must have all rows exactly "
                "the same size."
            )
        
        self.matv = matv
        return
    
    def __coerce__(self, other):
        if not isinstance(other, Matrix):
            other = Matrix(other)
        pass
    
    def conjugate(self):
        ret = self.matv[:]
        for idx in range(len(ret)):
            for jdx in range(len(ret[0])):
                ret[idx][jdx] = ret[idx][jdx].conjugate()

        return Matrix(ret)
    
    @property
    def rows(self):
        return len(self)
    
    @property
    def cols(self):
        return len(self[0])
    
    @property
    def T(self):
        """
        Transposes the matrix
        """
        return Matrix(list(map(list, zip(*self.matv))))
    
    @property
    def H(self):
        """
        Gets the complex transposition of the matrix
        """
        return self.conjugate().T
    
    def __len__(self):
        return len(self.matv)
    
    def __getitem__(self, *arg):
        """
        Support for indexing matrices.
        More complex indexing support will be added
        in the future.

        Right now, the only available syntax
        is the regular ol' Python container
        syntax as a 1- or 2-elem tuple, without slice support.
        """
        if isinstance(arg[0], int):
            return self.matv[arg[0]]
        
        return self.matv[arg[0][0]][arg[0][1]]
    
    def __setitem__(self, idx, value):
        """
        Minimal working support for Matrix.__setitem__
        Right now, syntax expressions are very lackluster,
        but updates will be made in the future.
        """
        assert len(idx) == 2 # DO NOT BREAK BY ACCIDENT
        self[idx] = value
        pass
    
    def __repr__(self):
        return f"Matrix({self.matv})"
    
    __str__ = __repr__