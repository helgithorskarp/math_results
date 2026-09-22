# Symmetric Firey Rogers–Shephard inequality

This directory supplies an analytic proof of the sharp symmetric-body
inequality in every dimension, together with all equality cases. It proves
Conjecture 4 of Fradelizi–Manui–Meyer–Ndiaye, arXiv:2607.03582v1, within the
stated classical convex-geometric trust boundary. **Independent review and
formalization are pending.** Publication alone is not verification.

For every full-dimensional centrally symmetric convex body K containing
zero, every d>=2, and every finite p>1, with q=p/(p-1),

    |K+_p(-K)| <= [sum_(i=0)^d binom(d,i)/binom(d/q,i/q)] |K|.

Here the center of symmetry need not be zero. Write K=C+x with C=-C.
Equality holds exactly when

    C polar = conv(F union (-F)),
    F = (C polar) intersect {u : x.u=1}.

Equivalently, almost every supporting hyperplane for surface area measure
contains x or -x. For a polytope, every facet must contain one of these
points. The description includes parallelotopes, crosspolytopes, and
nonpolytopal double cones. In dimension two it reduces to parallelograms
with zero as a vertex, the previously established planar equality theorem.

The proof uses an exact integral formula for the translated Firey volume.
A rank-one support-curvature identity reduces it to an even scalar kernel
with strictly positive second derivative. Its endpoint value is the sharp
gamma-binomial constant; its endpoint support gives the equality class.
All nonsmooth and boundary-origin cases are included by explicit limits.

Read [PROOF.md](PROOF.md) for the complete argument and
[SOURCES.md](SOURCES.md) for attribution and the literature boundary.
No general nonsymmetric inequality, stability theorem, or separate
asymmetric L_p-zonoid conjecture is claimed.

## Reproduce the finite checks

CPython 3.11.2 was used. Python 3.11+ and its standard library suffice;
there are no packages, downloads, private inputs, solvers, or large outputs.
Run from this directory:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Both Python runs must equal [EXPECTED.json](EXPECTED.json) and report
`VERIFIED`, with record digest

    54f36d57f8fc71d28b7d3602c0c47dc1767b734fa32ee7d08fb7824152d79bfe

The checker uses exact rational arithmetic, with Q+Q*pi for constants. It
checks 192 actual Firey curvature evaluations at integer p=2,...,9,
24 full-matrix rank-one determinants, 33 polynomial cofactor divergence
identities, 54 directly integrated spherical volumes for polynomial test
kernels, 18 kernel derivative identities, 5,460 beta/gamma coefficients,
39 exact p=2 constants, 15 equality fixtures, and 21 strict placements.
Five deliberately corrupted formulas are rejected. No `assert` statement
is needed for verification, so optimization cannot disable the checks.

These finite checks detect normalization, sign, determinant-exponent, and
endpoint errors. They do not prove the theorem for every real p, every
dimension, or every convex body. Those assertions follow from the analytic
proof, which uses classical support-volume and mixed-volume formulas,
Cheng–Yau cofactor divergence, and Hausdorff/area-measure continuity.

## Provenance

Researcher 6, graph-first campaign, 2026-09-22. The target was selected from
the solved planar Firey equality neighborhood and the all-dimensional p=2
translation transform. The finite inverse problem was already complete;
the present result addresses a separately stated full inequality.

The primary paper's latest version found on this date was v1. It proves
the zonoid/planar cases and states the general symmetric case as Conjecture
4. A bounded live primary-source search found no later proof of that full
claim. This is a search-relative novelty assessment, not a guarantee of
historical priority. Existing planar work is credited in SOURCES.md.
