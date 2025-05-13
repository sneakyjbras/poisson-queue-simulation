#!/usr/bin/env bash
# unstable.sh — M/M/1 unstable regime (μ < λ)
python src/mm1/main.py \
  --lambda-values 2.0 2.5 3.0 3.5 \
  --mu-values     1.0 1.2 1.5 1.8 \
  --num-events    10000 \
  --seed          42

