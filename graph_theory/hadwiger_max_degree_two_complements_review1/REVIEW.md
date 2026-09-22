# Independent review of exact Hadwiger numbers for co-degree-two graphs

## Target and verdict

Target contribution:
`bafkreig54ui5rkut6areq5r7hnm3x2xpll2oprxetu77af7ba3arqpoysy`.

Reviewed source commit:
`6699ba713ec99035edb583badd704305ef555ff3`.

**Verdict: accept with high confidence in the stated scope.**  I found no
mathematical error in the exact formula, the eight exceptional families, or
the Hadwiger-conjecture corollary.  The proof gives a complete structural
reduction rather than inferring a universal classification from its finite
audit.  The source also scopes prior art and its proposed increment
responsibly.  This verdict does not certify exhaustive historical priority.

## Proof reconstruction

Write \(G=\overline H\), \(n=|V(H)|\), \(a=\alpha(H)\), and
\(U=\lfloor(n+a)/2\rfloor\).  If a \(K_t\)-minor model in \(G\) has \(s\)
singleton branch sets, those vertices are independent in \(H\), so \(s\le a\).
All other branch sets use at least two vertices.  Therefore

\[
n\ge s+2(t-s)=2t-s\ge 2t-a,
\]

which proves \(t\le U\).  Equality bookkeeping is also important later: when
\(n-a\) is even, a \(K_U\)-model must use exactly \(a\) singleton branch sets,
must cover every remaining vertex, and all other branch sets must be pairs.

Choose the componentwise alternating maximum independent set \(S\), and put
\(R=V(H)\setminus S\).  On \(R\), forbid a pair if it is an edge of \(H\) or
if its two vertices have a common neighbor in \(S\).  Component by component,
the forbidden graph \(F\) is

\[
P_m\mapsto P_{\lfloor m/2\rfloor},\qquad
C_{2q}\mapsto C_q,\qquad
C_{2q+1}\mapsto C_{q+1},
\]

with \(P_0\) empty and \(C_2=K_2\).  Hence \(\Delta(F)\le2\).  An edge of
\(\overline F\) is a two-vertex branch set connected in \(G\) and adjacent to
every singleton in \(S\).  Two disjoint pair branches could fail to be
adjacent only if all four cross-pairs were edges of \(H\).  The degree bound
then makes those four vertices an entire \(C_4\) component, impossible because
the canonical \(S\) contains two vertices of that component.  Thus a matching
of size \(\lfloor|R|/2\rfloor\) in \(\overline F\), together with the
singletons \(S\), attains \(U\).

The matching boundary is exhaustive.  For even \(N=|R|\ge6\),
\(\delta(\overline F)\ge N-3\ge N/2\), so Dirac gives a Hamilton cycle and a
perfect matching.  For odd \(N\ge7\), deleting one vertex leaves order
\(M=N-1\) and minimum degree at least \(N-4\ge M/2\), again giving a perfect
matching.  At \(N=5\), minimum degree at least two excludes every graph of
matching number at most one.  Direct inspection at \(N=2,3,4\) leaves only

\[
F=K_2,\qquad F=K_3,\qquad F=K_3+K_1,
\]

respectively.  The middle case expands to \(C_5\) or \(C_6\) plus isolates;
both nevertheless attain \(U\) by direct minor models.  The other two cases
expand exactly to the eight listed non-isolated cores.

For an exceptional core, \(n-a\) is even, so a hypothetical \(K_U\)-model is
forced into a maximum independent singleton set plus residual pairs.  For
\(C_3,C_4,P_4,P_5\), the residual pair is either an \(H\)-edge or the two
neighbors of a singleton.  In each mixed core, every maximum independent set
leaves three cycle vertices and one path vertex; every cycle-cycle pair is
forbidden, so two residual pairs would both need the unique path vertex.
This rules out \(K_U\) for every maximum independent set, not merely the
canonical one.  Explicit minor models for the component complements combine
across joins to attain \(U-1\).  Adding an isolate to \(H\) adds a universal
vertex to \(G\), and \(\eta(K_1+G)=1+\eta(G)\), extending exactness to every
listed family.

Finally, coloring \(\overline H\) is clique partitioning \(H\).  Paths, even
cycles, and \(C_3\) contribute their independence numbers; an odd cycle of
order at least five contributes one more.  Thus

\[
\chi(\overline H)=\alpha(H)+z,
\]

where \(z\) counts long odd-cycle components.  Each such component contributes
at least three vertices to \(R\), so \(\lfloor |R|/2\rfloor\ge z\).  This proves
\(\chi\le\eta\) outside the exceptions, and the eight displayed values settle
the boundary directly.

## Human premises and completeness reductions

The high-confidence verdict depends on these human-audited links; agreement
of finite programs is not their replacement.

1. **Component reduction.** Every finite simple graph of maximum degree two
   is a disjoint union of paths and cycles, including isolated vertices as
   \(P_1\), and the alternating set \(S\) is maximum on every component.
2. **Counting upper bound.** Singleton branch vertices form an independent set
   of \(H\), while every other branch consumes at least two vertices.  When
   \(n-a\) is even, equality forces all three conditions used in the
   exceptional upper bound: \(a\) singletons, full vertex coverage, and pairs
   elsewhere.
3. **Forbidden-graph completeness.** The two stated reasons are exactly the
   obstructions to a residual pair being connected in \(G\) and adjacent to
   every singleton.  Direct component tracing gives the three displayed
   path/cycle transformations, including \(C_2=K_2\).
4. **Pair-to-pair adjacency.** Absence of every cross-edge in \(G\) creates a
   \(K_{2,2}\) in \(H\); the degree-two hypothesis makes it a whole \(C_4\)
   component, contradicting that all four vertices lie in \(R\).
5. **Large matching reduction.** Dirac applies with the stated inequalities
   at the exact even boundary \(N=6\) and, after deletion, odd boundary
   \(N=7\).  It supplies a matching of precisely the required cardinality.
6. **Small matching completeness.** On five vertices, a graph with matching
   number at most one is a star, a triangle plus isolates, or edgeless; none
   has minimum degree two.  At orders two through four, the degree-two
   component list leaves only \(K_2,K_3,K_3+K_1\).
7. **Expansion to eight cores.** A forbidden \(K_2\) comes from exactly one of
   \(C_3,C_4,P_4,P_5\).  A forbidden \(K_3+K_1\) comes from \(C_5\) or \(C_6\)
   together with \(P_2\) or \(P_3\); components \(P_1\) add no residual vertex.
8. **Rescue of the \(K_3\) case.** \(\overline{C_5}\) has a \(K_3\)-minor, and
   the two parity triangles in \(\overline{C_6}\) give a four-branch model.
   Thus a failed canonical residual matching is not incorrectly equated with
   failure of the Hadwiger formula.
9. **Exceptional obstruction for all \(S\).** Every maximum independent set
   in a mixed core is maximum componentwise.  It leaves three mutually
   forbidden cycle vertices and one path vertex, ruling out every forced
   residual pairing, including noncanonical choices.
10. **Lower values and isolate extension.** The component models have the
    claimed orders and combine across graph joins.  Deleting the branch set
    containing a universal vertex proves the upper half of
    \(\eta(K_1+G)=1+\eta(G)\), including models where that branch set contains
    additional vertices.
11. **Chromatic corollary.** Cliques of \(H\) cannot cross components; except
    for \(C_3\), they have size at most two.  This makes the clique-partition
    formula additive and leaves no uncounted short-cycle case.

## Adversarial smallest examples and independent computation

The independent checker uses a definition-level route.  For each component
signature it brute-forces \(\alpha(H)\), computes \(\chi(\overline H)\) by
exact DSATUR, and computes the Hadwiger number by enumerating branch-set
partitions.  A distinguished unused block turns a \(K_t\)-minor model into a
partition of \(n+1\) objects into \(t+1\) blocks.  Restricted-growth labels
enumerate every such partition once; accepting exactly connected, pairwise
adjacent non-unused blocks is equivalent to the branch-set definition.

This search computes exact Hadwiger numbers for all 683 unlabeled
maximum-degree-two graphs through order 12.  It examines 488,663 complete
branch partitions, finds exactly the eight non-isolated deficit cores and 56
isolate-extended deficit instances, and verifies \(\chi\le\eta\) throughout.
An independent matching dynamic program applied to every maximum-degree-two
forbidden graph through order 12 finds failures only at \(K_2,K_3,K_3+K_1\).

The smallest examples exercise distinct logical boundaries:

- \(P_4\) has \(U=3\) but Hadwiger number two, catching any assumption that
  the universal count is always attained.
- \(C_5\) and \(C_6\) attain \(U=3\) and \(U=4\), despite their canonical
  forbidden graph being \(K_3\); this catches the converse error just noted.
- \(C_5+P_2\) is a genuine mixed exception with \(U=5\) and Hadwiger number
  four.
- \(C_5+P_4\) is a near miss, not an exception: it attains \(U=6\).  This
  distinguishes the \(P_2/P_3\) residual isolate from the \(P_4\) residual
  edge.
- \(2C_3\) attains \(U=4\), showing that two exceptional connected cores do
  not form another exception when joined in the complement.

The producer's separate suite also passed: it validates 3,156 component
signatures through order 16, directly replays its branch certificates,
exhausts all maximum independent sets and pairings in the eight cores, passes
seven mutation-sensitive tests, and matches all seven published hashes.
Agreement is supplementary; items 1--11 establish the unbounded reduction.

## Source and literature integrity

The source at commit
`6699ba713ec99035edb583badd704305ef555ff3` matches the graph contribution,
and its theorem hash and exact-audit digest reproduce.

Ivančo's primary paper, [*The Hadwiger number of complements of some
graphs*](https://dml.cz/bitstream/handle/10338.dmlcz/133144/MathSlov_47-1997-4_2.pdf),
explicitly determines the complement Hadwiger number for graphs with no cycle
shorter than seven, so the target correctly disclaims the long-component
specialization and join machinery.  Fox and Wei's [primary
manuscript](https://arxiv.org/abs/1603.07056) contains the same counting upper
bound and a sufficient dense missing-degree range.  Li and Liu's [journal
record](https://doi.org/10.1016/j.ejc.2006.03.002) concerns powers of cycles
and their complements and establishes Hadwiger's conjecture there, rather
than the all-component exact classification.

A bounded exact-phrase and structural search also located tabulated formulas
for individual path complements, but no primary source stating the complete
mixed-component formula with these eight exceptional cores.  This supports
only the target's search-relative novelty wording; it does not establish
historical priority.

## Strengthening and improvement opportunities

- Replace the Dirac invocation with a short direct lemma: if \(F\) is a
  disjoint union of paths and cycles, then \(\overline F\) has a matching of
  size \(\lfloor |V(F)|/2\rfloor\) except for \(K_2,K_3,K_3+K_1\).  Proving
  this componentwise or from Tutte's theorem would make the central boundary
  reusable and the proof entirely tailored to the class.
- State the construction algorithmically.  Building \(S\) and \(F\), finding
  the residual matching, and emitting branch sets gives a polynomial-time
  certificate algorithm; a direct componentwise matching lemma could reduce
  this to linear time after the component decomposition.
- The theorem and clique-partition formula immediately give the exact gap
  \(\eta(\overline H)-\chi(\overline H)\).  Classifying equality in Hadwiger's
  inequality for this class would be a clean corollary, with the eight
  exceptional adjustments handled separately.
- Extending the method to \(\Delta(H)=3\) would require a new structural
  replacement for the degree-two forbidden graph and a classification of its
  matching obstructions; simply enlarging the finite audit would not close
  that gap.

## Reproducibility and limits

Run `./run_checks.sh` in this directory with standard-library Python 3.11 or
later.  The exact branch-partition audit takes about five seconds in the
review environment.  It is not a formal proof of the unbounded component
reduction or Dirac's theorem and does not certify exhaustive bibliographic
priority.  No external solver, floating-point arithmetic, dataset, or omitted
large certificate is used.
