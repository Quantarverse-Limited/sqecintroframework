from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from SQEC.qec import SpaceRadiationSimulator, SpaceHardenedQEC, Visualizer

def test_qec():
    print("Initializing Space Radiation Simulator...")
    radiation_sim = SpaceRadiationSimulator(altitude=600, inclination='SSO', mission_duration=1.0)

    print("Creating Quantum Error Correction object...")
    qec = SpaceHardenedQEC(radiation_sim, error_probability=0.01)

    print("Generating 4-2-2 Quantum Circuit...")
    circuit = qec._create_circuit()
    print(circuit.draw()) 


    print("Running the experiment with noise model...")
    result_counts = qec.run_experiment(circuit, shots=1300000)

    print("Analyzing the results...")
    visualizer = Visualizer(circuit)
    analysis_results = visualizer.analyze_results(result_counts)

    # Displaying analysis
    print("\n---  Syndrome Distribution Analysis ---")
    for syndrome, count in analysis_results['error_types'].items():
        print(f"Syndrome {syndrome}: {count} occurrences ({analysis_results['error_percentages'][syndrome]})")

    print(f"Total shots: {analysis_results['total_shots']}")
    print(f"Valid shots (post-selection): {analysis_results['valid_shots']}")
    print(f"Post-selection ratio: {analysis_results['post_selection_ratio']:.2f}")

    # Plot results
    print("Plotting results...")
    visualizer.plot_error_analysis(analysis_results)

    # Histogram of final results
    plot_histogram(result_counts, title="Final Measurement Distribution")
    plt.show()

if __name__ == "__main__":
    test_qec()

