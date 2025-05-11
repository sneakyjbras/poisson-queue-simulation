#!/usr/bin/env bash
# run_sweep.sh
# Bash script to sweep Poisson process simulations with varied λ and N

# Discrete λ values
RATES=(0.5 1.0 2.0 5.0 10.0 20.0 25.0 50.0 75.0 100.0)
# Discrete N values
NUM_EVENTS=(10 50 100 250 500 750 1000 2500 5000 7500 10000 25000 50000)

# Other parameters
WORKERS=16
DELTA=1.0
OUTPUT_DIR="poisson_sweep"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Run the Python script with arrays
python src/main.py \
  --rates "${RATES[@]}" \
  --num-events "${NUM_EVENTS[@]}" \
  --delta $DELTA \
  --workers $WORKERS \
  --save-plots \
  --output-dir $OUTPUT_DIR

echo "Sweep finished. Plots saved in $OUTPUT_DIR/"

