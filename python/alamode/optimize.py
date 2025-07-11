import numpy as np
from scipy.optimize import minimize


def fminsearchbnd(fun, x0, bounds, args=(), options=None):
    def penalized(x, *a):
        pen = 0
        for xi, (low, high) in zip(x, bounds):
            pen += max(0, low - xi) ** 2 + max(0, xi - high) ** 2
        return fun(x, *a) + 1e6 * pen

    res = minimize(
        penalized, x0, args=args, method="Nelder-Mead", options=options or {}
    )
    return res.x, res.fun
