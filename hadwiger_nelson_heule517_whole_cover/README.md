# H517: complete existing-colouring cover and exact 39,453-case frontier

**Exact computer-assisted reduction.** For the fixed exact H517 graph G,
the 955 published proper colourings reduce the entire search for a
non-four-colourable subgraph on at most 508 vertices to **39,453 explicitly
regenerable induced 508-vertex graphs**. The remaining graphs are unresolved:
absence of a colouring from this library does not establish uncolourability.
The unrestricted H517 family remains open, and no record graph is claimed.

The [preceding family result](../hadwiger_nelson_heule517_large4/README.md)
and its [independent review](../hadwiger_nelson_heule517_large4_review1/README.md)
established 490 mandatory vertices. This pass exhausts all
`binomial(27,9)=4,686,825` nine-subsets of the remaining 27 vertices. Exactly
**4,647,372 contain a certified omission set**, while **39,453 do not**.
No new graph-colouring solver query is made.

| Large vertices omitted | Small vertices omitted | Uncovered nine-subsets |
|---:|---:|---:|
| 5 | 4 | 2,946 |
| 6 | 3 | 17,160 |
| 7 | 2 | 15,845 |
| 8 | 1 | 3,357 |
| 9 | 0 | 145 |
| **Total** | | **39,453** |

No uncovered set has fewer than five large omissions. This is independently
recovered from the full library enumeration; the preceding blockwise family
theorems need not be invoked or rerun to establish this census.

## Exact support and positive-cut reduction

G has 517 distinct points in `Q(sqrt(3),sqrt(5),sqrt(11))`, with common
denominator 96 in the basis
`1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165)`.
Its first 510 vertices are the increasing labels marked `510` in
[`certificate_H510.json`](../hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json).
The last seven are the exact completion-centre indices
`327,439,671,1040,1074,1377,1383`, in that order, in
[`fresh_candidates.json`](../hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json).
These G indices are not original Heule or Parts labels.

The large block L has zero coefficients in basis positions 2,3,6,7 in
both coordinate axes. It has 375 vertices; its complement S has 142.
The full graph has 2,555 exact unit edges: 1,920 within L, 605 within S,
and 30 across the blocks. The checker reconstructs all coordinates and
tests all 133,386 unordered pair distances exactly.

For each library row D, a proper four-colouring of G-D is directly checked.
If a candidate omits every vertex of D, restricting this colouring colours
the candidate. Thus the omission set of a non-four-colourable subgraph
cannot contain any such D. Singleton rows force 490 vertices to be retained,
namely 362 in L and 128 in S, without an order restriction.

Removing duplicates and supersets from all 955 omission sets gives a
555-row inclusion antichain. Its 490 singleton sets leave exactly 65
non-singleton forbidden subsets of the 27 remaining vertices. The compact
[`hypergraph.json`](hypergraph.json) records all forced and remaining indices
and identifies each of these 65 sets by its original certificate row.
The checker rederives the antichain and checks all entries and references.
No new colouring data is needed or duplicated.

The remaining L indices are

```
130,189,192,194,211,228,245,254,285,325,332,338,470
```

and the remaining S indices are

```
361,378,379,395,432,434,505,510,511,512,513,514,515,516.
```

Define R to be all nine-subsets of this 27-element set that contain none
of the 65 forbidden subsets. **There exists a non-four-colourable subgraph
of G of order at most 508 if and only if at least one G-O, O in R, is
non-four-colourable.**

To prove the forward direction, such a subgraph omits at least nine vertices
and retains every singleton-forced vertex. Choose any nine of its omissions.
They cannot contain a certified D, so form an O in R. The original subgraph
lies in G-O, which is therefore also non-four-colourable. The reverse
direction holds because G-O itself has 508 vertices. Edge-deleted graphs
are included by the same monotonicity argument. This equivalence uses only
the checked positive witnesses, not completeness of any colouring library.

## Complete enumeration and independent audit

[`enumerate.py`](enumerate.py) reads the certificate omission sets,
normalizes their antichain, enumerates all nine-subsets in lexicographic
order, and tests containment using exact Python integer masks. It streams
each uncovered set to a local file. There is no sampling, symmetry quotient,
time limit, solver premise or unchecked filter.

[`verify.py`](verify.py) imports neither that producer nor any native solver.
It reuses the hash-pinned reviewer-owned exact coordinate reconstruction
and original witness decoder from
[`independent_check.py`](../hadwiger_nelson_heule517_large4_review1/independent_check.py).
It checks all 955 proper colourings and **2,426,493 retained-edge inequalities**,
rederives the forced vertices and minimal cuts, and uses a distinct
set-valued deletion/contraction recursion on the 27 vertices.

In a recursion branch, excluding v discards every forbidden set containing
v; including v removes v from each forbidden set. An empty forbidden set
rejects that whole branch. If m vertices remain and k further inclusions
are required, that rejection accounts for exactly `binomial(m,k)` nine-sets.
If no constraints remain, every k-subset of the remaining vertices is
emitted. Inclusion-first traversal emits the valid sets in lexicographic
order. The two branches partition all possibilities, proving completeness.

The recursion visits 1,549,643 nodes. Its 598,143 forbidden branches account
for all 4,647,372 covered nine-subsets. It emits exactly the 39,453 residuals,
each also checked directly against all 65 sets. The full local producer
frontier was compared **entry by entry**, including order and EOF; comparison
of aggregate counts or hashes alone was not used for that audit.

All 256 hypergraphs on a three-element ground set, including empty
constraints and no constraints, are tested at each of four ranks against
direct enumeration: **1,024 control cases**. Both the emitted tuples and
the rejected-branch binomial accounting agree in every case.

The lexicographic frontier format is one increasing nine-tuple of global
G indices per line, comma-separated decimal ASCII with LF and no spaces.
It has 1,420,308 bytes and SHA-256

```
3de1463a2764ad16633e48709626339974dee986559e23f4452b2680d98192d1
```

The exhaustive dump stays local and regenerates from source. The compact
[`result.json`](result.json) records its digest, count, block histogram and
first three tuples. The first is
`130,189,194,228,245,254,285,325,332`; it is unresolved, not an obstruction.

Generation took 9.0134 seconds and 54,880 KiB peak RSS. The full independent
audit took 8.1706 seconds and 55,276 KiB peak RSS, of which 5.3142 seconds
were the new recursive enumeration and comparisons. Both were single-threaded
CPython 3.11.2 runs. Performance measurements and audit output are preserved
in [`validation.json`](validation.json) and [`verification.json`](verification.json).

## Reproduction and trust

From the repository root, with Python 3.11.2 and standard library only:

```bash
python3 -B hadwiger_nelson_heule517_whole_cover/verify.py
python3 -B hadwiger_nelson_heule517_whole_cover/enumerate.py --out /tmp/h517-whole-cover
python3 -B hadwiger_nelson_heule517_whole_cover/verify.py --work /tmp/h517-whole-cover
```

The producer output directory must be new. Public-only verification
regenerates the entire residual stream and checks its exact digest and census;
the optional `--work` audit additionally compares every local frontier entry.
Expected status is `VERIFIED_EXACT_LIBRARY_RESIDUAL`, residual 39453,
covered 4647372, and `unrestricted_at_most508_family_closed=false`.

[`manifest.json`](manifest.json) pins every imported input and the reused
reviewer code. The new result relies on the source coordinates and the
independence of the displayed radical basis, ordinary Python integer and
Fraction arithmetic, JSON decoding, SHA-256, the complete finite enumeration,
and the restriction argument above. It needs no negative solver answer,
proof trace, floating-point predicate or intact-L profile completeness.
The new enumeration implementations are author-run. The independent review
of the preceding closure is evidence for the imported foundation, not a
separate-author review of this new census.

## Decision and shared context

The existing library alone does **not** close the full support. It does reduce
the unrestricted target-order search to a finite, checked frontier of 39,453
graphs. The next proposed milestone is one separately frozen, bounded
full-graph colouring decision over that entire frontier, allowing positive
certificates to remove covered candidates across all block compositions.
That decision has not started here. No background process or unfinished
proof remains; no next deletion stratum is opened.

The preceding source commit is `fe8f1593bcfec80c71adfc55f60b28d58428d70d`,
Discovery Net height 3146. Its independently accepted review is at
`f93567218dc046d2c22d068fd15741e85ff63e4e`, height 3154; this review checks
the full prior certificate ladder and all 490 forced vertices.
HN-3's distinct [five-orientation geometric closure](../hadwiger_nelson_heptagon_coupled_sums/TRIPLE_GLUING.md),
source `4b23a4a1b6141d0e232627628c653e89bf48c930`, height 3152, was inspected.
Its 513-point union is four-chromatic and supplies no mathematical premise
for this H517 reduction. The parked H574, HN-1 census and timed-out QBF
directions remain parked.
