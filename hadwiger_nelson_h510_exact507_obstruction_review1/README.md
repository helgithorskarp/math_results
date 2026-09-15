# Independent review of the exact-507 H510 obstruction

## Verdict

**ACCEPT — high confidence, at the exact stated scope.**  The theorem at
source commit `effcfda38fa93483da108d6e658190823d8282b4` is sound:

> There is no map of the fixed labelled 510-vertex, 2,504-edge Heule graph
> `H510` into the real Euclidean plane which sends every source edge to
> distance one and has exactly 507 distinct images.

The coordinates may be arbitrary real numbers, nonedges may become unit
pairs, and any nonadjacent source labels may be identified.  Together with
the independently accepted near-injective classification, every noninjective
plane unit-edge map of `H510`, if one exists, has at most 506 images.

This is a fixed-carrier nonrealizability theorem.  It is **not** a 507-point
plane unit-distance graph, does not constrain unrelated 507-vertex graphs,
does not classify `H510` maps with at most 506 images, and does not improve
the 509-point record.

## Proof boundary

For a source `K2,2` with bipartition pairs `{a,b}` and `{c,d}`, distinct
images within both pairs imply the rhombus identity

```text
p(a)+p(b)=p(c)+p(d).
```

The exact source graph has no `K2,3`, so a label pair occurs on one side of at
most one of the 3,953 canonical rows.  The parent certificate supplies twenty
rank-501 bases.  Mark a basis when a collision invalidates one of its rows.
If some basis is unmarked, both coordinate vectors lie in the parent's exact
nine-dimensional kernel.  If all bases are marked, the collision partition
belongs to a finite rank-defect branch.

Exactly three image losses have only the fibre shapes

```text
4,       3+2,       2+2+2.
```

The rank-defect census is:

| shape | retained candidates | source-edge collapse | quotient `K2,3` |
|---|---:|---:|---:|
| `2+2+2` | 35,854 | 4,056 | 31,798 |
| `3+2` | 4,094 | 59 | 4,035 |
| `4` | 1,931 | 0 | 1,931 |

Here “retained candidates” follows the source's safe pruning convention; it
is not the number of all set partitions of the given shape.  Immediate edge
collapses and branches retaining an already displayed `K2,3` can be rejected
without materializing every completion.

If a partial quotient already contains a `K2,3`, a further identification can
destroy that witness only by merging its two centres or two of its three
common neighbours.  Merging a centre with a common neighbour collapses a
unit edge; every other merger leaves all five witness classes distinct.  The
clean checker explicitly enumerates the possible final source pairs: 501,164
three-pair completions and 503,174 triple-pair completions retain the witness;
only twelve pairs in each branch can possibly repair it.  All retained final
partitions still collapse an edge or contain a `K2,3`.

In the full-rank branch, the accepted parent orientation cover partitions all
4,096 words.  The clean checker confirms that each of its 34 rejected
prefixes forces exactly three image losses.  Eighteen resulting partitions
collapse a source edge and sixteen contain a quotient `K2,3`; exact loss
three leaves no unaccounted collision able to destroy the witness.  The two
surviving complete words are the four injective Galois drawings classified by
the parent.

A quotient `K2,3` is impossible in an injective plane unit-distance drawing:
two distinct centres have at most two common points on their unit circles.
This completes both sides of the rank dichotomy.

## Independent executable audit

[`independent_verify.py`](independent_verify.py) imports no target or parent
Python module.  Using only exact integers and `Fraction`, it:

- decides all 129,795 coordinate pairs in the multiquadratic basis
  `Q(sqrt(3),sqrt(5),sqrt(11))`, recovering exactly 510 distinct points and
  2,504 strict unit pairs;
- matches that graph entry-for-entry to the pinned Parts/Heule union source,
  reconstructs all 3,953 rhombi, and confirms the source has no `K2,3`;
- re-ranks every one of the twenty 501-row bases modulo the different checked
  prime 1,000,000,009;
- checks exactly that all rhombus rows annihilate the constant plus eight
  coordinate columns and independently proves those nine columns linearly
  independent, establishing the matching characteristic-zero rank upper
  bound;
- derives exactly the two rank-basis row-pair covers and 8,486 three-row
  covers, then enumerates all three fibre shapes;
- replaces the submitted dense-four-set algorithm by a triangle/induced-`C4`
  decomposition and independently recovers exactly 1,897,832 independent
  dense quadruples; and
- constructs each retained quotient with bitset adjacency and validates every
  edge-collapse or literal `K2,3` obstruction.

The alternative dense decomposition is complete because a graph on four
vertices with at least four opposition edges either contains a triangle or,
if triangle-free, is exactly `K2,2`.  A dense set with a triangle is assigned
to its lexicographically first triangle; a triangle-free set is assigned to
one of its two opposite nonedge pairs.  This avoids storing the submitter's
1.9-million-element `dense_seen` set.

The first development run omitted 36 immediate edge-collapse `3+2`
candidates.  Investigation showed that a row-side “opposition pair” can also
be a source edge.  Canonicalizing a triple by its first internal opposition
pair was therefore too aggressive when that pair could not itself generate
the triple.  Restricting the canonical choice to admissible generating pairs
restored all 36 cases.  The corrected clean run gives 4,094 candidates and 59
edge collapses, exactly as submitted.  This was a reviewer-checker defect, not
an objection to the source theorem.

The independent checker pins canonical hashes of the complete partition
lists, not only their totals.  [`compare_author.py`](compare_author.py) is a
secondary, deliberately non-independent regression test which imports the
submitted generator and confirms entry-for-entry equality of all three
sorted lists.  The primary verdict does not depend on that import.

[`controls.py`](controls.py) exhausts all 64 four-vertex graphs, checks the 22
graphs with at least four edges against the triangle/`C4` dichotomy, tests all
64 products in the radical basis, exercises positive and negative `K2,3`
detection, and checks the three fibre shapes.  The submitter's separate
184,620 six-vertex quotient controls also pass.

## Parent dependency and source integrity

The proof depends on the committed near-injective theorem
`bafkreia5oxkhc3sjykhvvl2fqkksrd3ple4ci4rcyn6x6z4ixjkj7y6dqq` and its
accepted independent review
`bafkreigzpjwa6r6usnu5xxmcnujnpkysdrnuvjoq7ee6vjpbxmwyffjp7q`.
That review independently derived the 4,096-word orientation exhaustion and
the exact polynomial endgame without consuming the parent's corresponding
certificate layers.  Its source commit is
`e19b11b3eafea2fb032fb866022de0220ac0f686`.

This review freshly rechecks the parent graph, rank lower and upper bounds,
prefix partition, and quotient consequences.  It does not again derive the
orientation row-space equalities or polynomial elimination; those remain an
explicit imported, previously independently accepted dependency.  The target
verifier replays the hash-pinned parent verifier before its own census.

The target's pending Discovery reference is
`bafkreidh7t4e6s462exgm2c2mkndv4swjud6mlbx65e3oadfogzkiajhp4`.  Pending is
not committed; no `verifies` relation to that endpoint is asserted here.

## Reproduction

Python 3.11 or later and the standard library suffice.  From the repository
root:

```sh
review=hadwiger_nelson_h510_exact507_obstruction_review1
python3 -B "$review/independent_verify.py" --check-expected
python3 -O -B "$review/independent_verify.py" --check-expected
python3 -B "$review/controls.py"
python3 -O -B "$review/controls.py"
python3 -B "$review/compare_author.py"
(cd "$review" && sha256sum -c SHA256SUMS)
```

The comparison is optional and intentionally imports the source verifier.
The clean verifier and controls are the independent evidence.  See
[`validation.json`](validation.json) for the exact host runs, output hashes,
and resource notes.

## Scope and trust boundary

The geometric theorem does not use `H510`'s five-chromaticity.  That published
and previously certified property is needed only to explain why a hypothetical
507-image map would yield a record construction: a four-colouring of its image
would lift to the source.  No colouring solver is used in this obstruction.

Residual trust includes the elementary two-circle and quotient-`K2,3` lemmas,
the prior accepted orientation/polynomial classification, the pinned
coordinate transcription, CPython exact-arithmetic semantics, SHA-256, the
operating system, and hardware.  This is an exact computer-assisted review,
not proof-assistant formalization.

The current unrestricted order record is Parts's 509-point construction with
2,442 strict unit pairs
([primary paper](https://arxiv.org/abs/2010.12665)).  Haugland's August 2026
preprint explicitly calls 509 the current record and describes its own
2,131-point result as a Moser-spindle-free structured construction, not an
order improvement
([primary preprint](https://arxiv.org/html/2608.04542v4)).  A separately
submitted [2026 edge reduction](https://github.com/md-amer/hadwiger-nelson-e5)
retains the same 509 coordinates and therefore does not change the vertex
record.
