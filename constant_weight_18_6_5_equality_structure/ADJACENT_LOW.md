# Adjacent degree-two points: deficits two and three are excluded

Author: six-code-1, researcher. Date: 2026-09-30.

Let \(F\) be a family of five-subsets of an 18-set, with distinct
members intersecting in at most two points. Write \(r_x\) for point
replication, \(d_{xy}\) for pair multiplicity, and \(t_{xy}=5-d_{xy}\).
The deficit support joins \(xy\) when \(t_{xy}>0\); its degree at
\(x\) is \(k_x\).

**Computer-assisted theorem.** If \(|F|=72\) and \(k_u=k_v=2\),
then \(t_{uv}\) is neither two nor three. Together with
[SUPPORT16.md](SUPPORT16.md), an adjacent degree-two pair could only
have edge weight four. The complementary six-code-3
[saturated single-pair theorem](../coding_theory/a18_6_5_saturated_single_pair/PROOF.md)
excludes that weight. Combining these results, the support-degree-two
points form an **independent set of size at most two**.
The degree-one/zero-pair case is outside
this adjacency theorem; the complementary
[saturated absent-pair theorem](../coding_theory/a18_6_5_saturated_absent_pair/PROOF.md)
excludes that case at size 72. It is context, not a premise here.
No \(h\ge17\) conclusion or numerical
improvement of \(69\le A(18,6,5)\le72\) is claimed.

The weight-two exclusion is ordinary mathematics. Only the
distinct-anchor weight-three case uses finite computation.
The local statements below require only saturation of \(u,v\),
and are stronger than a restriction to exactly two low-degree points.

## 1. Saturated links and the local conclusions

Every \(d_{xy}\le5\): the three-point remainders of blocks on a
fixed pair are disjoint. At a point with \(r_x=20\), the deficit
row sums to five. Its shortened quadruple packing leaves sixteen
pairs, with leave degree \(1+3t_{xy}\) at \(y\).

If \(k_x=2\), its leave is a double star with centers equal to its
two support neighbors. The centers are adjacent; every other point
has exactly one leave edge to a center. See [PROOF.md](PROOF.md)
and the ordinary merge proof in [AFFINE_SPLIT.md](AFFINE_SPLIT.md).
Merging the centers gives an affine plane of order four. The full
historical uniqueness argument is supplied in
[AFFINE_NORMALIZATION.md](AFFINE_NORMALIZATION.md).

Assume \(r_u=r_v=20\), \(k_u=k_v=2\), and \(t_{uv}=w\),
where \(w\in\{2,3\}\). Let their other support neighbors be
\(a,b\), respectively. The endpoint deficits to those anchors
are \(5-w\). Our local conclusions are:

* For \(w=2\), distinct anchors are impossible. If \(a=b\),
  the common anchor has replication at most seventeen.
* For \(w=3\), a common anchor has replication at most eighteen.
  If the anchors differ, each has replication at most nineteen.

These are upper restrictions, not assertions that their endpoints
are attainable. Brouwer's established \(A(17,6,4)=20\) gives
\(r_x\le20\) in any packing under discussion. At size 72,
\(\sum r_x=360\) forces every replication to be twenty, contradicting
each alternative above. The local conclusions themselves do not
import Brouwer's theorem: \(r_u=r_v=20\) are their hypotheses.

## 2. The weight-two block conflict

Suppose \(w=2\) and \(a\ne b\). Let \(W\) be the seven
leave thirds on \(uv\); it contains both \(a,b\), since the
two double stars force \(uva,uvb\) to be leave triples. Put
\(D=W\setminus\{a,b\}\), of size five.

In the double star at \(u\), a point other than its centers
\(v,a\) has exactly one uncovered pair to those centers.
Consequently the covered thirds on \(ua\) are precisely
\(W\setminus\{a\}=\{b\}\cup D\). The two blocks on \(ua\)
partition these six points into triples. Write them as
\[
\{a,u,b,p,q\},\qquad \{a,u,r,s,t\},
\quad D=\{p,q,r,s,t\}.
\]
Likewise, the covered thirds on \(vb\) are
\(W\setminus\{b\}=\{a\}\cup D\). In particular its block
containing \(a\) has the form \(\{a,b,v\}\) plus two points
of \(D\).

Neither chosen point can be \(p\) or \(q\), since that would
give a three-point intersection with the first \(ua\)-block.
Both must therefore lie in \(\{r,s,t\}\), giving a three-point
intersection with the second block. This contradiction uses no
assumption on the support degrees of the other sixteen points.

The checker also verifies the conflict for all ten labeled choices
of \(\{p,q\}\) and all ten possible two-point tails, 100 cases.
This is auxiliary validation; the ordinary proof is complete above.

## 3. Common anchors give elementary replication bounds

Now let \(a=b\). The leave thirds on \(uv\) form a set \(W\)
of size \(1+3w\), including \(a\). There are \(15-3w\)
other points outside \(W\). The double stars imply that for every
such point \(x\), both \(aux\) and \(avx\) are leave triples.
Thus \(d_{ax}\le4\): multiplicity five would leave just one
third on \(ax\). The remaining \(3w\) points have multiplicity
at most five with \(a\), while \(d_{au}=d_{av}=w\).
Therefore
\[
4r_a=\sum_{y\ne a}d_{ay}
 \le 2w+4(15-3w)+5(3w)=60+5w.
\]
For \(w=2\) this gives \(r_a\le17\); for \(w=3\),
\(r_a\le18\). No plane classification or computation is used.

## 4. Normalize the distinct-anchor weight-three case

Assume \(w=3\), \(a\ne b\). At \(u\), the two centers
\(v,a\) have shortened replications two and three. Merge them
to the origin of the affine plane. Its two \(v\)-assigned
directions can be sent to the axes of \(\mathbb F_4^2\).
The forced leave \(uvb\) places \(b\) on an \(a\)-assigned
origin line. Both its coordinates are nonzero; diagonal scaling
sends it to \((1,1)\). This gives the universal labeling
\[
u=17,\quad v=0,\quad a=16,\quad b=5=(1,1).
\]
Field points have labels \(4x+y\), with field labels
\(0,1,2,3\) and \(\omega^2=\omega+1\).
The twenty words through \(u\) are the twenty field lines plus
\(u\), with origin zero kept on the two axes and replaced by
\(a=16\) on the other three origin lines. All configurations
with distinct anchors are covered by this relabeling. There is
no global automorphism assumption on \(F\).

At \(v\), merging its centers \(u,b\) also gives an affine
plane. Its two \(u\)-words are fixed by the first star:
\[
\{u,v,1,2,3\},\qquad\{u,v,4,8,12\}.
\]
The covered thirds on \(vb\) are the other nine points
\[
C=\{6,7,9,10,11,13,14,15,16\}.
\]
Indeed the leave thirds on \(vb\) are \(u\) and the six
nonorigin axis points. The three \(vb\)-words partition \(C\)
into triples. There are exactly
\(9!/(3!^3 3!)=280\) unordered partitions. Of their 84 possible
triples, 39 form words compatible with the fixed \(u\)-star;
exactly 24 complete partitions survive. Every partition is checked.

For a surviving partition, the five known \(v\)-words give five
origin triples partitioning the fifteen-point set
\[
H=\{0,\ldots,17\}\setminus\{u,v,b\}.
\]
The other fifteen shortened \(v\)-quadruples use only \(H\)
and cover precisely the 90 pairs between those five groups of
size three. Include every four-subset of \(H\) whose pairs are
prescribed and whose word with \(v\) is compatible with every
\(u\)-word. Exact pair covers enumerate every possible second
star. Across all 24 partitions there are exactly **sixteen**.
The manifest gives their actual fifteen nonorigin quadruples,
not only an aggregate count. These are labeled normal forms,
not a claim of sixteen inequivalent global codes.

## 5. A point-capacity bound excludes a saturated external anchor

Fix any one of those sixteen compatible second stars. Their union
with the first star has 38 words and fixes eight words through
\(b\): five through \(ub\) and three through \(vb\).
These two groups are disjoint because \(uvb\) is in the leave.
Every further word through \(b\) avoids \(u,v\). Its remaining
four-set lies in \(H\) and must meet each of the 38 fixed words,
after \(b\) is restored, in at most two points. Enumerating all
\(\binom{15}{4}=1365\) four-sets therefore gives the complete
necessary candidate set \(Q\).

Let \(G_Q\) have precisely the pairs appearing in some candidate
quadruple. If \(m\) candidate quadruples are chosen with disjoint
pair sets, every chosen quadruple through \(x\) uses three
distinct incident pairs of \(G_Q\). Hence it contributes at most
\(\lfloor\deg_{G_Q}(x)/3\rfloor\) to the point replication, and
\[
m\le \left\lfloor\frac14
   \sum_{x\in H}\left\lfloor\frac{\deg_{G_Q}(x)}3\right\rfloor
   \right\rfloor.                                      \tag{1}
\]
Pair disjointness is necessary because the full words share \(b\).
This is an ordinary inequality applied to the complete finite
candidate universe; no packing optimization is needed.

The exact results are:

| Candidate quadruples | Capacity bound in (1) | Second stars |
|---:|---:|---:|
| 30 | 9 | 2 |
| 30 | 10 | 4 |
| 29 | 11 | 4 |
| 34 | 11 | 6 |
| Total | at most 11 | 16 |

Thus \(r_b\le8+11=19\) in every case. Interchanging \(u,v\)
gives the same bound at \(a\). These are necessary upper bounds;
the table does not assert that each capacity is attained.

## 6. Completeness and a different replay

`check_adjacent_low.py` builds the first plane over \(\mathbb F_4\),
enumerates all 280 origin partitions, and enumerates every exact
cover of the second star's 90 prescribed pairs. At each recursion,
choose an uncovered pair and branch on every active quadruple
containing it. Selecting that quadruple removes exactly the
columns intersecting its used pairs. Every possible cover has one
of those branches; induction on uncovered pairs proves the covering
argument. No quotient or heuristic filter is used in this search.
Every returned cover and the resulting two-star packing are checked
directly before the anchor bound is calculated.

`verify_adjacent_low.py` instead builds the first plane from the
twelve even permutation graphs on a four-by-four array. It uses
Gosper fixed-weight masks and XOR Hamming distances for candidates.
It enumerates complete relative field planes, rather than solving
the pair-cover problems. The normalization is checked as follows.

Enumerate all 180 nonsingular two-by-two matrices over \(\mathbb F_4\)
and both field-automorphism choices. Check all 360 distinct induced
point permutations and every image of all twenty plane lines.
Their action on the five origin directions gives every one of the
120 permutations, each three times. The direction kernel has three
elements and acts transitively on the three nonorigin points of the
first direction. These are actual map and line checks, not assumed
automorphism-group orders.

For an arbitrary second plane, historical uniqueness supplies an
isomorphism to the field plane. Compose with one of the checked
maps to align its five ordered origin triples with the five field
directions. Then a direction-kernel map fixes the image of the least
point in its first triple. All remaining bijections are exactly
\(2(3!)^4=2592\) assignments. Enumerating these and checking their
distinct line sets covers every second plane for each partition.
No row/column agreement between the two planes is imposed. The
replay checks all 62,208 normalized planes across the 24 partitions,
again finds the sixteen second stars, and obtains the same anchor
candidate sets and degree bounds.

With `--compare-primary`, every initial pair row and candidate column,
every one of the sixteen second stars, and every anchor candidate
quadruple is compared entry by entry between the two methods.
The primary exact-cover and capacity routines are also compared with
direct brute force on all 1,100 simple graphs of order at most five.
The known affine plane is a positive cover fixture. Two malformed
stars are rejected by their mathematical validator, independently
of expected-output hashes. These checks are algorithmic validation
by this researcher, not independent peer review.

Run from the repository root, CPython 3.11.2 or compatible Python3,
standard library only, one process and thread:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B constant_weight_18_6_5_equality_structure/check_adjacent_low.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B constant_weight_18_6_5_equality_structure/verify_adjacent_low.py --compare-primary
```

`adjacent_low_expected.json` records the sixteen second stars and
their checked capacity data, plus compact replay counts and hashes.
It is a replay manifest, not a standalone nonexistence certificate.
Either a 200,000-node or ten-second per-case primary cap, or a
ten-second per-case replay cap, raises `INCOMPLETE`; an unfinished
run proves no exclusion. No cap was reached in successful checks.

## 7. Consequence and trust boundary

At size 72 every point has replication twenty, by the imported
Brouwer theorem. All the weight-two and weight-three alternatives
above are therefore impossible. The preceding sixteen-point
support lemma leaves at most two degree-two vertices. An edge of
weight one between them would force their other support neighbors
to be distinct degree-two vertices: each receives weight four,
and a saturated weighted row of five then has only one other edge.
That would give four degree-two vertices. A weight-five edge would
itself exhaust each endpoint's row, giving support degree one.
Thus only weight four can
join the remaining pair.

The separately published saturated single-pair theorem of six-code-3
gives \(|F|\le56\) if two replication-twenty points have pair
multiplicity one. A weight-four deficit is exactly that situation.
Importing this additional theorem therefore excludes the remaining
adjacency: the degree-two vertices are independent and number at
most two. This joint corollary adds a dependency on the cited
single-pair theorem; our local replication bounds and the main
weight-two/weight-three exclusions do not use it.

The main adjacency exclusions depend on the written double-star,
merge, uniqueness, normalization and completeness bridges and the
exact finite computations. The global implication imports Brouwer's
point bound. The final at-most-two carrier corollary additionally
imports SUPPORT16, with its explicit transitive Rees--Stinson
dependency. The earlier SUPPORT16 theorem has an
[independent review](../constant_weight_18_6_5_support16_review5/REVIEW.md).
That review predates and does not verify these new adjacency exclusions.
The independent-set corollary additionally imports the separate
saturated single-pair theorem, source commit
`8321eee86a06b25634651516e22d1fcbd8b76902`.
The new theorem is not formalized or independently reviewed.
There is no solver verdict, floating-point proof, timeout inference,
large omitted proof corpus or global 72-code enumeration. No
historical-priority claim is made. The 47-type individual-link
carrier is unchanged.

Primary context: Brouwer (1975), report ZW62/75,
<https://ir.cwi.nl/pub/6883/6883D.pdf>; historical affine uniqueness
in Bishnoi (2012), Theorem3.6,
<https://anuragbishnoi.wordpress.com/wp-content/uploads/2014/09/report21.pdf>;
and the maintained 69--72 table, rechecked 2026-09-30,
<https://aeb.win.tue.nl/codes/Andw.html>.
The Rees--Stinson theorem used by the earlier support-size chain is
Lemma3.5 (1987), <https://cs.uwaterloo.ca/~dstinson/papers/J69.pdf>.
