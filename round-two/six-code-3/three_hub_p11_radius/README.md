# Exact three-hub P11 obstruction

six-code-3, researcher. Conditional author-checked theorem: every71-word
A(18,6,5) packing with exactly three unsaturated points has their total
pair replication at least11. Both point profiles are covered. The new
radius lemma and actual K5 triple obstruction exclude all20 P10 branches.
Independent mathematical review is pending; ordinary bridges are unformalized.

Read [PROOF.md](PROOF.md) and [DEPENDENCIES.json](DEPENDENCIES.json).
Only CPython3.11+ and its standard library are needed. From the repository
root run sequentially, choosing fresh scratch directories:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 round-two/six-code-3/three_hub_p11_radius/reproduce.py \
  --work scratch/three-hub-p11-normal
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -O round-two/six-code-3/three_hub_p11_radius/reproduce.py \
  --work scratch/three-hub-p11-optimized
```

Both full RESULT.json files should be identical, SHA256
96b21e91ae18caf2d029fdd5a893f4136cb6ca0bffda726b7c3c16662199859d.
The runner independently reconstructs426 literal marked rows,56 types and
all118 necessary populations, compares every complete object, and checks
14 semantic/scope controls. The final5-unit K5 bridge is an ordinary
proof, not formalization or enumeration of physical71-word codes.
Expected data were frozen before the independent run. Fixed guards are
never increased and an incomplete run supplies no absence conclusion.
Large generated records remain in the requested scratch directory.

The public source is this compact directory:
https://github.com/helgithorskarp/math_results/tree/main/round-two/six-code-3/three_hub_p11_radius
