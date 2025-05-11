# Poisson Process Simulation

This project simulates a Poisson process over varying parameters and compares empirical counts per time interval against the theoretical Poisson distribution.

## Directory Structure

```
poisson-queue-simulation/
├── src/
│   ├── main.py
│   ├── poisson_sim.py
│   └── histogram.py
└── README.md
```

## Requirements

* Python 3.8+
* NumPy
* Matplotlib

Install dependencies:

```bash
pip install numpy matplotlib
```

## Usage

Run `main.py` with desired parameters. The script supports:

* `--rates`: one or more λ values
* `--num-events`: one or more N values
* `--tmax`: optional fixed time horizon
* `--delta`: histogram bin width (default 1.0)
* `--workers`: number of parallel processes (default: CPU count)
* `--save-plots`: flag to save overlay plots
* `--output-dir`: directory for saved plots (default: `histograms`)

An example can be found in the root directory named `run_example.sh`.

### Suggested Parameter Sweep

To cover a broad range, you can use:

* **λ values**: `0.1 0.5 1.0 5.0 10.0 50.0 100.0`
* **N values**: `10 100 1000 10000 50000`

This gives 7 × 5 = 35 simulations.

### Example Command

From the project root:

```bash
python src/main.py \
  --rates 0.1 0.5 1.0 5.0 10.0 50.0 100.0 \
  --num-events 10 100 1000 10000 50000 \
  --delta 1.0 \
  --workers 16 \
  --save-plots \
  --output-dir poisson_sweep
```

This will run 35 simulations in parallel, histogram counts into 1-unit bins, and save timestamped PNGs in `poisson_sweep/`.

## Notes

* The script uses Python-level parallelism (`ProcessPoolExecutor`) for efficiency.
* Empirical vs. theoretical overlay plots help validate that counts per interval follow `Pois(λΔ)`.

