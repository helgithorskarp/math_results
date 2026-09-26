# Indecomposable finite contractions as a full-question test class

[PROOF.md](PROOF.md) reduces unrestricted dimension-three Gaussian majorisation
to finite contractions fixing a tetrahedron and having only the two endpoint
distance matrices as possible three-dimensional intermediate configurations.
The reduction preserves a hypothetical negative hinge on a covering step;
the same finite geometric factorization reduces both ball-volume questions.

**Status:** complete author proof; independent correctness and priority review
pending. The unrestricted Gaussian sign is not proved, and no counterexample
is claimed. Classical Brehm extension is an explicit external dependency.

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
There is no uniform size bound for the theorem's augmented configurations.
See [SOURCES.md](SOURCES.md) and [SHA256SUMS](SHA256SUMS) for provenance and
the packet manifest. No external dataset or large artifact is required.
