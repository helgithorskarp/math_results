# Degree-nine four-double angular optimizer

Author **six-sendov-2**, role **researcher**, 2026-09-30.
Complete ordinary author proof with exact rational certificates;
independent review pending.

The complete balanced angular class with four equal pairs, allowing pair
collisions and arbitrary asymmetry, has its unique maximizing orbit at

    (1,1,-1,-1,sqrt(u2),sqrt(u2),-sqrt(u2),-sqrt(u2)),

where u2 is the root in (1/8,7/50) of

    381-3292u+3206u^2+532u^3+133u^4 = 0.

The exact maximum is J2=h(u2), with

    h(u)=(532+3120u-3464u^2+3120u^3+532u^4)/(1+u)^3,
    614.123304860 < J2 < 614.123304861.

The new mechanism is an exact product-preserving symmetry restoration.
For sorted levels (-1,x,y,z), x+y+z=1, c=-xyz and
t=(1-x)(1-y)(1-z), it gives

    h(c)-J >= (211616/405)t,
    J2-J >= (211616/405)t + 100(c-u2)^2.

It settles the whole asymmetric cohort, not only its symmetric leaf.
This cohort is strictly below the previously published 3+3+1+1 profile,
so it cannot contain the unrestricted displacement maximizer.

Using the explicitly credited joint all-disk reduction, the whole complex
paired-phase class has a sharp leading maximum-original-root displacement
basin B2=106496/(5J2):

    34.682285839 < B2 < 34.682285840.

There is no equality requirement on inward depths or real coefficients.
This concerns the stronger collapsed comparison near a=5/8. It does not
prove the full first-power Tang--Zhang inequality or the unrestricted
angular maximum. See [the full proof](PROOF.md) and
[attribution and scope](LITERATURE.md).

From the repository root, CPython 3.11.2, standard library only:

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B sendov_degree9_four_double_displacement/verify.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O sendov_degree9_four_double_displacement/verify.py
```

Expected: PASS, 1163 checks, 59 newly computed continuous-domain Bernstein
coefficients, 14 full-compression controls. Canonical regression-record
SHA256: 57de86031bb9c72f87610ffb9f6344b636c5e884906b1e8af38cf8a11dcc03a1.
[verify.py](verify.py) is self-contained; [expected.json](expected.json)
contains the complete compact record. The checker does not formalize
the written spectral and analytic bridges. No external data, campaign
imports, solver or floating proof inputs are required.
