# Reproduction

Run from this directory with Python 3.  No third-party Python module is
required.

Quick physical-closure and mixed-phase screens:

```bash
python3 scratch_fixed_circle_closure_sweep.py --depth 2 --node-limit 10000000
python3 scratch_mixed_phase_sumset_search.py --phase-count 3 --maximum-exponent 8 --node-limit 20000000
python3 scratch_mixed_phase_sumset_search.py --phase-count 4 --maximum-exponent 4 --node-limit 20000000
python3 scratch_mixed_phase_sumset_search.py --phase-count 5 --maximum-exponent 3 --node-limit 50000000
```

Exact arithmetic sweeps (slower):

```bash
python3 scratch_common_neighbor_sumsets.py --mode two --node-limit 2000000
python3 scratch_common_neighbor_power_ladder.py --maximum-power 21 --node-limit 20000000
```

The exact programs represent each coordinate in the basis
`1,sqrt(3),sqrt(11),sqrt(33)` with rational coefficients and decide equality
and squared distance exactly.  Every reported positive colour word is checked
directly against the reconstructed strict unit edges.  The DSATUR search is
not a proof logger, so an apparent non-four-colourable result is deliberately
labelled `PROVISIONAL` and would require an independent SAT/DRAT certificate.

The closure and broad mixed-phase programs use double precision to discover
coincidences and edges.  They report the smallest gap between a rejected pair
distance and one, and directly validate positive colour words against the
discovered graph.  Their negative construction result is experimental: the
scripts do not supply interval or exact certificates that no unit edge was
missed.  This limitation is part of the stated claim, not hidden in tooling.

