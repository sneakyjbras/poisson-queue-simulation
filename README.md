# Poisson Process and M/M/1 Queue Simulation

This project provides a lightweight framework to:

* Simulate **Poisson processes** and generate event‐time histograms.
* Simulate **M/M/1 queues** and compute performance metrics.

Both modules support sweeping over multiple parameter values in parallel.

---

## Requirements

* **Python 3.x**
* Install dependencies via pip (e.g. `numpy`, `matplotlib`).

---

## Poisson Process Simulation

Run the Poisson CLI under `src/poisson`:

```bash
python src/poisson/main.py \
  --rates 0.5 1.0 2.0      \  # one or more λ values
  --num-events 1000 5000    \  # one or more N values
  --delta 1.0               \  # histogram bin width
  --save-plots              \  # save histogram vs theoretical PMF
  --output-dir poisson_out  \  # (optional) output folder
  [--tmax <time>]           \  # (optional) max time horizon
  [--superimpose]           \  # (optional) combine processes
```

* Computes counts per interval and (if requested) saves plots in `poisson_out/`.
* Use `-h` or `--help` for full options.

---

## M/M/1 Queue Simulation

Run the M/M/1 CLI under `src/mm1`:

```bash
python src/mm1/main.py \
  --lambda-values 0.8 1.0   \  # one or more arrival rates
  --mu-values 1.5 2.0        \  # one or more service rates
  --num-events 10000         \  # number of departure events
  [--seed 42]                \  # (optional) RNG seed
```

* Simulates each (λ, μ) pair in parallel.
* Prints a table with:

  * **E\[N]**: average number in system
  * **E\[T\_sys]**: average time in system
  * **E\[T\_q]**: average waiting time
  * **Util%**: server utilization
* Use `-h` or `--help` for full options.

---

## License

This project is released under the MIT License. Feel free to use and modify.

