# All-variance Gaussian majorisation near asymmetric paired layers

There is **one positive spatial neighborhood** of the team's asymmetric
nine-point pair in which every admissible paired-layer contraction satisfies
Gaussian majorisation at **every variance and threshold**. The neighborhood
works uniformly for weights in an explicit L1 ball of radius 1/25000.
Its spatial radius is proved to exist; no numerical value is certified.
Read the [all-variance theorem](ALL_VARIANCES.md). Independent review is pending.

This completes both extreme variance regimes around the new spatial-stability
result. A sequence of counterexamples in this constrained class cannot approach
the reference geometry by letting its variance tend to zero or infinity.
The full R3 conjecture remains open, and no new Kneser--Poulsen case is claimed.

The admissible geometries are X=(0,A,-B) -> Y=(0,A,B), where A,B lie in
z=1, are centrally symmetric in the two transverse coordinates, and satisfy
a dot b >= 0. The reference clouds are

```text
A0=((1,0,1),(0,1,1),(-1,0,1),(0,-1,1)),
B0=((1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1)),
p=(8,12,7,15,44,21,11,23,43)/184.
```

For every sufficiently small labelled perturbation within this geometric
class, every probability w with ||w-p||_1 <= 1/25000 satisfies

```text
integral (mu*gamma_s-h)_+ <= integral (T#mu*gamma_s-h)_+
                       for every h >= 0 and every s > 0.
```

The class includes a nontrivial interval of undamped sheared nonsimplicial
dual cones, with asymmetric weights, beyond the original centered fixed rays.
This is a constrained geometric neighborhood, not a claim for arbitrary
nonatomic perturbations at every variance.

The new self-contained [small-variance proof](PROOF.md) is quantitative and
broader: it covers all thresholds for 0 < s <= 10^-10 under explicit norm,
weight and anchor-distance bounds on arbitrary finite paired layers. These
include the entire shear interval |e| <= 1/1000. It combines a uniform
union-volume gap with a coarea estimate controlling every possible negative
origin contribution and a larger positive overlap near a heavy anchor.

[ALL_VARIANCES.md](ALL_VARIANCES.md) then proves robustness of the credited
spherical gap, giving every hinge at s >= 45056 for labelled perturbations
at most 1/16384. Researcher 8's new compact-interval spatial-stability theorem
covers the interval [10^-10,45056]. The minimum of these three spatial radii
is positive and works for all variances. It is not valid to advertise the
explicit endpoint radii as the uncomputed full-variance radius.

## Reproduction

The new supplementary checker uses CPython>=3.11, standard library only.
From this directory:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Expected checker output:

```text
PAIRED_LAYERS_MAJORISATION_EXACT_AUDIT_PASS
certificate_sha256=96ce60d4a395811f0ffd7bcdb64518e70d987726035adcc36bf7c5390ade0650
```

The finite checks audit the continuum proof's rational budgets and all
polynomial shear identities; they do not replace the written analytic
arguments. EXPECTED.json is the compact deterministic audit record.

The all-variance completion additionally uses the team's existing exact
orbit and strictness certificates and validated spherical certificate.
Reproduce those essential finite inputs without duplicating their source:

```sh
python3 ../gaussian_majorisation_square_cone_orbits/verify.py --check
python3 ../gaussian_majorisation_square_cone_orbits/independent_check.py --check
python3 ../gaussian_majorisation_open_stability/verify.py --check
python3 ../gaussian_asymmetric_eventual_majorisation/verify.py
```

The last command requires python-flint/Arb as documented in that packet.
Our replay used CPython 3.12.14 and python-flint 0.9.0; the original validated
packet documents python-flint 0.8.0. [VALIDATION.md](VALIDATION.md) records
outputs and the exact trust boundary. [SOURCES.md](SOURCES.md) credits each
essential theorem and the prior construction. No exploratory data, hidden
certificate, solver, or proof assistant is required.
