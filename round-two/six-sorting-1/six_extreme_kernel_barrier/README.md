Author and executing agent: **six-sorting-1, researcher**, 2026-10-01.

The literal native kernel0 prefix has eighteen original three-low,
three-high clampings with certified lower weight281018368>2^28.
The semantic pruning theorem and S(7)>=16 force total sorting size>=45,
with arbitrary suffix orientations, order and depth. Combined with the
published native-prefix cover, this leaves32 nine-wire size12 targets.
The unrestricted thirteen-input interval remains44..45.

Read [PROOF.md](PROOF.md), the [selected-witness certificate](certificate.json)
and the [standalone scalar checker](verify.py). Python3.11+ standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B generate.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B verify.py
```

Expected: `SIX_EXTREME_KERNEL_CERTIFICATE_REGENERATED` and
`ALL_SIX_EXTREME_KERNEL_LOWER_WITNESS_CHECKS_PASSED`. The producer enumerates
34320 original clampings; the proof and checker need only18 selected
original cubes, each with128 assignments. Certificate SHA256:
`cebd66e3f1e6ce2a161b2051797cfa632084e2abe0d7cef90286b9ab92b1b781`.
The scalar run checks2304 proof assignments,4608 positive clamping
assignments,16384 thirteen-input and128 seven-input positive controls,
and rejects six damaged certificates/fixture pins. It imports no producer,
profiler, search or solver. Algorithmic independence is not an external
reviewer verdict or formalization; analytic and published-cover dependencies
are explicit in the proof. No large corpus or private data is required.
