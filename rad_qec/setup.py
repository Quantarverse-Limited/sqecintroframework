from setuptools import setup, find_packages
import os
readme_path = 'README.md'
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()
else:
    long_description = "A package for simulating space radiation effects on quantum systems and implementing space-hardened quantum error correction"
setup(
    name='SQEC',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'qiskit',
        'qiskit-aer',
         'matplotlib',
         'numpy'
    ],
    author='Arun Balabhadran, Cherian P I, Quantarverse LTD',
    description='A Qiskit-based Quantum Error Correction simulation package',
    long_description=long_description,
    long_description_content_type='text/markdown',
)

