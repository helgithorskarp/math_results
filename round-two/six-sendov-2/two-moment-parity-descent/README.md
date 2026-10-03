# Two-moment parity descent

Actual author **six-sendov-2**, researcher. Complete ordinary proof,
unformalized and independently unreviewed.

For eight distinct real original slopes with balance zero, squared norm
one and third/fifth moments zero, [the proof](PROOF.md) gives a uniform
legal angular gradient at every actual constant-term center:

\[
 |g_1|>|\mu_7|/4\quad(\mu_7\ne0).
\]

The exact six-moment parity blocks also give the every-profile penalty
\(C<\bar C(E,G,0)-\mu_7^2/56\) when the seventh moment is nonzero.
The right side is an **unconstrained** algebraic even-center value.
Together with the credited even stationary exclusion, no all-distinct
profile is stationary on the four-dimensional two-moment-zero locus;
every constrained maximum occurs at an original-root collision.
This does not bound the nonsymmetric collision boundary or establish
the global complex degree-nine first-power Tang--Zhang inequality.

Python3.10+ standard-library reproduction from the repository root:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/two-moment-parity-descent/verify.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O round-two/six-sendov-2/two-moment-parity-descent/verify.py

The whole record SHA256 is
`920e601e7fd92b7aceca107ced82afcdaed014deccddefdaaca2bf98b014cfac`. All complete
polynomial records, 16 moving-node derivatives at four exact controls,
original/critical real-root counts and nine rejected semantic damages
are rebuilt and compared with [expected.json](expected.json).
Only three controls have actual real original roots at the center;
the fourth preserves the exact four-real-root feasibility obstruction.
Run `verify.py --record` to print the entire recomputed record, or
`verify.py --fixture PATH` to verify a separate complete fixture.

Optional [compare_cas.py](compare_cas.py) uses SymPy1.14 to independently
derive all polynomial trace, moment and derivative maps. It is a
same-author arithmetic comparison, not independent review or a dependency
of the standard-library reproduction. The ordinary positivity, calculus,
hyperbolicity, local-root chart and credited input proofs remain explicit
trust boundaries. See [LITERATURE.md](LITERATURE.md) for scope and exact
prior-art provenance.
