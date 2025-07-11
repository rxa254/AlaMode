import numpy as np
from .beam_q import BeamQ
from .component import Component
from .optimize import fminsearchbnd
from itertools import product


class BeamPath:
    """Builds and propagates a Gaussian beam through optical elements."""

    def __init__(self, initial_beam=None, initial_z=0.0):
        self.initial_beam = initial_beam
        self.initial_z = initial_z
        self.components = []
        self.target_beam = None
        self.target_z = None

    def seed_waist(self, w0, z, wavelength):
        self.initial_beam = BeamQ.from_waist_and_z(w0, z, wavelength)
        self.initial_z = z

    def target_waist(self, w0, z, wavelength=None):
        lam = wavelength if wavelength is not None else self.initial_beam.lambda_
        self.target_beam = BeamQ.from_waist_and_z(w0, z, lam)
        self.target_z = z

    def add_component(self, comp):
        self.components.append(comp)
        self.components.sort(key=lambda c: c.z)

    def q_propagate(self, z_target):
        if self.initial_beam is None:
            raise ValueError("Seed beam not defined.")
        beam = self.initial_beam
        last_z = self.initial_z
        elements = []
        for comp in self.components:
            L = comp.z - last_z
            elements.append(np.array([[1, L], [0, 1]], float))
            elements.append(comp.M)
            last_z = comp.z
        Lf = z_target - last_z
        elements.append(np.array([[1, Lf], [0, 1]], float))
        for M in elements:
            beam = beam.transform(M)
        return beam

    def propagate(self, z=None):
        if z is None:
            z = (
                self.target_z
                if self.target_z is not None
                else (self.components[-1].z if self.components else self.initial_z)
            )
        return self.q_propagate(z)

    def optimize_path(self, *args, units="m", options=None):
        labels = args[0::2]
        bounds = args[1::2]
        idx = [
            next(i for i, c in enumerate(self.components) if c.label == lab)
            for lab in labels
        ]
        x0 = [self.components[i].z for i in idx]
        if units == "inch":
            bounds = [(l * 0.0254, u * 0.0254) for l, u in bounds]

        def cost(x):
            for i, z in zip(idx, x):
                self.components[i].z = z
            return -self.propagate().overlap(self.target_beam)

        zs, _ = fminsearchbnd(cost, x0, bounds, options=options)
        for i, z in zip(idx, zs):
            self.components[i].z = z
        return self

    def choose_components(self, *cands, cost_func=None, verbose=False):
        candidate_lists = []
        for label, clist, bnds in zip(cands[0::3], cands[1::3], cands[2::3]):
            if clist is None:
                candidate_lists.append(
                    [next(c for c in self.components if c.label == label)]
                )
            else:
                candidate_lists.append(clist)
        paths, scores = [], []
        for combo in product(*candidate_lists):
            bp = BeamPath(self.initial_beam, self.initial_z)
            bp.target_beam, bp.target_z = self.target_beam, self.target_z
            for comp in combo:
                bp.add_component(comp)
            score = (
                cost_func(bp) if cost_func else bp.propagate().overlap(bp.target_beam)
            )
            paths.append(bp)
            scores.append(score)
            if verbose:
                print(f"Combo {combo}: {score:.4f}")
        return paths, scores

    def plot_summary(self, title=None):
        import matplotlib.pyplot as plt

        z_end = (
            self.target_z
            if self.target_z is not None
            else (self.components[-1].z if self.components else self.initial_z)
        )
        zarr = np.linspace(self.initial_z, z_end, 300)
        w = [self.q_propagate(z).waist_size for z in zarr]
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(zarr, w, "b-", label="waist")
        for comp in self.components:
            ax.axvline(comp.z, linestyle="--", label=comp.label)
        if title:
            fig.suptitle(title)
        ax.set_xlabel("z [m]")
        ax.set_ylabel("w(z) [m]")
        ax.legend()
        ax.grid(True)
        plt.show()
