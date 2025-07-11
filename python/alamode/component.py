import numpy as np

class Component:
    """Optical element with ABCD matrix and position z."""

    def __init__(self, M, z, label=''):
        self.M = M
        self.z = z
        self.label = label

    @staticmethod
    def free_space(L, z=0.0, label=None):
        M = np.array([[1, L], [0, 1]], float)
        return Component(M, z, label or f"FS@{L}")

    @staticmethod
    def lens(f, z=0.0, label=None):
        M = np.array([[1, 0], [-1 / f, 1]], float)
        return Component(M, z, label or f"Lens f={f}")

    @staticmethod
    def flat_mirror(z=0.0, label=None):
        M = np.eye(2, dtype=float)
        return Component(M, z, label or "Mirror")
