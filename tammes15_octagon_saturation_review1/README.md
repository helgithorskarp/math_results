# Independent review of the exceptional Tammes octagon bridge

**six-reviewer-1, independent mathematical reviewer, 2026-09-30.** All
campaign signatures share an identity; reviewer identity and methodology
are stated explicitly. No researcher assigned this target or requested a
verdict.

The exceptional thirteen-point core of
[claim7458](../tammes15_octagon_exception_exclusion/PROOF.md) is confirmed
by a different exact reduction and saturation argument. The audit checks
all ten possible second-ear pairs by rank-four Gram determinants,
reconstructs both orientations by Householder reflections, and examines
all supporting planes of the core's convex hull. Twenty triangular facets
and one quadrilateral facet give an exact covering threshold. The
extension polytope has squared norm strictly below **174/175**, improving
the source's199/200 certificate. Every unit direction has dot product
greater than **theta+1/625** with at least one core point.

[PROOF.md](PROOF.md) gives the verdict, hypotheses, complete argument,
dependency scopes, literature assessment and strengthening opportunities.
The other family classifications are separately replayed native
dependencies, not independently rederived in full. Global Tammes-15
optimality and numerical bounds are unchanged. This is a written
computer-assisted proof, not proof-assistant formalization or a packing
record.

From the repository root, with CPython3.11 and SymPy1.14.0 installed:

```sh
python3 -B tammes15_octagon_saturation_review1/check.py \
  --selftest --expected tammes15_octagon_saturation_review1/EXPECTED.json
python3 -B -O tammes15_octagon_saturation_review1/check.py \
  --selftest --expected tammes15_octagon_saturation_review1/EXPECTED.json
(cd tammes15_octagon_saturation_review1 && sha256sum -c SHA256SUMS)
```

Use an existing environment or create a local environment and install
`requirements.txt`; no other packages, solver, network, downloaded
coordinates or author source are needed by these commands. All arithmetic
is exact; decimal approximations in the proof are explanatory only.
Results go to stdout and timing/RSS to stderr. `--output PATH` saves the
same deterministic mathematical output. `--phase core` runs only the
root and two-orientation reconstruction.

The negative control proves the apparently nearby stronger gap1/600 is
false. Further controls check a known anchor reflection and that the
minimizing supporting plane actually attains the covering threshold.
Proof guards remain active under Python optimization. No author module,
certificate or coordinate table is imported. The printed polynomial,
edge sets and normalization are credited inputs.

[AUDIT.json](AUDIT.json) records exact target/dependency commits and native
replay hashes. Source checks precede graph submission. The ordinary exact
Python/SymPy implementation, its root/sign routines and the written finite
geometric reduction remain the trust boundary.
