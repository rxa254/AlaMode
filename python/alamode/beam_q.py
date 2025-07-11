import numpy as np


class BeamQ:
    """Represents the complex q-parameter of a Gaussian beam, ported from MATLAB."""

    def __init__(self, q, wavelength, waist_z=None):
        self.q = q
        self.lambda_ = wavelength
        # In MATLAB, q = z + i z_R, so waist_z = real(q)
        self.waist_z = waist_z if waist_z is not None else np.real(q)

    @classmethod
    def from_q(cls, q, wavelength):
        return cls(q, wavelength)

    @classmethod
    def from_waist_and_z(cls, w0, z, wavelength):
        zR = np.pi * w0**2 / wavelength
        q = z + 1j * zR
        return cls(q, wavelength, waist_z=z)

    @classmethod
    def from_waist_and_r(cls, w0, R, wavelength):
        # at z=0, q = i zR, and R = R0
        zR = np.pi * w0**2 / wavelength
        # q = z - i zR where R = z*(1+(zR/z)^2) => at z = R, solves R = 0? MATLAB chooses pattern
        # We'll approximate: waist at 0
        q = 1j * zR
        beam = cls(q, wavelength, waist_z=0.0)
        beam._initial_R = R
        return beam

    @classmethod
    def from_beamwidth_and_r(cls, w, R, wavelength):
        # full width w = 2*w0
        w0 = w / 2
        return cls.from_waist_and_r(w0, R, wavelength)

    @property
    def waist_size(self):
        # w0 = sqrt(Im(q)*lambda/pi)
        return np.sqrt(np.imag(self.q) * self.lambda_ / np.pi)

    @property
    def rayleigh_range(self):
        return np.pi * self.waist_size**2 / self.lambda_

    @property
    def divergence_angle(self):
        return self.waist_size / self.rayleigh_range

    @property
    def beam_width(self):
        # w(z) = w0 * sqrt(1 + ((z - waist_z)/zR)^2)
        z = np.real(self.q)
        return self.waist_size * np.sqrt(
            1 + ((z - self.waist_z) / self.rayleigh_range) ** 2
        )

    @property
    def radius_of_curvature(self):
        z = np.real(self.q)
        zR = self.rayleigh_range
        if np.isclose(z, self.waist_z):
            return np.inf
        return z * (1 + (zR / (z - self.waist_z)) ** 2)

    @staticmethod
    def transform_value(q_in, M):
        """Static ABCD transform: (A q + B)/(C q + D)"""
        A, B, C, D = M.ravel()
        return (A * q_in + B) / (C * q_in + D)

    def duplicate(self):
        """Create a copy of this beam object."""
        return BeamQ(self.q, self.lambda_, waist_z=self.waist_z)

    def transform(self, M):
        """Apply an ABCD matrix M to this beam and return new BeamQ."""
        q_out = BeamQ.transform_value(self.q, M)
        new_beam = self.duplicate()
        new_beam.q = q_out
        return new_beam

    def overlap(self, other):
        """Mode overlap fraction of two beams on axis."""
        w1 = self.waist_size
        w2 = other.waist_size
        diff = other.q.conjugate() - self.q
        return (2 * np.sqrt(w1 * w2) / (w1 + w2)) ** 2
