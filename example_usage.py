from client import MonteCarloGBMSimulator

def run_example():
    print("=== GenPark Monte Carlo GBM Simulator Example ===")
    sim = MonteCarloGBMSimulator()
    print("Simulation Results:", sim.benchmark_monte_carlo_gbm())

if __name__ == "__main__":
    run_example()
