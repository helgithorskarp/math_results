# A five-variable quadratic pencil for real angular stationary octics

Actual **six-sendov-2**, researcher. Complete ordinary reduction with
exact polynomial certificates; unformalized and independently unreviewed.

The degree-five system of [Lemma9496](../mass-stationary-chart/PROOF.md)
now admits five further coefficient eliminations with proved nonzero
pivots. With N1, r=p3/p5, s=p4/p5 and t=p5>0, only B,E,r,s,t remain.
The full stationary residuals are five quadratics in t. Their matrix
rank and projective-conic conditions handle every scalar branch, while
critical-root reality and positive masses preserve original feasibility.

A small mod13 Bezout certificate also excludes B=s=0: no eight-distinct
stationary profile can simultaneously have zero third original moment
and zero quartic mass coefficient. Neither individual zero is excluded.

Read the [full proof](PROOF.md), [prior work and scope](LITERATURE.md),
[standalone source](verify.py) and [whole expected record](expected.json).
From the repository root, Python3.10+ standard library only:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/degree-five-triangular/verify.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O round-two/six-sendov-2/degree-five-triangular/verify.py

Add --export /tmp/sendov-pencil.json to generate the entire rational
matrix and reconstructed h,p,C for further exact work. The export is
computed from source, not taken from the fixture or a CAS cache.
The five residual term counts are 43/54/71/29/44;32 universal identities,
all degree and localization bounds,15 exact rank/conic controls, both
entire unit certificates and9 mathematical damage rejections are checked.
The complete fixture must agree, including missing and extra fields.

This supplies an exact four-parameter rank/conic frontier with lower-rank
cases retained. It does not classify all solutions, include original
collisions in the stationary domain, determine the global angular maximum,
or prove the complex first-power endpoint. Independent review of other
campaign inputs is not a review of this new result.
