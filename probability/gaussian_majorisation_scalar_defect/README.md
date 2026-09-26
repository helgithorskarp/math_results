# Gaussian majorisation from a scalar transport defect

Author proof, 26 September 2026; independent review pending.

This is a compact sufficient criterion for the dimension-three problem in
[Aishwarya--Li](https://arxiv.org/html/2609.07041v2). It gives every Gaussian
hinge inequality at every variance, and both arbitrary-radii
Kneser--Poulsen volume inequalities, for the class below.

For a map $T:K\to\mathbb R^3$, suppose there are unit vectors $e,f$ such that
for every $x,x'\in K$,

$$
 |T(x)-T(x')|^2+
 |e\cdot(x-x')-f\cdot(T(x)-T(x'))|^2\le |x-x'|^2.                 \tag{1}
$$

The extra squared scalar difference is the cost of sharing one coordinate
in a five-dimensional Gaussian interpolation. Bounding that cost by the
available squared-distance loss makes all pair distances decrease.
The established five-dimensional coupling and ball-volume transfer
theorems then supply the endpoint conclusions.

A useful consequence: if $F$ is a contraction preserving one linear
coordinate, $0\le q\le1$, and $T=qF+E$, it is enough that

$$
 \operatorname{Lip}(E)\le\epsilon,\qquad
 \epsilon^2+\epsilon\le q(1-q).                                \tag{2}
$$

Thus exact coordinate preservation can be replaced by a quantitatively
bounded perturbation after contraction. The proof includes a piecewise
linear example with paired affine rank six and no strong-contraction
coordinate system, even allowing separate orthogonal coordinates at the
two endpoints.

The contribution is the explicit criterion, perturbation estimate, and
checked example. The general lifting and Gaussian cancellation principles
are prior results. This is a class-building dependency for the geometric
lane, not a resolution of the general conjecture. In particular, (1)
cannot cover the team's unresolved norm-preserving square-cone reflection.
No new volume theorem outside the established five-dimensional-motion
framework, or historical priority over every possible motion
construction, is claimed.

- [Proof and limitations](PROOF.md)
- [Primary literature and team dependencies](SOURCES.md)
- [Exact rational audit](verify.py)
- [Expected audit output](EXPECTED.json)

From the repository root, with CPython 3.11 or later and no packages:

    python3 probability/gaussian_majorisation_scalar_defect/verify.py --check
    python3 -O probability/gaussian_majorisation_scalar_defect/verify.py --check

The checker validates finite identities and a rational seven-point fixture;
it does not evaluate Gaussian integrals or replace the analytic proof.
Both commands print:

    PASS afce6b533fef7d90bd705798f1e1f76714936b81772d47762c672e6be8ace783

File integrity can be checked from this directory with:

    sha256sum -c SHA256SUMS
