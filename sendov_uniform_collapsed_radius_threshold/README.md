# Collapsed reciprocal stability, uniformly in the degree

Author: **six-sendov-2**, role **researcher**.

For degree n>=4, m=n-1, a simple marked root a in [0,1], and all roots in
the closed unit disk, center the other-root reciprocals at v=1/(1+a).
Write E=sum|u-v|^2, epsilon=max|u-v|, and
kappa=(1+a)[a-(n+1)/(2(n-1))].

The [proof](PROOF.md) establishes, for epsilon<=1/(4n),

    F(a) >= 2m/(1+a) + (kappa-37mn^3 epsilon)E.

The limiting infimum of the gap/energy ratio is exactly kappa.
Above the cutoff (n+1)/(2(n-1)), the explicit condition
epsilon<=kappa/(80mn^3) gives a positive coefficient kappa/2.
A sufficient original-root cap is max|z+1|<=kappa/(40mn^3).

A single conjugate pair moving on the unit circle proves that the radial
baseline fails arbitrarily near collapse at and below the cutoff, in
both odd and even degrees. Its negative second-order coefficient in
h=1-c is checked symbolically in m. This is an obstruction to the radial
baseline, which exceeds the conjectural first-power endpoint F>=n-1 for
a<1. It does not disprove that endpoint.

The uniform neighborhood is coarser than the author's earlier degree-nine
one; the earlier constants remain useful. The new scope is the uniform
degree theorem, its sharp limiting energy coefficient and the cutoff in
every degree n>=4. See [literature and exact reuse](LITERATURE.md).

## Reproduce the symbolic checks

Python 3.11.2, standard library only. From repository root:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
    python3 sendov_uniform_collapsed_radius_threshold/verify.py

Expected: PASS, 58 exact checks, four rejected coefficient mutations,
symbolic degree parameter m=n-1, no external inputs or floating-point
operations. Checks are identities over rational sparse polynomials and
uniform sign certificates, not a scan through finitely many degrees.
Typical runtime is below one second with one process and one thread.

The contour proof, universal trace contractions, root existence and local
asymptotics are ordinary mathematical arguments in PROOF.md. The checker
validates their algebra; it is not a formalization or independent review.
Independent review is pending. No optimal basin radius or global
first-power theorem is claimed.
