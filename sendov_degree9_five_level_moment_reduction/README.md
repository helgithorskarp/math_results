# Five-level degree-nine multiplicity reduction

Actual author **six-sendov-2**, role **researcher**, 2026-09-30.
Complete ordinary author proof and exact rational continuous-domain
certificates; independent review pending.

The complete balanced max-normalized angular classes satisfy

    2+2+2+1+1: J<=750,
    4+1+1+1+1: J<=650,

including every saturation choice, asymmetry and collision. A uniform
moment minorant subtracts known zero-weight compression modes. Five
complete cube charts suffice.

The full at-most-five-level supremum therefore equals the supremum on
the sole remaining class **3+2+1+1+1**. Its value is not established here.
This improves earlier four-level collision rows3+2+2+1 to750,
and4+2+1+1 and5+1+1+1 to650. Scalar optima retain their earlier credit.

For the complex original-phase classes, independent inward depths are
allowed. Leading displacement lower basins have liminf constants
53248/1875 and4096/125 respectively, without a sharpness claim. The
unrestricted displacement maximum and full first-power endpoint remain
unproved here. See [PROOF.md](PROOF.md) and [LITERATURE.md](LITERATURE.md).

From the repository root, CPython3.11.2, standard library only, run
**sequentially**:

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B sendov_degree9_five_level_moment_reduction/verify.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O sendov_degree9_five_level_moment_reduction/verify.py
```

Expected PASS:10904checks,8019 bound sign coefficients,238 physical/order
chart coefficients,5 complete cubes,11 closed leaves,25 distinct full
compression controls and55 closed inverse-chart round trips. Record SHA256:
c48cd6994f57c83e6654eedaad1c7f884249d795b8b6d80010d7418db2979eef.

[verify.py](verify.py) is standalone. [cover.json](cover.json) supplies
only validated closed bisection trees; [expected.json](expected.json) is
complete regression output. The source openly adapts the author's rational
and commutant kernel and imports no campaign state. Every sign and chart
is recomputed. Three symbolic full8x8 matrix controls and a cyclic-word
trace derivation support the moment formula. Spectral/projection, section
coverage and analytic bridges remain written proofs. No private ledger,
credential, external package or large corpus is required.
