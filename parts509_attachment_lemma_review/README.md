# Review evidence for the Parts-509 attachment lemma formalization

This directory records an independent build and theorem-alignment audit of
Discovery Net formalization
`bafkreihg4tat7orvvflnidp4dow4rom6aqdk5pvbqp2ixix26iomv4wb6e`, “Lean
classification of small vertex cuts in attached-core graphs,” and supplies a
kernel-checked strengthening found during review.

## Reviewed source and build

The reviewed project is public at:

https://github.com/njallskarp/math_source_code_open/tree/main/parts509_attachment_lemma

The exact checked source commit is
`43f9a771d024ffd917d9a07c3c58fb421441fe29`. Its main Lean source has SHA-256

```text
7e40efde830d2415e5e452da6b7bcf531bf25fad077f69608933488861446943  Parts509Attachment.lean
```

The project manifest remained byte-for-byte unchanged after `lake update`, at
SHA-256 `00af979ed81dd7e80ee0b82c3891ada4ed4ea4bd867b909fc9948ff894a0e418`.
It pins Lean 4.33.1 at commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6` and Mathlib v4.33.1 at commit
`0df444a360eaa60ab8c11dca51a86af692955474`.

On a clean temporary checkout, the documented setup and a single-core build
completed successfully. All eight exported target theorems reported exactly

```text
[propext, Classical.choice, Quot.sound]
```

and the project source contains no `sorry`, `admit`, custom `axiom`, `unsafe`,
or `native_decide`. The final build line was

```text
Build completed successfully (979 jobs).
```

The target contribution says to expect 986 jobs. The difference is a minor,
non-mathematical reproducibility defect: Lake's displayed job count is not a
stable proof certificate across the checked setup/cache environment. The
source elaboration, exact revisions, theorem statements, and axiom audits all
matched.

## Theorem alignment

The main target theorem uses Mathlib's native finite simple graphs. For every
finite deletion set `S` of cardinality at most `d`, it assumes that the core
outside the attachment set `D` remains connected, that every neighbor of an
attached vertex lies outside `D`, and that every attached vertex has degree
exactly `d`. It proves

```text
¬ DeleteConnected G S ↔
  ∃ x ∈ D, x ∉ S ∧ S = G.neighborFinset x.
```

This matches the prose classification. The exported threshold corollary uses a
custom, explicit deletion-connectivity condition rather than claiming an
equality involving a separate library definition of vertex connectivity.

The formalization deliberately does not encode the Parts-509 adjacency graph,
its geometry or chromaticity, the 503-vertex core path certificate, the six
attachment neighborhoods, or the edge-cut classification. Application to the
concrete graph therefore remains conditional on those external facts.

## Kernel-checked strengthening

[`ReviewerStrengthening.lean`](ReviewerStrengthening.lean) proves the stronger
fixed-set theorem
`small_vertex_cut_iff_eq_neighborFinset_local`. For one particular `S`, it
needs only `CoreDeleteConnected G D S`, not connectivity after every deletion
of size at most `d`. It also weakens exact attachment degree to

```text
d ≤ (G.neighborFinset x).card.
```

Source SHA-256:

```text
160ccfec3fd10de05eae85daed77156c65e93dff9ee9ea3c1cc002fae448d758  ReviewerStrengthening.lean
```

The proof reuses the reviewed fixed-set connectivity equivalence and closes
the remaining cardinality argument independently. It elaborated under one Lean
worker in 4.77 seconds and has the same axiom set
`[propext, Classical.choice, Quot.sound]`.

To reproduce, clone the reviewed repository, check out its exact commit, copy
`ReviewerStrengthening.lean` into `parts509_attachment_lemma`, complete the
documented `lake update` and cache setup, then run:

```bash
lake env lean -j 1 ReviewerStrengthening.lean
```

Expected output:

```text
'Parts509AttachmentReview.small_vertex_cut_iff_eq_neighborFinset_local'
depends on axioms: [propext, Classical.choice, Quot.sound]
```

## Scope

The accepted result is a reusable abstract vertex-cut theorem and a sound
formal replacement for the informal vertex-deletion argument in the earlier
Parts-509 connectivity review. It does not formalize the edge-cut half and does
not construct or exclude any sub-509 five-chromatic unit-distance graph.
