[![CI](https://github.com/rxa254/AlaMode/actions/workflows/ci.yml/badge.svg)](https://github.com/rxa254/AlaMode/actions/workflows/ci.yml)

# AlaMode

AlaMode is a MATLAB toolbox for modeling Gaussian beam propagation, mode matching, and optical component chains. It provides core classes and utilities commonly used in laser interferometer design and optical analysis.

---

## Features

- **Beam parameter (`BeamQ`)**  
  - Compute beam waist, radius of curvature, and Gouy phase  
  - Propagate through ABCD optical systems  
  - Calculate mode-overlap integrals  

- **Optical chain (`BeamPath`)**  
  - Define sequences of optical elements (lenses, mirrors, free-space segments)  
  - Optimize element positions for mode matching via bounded Nelder–Mead (`fminsearchbnd`)  
  - Visualize beam radius and wavefront along the path  

- **Component definitions (`Component`)**  
  - Factory methods for standard optics: `flat_mirror`, `curved_mirror`, `lens`, `free_space`  
  - Ensures port labeling and dimensional consistency  

- **Utilities**  
  - `dsxy2figxy` — convert data coordinates to figure-fraction coordinates for annotations  
  - `fminsearchbnd` — bounded variant of MATLAB’s `fminsearch`  

- **Examples**  
  - `pslmode.m` — PSL mode-matching example  
  - `choosecompsexample.m` — component selection demo  
  - `beamfitexample.m` — beam-fitting to measured data  
  - `customcostexample.m` — defining custom optimization objectives  

---

## Repository Structure

```plaintext
AlaMode/
├── alm.m
├── @beamPath/
│   └── beamPath.m
├── @beamq/
│   └── beamq.m
├── @component/
│   └── component.m
├── dsxy2figxy.m
├── fminsearchbnd.m
└── examples/
    ├── pslmode.m
    ├── choosecompsexample.m
    ├── beamfitexample.m
    └── customcostexample.m
```

---

## Requirements

- MATLAB R2018a or later  
- Optimization Toolbox (optional; `fminsearchbnd` is self-contained)

---

## Installation

1. **Clone the repository**  
   ```sh
   git clone https://github.com/rxa254/AlaMode.git
   ```

2. **Add to your MATLAB path**  
   ```matlab
   addpath(genpath('path/to/AlaMode'));
   ```

---

## Usage

Once added to your path:

```matlab
% Launch the main entry point
alm

% Or run one of the examples:
pslmode
```

Inspect beam-radius vs. position plots, optimization progress, and mode-matching metrics.

---

## License

See [LICENSE.txt](LICENSE.txt) for details.
