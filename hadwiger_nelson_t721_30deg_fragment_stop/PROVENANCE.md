# Provenance and selection boundary

- Primary coordinate input: Marijn Heule's `CNP-SAT/vtx/T721.vtx` at upstream
  commit `bb414955a6ef5f49f7df2b245b1e778aa67c068a`.
- Input SHA-256: `a63fa371d7cf42faa8a3b26d56df81b0c25c1f149d6791dd25c7c356abe1b7c6`.
- Exact parser and multiquadratic arithmetic: reused from the public,
  independently reviewed `hadwiger_nelson_t721_weighted_cover` package.
- Fragment semantics: the earlier positive-cover label set plus a deterministic
  16-label exact-incidence enrichment; no non-four premise is imported.
- Frozen physical placement: rotations by 15 and 45 degrees around source
  label 2, the origin.

The relative 30-degree placement was frozen after a finite geometric contact
preflight and before the first chromatic query.  The first ordinary
four-colour query returned SAT.  Its word is preserved and checked directly.
The 26-vertex nonthree witness was subsequently minimized only to strengthen
the exact description of the already failed support; the published verifier
does not trust the minimization solver.

The package contains no credentials, private ledger data, solver dumps,
checkpoints, or generated binary artifacts.
