# Independent review: flag completions of equivelar tori

This directory records an independent review of the claimed homotopy
trichotomy for the flag completion of a degree-six torus triangulation with
`K4`-free one-skeleton.

**Verdict: accept with high confidence.**  The all-size argument is correct as
stated under its explicit hypotheses.  No substantive gap or counterexample
was found.  The detailed premise audit, limitations, and literature check are
in [`REVIEW.md`](REVIEW.md).

The reviewed source is
[`equivelar_torus_flag_completion`](../equivelar_torus_flag_completion/), at
commit `39f918594d0f6a909b945e9fae814f1077567a9f`.

## Reproduce the independent finite audit

Requirements: Python 3.11 or later; no third-party packages or downloads.

```bash
python3 audit.py
```

The run enumerates every HNF sublattice parameter tuple of index at most 60.
It asserts the submitted five-way aggregate counts, the structural
classification in every `K4`-free case, three-prime homology, six named small
fixtures, and three disk-attachment controls.  Its expected compact output is
recorded in [`expected.json`](expected.json).  A typical run takes about 40
seconds on one CPU in the campaign workspace.

## Independence and trust boundary

`audit.py` does not import the submitted verifier.  It discovers quotient
cosets by Cayley-graph breadth-first search and compares them by literal
lattice-membership tests; the submitted verifier instead uses a closed
quotient reduction formula.  Surface faces and graph cliques are independently
constructed, and boundary ranks are recomputed over three prime fields.

The enumeration is corroboration, not an all-size proof.  It depends on the
human-audited flat-lattice reduction and HNF completeness.  The homotopy types
are established by the written geometric/CW proof, not inferred from matching
Betti numbers.  No claim of exhaustive historical priority is made.
