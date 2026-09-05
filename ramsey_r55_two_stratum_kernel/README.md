# A two-stratum completion kernel for proper three-root signatures

This package supplies a **structural graph-realization reduction**, not a
new edit-budget sweep or local descent. Fix three roots and assume every
other vertex has one or two red incidences to them. An edge between two
nonroots is free exactly when their three-bit signatures are complementary.

The visible skeleton has no completely fixed monochromatic K5 **if and
only if** it passes six full root-neighborhood tests, has no red K5 in
the union of the singleton-signature cells, and has no blue K5 in the
union of the pair-signature cells. The two extra tests are individually
necessary in this general signature family. [PROOF.md](PROOF.md) gives
an elementary proof, two minimal-size limitation fixtures, the complete
residual-clause equivalence, and the degree interface.

For the retained cell sizes `(8,8,6,10,4,4)`, this leaves a conditional
completion problem on **124 edges**, in blocks `8x4`, `8x4`, `6x10`.
The two additional induced vertex sets have orders 26 and 14. The
complete residual formula has only widths **1,2,3,4,6**, never 5.
Prescribed degrees factor into three bipartite margin problems; the
Ramsey clauses still couple those blocks. Passing all eight tests does
not establish that the remaining formula is satisfiable.

No 43-vertex graph passing preflight is constructed here. No Ramsey
number bound, full degree-profile exclusion, optimal repair distance,
or historical-priority claim is made. Empty or full signatures are
outside the theorem. The 470 aggregate cases are not all covered
without checking this hypothesis.

## Exact bounded evidence

The finite validation has three distinct scopes:

- **Signature theorem:** 252 five-signature multisets; a separate
  ordered enumeration checks all 7,776 assignments and each canonical
  pattern. The only fully visible supports mixed in every coordinate
  are the singleton triple and the pair triple. There are 12 resulting
  multiplicity patterns, six requiring the red test and six the blue
  test. All 190 truth-table entries for both colors and widths
  `0,1,2,3,4,6` are checked, including the empty-clause case.
- **Small complete graph interface:** a specified 15-vertex fixture is
  constructed from quadratic-residue edges modulo 17 by retaining the
  proper-signature vertices and toggling the first eligible visible
  central edge, `(3,4)`. The original 17-vertex graph's K4-freeness in
  both colors is checked literally; no Paley/Ramsey theorem is imported.
  The new fixture passes all eight preflight tests. Its entire residual
  formula is the one blue-K5 clause `x_3 OR x_11`, with variables numbered
  from zero in [small_kernel.json](small_kernel.json). All **4,096** free
  assignments are compared with actual full-graph five-set checking:
  **3,072** are Ramsey(5,5); exactly **two** also realize its given degrees,
  assignments `408` and `2436`. These are small fixtures, not target graphs.
- **Existing 43-vertex seed:** the byte-pinned
  [353-K5 endpoint](../ramsey_r55_k5_neutral_component/EXIT_GRAPH.json)
  has 124 free and 656 visible central edges. Independent reconstruction
  gives 3,113 residual clause occurrences with width histogram
  `0:144, 1:241, 2:1149, 3:707, 4:456, 6:416`.
  Its 144 immutable K5s include **20 red singleton-stratum and 28 blue
  pair-stratum K5s outside every root neighborhood**. The other 96 lie
  in at least one such neighborhood. The full extra tests have 41 red
  and 39 blue defects, with overlap. All these entries are published in
  [seed_audit.json](seed_audit.json), not merely aggregate counts.
  Preflight fails, so this is not a promising frozen 124-edge instance.

The immutable total 144 was already known. Its decomposition here
illustrates the new two-stratum theorem; it is not counted as a fresh
exclusion or a second discovery of the frozen-seed barrier.

The degree interface supplies exact integral edge witnesses or cuts.
All 81 margin vectors for a 2x2 block are checked against all 16 binary
matrices, and every produced flow/cut certificate is audited directly.
Six further boundary cases include empty blocks, invalid margins, and
a nontrivial 3x3 infeasibility cut. Seventeen corruption/negative controls
pass, along with color complementation of all three small fixtures.

## Source separation and reproduction

CPython **3.11.2 standard library only**. No solver, numerical package,
compiler, graph catalogue, or private runtime state is required.

[kernel.py](kernel.py) is the reusable bitset-based preflight, full
residual compiler and integral margin interface. [generate.py](generate.py)
constructs fixtures and evidence. [verify.py](verify.py) imports neither
of them, nor any inherited checker: it reconstructs the formula with
set-based permissive-color clique enumeration, checks each small actual
graph by literal five-sets, and verifies the flow/cut witnesses directly.
The only external input is the pinned seed JSON in this repository.

From this directory, choose fresh work directories outside Git:

```sh
sha256sum -c SHA256SUMS
python3 -B generate.py --work /scratch/new-r55-two-stratum
python3 -B verify.py --source /scratch/new-r55-two-stratum --report /scratch/new-r55-two-stratum-check.json
python3 -B controls.py --source /scratch/new-r55-two-stratum --report /scratch/new-r55-two-stratum-controls.json
cmp fixtures.json /scratch/new-r55-two-stratum/fixtures.json
cmp small_kernel.json /scratch/new-r55-two-stratum/small_kernel.json
cmp report.json /scratch/new-r55-two-stratum/report.json
cmp margin_certificates.json /scratch/new-r55-two-stratum/margin_certificates.json
cmp seed_audit.json /scratch/new-r55-two-stratum/seed_audit.json
cmp verification.json /scratch/new-r55-two-stratum-check.json
cmp controls_report.json /scratch/new-r55-two-stratum-controls.json
```

Repeat the three commands with `python3 -B -O` and distinct output
paths, then compare every generated JSON and both reports. The normal
and optimized runs agree byte for byte. Observed optimized runtime:
generation 4.723232 seconds, peak 24,556 KiB; complete independent
verification 30.529125 seconds, peak 26,104 KiB. They ran concurrently;
these are reproducibility measurements, not a performance comparison.
The finite work terminates on fixed domains; there are no timeouts,
UNKNOWN outcomes or ongoing processes in this package.

Canonical full 43-vertex residual formula SHA256:
`fab0d57ec341a76d6ab547dd594f6b6197a076414fed089059f117f6cc50dd36`.
It hashes JSON with sorted keys and compact separators. The formula's
full occurrence list is regenerated, not published as bulky state.
The exact small accepted-assignment list has SHA256
`8ae71583f5c25b822a9484fe2166080939e91d581a4681efcecd18c7e7dbf69b`.
The checker compares individual small assignments and kernel entries;
these digests are not substitutes for replay.

## Dependencies, coordination, trust and next boundary

The independent [three-anchor survivor](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_d22_three_anchor_survivor),
Discovery Net `bafkreicfvni3jmncd5mbdbi7jw3gvonlnotc3tkz27wt3jpnykjq3jwyny`
at height 2907, exposed a fully visible central-K5 gap in a different
signature family including a full signature. Its body was inspected,
but its source was not replayed and no claimed exclusion is imported.
The general gap is not rediscovered here. The new specialization is the
exact two-extra-test characterization for the six **proper** signatures,
together with a complete (not width-prefix) completion interface.

The pre-publication refresh through height **2934** found the newly
published [five-cube-orbit classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_three_cube_mixed_orbits),
Discovery Net `bafkreieffob5vhnmz5n4omjv7rrmqhfdbjrdhn3lz4tz3db3jijqyn5u7u`
at height 2931, source commit `8d576378618dc348cf6cc53d0d226f7a70254d7f`.
It classifies all 88 qualifying five-signature multisets in the full cube
and gives the general invariant cut scheme. **It subsumes the support
classification used in this package.** Our in-progress special-case
derivation is retained as explicit independent corroboration on the
proper-six-signature domain, not claimed as a new general classification
or as an independent review of all five cube orbits. The source body
was read; the external full-cube code was not replayed. The contribution
here is the specialization to just two necessary one-color tests after
mixed-K5 prevention, and the fully tested residual/degree completion
interface. The 124-edge conditional scope and its failed seed preflight
remain unchanged. No external classification verdict is a proof input
to the separate elementary proof supplied here.

The previous [creation-sensitive cover](../ramsey_r55_creation_sensitive_cover)
is preserved. Its seed-specific 39-visible-edit lower bound now has an
[external independent acceptance](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_creation_sensitive_cover_independent_review_20260905),
Discovery Net `bafkreighkhxx2y7vfkosheyfii3ojhn3hf7kd46wcckxwpvlpwl2iaclpq`
at height 2927, source commit `508d89a9cba48a78ce0935fc89fbfed35125834c`.
The review's body reports a smaller necessary set of degree/profile
equations. Neither the cover theorem nor that refinement is a proof
input to this package, and no budget-39 test is performed.

At startup, the teammate's new [empty-signature boundary](../ramsey_r55_order3_eleven_empty_signature)
reported seven more full symmetry-case refutations, leaving 38
four-versus-seven core classes plus two three-versus-eight cores open.
Its new claims and preceding 34 refutations await independent review.
That symmetry lane is separate and is not searched here. External
height-2921 c13 footprint-pair evidence was inspected but is not used.

This package's new theorem and computational evidence have internal
algorithmic cross-checks, **not independent peer review or formalization**.
Trust boundaries are the elementary unformalized proof, the displayed
finite-domain coverage arguments, the exact source semantics, CPython,
ordinary hardware and SHA256 for input identity. The universal theorem
comes from the hand proof, not extrapolation from the 15-vertex fixture.

The coherent milestone stops here. The next useful direction is one
bounded construction of a degree-compatible visible skeleton enforcing
all eight tests (and any retained hard-profile equalities), followed by
the **whole** 124-edge formula with its degree margins. No such new
construction, larger search, local descent or extra budget is started.
