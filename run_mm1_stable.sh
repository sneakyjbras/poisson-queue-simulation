#!/usr/bin/env bash
# stable.sh — M/M/1 stable regime (μ > λ)
python src/mm1/main.py \
  --lambda-values 0.5 1.0 1.5 2.0 \
  --mu-values     2.5 3.0 4.0 5.0 \
  --num-events    10000 \
  --seed          42

