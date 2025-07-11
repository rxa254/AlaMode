import pytest
import matplotlib.pyplot as plt
from alamode.utils import dsxy2figxy

def test_dsxy2figxy_point():
    fig, ax = plt.subplots()
    x, y = dsxy2figxy(ax, (0.2, 0.3))
    assert 0 <= x <= 1 and 0 <= y <= 1

def test_dsxy2figxy_rect():
    fig, ax = plt.subplots()
    bbox = ax.get_position()
    x, y, w, h = dsxy2figxy(ax, (0.1, 0.2, 0.5, 0.4))
    expected_w = 0.5 * bbox.width
    expected_h = 0.4 * bbox.height
    assert w == pytest.approx(expected_w, rel=1e-3)
    assert h == pytest.approx(expected_h, rel=1e-3)
