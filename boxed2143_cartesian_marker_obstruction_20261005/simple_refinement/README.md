# Simple boxed-2143 extensions in one Cartesian-tree pair

For every input permutation pi of length m>=1, padding it by a new minimum
on the left and a new maximum on the right, then applying the band-marker
map, gives a recoverable simple permutation of length3m+4. It preserves the
COMPLETE set of boxed2143 occurrences. Every input of the same length gives
the same minimum/maximum Cartesian-tree pair. Thus s_(3m+4)>=a_m, where s_n
counts simple boxed2143 avoiders and a_n counts all boxed2143 avoiders.

The map does not turn nonavoiding inputs into avoiders. A separate uniform
argument gives exactly M-1 viable next-rank positions among all SIMPLE
avoiding completions after a common low-marker prefix in a common tree
pair, for every M>=2. This excludes constant local branching even for simple
avoiders. Neither claim bounds global fiber weights or settles growth.

Sage authored the exact uniform Claims S1--S3 in
`author/MARKER_SIMPLE_REFINEMENT_DRAFT.md`. Theo, a different existing team
researcher, accepted their ENTIRE stated partial scope. His unchanged
written reconstruction is `review/SAGE_SIMPLE_MARKER_REVIEW.md`. This is
internal checking, not external peer review or novelty certification.
The agreed full question remains: is a_n bounded by C^n for some finite C
and every n>=1? It remains unresolved in this packet.

## Provenance and scope

The earlier marker theorem and its separate checked source are dependencies:
https://github.com/helgithorskarp/math_results/tree/2d02dc425cf66e89a01676bae3f19b076caf28c8/boxed2143_cartesian_marker_obstruction_20261005
This refinement is a separate scope. It does not alter the earlier proof,
review, source bytes or pending graph original.

The primary literature target is Kitaev--Qiu--Xu, Coincidences and Growth of
Boxed Mesh Patterns, arXiv2609.13764v1, Theorem4.4(iii), Section7:
https://arxiv.org/html/2609.13764v1 . The full bounded-exponential question
remains open there. The known generic Cartesian-tree/linear-extension
framework is not claimed as new; see Giraudo1204.4776 and ISAAC2024
DOI10.4230/LIPIcs.ISAAC.2024.17, cited in the dependency proof.

All seven frozen author files and their original manifest are unchanged.
Their historical DRAFT/pending wording records the pre-review snapshot;
the current accepted scope is the separate written Theo review. The author
helper `check_lyra_boundary.py` is included byte-for-byte because its literal
sparse-label occurrence function is used by the author controls. Its other
review routines are not part of these reproduction commands or claims.
Historical reviewer manifests and evidence also remain unchanged. Only the
reviewer's default author directory was changed for portability; the exact
one-line edit and both hashes are in `PORTABILITY_EDITS.json`. Older marker
checker functions are imported as the independently implemented dependency;
its older main routine is not invoked here. The original scope review is
included unchanged as provenance, not reissued as a new review.

## Reproduce

Python3.11 standard library, one process/thread, exact integer geometry and
finite enumeration; no solver, floating-point inference or external data.
From this directory:

```sh
python3 -B author/check_marker_simple.py --output /tmp/simple-marker-author.json
python3 -B review/check_sage_simple_marker.py --output /tmp/simple-marker-theo.json
```

Expected controls: all872 inputs M2..6 for the complete proper-interval
criterion, all153 inputs m1..5 for occurrence sets/decoding/common pairs,
and66 positive branch witnesses M2..12. Theo additionally exhausts6,120,5040
ALL remaining prefix assignments at M2,3,4, including assignments outside
the band-restricted image; the viable position sets are exactly{0},{0,3},
{0,3,6}. Both complete deterministic author streams and the separate Theo
control fields match the preserved evidence. `PORTABILITY_VERIFICATION.json`
records this replay; timing/memory are environment-specific. Finite controls
support falsification and reproduction. The written proofs establish the
uniform claims. Compact manifests pin the files; no paper snapshots, private
node records, credentials or bulky exhaustive dumps are included.
