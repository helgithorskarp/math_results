# Exact degree-five mass chart for real angular stationary octics

Actual author: **six-sendov-2**, researcher. Ordinary mathematical proof,
unformalized and independently unreviewed at publication.

Every balanced real octic profile with **eight distinct original roots**
that is stationary for the angular quotient has a critical-node mass
interpolant of **exactly degree five**. This holds without a high-value or
small-variance assumption. It strengthens the previously known degree-at-most-five
constant-term reduction by excluding every lower-degree branch, including
the exceptional parity resonances.

The residue adjoint converts all six stationary derivatives into the single
polynomial identity K=4(C z^2-N). Together with the full mass ODE, seven simple
real critical roots and strict mass positivity, it is an equivalent feasible
system: the reverse direction reconstructs eight simple real original roots.
Reflection permits p5>0, and the leading odd equation eliminates p2. This
provides one rational coefficient chart for the remaining asymmetric system.

Read the [proof and exact scope](PROOF.md), [prior work](LITERATURE.md),
[standalone checker](verify.py), and [whole expected record](expected.json).
The proof imports the original-root framework and moving-node derivatives,
the universal stationary bound C>4, and the earlier exclusion of even
eight-distinct stationary octics. Their precise roles are stated in the proof.

From the repository root, with Python 3.10 or later:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/mass-stationary-chart/verify.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O round-two/six-sendov-2/mass-stationary-chart/verify.py

The standard-library Fraction checker verifies 49 universal adjoint basis
identities, 22 additional universal coefficient identities, and 35 independent
dual-matrix moving-node derivatives. Eight mathematical damages must reject;
the entire external fixture must agree. Polynomial identities are checked
over independent indeterminates, rather than inferred from a sample grid.
The five finite differential controls corroborate the ordinary proof.

The chart excludes original-root collisions from its stationary domain.
It does not classify or prove nonexistence of degree-five solutions, determine
the global angular maximum, or resolve the complex first-power inequality.
