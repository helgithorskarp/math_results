# Arbitrary three-deletion repairs of saturated C5 packings

Author: six-code-2, researcher. Read [PROOF.md](PROOF.md) for exact scope and prior art.
For every base in the specified saturated-fixed-point 68-word family, and every
point relabeling of such a base, an arbitrary packing sharing at least 65 words
has at most 68 words. The repaired packing needs no symmetry.

The equality census and five point-isomorphism types are already committed prior
results. The new three-deletion repair bound is same-author checked and has no
independent mathematical review. The unrestricted problem remains open.

Python 3.11 or later, standard library only. Run serially in a new scratch directory:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-code-2/order_five_local_structure/reproduce.py --work /tmp/c5-three-normal
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B round-two/six-code-2/order_five_local_structure/reproduce.py --work /tmp/c5-three-optimized
```

Each whole run and each checker has an initial 60-second guard; incomplete runs
are not absence proofs. Use one CPU job at a time and the unchanged 1CPU/2GiB scope.
`EXACT_RESULT.json` should agree byte for byte in normal and optimized runs and
with `EXPECTED.json`. Runtime, interpreter and memory metadata go in separate
`EXECUTION.json`. No private corpus is needed.

`CLASSIFICATION.json` and `INSTANCE.json` are exact copies from source commit
8ad8ea28df4a8fd12f4927e4bad879a1831f96ab. `THREE_CERTIFICATE.json` is compact
coverage data, checked by complete physical regeneration. `TYPE_CERTIFICATE.json`
is a supplementary positive point-map and invariant certificate, not a new claim
to the five-type classification. Keep generated outputs outside this package.
