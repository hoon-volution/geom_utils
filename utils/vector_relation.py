import numpy as np
from typing import TypeAlias


Vector: TypeAlias = tuple[float, float] | np.ndarray


class VectorRelation:
    """
    Represents the relation between two vectors
    """
    TOL = 1e-2

    def __init__(self, vector1: Vector, vector2: Vector):
        self.vector1 = np.array(vector1)
        if (norm1 := np.linalg.norm(vector1)) != 0:
            self.unit_vector1 = self.vector1 / norm1
        else:
            self.unit_vector1 = self.vector1

        self.vector2 = np.array(vector2)
        if (norm2 := np.linalg.norm(vector2)) != 0:
            self.unit_vector2 = self.vector2 / norm2
        else:
            self.unit_vector2 = self.vector2

    @property
    def tol(self) -> float:
        return self.TOL

    @property
    def det(self) -> float:
        return np.linalg.det([self.unit_vector1, self.unit_vector2])

    @property
    def dot(self) -> float:
        return np.dot(self.unit_vector1, self.unit_vector2)

    @property
    def are_parallel(self) -> bool:
        return np.isclose(self.det, 0, atol=self.tol)

    @property
    def are_perpendicular(self) -> bool:
        return np.isclose(self.dot, 0, atol=self.tol)

    @property
    def are_codirectional(self) -> bool:
        return np.isclose(self.dot, 1, atol=self.tol)

    @property
    def are_antidirectional(self) -> bool:
        return np.isclose(self.dot, -1, atol=self.tol)

    def get_angle(self,
                  use_radians: bool = True,
                  signed: bool = True) -> float:
        """
        :param use_radians:
            determines whether result will be in radians or degrees
        :param signed:
            If True, the result ranges from -pi(-180) to +pi(+180).
            If False, the result ranges from 0 to +2*pi(+360).
        :return: Angle between two vectors
        """

        cosine = np.clip(self.dot, -1, 1)
        angle = np.arccos(cosine)  # in radian

        sign = np.sign(self.det)
        if sign != 0:
            angle *= sign

        if not signed:
            angle %= 2 * np.pi

        if not use_radians:
            angle = np.rad2deg(angle)

        return angle
