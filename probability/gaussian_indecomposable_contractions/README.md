# Indecomposable finite contractions as a full-question test class

The new [coordinate-height theorem](COORDINATE_HEIGHT.md) bounds every
rational root-aligned placement by an explicit numerator/denominator height
`H=O(N^7 2^(17N)(B+4))` for N rational input pairs of height B. This fills
the arithmetic gap left by the earlier effective construction. Clearing
affine-matrix denominators before multiplying reflection words keeps their
height growth linear in the word length.

The [finite-input handoff](COORDINATE_HANDOFF.md) combines this with the
rational paired-cubature producer and linear chain-height bound. For every
fixed hypothetical defect it supplies an indecomposable witness with fully
specified coordinate, label, weight, radius and adverse-gap bounds. The
exposed-edge theorem then supplies uniform signed outer threshold intervals
for this finite class. The middle sign is still open. This is a **complete
author proof pending independent review**, with no practical enumeration,
new positive class or Kneser--Poulsen conclusion.

Run its compact exact controls with standard-library Python 3.11 or later:

```sh
python3 -B probability/gaussian_indecomposable_contractions/coordinate_height.py --check
python3 -B -O probability/gaussian_indecomposable_contractions/coordinate_height.py --check
```

Expected status: `RATIONAL_COORDINATE_HEIGHT_CONTROLS_PASS`.
[COORDINATE_EXPECTED.json](COORDINATE_EXPECTED.json) records plane-repair,
barycentre, reflection-product, mass-denominator and endpoint-budget checks.
[COORDINATE_SOURCES.md](COORDINATE_SOURCES.md) credits the geometric and
analytic inputs. Earlier reviewed source files are preserved unchanged.

The new [linear-height theorem](LINEAR_HEIGHT.md) replaces the previous
exponential chain-length bound by `v-4` for a common tetrahedral framework
with v vertices. Selected opposite-vertex distances are binary and can
decrease only once; they determine every placement after fixing a root.
For an N-atom input with negative hinge gap delta, this improves the
guaranteed indecomposable gap from `delta*2^(-M_N)` to
`delta/[2(M_N-1)]`. The label bound improves to `M_N+3`.

The [new handoff](LINEAR_HANDOFF.md) carries this into the accepted
paired-cubature frontier and distinguishes absolute-error requirements
from working precision and runtime. This is a **complete author proof
pending independent review**. It gives effective complexity information,
not a Gaussian sign or a new positive map family. Previously reviewed
proof and evidence files remain unchanged.

Run the new compact controls with standard-library Python 3.11 or later:

```sh
python3 -B probability/gaussian_indecomposable_contractions/linear_height.py --check
python3 -B -O probability/gaussian_indecomposable_contractions/linear_height.py --check
python3 -B probability/gaussian_indecomposable_contractions/linear_height.py --budget 7
```

Expected status: `LINEAR_CHAIN_HEIGHT_CONTROLS_PASS`.
[LINEAR_HEIGHT_EXPECTED.json](LINEAR_HEIGHT_EXPECTED.json) records complete
small distance intervals, cycle and collision handling, a failed converse,
four damaged-input rejections, and exact loss/precision budgets. The controls
do not integrate Gaussians, construct the enormous bounded mesh, or prove
the universal theorem by enumeration.

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
