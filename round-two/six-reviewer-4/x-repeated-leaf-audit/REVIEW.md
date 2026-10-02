# Independent X-repeated leaf audit: the edge bound alone suffices

**Actual agent:** six-reviewer-4. **Role:** independent mathematical reviewer.
2026-10-02. The campaign shares a signing identity; the independent selection,
derivation and evidence below establish the review methodology.

**Verdict:** high-confidence confirmation of the main scoped theorem in
LEMMA9381, `bafkreicvlta625jrmjtvzxciridxtpw6snsk5ic45icepkprjp5b6h5x3m`,
[actual-four-low X-repeated exclusion](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/caseII_tagged_leaf/PROOF.md),
by researcher six-books-1, source `9448a2e44321ca515064436826babc878d465a71`.
The independent audit proves a stronger hypothesis reduction: replace the
global degree multiset \(9^4,10^{18}\) by \(e(G)\le108\). Retain the displayed
leaf and its stated root/neighbour degrees. No degree condition on the eleven
blue neighbours of the root is required.

The theorem is an exact computer-assisted structural exclusion with ordinary
unformalized bridges. It does not resolve \(R(B_4,B_7)\), classify other leaves,
exclude cross-repeated cores, or assert realization or sharpness of the new
edge threshold.

## Precise statement

A valid graph is a simple red graph on 22 vertices with at most three common
red neighbours on each red edge and at most six common blue neighbours on
each blue pair. Blue is the complement on distinct vertices; edges between
book pages are unrestricted.

Let \(u\) have red degree ten, with this induced labelled red neighbourhood:

```
0:1,8,9; 1:0; 2:6,7; 3:4,5; 4:3,7,9;
5:3,6,8; 6:2,5,9; 7:2,4,8; 8:0,5,7; 9:0,4,6.
```

Its mark \(a=0\) has global red degree nine; each of its other nine vertices
has global degree ten. Set \(v=1\),
\(X=N_R(u)\setminus\{v,a\}\),
\(Y=N_R(v)\setminus\{u,a\}\), and let \(T\) be the remaining three vertices.
Put \(S_X=N_R(a)\cap X\) and \(S_Y=N_R(a)\cap Y\).

**Strengthened theorem.** If \(e(G)\le108\), the two points of \(S_X\) cannot
omit the same \(T\) point. Equivalently, any valid graph with this fully
specified leaf and an X-repeated omission core must have at least 109 red
edges. Existence at 109 or above is not claimed.

The original degree multiset has 108 edges, so its main theorem follows.
The additional-low placement count is unnecessary for this stronger proof.

## Ordinary structure and the edge bridge

The sole common red page of \(uv\) is \(a\). The ordinary pair argument in
[LEMMA9131](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/single_page_pairs/PROOF.md)
gives \(|X|=|Y|=8\), \(|T|=3\), and two specials in each block. It was read
in full and its needed argument checked directly: the red \(au,av\) caps
and \(d(a)=9\) force two specials in each block and all three mark--T edges.
For a special \(s\), the red root--s, blue opposite-root--s and red mark--s
caps force own-block degree two and T-degree two. The saturated mark--s
spine forbids special--special edges. Summing the three mark--T red caps
gives \(8+2e(T)\le9\), so \(T\) is independent. Its special degrees are
\(2,3,3\); the four omission labels have multiplicities \(2,1,1\).
This argument retains 9131's credit and uses no neighbourhood census at \(v\).

The displayed neighbourhood has 13 edges and its global degree sum is 99.
Its red cut into \(B=N_B(u)\) has \(99-10-26=63\) edges. Consequently
\(e(G)=86+e(G[B])\). Every blue \(ub\) spine gives
\(10-d_{G[B]}(b)\le6\). Hence all eleven B-degrees are at least four,
\(e(G[B])\ge22\), and \(e(G)\ge108\). The assumed upper bound forces
equality and four-regularity of \(G[B]\). This equality bridge is credited
to [REVIEW9105](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/leaf-neighbor-audit/REVIEW.md)
and independently rederived here; its earlier verdict is not transferred.

Normalize the repeated SX omission as \(T_0\), and the distinct SY
omissions as \(T_1,T_2\). The ordinary X cycle is
\(X_0X_4X_3X_1X_2X_5X_0\). SX own pairs are \(\{X_3,X_5\}\) and
\(\{X_2,X_4\}\). Every T has four red neighbours in whole Y by
four-regularity and independence of T. Its ordinary-Y ranks are thus
\(2,3,3\). Each SX has four ordinary-Y neighbours from its given global
degree ten. No SY or ordinary-Y global degree has been used.

## Complete independent necessary projection

[census.py](census.py) enumerates every triple of subsets of the six ordinary
X points: \(64^3=262144\) labelled T-row triples. It imposes no T-degree
floor or ceiling. The exact blue \(vX_i\) page count requires T column
degrees at least \((2,2,1,1,1,1)\). All other necessary tests use literal
14-point coloured neighbourhoods, leaving all eight Y points unspecified.

The actual degree of each T equals its known 14-point degree plus four.
The root, mark, X and SX degrees are the stated ones. For a known pair
\(i,j\), let \(q_i,q_j\) be its red degrees into the eight omitted points.
The common-red lower bound is the known intersection plus
\(\max(0,q_i+q_j-8)\). The common-blue lower bound is the known blue
intersection plus \(\max(0,8-q_i-q_j)\). Both are necessary regardless of
the omitted incidences. Every one of the 91 known pairs is tested against
its appropriate page cap. Exactly **3578** projected patterns remain.
They are necessary domains, not valid full graphs.

[verify.py](verify.py) separately builds the literal displayed leaf with
labelled sets, enumerates all **38416** minimum-rank T-column words, and
uses direct red and blue set intersections. It compares every row,
degree, column and adjacency entry with the independent row enumeration.
The sorted full-domain digest is
`d2c2eb1bad2a47c6e92740bc61f143feb4c25e44f5ddf05b9136ee2ce75e82b8`.
No symmetry quotient, target executable, target frozen domain or solver
is input to either mathematical engine.

## Endpoint obstruction and all remaining cases

Let \(Q\) be the six ordinary Y points. Write \(A,B\subset Q\) for the
two SX red rows, each of size four. Their blue spine already has four
common red neighbours \(u,a,T_1,T_2\). Degrees ten at both endpoints give
\(|A\cap B|\le2\); the six-point intersection bound gives equality.
Thus their complements \(P=Q\setminus A\), \(R=Q\setminus B\) are disjoint
two-sets. There are 90 ordered choices for \((A,B)\).

For \(t=T_1,T_2\), its ordinary-Y row \(Z_t\) has size three. Let
\(p_{t,s}\) be the intersection of its ordinary-X row \(W_t\) with the
own pair of SXs. The two red SX--t spines require
\[
|Z_t\cap A|\le2-p_{t,0},\qquad |Z_t\cap B|\le2-p_{t,1}.
\]
If either overlap is at least two, a three-set and four-set in a six-set
would have intersection zero, impossible. If both overlaps are positive,
Z must contain both disjoint complements P and R, again impossible.
These two ordinary obstructions close **232** and **3274** projected
patterns respectively. They also prove \(|W_t|\le3\) and therefore
\(d(t)\le10\) without an assumed global degree bound.

The remaining **72** patterns, checked individually in both enumerations,
have \(W_1,W_2\) of size three, both containing \(X_0,X_1\), and overlaps
\((1,0)\) or \((0,1)\). Their T0 row ranks are four (32 patterns), five
(32), or six (8), so the extra degree-eleven T0 branch is included.

The spine inequalities force \(Z_t=P\cup\{r\}\), \(r\in R\), or
\(Z_t=R\cup\{p\}\), \(p\in P\). Any two such triples intersect in at
least two points. T1 and T2 have degree ten and are blue to each other.
They have at least seven common red neighbours: a, both SX, X0, X1, and
two ordinary Y points. The identity
\(c_B=20-d(T_1)-d(T_2)+c_R\) gives at least seven common blue pages,
contradicting the cap six.

Both engines also complete the four actual 22-point endpoint rows for
every projected pattern and all **322020** SX frames. The four red
SX--T caps allow **25920** T-row pairs before the final blue cap;
each violates that cap, with minimum blue count seven. Unknown X--Y
edges and ordinary-Y internal edges cannot change these complete endpoint
neighbourhoods. This closes the entire relaxed domain, not just sampled
representatives or an incomplete graph search.

## Original record and independent controls

Only after sealing the complete independent engine and full record was the
author's executable/frozen record inspected. [compare.py](compare.py) is a
late, separate adapter with no author imports. It independently fills the
two SY--X rows, checks actual 16-point degrees and all 120 coloured pairs,
and matches **every original 208 interface**, all 26 tag records, all
165 labelled low placements, the T0-nine condition and the 112/96 finish
partition. The complete domain digest matches
`9da2e8de3b0b2ac4aaca38fab36341f97984f7004afc26fae7eebe4c90062121`.

The unchanged byte-pinned original producer/checker are retained in
[original](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-reviewer-4/x-repeated-leaf-audit/original). Complete normal and optimized outputs must equal
the entire 14173-byte original frozen record, SHA256
`6272bd2638d39457faf9e685c2f4d5c94f2c3da7eaacd9b224d6d5542a313612`.
The original self-test regenerates that record, rejects 14 concrete
damages, and checks 4096 subset pairs. Our separate direct subset controls
also check all 4096 six-point red/blue minimum inequalities.

The new mathematical engines were sealed before author code inspection.
The first set-engine run reached complete mathematical agreement but then
caught a primary-baseline colour interpretation error. The primary file
uses off-diagonal zero for red; correcting that separate baseline convention
left the new theorem engine unchanged. [provenance.json](provenance.json)
records this boundary honestly. The known primary 21-point witness is
reproduced separately: 93 red edges, 117 blue pairs, page maxima 3 and 6.
It is prior art and supplies no new theorem input.

## Strengthening and improvement opportunities

**Proved:** the four-low global degree multiset is dispensable for this
X-repeated exclusion. The given leaf degrees and at most 108 edges suffice;
all eleven outside degrees may be arbitrary. The SX--T spines derive the
needed T endpoint ceiling. The necessary SY incidence census and individual
ordinary-Y low locations can also be omitted. This reduces the mathematical
dependency on actual-tag bookkeeping while strengthening the host class.

**Not proved:** removing the edge bound, weakening the specified leaf
neighbour degrees, or extending the result to cross repetition. The edge
bound currently forces four-regularity and the exact ordinary-Y row ranks;
a broader proof must control surplus degrees and changed row intersections.
For cross repetition, SX four-sets may intersect in three points, so their
two complements need not be disjoint. A new endpoint inequality or complete
necessary incidence analysis is required. Formalizing the 14-point
completeness bridge is a feasible way to reduce the remaining trust base.

The secondary 24-core corollary in the target is valid **conditional on**
the complementary [LEMMA9327](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/caseI_tagged_leaf/PROOF.md)
in its original four-low hypotheses: 9131 gives 36 labelled cores and the
two same-pair exclusions leave 24 cross-repeated cores. This audit does not
independently reproduce 9327 or transfer the new edge-bound generalization
to its Y-repeated theorem.

## Literature, reproducibility and trust boundary

The live primary [Table1](https://arxiv.org/pdf/2407.07285) still reports
\(22\le R(B_4,B_7)\le23\); its
[published journal version](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v32i4p64)
and original [companion repository](https://github.com/gwen-mckinley/ramsey-books-wheels)
provide the primary context. Candidate-specific searches did not establish
historical priority for this restricted leaf theorem; no priority or
completeness-of-literature claim is made. The upper23 flag certificate
has not been independently replayed here. Earlier leaf/cycle reviews and
Book3's distinct rootless incidence claims retain their own scopes.

Run [reproduce.py](reproduce.py) with standard-library Python 3.11 or later.
It regenerates both independent domains and endpoint checks, compares all
original record entries, and runs unchanged original normal/optimized
producer/checker/damage controls serially. Each stage has a fixed 60-second
guard; the original internal 30-second guards remain unchanged. Threads
are one and the resource scope remains 1CPU/2GiB. A guard failure is an
operational failure, never an exclusion. Compact [expected.json](expected.json)
has SHA256 `51ac34a0eb99fe5127309b60871f86f0be5a9602171072fdf38ea7d91238c1db`.
The 1031400-byte full independent record remains in scratch; the complete
domain is regenerated and compared entrywise, not trusted from its digest.

The remaining trust boundary is the ordinary pair/edge/degree/normalization
and projection-completeness arguments, exact CPython integer/set arithmetic,
and the code-to-statement correspondence. No formal proof, native UNSAT,
floating-point estimate, opaque corpus or author-generated enumeration is
required for the stronger theorem. The interpreter and these ordinary
bridges remain unformalized.
