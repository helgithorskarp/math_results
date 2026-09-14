# Review of the native fixed-base five-point repair exclusion

## Result reviewed

The target defines an actual plane point set

```
A = the archived 159-point Parts set,
D = its 30 oriented unit differences,
rho = (7 + i sqrt(15))/8,
L = A union (A + D),
H = L union rho L.
```

Exact duplicate contraction gives `|H|=3919` and 29,125 strict unit edges.
The fixed set `B` consists of 503 explicit host IDs. Its identification with
503 displayed vertices of Parts' 509-vertex graph was independently accepted
in the parent review; the six absent zero-based labels are
`25,74,106,107,298,336`.

The reviewed theorem is precisely

> For every `S` contained in `H minus B` with `|S| <= 5`, the induced strict
> plane unit-distance graph on `B union S` has chromatic number at most four.

## Proof audit

### Geometry and positive words

The target tree at commit `eec9c106...` matches the reviewed files, and its
package hashes pass. A fresh run of the earlier clean-room geometry checker
reconstructed all 3,919 distinct points in
`Q(sqrt(3),sqrt(5),sqrt(11))`, examined all 7,677,321 unordered pairs, and
recovered exactly 29,125 unit edges. Its point and edge hashes were
respectively

```
fa6c2aa721db1dc24bf96ea71bb0b944c50646d0f0276f3d5f47fa8b7cb766a3
e6e4757bfcb92fc54f2ad57759c16653e75f920073006ef846c9ce2486f1ec3d
```

This checker imports no target module. It uses one finite-field
homomorphism only as a sound sieve and decides every survivor again by
generic exact multiquadratic multiplication.

The new independent checker validated 126 distinct words over
`{0,1,2,3,.}`. Every word retains all of `B`, and all coloured endpoints of
every exact edge receive different colours. In total 2,801,272 retained-edge
incidences were checked. If `O_i` is the omitted set of word `i`, any
non-four-colourable repair `S` must meet every `O_i`: otherwise word `i`
restricts to a four-colouring of `B union S`. This uses only sound positive
witnesses, not completeness of a colouring search.

### Minimality and padding

Suppose a counterexample of size at most five exists and take an
inclusion-minimal one with `B` fixed. Every new point then has degree at least
four in the repaired graph, because a four-colouring after deleting a point
of degree at most three extends to that point. There are 585 free host points
having at least four neighbours already in `B`. Adding unused members of this
pool pads the minimal counterexample to exactly five vertices, preserves
non-four-colourability, and gives every padded point degree at least four.
The supply is vastly larger than the at most four padding points required.

Thus it is enough to exclude five-sets `T` satisfying

```
d_B(v) + d_{H[T]}(v) >= 4  for every v in T.
```

This reduction imposes no minimum-degree condition on vertices of `B`.

### Connected components of order at least three

The clean-room checker grows canonical sorted tuples from all free
singletons. At stage `k`, it attaches every boundary neighbour and keeps a
connected tuple only when

```
d_B(v) + d_S(v) + (5-k) >= 4  for every v in S.
```

This pruning is complete. Every connected five-set has a connected-prefix
ordering, and every prefix of a degree-qualified final set obeys the displayed
upper bound because at most `5-k` later vertices can add to any current
degree. Hash-set canonicalization is definition-level duplicate removal; it
does not use the target's ESU or spanning-tree generators.

The result was 1,856,054 distinct qualified connected five-sets. None hits all
126 omission sets, so each is contained in one positive word. The same growth
found exactly 18,965 qualified connected triples and 175,654 qualified
connected quadruples.

For a quadruple component, the remaining isolated point must be one of the
585 high-base-degree points. For a triple component, the remaining two points
must be either two high-base-degree singletons or one of 2,549 free edges whose
endpoints each have at least three base neighbours. Allowing overlaps and
extra adjacencies enlarges these completion pools and is therefore safe for a
negative result. A direct rare-bit superset query found no omission-covering
union after 4,495,376 candidate-mask tests for the quadruples and 264,431,623
for the triples.

As a target-side cross-check not performed by its default command, the full
ESU program was run on the production input. It independently reported
1,856,054 qualified five-sets and zero survivors; its canonical triple and
quadruple inventories agree exactly with the spanning-tree inventories after
sorting.

### Singleton and pair components

If all components have order at most two, an isolated point has at least four
base neighbours. Each paired endpoint has at least three base neighbours. A
pair of high points can be represented by two cost-one singleton atoms;
otherwise the edge is one of 1,238 cost-two atoms involving a point of base
degree three. Consequently any counterexample induces a cover of all 126
omission indices by 585 cost-one and 1,238 cost-two atom masks, of total cost
at most five.

The independent checker first applies only equivalence-preserving reductions:
duplicates are collapsed, and a mask is removed when it is contained in a
mask of no larger cost. Any cover using a removed atom can replace it by its
dominator. This leaves 419 maximal singleton masks and 1,063 maximal pair
masks. It then exhausts zero, one and two pair choices, using exact integer
mask recursion only for the remaining singleton budget. It closed all
564,453 two-pair cases, made 1,667,939 singleton-recursion calls, and found no
cost-five cover. This is a separately written Python computation over an
independently reconstructed edge graph, not a replay of the target's input
file.

Together the component cases exclude every degree-qualified `T`, contradicting
the padded minimal counterexample. The theorem follows.

## Target replay and controls

- The normal target replay passed in 38.5 seconds, including its two exact
  cover computations.
- The optimized-Python replay with C++ undefined-behaviour sanitization passed
  in 41.7 seconds and agreed on every stable mathematical field.
- The target's 12 small graph and 80 cover controls passed; 71 cover controls
  are positive instances, and four malformed words were rejected.
- The independent checker's ten brute-force graph controls and 80 brute-force
  cover controls passed, with both feasible and infeasible cover instances.
  A deliberately bad residual completion and three semantic certificate
  corruptions were rejected.
- Seventeen reported 508/509 positive search controls were independently
  checked on 41,303 retained edges. They are colourable controls only and do
  not establish a six-addition exclusion.

## Verdict and limitations

**ACCEPT with high confidence for the stated fixed-base, fixed-host theorem.**
No logical gap, missing geometric edge, certificate mismatch, undefined
solver premise, or incomplete component type was found.

The conclusion is deliberately restricted:

- `B` cannot change and no vertex of it may be deleted;
- only points of the explicit 3,919-point `H` may be added;
- this review certifies the target's five-addition bound only; the later
  author-side six-addition package at commit `c418ae6` is not reviewed here;
- arbitrary subgraphs of `H` that omit base points remain unclassified;
- no five-chromatic graph of order at most 508 is produced or excluded
  globally;
- the theorem does not improve `5 <= chi(R^2) <= 7`.

Parts' 509-vertex, 2,442-edge construction remains the unrestricted published
record. Haugland's 2,131-point construction is subject to the additional
Moser-spindle-free restriction and does not supersede that record. The target
therefore closes one credible record-repair lane and is an explicit dependency
of the later six-point extension; it is not itself a record advance.

A final repository refresh also found the exact paired-Golomb closure at
commit `e0c61f0` and the exact native six-point extension at `c418ae6`. Neither
package reports a sub-509 five-chromatic construction, so neither displaces
the record calibration or this dependency review. Their new claims require
separate independent assessment.

The default target verifier does not rerun the advertised full ESU comparison;
the source and author validation record it separately. This review performed
that full comparison, so the packaging omission does not weaken the accepted
mathematical conclusion. The exact Parts-coordinate identification of the 503
base points is inherited from the separately published parent review rather
than recomputed again here; the present theorem itself is also meaningful
directly for the explicit 503 host IDs.

The exact arithmetic implementation, ordinary Python/C++ execution, finite
enumeration completeness arguments, and supplied positive words remain the
trust boundary. This is independent computational review, not formalization.
