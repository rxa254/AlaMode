## AlaMode: MATLAB Gaussian-Beam Toolbox

AlaMode is a MATLAB toolbox for modeling Gaussian-beam propagation, mode matching, and optical component chains. It provides classes and utilities to design, analyze, and optimize complex optical systems—from simple telescopes to high-finesse cavities.

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Repository Structure](#repository-structure)
4. [Core Concepts & Classes](#core-concepts--classes)

   * [beamQ](#beamq)
   * [beamPath](#beampath)
   * [component](#component)
   * [Utilities](#utilities)
5. [Using AlaMode for Telescope Analysis](#using-alamode-for-telescope-analysis)

   * [Designing a Two-Lens Telescope](#designing-a-two-lens-telescope)
   * [Mode-Matching into a Cavity](#mode-matching-into-a-cavity)
6. [Example Workflows](#example-workflows)

   * [PSL Mode Matching (`pslmode.m`)](#psl-mode-matching-pslmodem)
   * [Component Selection (`choosecompsexample.m`)](#component-selection-choosecompsexamplem)
   * [Beam Fitting (`beamfitexample.m`)](#beam-fitting-beamfitexamplem)
   * [Custom Cost Optimization (`customcostexample.m`)](#custom-cost-optimization-customcostexamplem)
7. [Tips & Best Practices](#tips--best-practices)
8. [License](#license)

---

## Overview

The Gaussian-beam (`q`) parameter provides a concise way to track beam waist, curvature, and divergence through optical systems using ABCD matrices. AlaMode builds on this to:

* **Propagate** beams through free space, lenses, and mirrors
* **Optimize** component positions for maximal TEM$_{00}$ overlap
* **Visualize** beam radius and wavefront evolution
* **Customize** analysis via user-defined cost functions

## Installation

1. **Clone the repository**:

   ```matlab
   git clone https://github.com/rxa254/AlaMode.git
   ```
2. **Add to MATLAB path**:

   ```matlab
   addpath(genpath('path/to/AlaMode'))
   ```
3. **Run**:

   ```matlab
   alm  % displays help and example list
   ```

## Repository Structure

```
AlaMode/
├── alm.m                % Entry-point: help alm
├── @beamq/              % beamQ class folder
│   └── beamq.m
├── @beamPath/           % beamPath class folder
│   └── beamPath.m
├── @component/          % component factory folder
│   └── component.m
├── dsxy2figxy.m         % Data-to-figure helper
├── fminsearchbnd.m      % Bounded fminsearch wrapper
└── examples/            % Demonstration scripts
    ├── pslmode.m
    ├── choosecompsexample.m
    ├── beamfitexample.m
    └── customcostexample.m
```

## Core Concepts & Classes

### beamQ

Represents the complex beam parameter $q = z + i\,z_R$:

* **Constructor**: `bq = beamQ.fromWaist(w0, z0, lambda)`
* **Methods**:

  * `bq.waist()` – returns beam radius $w(z)$
  * `bq.R()` – wavefront radius of curvature
  * `bq.transform(M)` – ABCD propagation
  * `bq.overlap(bq2)` – on-axis TEM$_{00}$ overlap

### beamPath

Chains together `component` elements and propagates a `beamQ`:

* **seedWaist**: `path.seedWaist(w0, z0, lambda)`
* **addComponent**: `path.addComponent(component.free_space(0.1))`
* **propagate**: `path.propagate()`
* **optimizePath**: bounded Nelder–Mead to match a target beam
* **plotSummary**: visualizes $w(z)$ and component positions

### component

Factory methods for standard optics:

* `component.free_space(L, z0)`
* `component.lens(f, z0)`
* `component.curved_mirror(R, z0)`
* `component.flat_mirror(z0)`

### Utilities

* `dsxy2figxy(ax, [x,y,w,h])` – convert data coords to figure coords
* `fminsearchbnd(fun, x0, bounds)` – bounded optimization

## Using AlaMode for Telescope Analysis

You can model and optimize your own telescope designs:

### Designing a Two-Lens Telescope

1. **Seed** a beam with known waist:

   ```matlab
   bq0 = beamQ.fromWaist(0.5e-3, 0, 1064e-9);
   path = beamPath();
   path.seedWaist(bq0);
   ```
2. **Add lenses** at approximate distances:

   ```matlab
   path.addComponent(component.lens(0.1, 0.2));  % f=100mm at z=0.2m
   path.addComponent(component.lens(0.05, 0.5)); % f=50mm at z=0.5m
   ```
3. **Propagate and visualize**:

   ```matlab
   path.propagate();
   path.plotSummary();
   ```
4. **Optimize spacing** to achieve desired magnification or waist:

   ```matlab
   path.optimizePath('L1',(0.15,0.25),'L2',(0.45,0.55));
   ```

### Mode-Matching into a Cavity

To couple into a cavity with a known waist $w_c$ at length $L$:

```matlab
target = beamQ.fromWaist(w_c, L, lambda);
path.targetBeam = target;
path.optimizePath('L1',bounds1,'L2',bounds2);
```

## Example Workflows

### PSL Mode Matching (`pslmode.m`)

Demonstrates a multi-lens, multi-path optimization for high-overlap in pre-stable-laser chains. Use `help pslmode` for usage details.

### Component Selection (`choosecompsexample.m`)

Shows how to brute-force through discrete lens lists and pick the combination with highest overlap.

### Beam Fitting (`beamfitexample.m`)

Generates noisy beam-width data and fits for $w_0$ and $z_0$ via `lsqcurvefit`.

### Custom Cost Optimization (`customcostexample.m`)

Illustrates injecting a user-defined cost (e.g., overlap minus waist penalty) into the optimization.

## Tips & Best Practices

* Always start by seeding with an accurate waist measurement.
* Visualize $w(z)$ early to catch unexpected divergences.
* Use discrete brute-force when you have a small number of catalog lenses.
* For large parameter spaces, customize the cost function for robust convergence.

## License

Distributed under the MIT License. See `LICENSE.txt` for details.
