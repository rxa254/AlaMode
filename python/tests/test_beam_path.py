import numpy as np
import pytest
from alamode.beam_q import BeamQ
from alamode.component import Component
from alamode.beam_path import BeamPath

def test_free_space_propagation():
    w0, lam = 1e-3, 1064e-9
    bp = BeamPath()
    bp.seed_waist(w0, 0.0, lam)
    bp.add_component(Component.free_space(0.1, z=0.1))
    q2 = bp.propagate()
    z0 = np.pi * w0**2 / lam
    expected = w0 * np.sqrt(1 + (0.1/z0)**2)
    assert pytest.approx(q2.beam_width, rel=1e-2) == expected

def test_matlab_q_propagate_parity():
    w0, lam = 1e-3, 1064e-9
    L1, f, L2 = 0.1, 0.2, 0.05
    bp = BeamPath()
    bp.seed_waist(w0, 0.0, lam)
    bp.add_component(Component.lens(f, z=L1))
    q0 = BeamQ.from_waist_and_z(w0, 0.0, lam)
    M1 = np.array([[1, L1], [0,1]], float)
    M2 = np.array([[1, 0], [-1/f,1]], float)
    M3 = np.array([[1, L2], [0,1]], float)
    q1 = q0.transform(M1)
    q2 = q1.transform(M2)
    q3 = q2.transform(M3)
    q_test = bp.q_propagate(L1+L2)
    assert pytest.approx(q_test.q, rel=1e-9) == q3.q
