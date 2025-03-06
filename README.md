# Introductory Software Framework for Space-Hardened Quantum Error Correction 

## Introduction

This repository provides an introductory software framework for Quantum Error Correction (QEC) specifically tailored for space environments. It models the effects of space radiation (e.g., cosmic rays, solar particles) on quantum circuits and applies space-hardened error correction protocols to mitigate induced errors.

The framework is a key deliverable from a project funded through the STFC Cross Cluster Proof of Concept: SparQ Quantum Computing Call, titled "Space-Hardened Quantum Error Correction for Orbital Computing."

## Project Structure

```
rad_qec/
├── SQEC/
│   └── qec.py         # Core implementation
│       ├── SpaceRadiationSimulator  # Simulates space radiation environments
│       ├── SpaceHardenedQEC         # Implements QEC protocols
│       └── Visualizer               # Analysis and visualization tools
│    
│── setup.py       # Package installation configuration
│── test.py        # Test script for the framework
│
└── README.md          # This file
```

## Radiation Environment Models

The framework incorporates radiation data for different orbital parameters:

| Altitude (km) | Radiation Environment (SSO) | Radiation Environment (45°) |
|:-------------:|:---------------------------:|:---------------------------:|
|      600      |           0.010            |           0.008             |
|      700      |           0.015            |           0.010             |
|      800      |           0.020            |           0.012             |

## Installation

```bash
pip install SQEC
```


## Requirements

- Python 3.x
- Qiskit (Quantum Information Science Kit)
- NumPy
- Matplotlib


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This work was supported by the STFC Cross Cluster Proof of Concept: SparQ Quantum Computing Call.

## Contact

For inquiries about this project or potential collaborations, please contact:
- Email: aa@quantarverse.com

## Citation

If you use this software in your research, please cite:
```
Quantarverse Limited. (2025). Space-Hardened Quantum Error Correction for Orbital Computing.
STFC Cross Cluster Proof of Concept: SparQ Quantum Computing Call.

```
