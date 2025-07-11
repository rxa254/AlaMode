import numpy as np
import pytest
from alamode.component import Component
from alamode.beam_path import BeamPath
from alamode.beam_q import BeamQ

def test_free_space_abcd_matrix():
    L = 0.2
    comp = Component.free_space(L, z=L)
    M = comp.M
    assert np.allclose(M, np.array([[1, L], [0, 1]]))

def test_lens_abcd_matrix():
    f = 0.15
    comp = Component.lens(f, z=0.1)
    M = comp.M
    expected = np.array([[1, 0], [-1/f, 1]])
    assert np.allclose(M, expected)

def test_flat_mirror_identity_matrix():
    comp = Component.flat_mirror(z=0.5)
    M = comp.M
    assert np.allclose(M, np.eye(2, dtype=float))

def test_component_sorting_by_z():
    comp1 = Component.lens(0.1, z=0.3, label='L1')
    comp2 = Component.lens(0.2, z=0.1, label='L2')
    bp = BeamPath()
    bp.seed_waist(1e-3, 0.0, 1064e-9)
    bp.add_component(comp1)
    bp.add_component(comp2)
    zs = [c.z for c in bp.components]
    assert zs == sorted(zs)
