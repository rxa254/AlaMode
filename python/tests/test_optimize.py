import numpy as np
from alamode.optimize import fminsearchbnd

def test_fminsearchbnd_simple():
    # minimize (x-0.5)^2 with bounds [0,1]
    def fun(x):
        return (x[0] - 0.5)**2
    x_opt, fval = fminsearchbnd(fun, [0.2], [(0,1)])
    assert abs(x_opt[0] - 0.5) < 1e-3
