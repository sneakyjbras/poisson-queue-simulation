#!/usr/bin/env bash
# critical.sh — M/M/1 critical regime (μ = λ)
python src/mm1/main.py \
  --lambda-values 0.75 1.00 1.25 1.50 \
  --mu-values     0.75 1.00 1.25 1.50 \
  --num-events    10000 \
  --seed          42

