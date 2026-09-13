# Referee report

## Claim under review

The mathematical snapshot at
`c44e047d60d44b60b5878f13a9293ef33aac3bc5` claims that the native-contact
construction contains an induced 1,090-vertex, 6,011-edge plane unit-distance
graph of chromatic number five. It separately identifies 503 points shared
with the displayed Parts-509 realization, a precise six-hole repair target,
a four-colourable 507-point control, and a four-colourable 1,587-point
two-neighbour pool.

**Verdict: ACCEPT, high confidence, with the scope limitations below.**

## Exact geometric reconstruction

The review checker reads the hash-pinned 159 rows as Cartesian coordinates
at denominator 12 in the eight-element squarefree basis of

\[
K=\mathbb Q(\sqrt3,\sqrt5,\sqrt{11}).
\]

It uses a generic multiplication routine indexed by squarefree prime masks,
not the target's expanded four norm equations or its `radical_check.py`. It
finds 30 oriented unit differences, reconstructs (A+(A+D)), applies

\[
\rho=(7+i\sqrt{15})/8,
\qquad |\rho|^2=(49+15)/64=1,
\]

merges equal Cartesian points, and independently applies the exact radius
test. The three independent prime square classes give degree eight, so
coefficient equality is equality in the displayed real embedding.

Complete all-pairs edge enumeration uses the homomorphism to
\(\mathbb F_{1000081}\) determined by

```text
sqrt(3)  -> 35512
sqrt(5)  -> 183365
sqrt(11) -> 29480.
```

The checker proves the modulus prime by trial division and checks the three
root equations. Therefore every exact unit pair must survive the modular
test. Every survivor is then retested by generic multiplication in (K), so
the sieve cannot omit an edge. Across all 12,323,997 pairs, its survivor sets
were exactly the final edge sets: 21,217 pairs in the radius-two host and
29,125 in the full host.

The reconstruction matches the target byte-level invariants:

| object | vertices | edges | SHA-256 evidence |
|---|---:|---:|---|
| radius-two host | 3,049 | 21,217 | points `298f6a...a6136`; edges `5c8a69...fa2fe` |
| selected graph | 1,090 | 6,011 | IDs `ae59b8...fd48b`; CNF `aabe9d...fce5e` |
| full host | 3,919 | 29,125 | points `fa6c2a...766a3`; edges `e6e475...ec3d` |

All coordinates are thus actual plane points, and all listed graph edges are
actual unit distances. This is not merely an abstract chromatic graph.

## Chromatic certificate

The reviewer checker independently remaps the induced selected edges and
emits the four-colour formula. It has 4,360 variables and 31,677 clauses:
one at-least-one and six at-most-one clauses per vertex, four inequalities
per exact unit edge, and three unit clauses pinning the genuine triangle
`(1,6,9)` to distinct colours. Any proper four-colouring can be permuted to
satisfy those pins, so the symmetry reduction is equisatisfiable.

A fresh build of Kissat 4.0.4 generated a 10,739,017-byte proof with SHA-256

```text
c11236bd6febaab12773e0f0548a3c1a7e83dd8b68dfe8c7f0e703e644a9d929
```

from the independently emitted CNF. A fresh build of `drat-trim` returned
`s VERIFIED`: 23,400 original clauses and 91,045 of 141,669 lemmas were in
the backward core, with 8,457,902 resolution steps and no RAT lemma in the
core. This establishes non-four-colourability subject to the stated checker
trust boundary.

The published radius-two word is directly proper on all 21,217 edges and
restricts to a proper five-colouring of the selected graph. The full host's
separate five-colour word is proper on all 29,125 edges, and the full host
contains every selected physical point. Hence the selected graph and both
hosts have chromatic number exactly five.

## Repair interface and positive controls

The target's `record.py` replay passed. In addition, the review checker used
SymPy 1.14's general algebraic-number-field (`ANP`) representation rather
than importing the target or earlier Parts parser. It independently parsed
all 509 Mathematica coordinate pairs, verified 509 distinct elements of the
degree-eight field, and discovered exactly 503 matches in the 3,919-point
host. The missing zero-based Parts labels are

```text
25, 74, 106, 107, 298, 336.
```

This is equality in the one displayed coordinate placement. It is not an
abstract graph-isomorphism statement and does not classify other isometric
placements.

The exact graph on the supplied 503-point base plus four listed host points
has 507 vertices and 2,422 edges; its supplied four-colour word passed. This
proves only that one candidate is four-colourable. Likewise, rebuilding the
482-point radius-two base and adding every host point with at least two base
neighbours gives exactly 1,587 vertices and 10,021 edges, and its word is a
proper four-colouring. Restriction excludes every subgraph of that one
finite pool, not the 503-point full-host repair family and not other HN
constructions.

The minimum-degree condition and colouring-extension cuts described for the
unfinished selector are sound necessary conditions: a vertex of degree at
most three can be added to any four-colouring, and a candidate contained in
a checked colourable extension inherits that colouring. But the recorded
timeouts are `UNKNOWN`. This review attaches no mathematical conclusion to
the 23 tested candidates, the unfinished master problems, or the smaller
982-point heuristic state.

## Limitations and trust boundary

- The accepted graph has 1,090 vertices, so it does not improve Parts's
  unrestricted 509-vertex benchmark.
- No vertex-criticality, minimality, novelty, or priority claim is reviewed.
- The ≤508 fixed-placement repair question remains open. The 507-point word
  and 1,587-point pool are positive, restricted-family evidence only.
- The review checker receives the subset IDs and colour words as witnesses;
  it verifies but does not rediscover them.
- Exact geometry trusts the pinned coordinate transcription, the degree-eight
  radical interpretation, CPython integer arithmetic and ordinary hardware.
  The overlap check additionally trusts SymPy 1.14.
- The lower bound trusts the independently regenerated CNF, Kissat as proof
  producer, and `drat-trim` as proof checker. It is not proof-assistant
  formalized.

The current published-record check found Parts's 509-vertex, 2,442-edge graph
still cited as the unrestricted benchmark. Haugland's 2,131-point construction
has the additional Moser-spindle-free restriction and does not supersede it.
