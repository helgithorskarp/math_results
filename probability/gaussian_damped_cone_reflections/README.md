# Damped cone reflections and full Gaussian majorisation

This packet proves a uniform geometric criterion for full Gaussian
majorisation at every variance and threshold, and for three-dimensional
union/intersection inequalities for balls with arbitrary individual radii.
The unrestricted dimension-three question remains open.

Let `C_p = {(u,z): z >= 0, |u| <= p z}`. On the two cones define

```text
T_lambda(a) = lambda a,    a in C_p,
T_lambda(-b) = lambda b,   b in C_q,       0 < lambda <= 1.
```

All bounded probability laws on this domain, and all finite labeled ball
families, satisfy the comparisons whenever

```text
p q F(lambda^2) <= 2,
F(eta) = sqrt(1-eta^2) + eta (pi-arccos eta) + eta - 1.
```

The proof constructs a continuous contracting motion in R4. Its transverse
coefficient follows a tangent and circular arc in the complex plane, while
an auxiliary coordinate pays the exact cost of that motion. A calibration
proves that the formula is optimal **within the stated motion form**.
For noncircular sections, Theorem 1 gives the more general product-support
integral criterion. This is a uniform shrink-versus-rotation principle,
not a fixed-configuration asymptotic estimate.

The self-dual cone `C_1` admits the damped comparison with
`lambda=sqrt(2/3)`. More generally every proper dual-cone pair admits a
positive damping range. In contrast, the undamped full-dual map has an R5
motion exactly when the cone is simplicial. The negative direction uses
classical positive-operator geometry and extends the team's square-cone
obstruction; the positive simplicial direction is credited to that prior
team result. This motion obstruction does not disprove majorisation.

A rational 37-point example at `lambda=4/5` has paired rank six and excludes
the scalar-defect certificate even after independent endpoint rotations.
All 666 pairs strictly contract. Its new motion proves the Gaussian and
arbitrary-radius ball comparisons with unrestricted weights and radii.
Removing the damping gives an R5-obstructed dual-polygon reflection.

Read [PROOF.md](PROOF.md) for the full argument and precise quantifiers;
[SOURCES.md](SOURCES.md) identifies primary and team dependencies and the
bounded novelty audit. Independent mathematical review is pending.

## Reproduction

From this directory, with CPython 3.11 or later and no packages:

```sh
python3 verify.py --check
python3 -O verify.py --check
sha256sum -c SHA256SUMS
```

Expected:

```text
DAMPED_CONE_EXACT_AUDITS_PASS 346e454e4dfb6fa4dc6f6b63c04db86435165d51dbf5f23b76aef25f3526af0b
```

Checked with CPython 3.11.2 and 3.12.14. The deterministic
[EXPECTED.json](EXPECTED.json) records ten polynomial identities, exact
dual facets and ranks, all 666 pair distances, rational trigonometric
certificates, and four invalid controls. [verify.py](verify.py) uses only
integers and fractions. It does not infer universal inequalities from
sampling. The analytic argument and the explicitly credited Gaussian and
volume lifting theorems remain the mathematical trust boundary. No solver,
external dataset, large certificate, or proof assistant is involved.
