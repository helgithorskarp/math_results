# The complete four-level angular displacement classification

Actual author **six-sendov-2**, role **researcher**, 2026-09-30.
Complete author proof with exact rational continuous-domain certificates;
independent review pending.

Every balanced max-normalized eight-vector with at most **four distinct
slope values** has J<=J*, with equality exactly at permutations of

    (1,1,1,-1,-1,-1,sqrt(u*),-sqrt(u*)),

where the scalar value and u* are credited to the completed 3+3+1+1
theorem. The new exclusions close the three remaining multiplicity classes:

    3+2+2+1: J<=780,
    4+2+1+1: J<=780,
    5+1+1+1: J<=3328/5.

Together with the credited 2+2+2+2 and 3+3+1+1 results, this settles
all four-part partitions and all their collisions. A global unit-direction
distance bound has constant7/3. No reduction from arbitrary eight-level
profiles is asserted.

For complex degree-nine disk-root polynomials whose other-root phases
have at most four distinct values, inward depths may vary independently.
The sharp leading maximum-original-root displacement basin now has the
credited constant B*=106496/(5J*), with

    27.106707 < B* < 27.106708.

The new result is the complete four-level validity and optimizer
classification, not a new value of this constant. The full first-power
endpoint and unrestricted displacement maximum remain unresolved here.
See [PROOF.md](PROOF.md) and [LITERATURE.md](LITERATURE.md).

From the repository root, CPython3.11.2, standard library only,
run **sequentially**:

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B sendov_degree9_four_level_displacement/verify.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O sendov_degree9_four_level_displacement/verify.py
```

Expected PASS:6180checks,3020 newly computed sign coefficients,
20 complete fan squares,30 closed leaf rectangles and37 full-compression
controls. Complete-record SHA256:
7edc445e802f1b9e7e3bb03b61bb1ef4aecf1916a4f4ef48cfcb9298dccc92bc.

[verify.py](verify.py) is standalone. [cover.json](cover.json) supplies only
closed bisection trees, whose completeness and every sign are checked;
[expected.json](expected.json) is the full compact regression record.
Missing or altered inputs, omitted fans and omitted closed children are
rejected under `-O`. The checker does not formalize the written spectral,
coverage and analytic bridges. No campaign import, solver, external
census or floating proof input is used.
