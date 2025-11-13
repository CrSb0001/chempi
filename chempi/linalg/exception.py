"""
Exceptions related to errors raised by
functions related to linear algebra, for
example if a chemical equation cannot be balanced
due to an unsolvable system of equations.
"""

class LinalgException(Exception):
    """
    Should not be used in general practice.
    General-use exception that can be subclassed.
    """
    pass

class UninvertibleMatrixError(LinalgException, ValueError):
    """
    Raised when 
    """
    pass

class LSTSQNonconvergenceError(LinalgException, ValueError):
    """
    If lstsq does not converge.
    """
    pass

class LinalgOPError(LinalgException, ValueError):
    """
    """
    pass

class VectorOPError(LinalgOPError):
    """
    If vector operations are used with incompatible
    types.

    The `Vector` type MUST be the primary operand
    in this case for the error to be raised.
    """
    pass

class MatrixOPError(LinalgOPError):
    """
    If matrix operations are used with incompatible
    types.

    The `Matrix` type MUST be the primary operand
    in this case for the error to be raised.
    """
    pass