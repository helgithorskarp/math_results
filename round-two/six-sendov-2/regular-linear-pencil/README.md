# Regular linear and Gram stationary reduction

Actual **six-sendov-2**, role **researcher**. Complete ordinary author
lemma, unformalized and independently unreviewed.

The9550 matrix has a POLYNOMIAL unit for its constant column. This
reduces five quadratics in positive t to one normalized quadratic and
five linear equations, with no chosen row or generic divisor. A real
Gram test gives two polynomial-circuit equalities, two strict inequalities
and the unique t for rank two. Every remaining rank-one root branch is
retained. The entire s=0 matrix slice has rank at least two even over
complex coefficients, by two tiny univariate unit certificates. This
does not exclude p4=0 stationary profiles or classify s!=0 rank one.

Read [the complete proof](PROOF.md), [input/literature scopes](LITERATURE.md),
[exact source](verify.py) and [whole typed fixture](expected.json).

From the repository root:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/regular-linear-pencil/verify.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O round-two/six-sendov-2/regular-linear-pencil/verify.py

Python3.10+ standard library only. Both runs regenerate and compare
the entire typed record:23 new universal identities,15 synthetic Gram
controls,9 mathematical damages and2 rational/finite-field slice units.
They also regenerate the complete32-identity9550 input fixture and
verify its exact source pins. This is same-author reuse, not independent
review. Relative input directory degree-five-triangular must be present
from this repository; the full publication includes it unchanged.

Optional complete coefficient/circuit export:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/regular-linear-pencil/verify.py --export /tmp/sendov-linear.json

The export is computed from source, not an external certificate input.
S=sum a_i²,T=sum a_i*b_i,U=sum b_i² are complete polynomial circuits.
Large expanded Gram polynomials are unnecessary. Preserve the REAL
parameter domain in the sum-of-squares criterion and retain the
seven SIMPLE REAL criticals/STRICT positive masses before claiming
original-root feasibility. No global first-power solution is asserted.
