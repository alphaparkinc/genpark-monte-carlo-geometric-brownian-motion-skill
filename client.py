import math, random
from typing import Dict, Any

class MonteCarloGBMSimulator:
    @classmethod
    def simulate_paths(cls, S0: float, mu: float, sigma: float, T: float, steps: int = 100, num_simulations: int = 300) -> Dict[str, Any]:
        dt = T / steps
        nudt = (mu - 0.5 * sigma * sigma) * dt
        sidt = sigma * math.sqrt(dt)
        finals = []
        for _ in range(num_simulations):
            price = S0
            for _ in range(steps):
                u1 = max(1e-10, random.random())
                u2 = random.random()
                z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
                price *= math.exp(nudt + sidt * z)
            finals.append(price)
        sorted_p = sorted(finals)
        return {
            "S0": S0, "expected_mean_price": round(sum(finals) / len(finals), 2),
            "percentile_5th": round(sorted_p[int(0.05 * len(sorted_p))], 2),
            "percentile_95th": round(sorted_p[int(0.95 * len(sorted_p))], 2),
            "num_simulations": num_simulations
        }

    def benchmark_monte_carlo_gbm(self) -> Dict[str, Any]:
        return self.simulate_paths(100.0, 0.08, 0.20, 1.0, steps=50, num_simulations=200)
