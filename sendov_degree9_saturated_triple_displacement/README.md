# Whole saturated-triple degree-nine displacement maximum

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Complete ordinary written author proof with exact integer/rational evidence;
unformalized, independent review pending.

For every balanced real max-normalized eight-vector with at least three
coordinates equal +1 or at least three equal -1, the credited angular
displacement functional satisfies

    J<=J_*,
    J=J_* iff theta is a permutation of the credited theta_*,
    dist(theta/sqrt(mu_2),O_*)^2<=5000(J_*-J).

The other five entries vary throughout their full closed balanced section
and can create six actual values. The new grouped polynomial argument
closes this whole saturated-triple slice. Singleton saturation elsewhere
in 3+1^5, the 2+2+1^4 cohort, the whole six-level maximum and the full
complex first-power endpoint remain unproved here.

The scalar optimizer and restricted local theorem are credited inputs.
[PROOF.md](PROOF.md) proves complete section coverage, filtered-Gram
nonsingularity in the interior, the grouped strict/local argument,
collision extension and equality.
[LITERATURE.md](LITERATURE.md) records precise dependencies and context.

From this directory run sequentially with CPython 3.11.2 standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
```

Each must report `status: PASS`, **16,922 checks**, **15,849 exact signs**,
**60 scalar tables**, **three strict domination tables**, **ten full
defining-matrix controls**, and canonical regenerated-record SHA256

    d0536b760c4738cd99f7fa2d256d0b5eddc4e5140350bc0716b901ce1b7a4636

Every degree-22 target coefficient and every scalar Bernstein entry is
regenerated; all complete affine inverse conversions and first-order
degree elevations are checked. No traversal file, private computation,
network input, solver or floating-point proof input is used.

Normal/optimized author replays passed in 23.066/23.035 seconds. Across
sequential validation the maximum child RSS was 39,384 KiB. Four absent
or altered manifests (scalar sign hash, local cutoff and a defining Psi
control) were rejected under optimization. Runtime varies with host load;
one CPU mathematical job at a time and the unchanged two-GiB scope suffice.

`expected.json` is mandatory and compared in full. `--manifest PATH`
checks an alternative manifest. `--write-manifest PATH` is explicit
author generation, not verification. Exact Python/implementation and
the ordinary written bridges are the trust boundary, together with the
credited scalar/local results; this is not formal verification.
