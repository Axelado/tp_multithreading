#!/bin/bash
for i in {1..4}; do uv run python Minion.py  & done    # {1..n}  pour lancer n fois le script python
wait
