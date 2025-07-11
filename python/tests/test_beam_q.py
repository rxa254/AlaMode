import numpy as np
import pytest
from alamode.beam_q import BeamQ

def test_from_waist_and_z_properties():
    w0, z0, lam = 1e-3, 0.2, 1064e-9
    bq = BeamQ.from_waist_and_z(w0, z0, lam)
    assert pytest.approx(bq.waist_size, rel=1e-9) == w0
    assert pytest.approx(bq.rayleigh_range, rel=1e-9) == np.pi * w0**2 / lam
    assert pytest.approx(bq.divergence_angle, rel=1e-9) == w0 / (np.pi * w0**2 / lam)
    assert pytest.approx(np.real(bq.q), rel=1e-9) == z0

def test_transform_and_transform_value():
    lam = 1064e-9
    bq = BeamQ.from_waist_and_z(1e-3, 0.0, lam)
    M = np.array([[1, 0.1], [0, 1]], float)
    q2 = BeamQ.transform_value(bq.q, M)
    bq2 = bq.transform(M)
    assert pytest.approx(bq2.q, rel=1e-12) == q2

def test_duplicate_independence():
    lam = 1064e-9
    bq = BeamQ.from_waist_and_z(1e-3, 0.0, lam)
    bq2 = bq.duplicate()
    bq2.q = 5
    assert bq.q != bq2.q

def test_overlap_identical_beams():
    lam = 1064e-9
    bq = BeamQ.from_waist_and_z(1e-3, 0.0, lam)
    assert pytest.approx(bq.overlap(bq), rel=1e-9) == 1.0
