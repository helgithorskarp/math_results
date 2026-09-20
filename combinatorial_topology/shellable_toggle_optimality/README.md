# Optimal toggle words from simplicial shellings

For a finite pure shellable simplicial complex K, include its empty face and
adjoin a **new** greatest element hat1. In the Möbius-restricted lattice
toggle game, the minimum winning length on this augmented face lattice is

\[
\boxed{\ell(L(K))=\sum_{F\in K}|\mu(F,\hat1)|=h_K(2).}
\]

A supplied shelling constructs a legal word using each face F exactly
|mu(F,hat1)| times, always with its prescribed add/remove sign. The same word
minimizes **every nonnegative assignment of move costs**, with optimum
sum_F c(F)|mu(F,hat1)|. Thus an entire geometric class is excluded from the
search for an unwinnable finite lattice.

The [proof](PROOF.md) is self-contained. Its key step is an exact expression
for the upper Möbius values in terms of dual shelling intervals. Purity
prevents cancellation, making every intersection used by a recursive
clearing word legal. The classical Möbius lower bound and shelling/h-vector
identities are explicitly credited in [SOURCES.md](SOURCES.md).

This is a theorem about augmented **face** lattices, not arbitrary lattices
whose order complexes are shellable. It does not determine the smallest
unwinnable lattice. Shellability is supplied, not recognized by the algorithm.
There is no claim for all nonpure or nonshellable complexes. A nonpure example
shows why this compiler fails even though that example remains winnable.
Novelty is relative to a bounded literature search; independent review and
formal proof-assistant verification remain pending.

## Reproduction

From the repository root, with CPython 3.11 or newer:

```sh
python3 combinatorial_topology/shellable_toggle_optimality/verify.py
```

The checker uses only the standard library. It performs no network access,
random sampling, floating-point computation, solver call, or external data
import. It prints the deterministic [expected record](expected.json), with
status `VERIFIED` and evidence SHA-256

```text
b8f39ccd9efef3d1644b086a8b47768b66d33b0e4ed241f37f62342ed361beac
```

The evidence digest uses JSON with sorted keys and compact separators. The
file manifest is [SHA256SUMS](SHA256SUMS); check it from this directory with
`sha256sum -c SHA256SUMS`. Normal and `python3 -O` runs agree. A reference
CPython 3.11.2 run takes about one second; this is not a performance guarantee.

## What the checker establishes

- All 2,085 orders of all 94 nonempty uniform facet families on four labels
  are examined. Every one of the 1,695 valid shelling orders is compiled and
  replayed. The other 390 orders are rejected. Ghost labels are harmless;
  these are labelled families, not an unlabelled-complex census.
- Independent definition-level breadth-first searches verify the optimum
  for all 91 shellable families in that collection. State spaces have at
  most 16 face bits. The remaining three families are rejected for this
  theorem; no claim of unwinnability is made for them.
- Twenty-eight larger or boundary fixtures cover simplices, isolated
  vertices, a sphere boundary, glued tetrahedra, cones over cycles, uniform
  complexes, crosspolytope boundaries, stacked balls, and triangulated grids.
  They include many zero Möbius values and repeated moves with |mu|>1.
- The compiler uses bitmasks, while the replay builds literal face sets and
  computes Möbius values by the defining upper recurrence. Every individual
  move is checked for permission and monochromaticity. Facewise counts,
  signed counts, the dual-interval formula, and an independent f-to-h
  transform are checked entry by entry.
- Twelve Dijkstra computations, including zero-cost moves, independently
  confirm weighted optima on four small complexes.
- Nine malformed or out-of-scope inputs and four corrupt words are rejected.
  The documented nonpure compiler failure is detected at a zero-Möbius face;
  a different seven-move winning word and a BFS optimum are verified.

The universal proof is separate from these finite checks. Trust remains in
the unformalized argument, readable checker, and Python's exact integers and
set operations. No large certificate or hidden computation is omitted.

Prepared 2026-09-20 for the Discovery Net graph-first research campaign.
