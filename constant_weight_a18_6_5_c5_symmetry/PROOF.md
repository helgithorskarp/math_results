# Symmetry exclusion and matching construction

Agent: **six-code-2**. Role: **researcher**. Date: 2026-09-30.

Let \(V=\{0,\ldots,17\}\). A packing is a family \(F\subseteq\binom V5\)
whose distinct members meet in at most two points. Let

\[
g=(0\ 1\ 2\ 3\ 4)(5\ 6\ 7\ 8\ 9)(10\ 11\ 12\ 13\ 14),
\qquad G=\langle g\rangle.
\]

**Claim.** The largest \(G\)-invariant packing has 68 members. In
particular, every packing with at least 69 members lacks an automorphism
of cycle type \(5^3 1^3\).

This is a finite computer-assisted result with an ordinary mathematical
coverage argument. It does not change the unrestricted 69--72 bounds.

## 1. Imported point bound and reduction to fourteen full orbits

We use A. E. Brouwer's established theorem
\(A(17,6,4)=20\), proved in [report ZW62/75, December 1975](https://ir.cwi.nl/pub/6883/6883D.pdf),
particularly its abstract and Section 2. This theorem is imported, rather
than reproved by our code. Deleting a point common to all words through
it gives a length-17 weight-four code of minimum distance at least six.
Thus every point replication \(r_p\) in \(F\) is at most 20, and

\[
5|F|=\sum_{p\in V}r_p\le360,\qquad |F|\le72.
\]

Every block orbit has size one or five. A fixed five-subset must be a
union of point cycles, so the only three fixed blocks are the three
moving five-cycles. If \(f\) fixed blocks and \(m\) full orbits are used,
then \(|F|=5m+f\), with \(0\le f\le3\). Size 69 is impossible modulo
five. Sizes 70, 71 and 72 have \(m=14\), with \(f=0,1,2\), respectively.
Deleting their fixed blocks would give a packing of exactly fourteen
full orbits, hence 70 words. It suffices to exclude that case.

## 2. A fixed point must have replication 20

In a family consisting of fourteen full orbits, each of the three fixed
points 15, 16 and 17 has replication divisible by five. If all three had
replication at most 15, then

\[
350=5|F|\le15\cdot20+3\cdot15=345,
\]

a contradiction. One fixed point therefore has replication 20. A
permutation of the fixed points commutes with \(g\), so it may be labeled
17. The words through 17 are four full block orbits. They are a
20-word packing, and every pair of those words intersects in at most two.

## 3. Complete link enumeration and normalization

`verify.py` enumerates all \(\binom{18}{5}=8568\) point tuples and their
orbits under \(g\). The raw census is three fixed orbits and 1713 full
orbits. Direct pair intersections within each full orbit leave exactly
1125 internally admissible full orbits. Exactly 230 contain point 17.
Because 17 is fixed, either every word in an orbit contains it or none
does.

On those 230 vertices, an edge means that *every* cross-orbit word pair
intersects in at most two points. Four compatible orbits are precisely
the four-cliques of this graph. The verifier enumerates all of them by
their unique increasing sequence \(a<b<c<d\): for every adjacent pair
\(a<b\), it considers every common neighbor \(c>b\), and then every
common neighbor \(d>c\) also adjacent to \(c\). This covers every
four-clique once and excludes no possible 20-word link. There are **100**.

The verifier next builds seven explicit point permutations: independent
rotations of each moving cycle, exchanges of the first and second and
of the second and third moving cycles in aligned positions, simultaneous
multiplication of the five positions in each moving cycle by two modulo
five, and interchange of fixed points 15 and 16. Each fixes 17. For
each permutation \(h\), the verifier checks directly that
\(hgh^{-1}\in\{g,g^2\}\). Consequently each permutation normalizes \(G\),
preserves intersections, and permutes the possible links.

Breadth-first closure of a representative link under these seven
permutations reaches all **100** enumerated links. This proves
equivalence under a checked subgroup of the normalizer; a classification
of the full normalizer is unnecessary. The representative is the
lexicographically first four-clique, with global admissible-orbit indices
**85, 484, 1009, 1098**, starting at zero. Orbits are ordered
lexicographically as sorted tuples of sorted point tuples, as specified
in the source. No assumptions about an unknown link's geometry are used.

As an extra check, every link has old-point replication profile
\((0,5,\ldots,5)\). This property is an output of the complete enumeration,
rather than a filtering assumption.

## 4. Complete residual graph and certificate inference

For the representative's twenty words, the checker retains every one
of the 1125 admissible full orbits compatible with *all* those words.
Exactly **159** remain; direct checking shows that all avoid point 17.
Their compatibility graph has **4992** edges. Ten further full orbits
would be necessary to reach fourteen, so such a completion would give
a ten-clique in this precise graph.

`certificate.json` certifies that no ten-clique exists. Its 223 nodes
are checked without a search engine. At a node with candidate set \(P\)
and required clique size \(q>0\), either:

1. A cardinality leaf verifies \(|P|<q\); or
2. Explicit nonempty color classes partition exactly \(P\). Every pair
   in each class is checked to be nonadjacent. Number the classes
   \(1,\ldots,c\). For every vertex in classes \(q,\ldots,c\), in the
   certificate's reverse order, a child verifies the absence of a
   \((q-1)\)-clique among the current candidates adjacent to that vertex.
   The selected vertex is then removed. Finally the remaining candidates
   are contained in the first \(q-1\) independent classes, which cannot
   contain a \(q\)-clique.

These children cover all possibilities for a clique that contains any
of the processed vertices: take the first processed vertex in that
clique. A clique avoiding them all lies in the verified residual color
classes. Candidate sets are computed by the checker, rather than trusted
from the certificate. Missing branches, nonindependent classes and
incomplete partitions are rejected. Reaching \(q=0\) is rejected, since
it would mean a target clique has been completed.

Induction on the checked tree therefore proves the root's no-ten-clique
claim. This excludes the representative link's completion and, by
normalization, every possible link. Sections 1 and 2 then exclude every
\(G\)-invariant packing of size at least 69.

## 5. Matching classical 68-word construction

`witness68.txt` has 68 distinct weight-five words. The checker verifies
all 2278 pair intersections and checks that applying \(g\) preserves the
set. This establishes the matching lower bound with no construction
algorithm in the trust boundary.

The fixture comes from the classical inversive-plane \(S(3,5,17)\), with
an unused eighteenth point. In the earlier [Steiner source](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_a18_6_5_steiner_trade_bound/steiner.py),
the 68 circles are the projective linear images of
\(\operatorname{GF}(4)\cup\{\infty\}\) in
\(\operatorname{PG}(1,16)\), using the field polynomial \(x^4+x+1\).
Multiplication by the order-five element \(2^3\) fixes zero and infinity
and has three moving cycles. The old-to-new coordinate permutation is

```text
15 0 5 6 10 12 11 8 1 14 3 7 2 9 13 4 16 17
```

This identifies that classical action with the canonical \(g\) above.
The fixture is a reproduced known construction, not a new 68-word code.

## Status, literature and reproducibility boundaries

[Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html), checked
live 2026-09-30, records \(69\le A(18,6,5)\le72\). The unrestricted
69-word construction is due to Aw, Chee and Ling (2003). Orbit-based
clique reductions are classical; see Smith and Montemanni,
[Some constant weight codes from primitive permutation groups](https://doi.org/10.37236/2702),
Electronic Journal of Combinatorics 19(4) (2012), P4. Their reported
primitive-group range is 29--63, distinct from this prescribed action on
18 points. Targeted searches did not locate an earlier statement of
this exact symmetry maximum; that limited search does not establish
historical priority.

The new finite result is the complete exclusion for this specified
cycle type, with a separately checked compact certificate. The point
bound and lower construction are credited external/classical results.
The written mathematical coverage arguments have not been formalized.
The checker was written separately from the integer triple-incidence
generator and imports none of its code or data models. This is method
separation by the same researcher, not an independent peer review.

No conclusions are drawn about other order-five cycle types, codes
without this symmetry, failure of heuristic searches, or global
nonexistence of 70 words. See `README.md` for exact commands and
`expected.json` for output and SHA-256 values.
