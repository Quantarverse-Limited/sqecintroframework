# Introductory Software Framework for Space-Hardened Quantum Error Correction 

## Introduction

This repository provides an introductory software framework for Quantum Error Correction (QEC) specifically tailored for space environments. It models the effects of space radiation (e.g., cosmic rays, solar particles) on quantum circuits and applies space-hardened error correction protocols to mitigate induced errors.

The framework is a key deliverable from a project funded through the STFC Cross Cluster Proof of Concept: SparQ Quantum Computing Call, titled "Space-Hardened Quantum Error Correction for Orbital Computing."

## Capabilities

- Simulation of space radiation effects on quantum computing systems
- Implementation of novel space-hardened QEC protocols
- System-level radiation resilience modeling
- Visualization and analysis tools for performance evaluation
- Configurable radiation environments based on orbital parameters

## Project Background

This software framework represents a collaboration between:
- **Quantarverse Ltd** (Lead Organization)
- **Radiation Analysis Services Ltd** (Partner)
- **Quantum Software Lab, University of Edinburgh** (Partner)
- **National Quantum Computing Centre** (Support)

The project addresses the unique challenges of operating quantum computers in space environments, with potential applications in:
- Secure satellite communications
- Quantum computing as a service
- Sensitive data hosting in space
- Confidential financial transactions
- Quantum AI processing
- Bioinformatics and medical diagnostics

## Project Structure

```
rad_qec/
├── SQEC/
│   ├── qec.py         # Core implementation
│   │   ├── SpaceRadiationSimulator  # Simulates space radiation environments
│   │   ├── SpaceHardenedQEC         # Implements QEC protocols
│   │   └── Visualizer               # Analysis and visualization tools
│   │
│   ├── setup.py       # Package installation configuration
│   └── test.py        # Test script for the framework
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
# Clone the repository
git clone https://github.com/username/rad_qec.git
cd rad_qec

# Install dependencies
pip install numpy matplotlib qiskit

# Install the package
pip install .
```

Alternatively, install directly from PyPI:

```bash
pip install SQEC
```

## Quick Start

```python
from SQEC.qec import SpaceRadiationSimulator, SpaceHardenedQEC
import matplotlib.pyplot as plt

# Initialize the radiation simulator with orbital parameters
simulator = SpaceRadiationSimulator(altitude=700, inclination='SSO')

# Create a QEC instance with the simulator
qec = SpaceHardenedQEC(simulator=simulator)

# Run a quantum circuit with error correction
results = qec.run_circuit(shots=1024)

# Visualize the results
qec.visualize(results)
plt.show()
```

## Key Features

### Space Radiation Simulator

The `SpaceRadiationSimulator` class models the space radiation environment and calculates error rates based on:
- Orbital altitude
- Inclination angle
- Solar activity level
- Spacecraft shielding properties

### Space-Hardened QEC

The `SpaceHardenedQEC` class implements quantum error correction schemes specifically designed for space environments:
- Radiation-aware error models
- Adaptive error correction based on orbital parameters
- Optimization for space radiation patterns

### Visualization Tools

The framework includes comprehensive visualization tools to:
- Compare error rates across different orbital scenarios
- Evaluate QEC performance metrics
- Analyze system-level resilience

## Requirements

- Python 3.x
- Qiskit (Quantum Information Science Kit)
- NumPy
- Matplotlib

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This work was supported by the STFC Cross Cluster Proof of Concept: SparQ Quantum Computing Call. We would like to thank all project partners and the National Quantum Computing Centre for their contributions.

## Contact

For inquiries about this project or potential collaborations, please contact:
- Quantarverse Ltd, Didcot

## Citation

If you use this software in your research, please cite:
```
Space-Hardened Quantum Error Correction for Orbital Computing. 
Quantarverse Ltd, Radiation Analysis Services Ltd, and Quantum Software Lab (University of Edinburgh).
STFC Cross Cluster Proof of Concept: SparQ Quantum Computing Call, 2024.
```
