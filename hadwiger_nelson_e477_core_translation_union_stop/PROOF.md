# Proof outline

Let `E` be the pinned 477-point physical support and let `C` consist of its two
marked terminals together with the 253 labels appearing in the reviewed
deletion-witness list.  Hence `|C|=255`.

For each ordered pair of distinct points `p,q` in `C`, form the exact
coefficient difference `q-p`.  If a nonzero translation `t` occurs `m` times,
then exactly `m` points lie in `C intersect (C+t)`: every occurrence is a
unique pair `p,p+t`, and conversely every intersection gives one occurrence.
The complete difference multiset has maximum multiplicity 75 at exactly two
translations.  Its lexicographically first member is `(-3,3,3,3)`.

Consequently the frozen union has `255+255-75=435` physical points.  Exact
radical arithmetic tests every unordered pair and finds 1,589 unit pairs.
Mapping each of the 659 core edges into both copies and taking their set-union
gives 1,231 inherited physical edges.  The remaining 358 complete unit edges
are additional contacts.  Thus the graph is neither a disjoint-copy product
nor a member of the one-overlap/sole-cross-edge E477 spindle family.

The certificate assigns one of four colours to every physical point.  Direct
comparison on all 1,589 edges verifies properness, so `chi <= 4`.  The seven
specified labels in the first copy induce the eleven-edge Moser spindle.
Enumeration of all `3^7` named words finds no proper three-colouring, so
`chi >= 4`.  Therefore the complete strict physical graph has chromatic number
exactly four and cannot improve the five-chromatic vertex record.
