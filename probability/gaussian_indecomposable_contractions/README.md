# Indecomposable finite contractions as a full-question test class

The new [strong-chain closure theorem](STRONG_CLOSURE.md) shows that on a
finite distance interval, approximation by finite strong-contraction chains
implies an exact such chain. The existing seven-site positive control
therefore has a neighborhood excluding all these factorizations, even with
changing frames, unbounded factor counts and auxiliary labels. Strict
rational inputs in the shared finite frontier inherit the exclusion.
This is a **complete author proof pending independent review**, with no
new Gaussian sign, cap family, or computed neighborhood radius.

The [primary-literature comparison](CAP_PRIOR_ART.md) separates this stable
obstruction from established Gaussian and ball-volume transfer theorems.
It clarifies the accepted cap theorem's extension beyond strong chains,
without claiming exhaustive historical priority. The former orthocentric
templates and depth-one family remain closed at their reviewed scope.

Run only the new compact exact controls with:

```sh
python3 -B probability/gaussian_indecomposable_contractions/strong_closure_control.py --check
python3 -B -O probability/gaussian_indecomposable_contractions/strong_closure_control.py --check
```

Expected status: `FINITE_INTERVAL_STRONG_CLOSURE_CONTROLS_PASS`.
[STRONG_CLOSURE_EXPECTED.json](STRONG_CLOSURE_EXPECTED.json) records the old
fixture's two-state interval, exact determinants and three damaged-input
rejections. The compactness and all-frame arguments remain written proofs.

The [effective supplement](EFFECTIVE_BOUND.md) now bounds the auxiliary
mesh by an explicit `M_N=O(N^4 16^N)` tetrahedra for N prescribed atoms.
It gives at most `4M_N` labels and a surviving indecomposable gap greater
than `delta*2^(-M_N)`, with positive masses bounded below explicitly.
Rational input data give rational mesh and intermediate coordinates.
The [consumer handoff](EFFECTIVE_HANDOFF.md) composes this with R3's
accepted paired-cubature localization. The supplement now has an
[accepting independent review](../gaussian_effective_indecomposable_review2/REVIEW.md)
at its original source commit de9a0bb7af7179ea6e1b2c5b4013f84d6955f981.
**It supplies no Gaussian sign.** The original is committed at graph height
6260, with the accepting review at 6273. [GRAPH_STATUS.json](GRAPH_STATUS.json)
records the six original relations, subsequent verification/reproduction
edges, and the verified review source commit 57d54289ba7a63d7438bdd1910231adc82cf7596.
Two incorrect commit strings in the review graph body are documented there;
the source verdict and reviewed mathematical bytes are unaffected.

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
status header is preserved with the reviewed bytes. The separate effective
supplement review cited above supplies its own scoped acceptance. Both
original proof files retain their historical review-pending headers unchanged.
The unrestricted Gaussian sign and historical priority remain unresolved.
Classical Brehm extension is an explicit external dependency.

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
