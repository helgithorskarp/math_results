# Fixed-variance all-order stability for Gaussian majorisation

The [author proof](PROOF.md) transfers the team's positive comparisons to
spatially perturbed measures, with an exact strictness certificate for the
asymmetric square-cone family. Independent review and formalization are
pending. The unrestricted R3 problem remains open.

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

The general bridge applies to any strict finite atomic Gaussian comparison
with a peak gap and a mean-support gap. Any known finite all-order comparison
at one variance meets these strict conditions after an arbitrarily small
target homothety, provided the target is not a point mass. This links the
motion, common-target, scalar-defect and density-orbit mechanisms. The
square-cone example needs **no damping** for its strictness certificate.

## Relation to Team B's global criterion

| Result already available | What this packet adds |
|---|---|
| [Global coupling and moment criterion](../gaussian_majorisation_global_criterion/PROOF.md) | Exact zero defect persists under the specified spatial perturbations; all finite moment tests are positive. |
| [Square-cone orbit theorem](../gaussian_majorisation_square_cone_orbits/PROOF.md) | Strict orbit maxima, strict hinges, and arbitrary small spatial clouds on compact variance intervals. |
| [Axial-cone scope](../gaussian_axial_cone_rotations/SCOPE.md) and other geometric classes | Finite certified members enter the common local stability theorem after strict target homothety. The original geometric all-law and volume quantifiers stay with their sources. |
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

The new finite certificate proves strict maximum domination; it does not
replace the previous orbitwise hinge certificate. The volume bounds,
posterior-covariance flow identity, continuity and compactness arguments
are analytic proofs. The checker is supplementary exact evidence, not
independent peer review or proof-assistant formalization. Source provenance
and the class relationships are recorded in [SOURCES.md](SOURCES.md).
