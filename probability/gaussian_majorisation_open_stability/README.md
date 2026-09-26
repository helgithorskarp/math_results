# Fixed-variance all-order stability for Gaussian majorisation

The [finite-certificate interface](CERTIFICATE_INTERFACE.md) supplies a
precise input contract for the finite-atomic lane: normalized moment
intervals, a source peak bound from absolute moments, signed threshold
endpoints, and bounded-law transport budgets. Its optional local beta
error is O(N^(-1/2)) on a fixed positive threshold interval. It also records
the exact equivalence between the full conjecture and certificate existence
for every strict finite rational instance, using the existing reductions.
No practical universal degree or new positive geometric class is claimed.
The [exact arithmetic consumer](certificate_arithmetic.py) and
[conformance record](INTERFACE_EXPECTED.json) keep external analytic evidence
separate from arithmetic checks; no unknown Gaussian pair is certified.

The [functional-inequality handoff](HANDOFF.md) consolidates the existing
stability and finite-certificate results, with their exact quantifiers and
their place among the full-question reductions, geometric classes and
restricted examples. [HANDOFF_SOURCES.json](HANDOFF_SOURCES.json) pins its
source revisions and graph references. This is a summary, not an extension.

The [bounded-law proof](BOUNDED_LAWS.md) gives a common stability theorem
for arbitrary bounded probability measures, including nonatomic base laws.
Its three strict conditions characterize the interior of the Gaussian
majorisation set in the product W_infinity topology: a source mean-support
gap, a target peak gap, and strict hinges below the target peak. Every
known comparison with nonpoint target enters this interior after any
strict target homothety. The full comparison set is the closure of its
interior, also at each fixed variance.

It also gives a **finite sufficient certificate for every hinge at one
fixed variance**: signed low-threshold control, a source peak bound, and
finitely many beta moments above an explicit localization error. Such a
certificate exists for every interior pair. A practical degree is not
computed; nonnegativity of a finite moment list alone is insufficient.
The [original proof](PROOF.md) supplies the tail estimate and an undamped
strictness certificate for the asymmetric square-cone family. Independent
review and formalization are pending. The unrestricted R3 problem remains open.

For **every compact variance interval** I inside (0,infinity), there exists
epsilon_I>0 such that every atom of the asymmetric nine-point pair can be
replaced by an **arbitrary probability cloud** within epsilon_I of its
original position. The two endpoint clouds can be chosen independently.
Every Gaussian hinge still compares for all s in I, uniformly over the
entire original L1 weight ball of radius1/4000. The class includes actual
nonlinear contraction pairs with solid three-dimensional support.

This also proves positivity of every beta test and positive definiteness
of every finite endpoint Hankel matrix at each fixed variance in I. The
variance range does not grow with the matrix size. The spatial radius is
proved to exist; an optimized numerical value is not computed, and a
uniform radius over all positive variances is not claimed.

The general bridge now applies to arbitrary bounded base laws. A finite
support net supplies positive assigned cluster masses even for continuous
laws; the net is fixed before taking a low-threshold limit. This links
whole bounded-law members of the motion, common-target, scalar-defect and
density-orbit mechanisms. The square-cone example needs **no damping**
for its strictness certificate.

## Relation to Team B's global criterion

| Result already available | What this packet adds |
|---|---|
| [Global coupling and moment criterion](../gaussian_majorisation_global_criterion/PROOF.md) | Exact zero-defect interior is characterized; signed endpoint controls turn finitely many strict beta tests into an all-order certificate at fixed variance. |
| [Square-cone orbit theorem](../gaussian_majorisation_square_cone_orbits/PROOF.md) | Strict orbit maxima, strict hinges, and arbitrary small spatial clouds on compact variance intervals. |
| [Paired-layer all-variance completion](../gaussian_paired_layers_majorisation/ALL_VARIANCES.md) | This teammate source has already used the original stability theorem to join its two variance endpoints. Its constrained all-variance neighborhood is distinct from the arbitrary bounded-law neighborhoods here. |
| [Axial-cone scope](../gaussian_axial_cone_rotations/SCOPE.md) and other geometric classes | Arbitrary bounded-law members enter the common local stability theorem after strict target homothety. The radius depends on the chosen law and variance band; the domain-wide geometric and volume quantifiers stay with their sources. |
| Reviewed covariance obstruction | It persists in sufficiently small clouds, so the new positive examples still need a different density-level mechanism. |

The low-threshold step has a signed geometric margin and a fixed positive
cluster-mass floor. It does not use the false uniform vanishing-deficit
normalized tail-error bound. No new Kneser--Poulsen consequence is claimed.

## Reproduction

CPython>=3.11, standard library only, from this directory:

```bash
python3 verify.py --check
python3 -O verify.py --check
sha256sum -c SHA256SUMS
```

Expected output, matching normal/optimized CPython3.11.2 and CPython3.12.14:

```text
STRICT_ORBIT_AND_STABILITY_INPUTS_PASS 21fe6f1848494e490d45fff26a015f9c36084d6bf681c74b149a7db610c64b47
```

[verify.py](verify.py) checks the [48 target assignments](STRICT_TARGETS.json),
7,094 nonzero coefficient forms, all144 strict chamber-axis obligations,
and the exact weight, gradient and geometric input bounds. It compares
every coefficient from binomial expansion against repeated polynomial
multiplication and rejects an invalid assignment. No earlier code or order
matrix is imported. [EXPECTED.json](EXPECTED.json) is the audit record.

The preceding all-hinge theorem is a separate essential dependency. To
replay its two finite algorithms as well:

```bash
python3 ../gaussian_majorisation_square_cone_orbits/verify.py --check
python3 ../gaussian_majorisation_square_cone_orbits/independent_check.py --check
```

The finite certificate proves strict maximum domination; it does not
replace the previous orbitwise hinge certificate. The volume bounds,
posterior-covariance flow identity, continuity and compactness arguments
are analytic proofs. The bounded-law extension, exact interior, and finite
beta certification theorem are also analytic proofs; this unchanged checker
does not validate them by finite sampling. It is supplementary exact evidence, not
independent peer review or proof-assistant formalization. Source provenance
and the class relationships are recorded in [SOURCES.md](SOURCES.md).
