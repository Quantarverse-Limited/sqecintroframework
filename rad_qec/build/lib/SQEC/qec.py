import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator, Aer
from qiskit.primitives import Sampler
from qiskit_aer.noise import NoiseModel, depolarizing_error, pauli_error
import matplotlib.pyplot as plt
from IPython.display import display

class SpaceRadiationSimulator:
    def __init__(self, altitude=None, inclination=None, mission_duration=None):
        self.altitude = altitude
        self.inclination = inclination
        self.mission_duration = mission_duration
        self._calculate_error_rates()
    
    def _calculate_error_rates(self):
        """Calculate quantum error rates based on radiation environment."""
        base_rates = {
            600: {'SSO': 0.010, '45': 0.008},
            700: {'SSO': 0.015, '45': 0.010},
            800: {'SSO': 0.020, '45': 0.012}
        }
        
        base_rate = base_rates[self.altitude][self.inclination]
        scaled_rate = base_rate * self.mission_duration
        
        # Set limits to prevent unrealistic error rates
        self.error_rate = min(0.33, scaled_rate)
        
        # Different types of errors
        self.bit_flip_rate = self.error_rate * 0.6   # Bit flips from SEEs
        self.phase_flip_rate = self.error_rate * 0.4 # Phase flips from TID
        
        print(f"Space radiation simulation for {self.altitude}km {self.inclination} orbit")
        print(f"Mission duration: {self.mission_duration} years")
        print(f"Calculated error rates: {self.error_rate:.4f} (overall), " 
              f"{self.bit_flip_rate:.4f} (bit flip), {self.phase_flip_rate:.4f} (phase flip)")
    
class SpaceHardenedQEC:
    def __init__(self, radiation_simulator=None, error_probability=None):

        if radiation_simulator is None:
            self.radiation = SpaceRadiationSimulator()
        else:
            self.radiation = radiation_simulator

        self.error_probability = error_probability if error_probability else self.radiation.error_rate
        self.noise_model = self.get_noise_model() 
        self.circuit = self._create_circuit()  

    
    def get_noise_model(self):
        """
        Create a realistic noise model with depolarizing errors.
        
        Returns:
            NoiseModel: Qiskit noise model with appropriate error rates
        """
        noise_model = NoiseModel()
        # Single-qubit depolarizing error
        p = self.error_probability / 3
        single_qubit_depol = pauli_error([
            ('X', p), ('Y', p), ('Z', p), ('I', 1 - 3*p)
        ])
        
        # Two-qubit depolarizing error
        cnot_error = depolarizing_error(self.error_probability, 2)
        
        # Add errors for all gates
        for qubit in range(6):  # 4 data + 2 ancilla qubits
            noise_model.add_quantum_error(single_qubit_depol, ['x'], [qubit])
            noise_model.add_quantum_error(single_qubit_depol, ['h'], [qubit])
            noise_model.add_quantum_error(single_qubit_depol, ['z'], [qubit])
        
        for q1 in range(6):
            for q2 in range(6):
                if q1 != q2:
                    noise_model.add_quantum_error(cnot_error, ['cx'], [q1, q2])
                    noise_model.add_quantum_error(cnot_error, ['cz'], [q1, q2])
                    
        return noise_model
    
    def _create_circuit(self):
        """
        Create the quantum circuit with two rounds of syndrome extraction.
        
        Returns:
            QuantumCircuit: Complete QEC circuit
        """
        # Create registers
        data_qubits = QuantumRegister(4, 'q')
        ancilla_qubits = QuantumRegister(2, 'a')
        c1 = ClassicalRegister(2, 'c1')  # First round measurements
        c2 = ClassicalRegister(2, 'c2')  # Second round measurements
        
        qc = QuantumCircuit(data_qubits, ancilla_qubits, c1, c2)
        
        # Initialize data qubits
        qc.reset(data_qubits[2])
        qc.reset(data_qubits[3])
        qc.h(data_qubits[3])
        
        # Entangle logical qubits
        qc.cx(data_qubits[0], data_qubits[2])
        qc.cx(data_qubits[1], data_qubits[2])
        qc.cx(data_qubits[3], data_qubits[2])
        qc.cx(data_qubits[3], data_qubits[1])
        qc.cx(data_qubits[3], data_qubits[0])
        
        # First round of syndrome extraction
        qc.barrier(label='First round')
        self._add_syndrome_measurement(qc, data_qubits, ancilla_qubits, c1)
        
        # Second round of syndrome extraction
        qc.barrier(label='Second round')
        self._add_syndrome_measurement(qc, data_qubits, ancilla_qubits, c2)
        
        return qc
    def _add_syndrome_measurement(self, qc, data_qubits, ancilla_qubits, creg):
        """
        Add syndrome measurement round to the circuit.
        
        Args:
            qc (QuantumCircuit): Circuit to add measurements to
            data_qubits (QuantumRegister): Data qubit register
            ancilla_qubits (QuantumRegister): Ancilla qubit register
            creg (ClassicalRegister): Classical register for measurements
        """
        # Z syndrome
        qc.reset(ancilla_qubits[0])
        qc.h(ancilla_qubits[0])
        for i in range(4):
            qc.cz(ancilla_qubits[0], data_qubits[i])
        qc.h(ancilla_qubits[0])
        qc.measure(ancilla_qubits[0], creg[0])
        
        # X syndrome
        qc.reset(ancilla_qubits[1])
        qc.h(ancilla_qubits[1])
        for i in range(4):
            qc.cx(ancilla_qubits[1], data_qubits[i])
        qc.h(ancilla_qubits[1])
        qc.measure(ancilla_qubits[1], creg[1])
    
    def run_experiment(self, circuit, shots=None):
        simulator = Aer.get_backend('qasm_simulator')
        job_with_correction = simulator.run(circuit, noise_model=self.noise_model, shots=shots)
        result_with_correction = job_with_correction.result().get_counts()
        return result_with_correction

class Visualizer:

    def __init__( circuit,noise_model):
        SpaceHardenedQEC.circuit = circuit  # Store the circuit reference
        SpaceHardenedQEC.get_noise_model=noise_model

    def analyze_results(counts,shots=None):
        simulator = Aer.get_backend('qasm_simulator')
        job = simulator.run(SpaceHardenedQEC.circuit,SpaceHardenedQEC.get_noise_model, shots=shots)
        counts = job.result().get_counts()
        # simulator = Aer.get_backend('qasm_simulator')
        # simulator = AerSimulator(noise_model=self.noise_model)
        # result = simulator.run(self.circuit, counts).result()
        # counts = result.get_counts()
        
        error_types = {'00': 0, '10': 0, '01': 0, '11': 0}
        total_shots = sum(counts.values())
        valid_shots = 0
        
        # Count different syndrome patterns and valid shots
        for bitstring, count in counts.items():
            # Check if first and second round syndromes match
            if bitstring[-2:] == bitstring[:2]:
                syndrome = bitstring[-2:]
                if syndrome in error_types:
                    error_types[syndrome] += count
                    valid_shots += count
        
        # Calculate error percentages
        error_percentages = {}
        for syndrome, count in error_types.items():
            if valid_shots > 0:
                error_percentages[syndrome] = f"{count/valid_shots*100:.2f}%"
            else:
                error_percentages[syndrome] = "0.00%"
        
        return {
            'error_types': error_types,
            'error_percentages': error_percentages,
            'total_shots': total_shots,
            'valid_shots': valid_shots,
            'post_selection_ratio': valid_shots/total_shots if total_shots > 0 else 0}
    
    def plot_error_analysis(self, analysis_results):
        syndromes = list(analysis_results['error_types'].keys())
        counts = [analysis_results['error_types'][s] for s in syndromes]
        print("Circuit Diagram:")
        print("---------------")
        display(self.circuit.draw(output='mpl', style={'backgroundcolor': '#FFFFFF'}))
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 5))
        ax1.bar(syndromes, counts)
        ax1.set_title("Syndrome Distribution")
        ax1.set_ylabel("Count")
        ax1.set_xlabel("Syndrome (00=None, 10=X, 01=Z, 11=Y)")
        
        # Error percentages
        percentages = [float(analysis_results['error_percentages'][s].strip('%')) for s in syndromes]
        ax2.bar(syndromes, percentages)
        ax2.set_title("Syndrome Percentages")
        ax2.set_ylabel("Percentage (%)")
        ax2.set_xlabel("Syndrome (00=None, 10=X, 01=Z, 11=Y)")
        
        # Post-selection ratio
        labels = ['Valid', 'Invalid']
        sizes = [analysis_results['valid_shots'], 
                 analysis_results['total_shots'] - analysis_results['valid_shots']]
        
        ax3.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax3.set_title(f"Post-Selection Ratio: {analysis_results['post_selection_ratio']:.4f}")
        

        # Print analysis summary
        print("\nError Analysis:")
        print("---------------")
        print(f"Syndrome Distribution (counts): {analysis_results['error_types']}")
        print(f"Syndrome Distribution Percentages: {analysis_results['error_percentages']}")
        print("\nCircuit Analysis:")
        print("---------------")
        print(f"Total shots: {analysis_results['total_shots']}")
        print(f"Valid shots: {analysis_results['valid_shots']}")
        print(f"Post-selection ratio: {analysis_results['post_selection_ratio']}")   
    
    def plot_results(self, results):
        """
        Plot the results of quantum error correction experiment.
        
        Parameters:
        -----------
        results : dict
            Results from the run_experiment method
        """
        fig, axs = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot results with error correction
        plot_histogram(results['with_correction'], title="With Error Correction", ax=axs[0])
        
        # Plot results without error correction
        plot_histogram(results['without_correction'], title="Without Error Correction", ax=axs[1])
        
        # Plot ideal results
        plot_histogram(results['ideal'], title="Ideal (No Errors)", ax=axs[2])
        
        fig.suptitle(f"Quantum Error Correction in Space Environment\n"
                    f"{self.radiation.altitude}km {self.radiation.inclination} orbit, "
                    f"{self.radiation.mission_duration} year mission")
        plt.tight_layout()
        plt.show()