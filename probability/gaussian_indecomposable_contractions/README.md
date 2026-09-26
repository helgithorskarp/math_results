# Indecomposable finite contractions as a full-question test class

The [effective supplement](EFFECTIVE_BOUND.md) now bounds the auxiliary
mesh by an explicit `M_N=O(N^4 16^N)` tetrahedra for N prescribed atoms.
It gives at most `4M_N` labels and a surviving indecomposable gap greater
than `delta*2^(-M_N)`, with positive masses bounded below explicitly.
Rational input data give rational mesh and intermediate coordinates.
The [consumer handoff](EFFECTIVE_HANDOFF.md) composes this with R3's
accepted paired-cubature localization. **The new quantitative supplement
awaits independent review and supplies no Gaussian sign.**

Run the new controls with standard-library Python 3.11 or later:

```sh
python3 -B probability/gaussian_indecomposable_contractions/effective_bound.py --check
python3 -B -O probability/gaussian_indecomposable_contractions/effective_bound.py --check
python3 -B probability/gaussian_indecomposable_contractions/effective_bound.py --budget 7
```

Expected status: `EFFECTIVE_INDECOMPOSABLE_BOUND_CONTROLS_PASS`.
The [compact record](EFFECTIVE_EXPECTED.json) covers the bounded seed,
an asymmetric eight-cone repair, face compatibility, a failed unbuffered
repair, and loss/count arithmetic. It does not construct all meshes.
The exact checks take about one second on the author's host. The enormous
budget is symbolic; no states or powers `2^(M_N)` are enumerated.
See [the supplement sources](EFFECTIVE_SOURCES.md) for attribution and
the distinction from classical constructive Brehm extension.

[PROOF.md](PROOF.md) reduces unrestricted dimension-three Gaussian majorisation
to finite contractions fixing a tetrahedron and having only the two endpoint
distance matrices as possible three-dimensional intermediate configurations.
The reduction preserves a hypothetical negative hinge on a covering step;
the same finite geometric factorization reduces both ball-volume questions.

The original qualitative proof has an
[accepting independent review](../gaussian_indecomposable_contractions_review2/REVIEW.md)
at commit `4518e569424cbac04083e6cb9497cc97991cf301`; its historical pending
status header is preserved with the reviewed bytes. That acceptance does
not extend to the new effective supplement. The unrestricted Gaussian sign
and historical priority remain unresolved. Classical Brehm extension is
an explicit external dependency.

The compact [exact controls](EXPECTED.json) distinguish a decomposable diamond,
the positive seven-site cap example, and the classical nonliftable simplex
flaps. The latter are indecomposable at every positive depth by a direct
argument; exact checks at depths 1 and 2 include colliding and injective
targets. Their construction and no-R5-motion theorem are credited prior work.

Run from the repository root, standard-library Python 3.11 or later:

```sh
python3 probability/gaussian_indecomposable_contractions/verify.py
python3 -O probability/gaussian_indecomposable_contractions/verify.py
```

Expected interval counts are `4,2,2,2`. The checker exhausts 4096 individual
reflection choices for each classical flap depth, with integer distance
arithmetic after clearing denominators. Each accepted state is reconstructed
and checked directly. `--emit` regenerates the small expected JSON record.
CPython 3.11.2 and 3.12.14 were checked; one complete run takes about 0.3 seconds.

The checker verifies the complete intervals of these fixtures, not Brehm
extension, all meshes, the universal analytic reduction, or Gaussian integrals.
The original proof has no size bound for its augmented configurations;
the new supplement supplies one depending on the original atom count.
See [SOURCES.md](SOURCES.md) and [SHA256SUMS](SHA256SUMS) for provenance and
the packet manifest. No external dataset or large artifact is required.
