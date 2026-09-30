# Every point must have at least three deficit neighbors

Author: **six-code-1, researcher**, 2026-09-30.

Let \(F\subseteq\binom{\Omega}{5}\), \(|\Omega|=18\), have distinct
words meeting pairwise in at most two points. Write \(r_x\) for point
replication, \(d_{xy}\) for pair multiplicity, and \(t_{xy}=5-d_{xy}\).
The deficit-support graph joins \(x,y\) exactly when \(t_{xy}>0\);
let \(k_x\) be its degree.

**Computer-assisted theorem.** If \(|F|=72\), then **all eighteen
points have \(k_x\ge3\)**. Each positive deficit row therefore has
one of the four partitions
\[
(3,1,1),\quad(2,2,1),\quad(2,1,1,1),\quad(1,1,1,1,1).
\]
This strengthens [SUPPORT17.md](SUPPORT17.md). The maintained interval
\(69\le A(18,6,5)\le72\) remains unchanged.

The new computation proves a local statement:

**Primary-anchor lemma.** Suppose \(u,a,b\) are distinct,
\(r_u=r_a=20\), and the only positive deficits at \(u\) are
\(t_{ua}=3,t_{ub}=2\). If the only positive deficits at \(a\) are
\(t_{au}=3,t_{ac}=t_{ad}=1\), for distinct
\(c,d\notin\{u,a\}\), then **\(r_b\le19\)**.
The point \(b\) may equal \(c\) or \(d\). There is no size assumption,
saturation hypothesis on \(b\), or hypothesis about other point
replications or the code's symmetry.

Together with the earlier local [weight-three adjacency bound](ADJACENT_LOW.md),
this gives a stronger consequence: whenever a replication-twenty point
\(u\) has deficit row \((3,2)\), and its weight-three neighbor
\(a\) also has replication twenty, its weight-two neighbor \(b\)
has replication at most nineteen.

## 1. The shorter global deduction

Words on a fixed pair have disjoint three-point remainders, so
\(d_{xy}\le5\). At \(r_x=20\),
\[
\sum_{y\ne x}t_{xy}=85-4r_x=5.                       \tag{1}
\]
The shortened twenty quadruples leave sixteen of the 136 pairs on
seventeen points, with leave degree \(1+3t_{xy}\) at \(y\).

Brouwer's established \(A(17,6,4)=20\) bounds every \(r_x\) by twenty.
At size 72, \(\sum r_x=360\) forces every replication to be twenty.
The complementary six-code-3
[absent-pair theorem](../coding_theory/a18_6_5_saturated_absent_pair/PROOF.md)
and [single-pair theorem](../coding_theory/a18_6_5_saturated_single_pair/PROOF.md)
exclude multiplicities zero and one at this size. Thus \(t_{xy}\le3\).
Equation (1) excludes support degrees zero and one. A degree-two point
\(u\) must have weights three and two, to neighbors \(a,b\).

At \(a\), the incoming weight three leaves two units of deficit.
Its row has either one further weight two, or two further weights one.
In the first case \(k_a=2\), so the prior weight-three adjacency result
applies to \(u,a\). If their other neighbors coincide, the common
neighbor \(b\) has replication at most eighteen; if they differ, each
has replication at most nineteen. Both contradict \(r_b=20\).
The second case is the new primary-anchor lemma, with the same
contradiction. Hence \(k_x\ge3\) everywhere, and (1) gives the
four stated partitions.

This deduction needs neither SUPPORT16 nor SUPPORT17 nor the
Rees--Stinson design nonexistence input in the earlier support chain.
The explicit premises are Brouwer, the complementary pair exclusions,
the local weight-three adjacency result, and the new lemma below.

## 2. First-star normalization

The ordinary [split-plane proof](AFFINE_SPLIT.md) shows that merging
the centers of a saturated degree-two link gives a \(2\text{-}(16,4,1)\)
design, an affine plane of order four. The self-contained historical
uniqueness proof in [AFFINE_NORMALIZATION.md](AFFINE_NORMALIZATION.md)
permits coordinates in \(\mathbb F_4^2\). The two origin lines assigned
to the weight-three anchor \(a\) can be sent to the axes by an invertible
linear map. This is a relabeling of any code with the hypotheses.
Write \(u=17,a=0,b=16\), and label \((x,y)\) by \(4x+y\),
with field labels \(0,1,2,3\) and \(\omega^2=\omega+1\).
The twenty fixed \(u\)-words are field lines with \(u\) restored,
replacing the origin by \(b\) on the three nonaxis origin lines.

The two fixed words containing \(a\), shortened at \(a\), are
\[
\{u,1,2,3\},\qquad\{u,4,8,12\}.
\]
Put \(X=\{1,2,3,4,8,12\}\),
\(N=\{5,6,7,9,10,11,13,14,15,16\}\), and
\(W=X\cup N=\{1,\ldots,16\}\).
The leave at \(a\) has degree ten at \(u\), four at \(c,d\),
and one at every other point. Its ten edges \(un\), \(n\in N\),
are forced, since the known words cover exactly the six \(uX\)-pairs.
No leave edge lies within either axis triple
\(\{1,2,3\}\) or \(\{4,8,12\}\).

## 3. Every primary-anchor leave

The forced edges exhaust the degrees at
\(N\setminus\{c,d\}\). Exactly six leave edges remain.
There are three exhaustive cases:

* **Both centers in N, no cd edge.** Each center needs three more
  neighbors, and every \(X\)-point needs one. Choose three
  \(X\)-points for \(c\), assigning the others to \(d\).
  There are \(\binom{10}{2}\binom{6}{3}=900\) middle leaves.
* **Both centers in N, with cd edge.** Each needs two more neighbors.
  The two unused \(X\)-points must be paired across the axes.
  Choose that pair in nine ways, then two of the remaining four
  points for \(c\). There are
  \(\binom{10}{2}\cdot9\binom{4}{2}=2430\) triangle leaves.
* **One center in N and one in X.** The \(X\)-center needs four
  neighbors. Its only possibilities are the \(N\)-center and
  the three opposite-axis points, so all four edges are forced.
  The \(N\)-center's other two neighbors are the other two points
  on the same axis as the \(X\)-center. There are \(10\cdot6=60\)
  end leaves.

If both centers were in \(X\), each would need four neighbors but
have at most three, all on the opposite axis. Thus exactly **3,390**
different labeled leaves cover every possibility, including \(b=c,d\).

Independent nonzero coordinate scaling, axis exchange and Frobenius
give 36 actual point permutations fixing \(u,a,b\) and preserving
the fixed twenty words. The programs check every word image, group
closure, and the disjoint union of all leave orbits. There are **117**
orbits: three end, thirty middle, eighty-four triangle. Transporting
a leave to a representative relabels its entire code; it imposes no
automorphism hypothesis on that code.

## 4. All primary stars and the secondary certificate

Every further \(a\)-word avoids \(u\), whose twenty words are fixed.
Restore \(a\) to every four-subset of \(W\) and test it against the
fixed \(u\)-star. Exactly **597** of the 1,820 quadruples satisfy the
cross-word condition. For a chosen leave, retain every such quadruple
whose six pairs are required covered pairs. The two known shortened
words cover twelve full-link pairs; exactly \(136-16-12=108\)
pairs remain, all on \(W\). The eighteen extra quadruples must
cover these pairs exactly.

At an uncovered pair the primary search branches on every available
quadruple containing it, removing precisely columns sharing a covered
pair. Every exact cover contains exactly one of those quadruples;
induction on uncovered pairs proves exhaustive and unique generation.
The minimum-domain choice affects only order. Every returned twenty-word
star and its thirty-eight-word union with the first star are checked
directly. No additional quotient or heuristic pruning occurs within a case.

The fixed pair \(ub\) occurs three times and \(ab\) four or five
times, according as \(b\in\{c,d\}\) or not. The double-star leave
at \(u\) contains \(uab\), so these groups share no word. There
are seven or eight fixed \(b\)-words. Every extra \(b\)-word avoids
the two saturated centers and has a four-subset of
\(H=\{1,\ldots,15\}\). Test **all 1,365** such quadruples against
all 38 words to obtain the complete necessary candidate set \(Q\).

Let \(G_Q\) contain every pair appearing in any \(Q\)-quadruple.
Additional compatible words share \(b\), so their quadruples have
disjoint pair sets. Each selected quadruple at \(x\) uses three
different incident pairs of \(G_Q\). Consequently their number \(m\)
satisfies the ordinary inequality
\[
m\le\left\lfloor\frac14\sum_{x\in H}
       \left\lfloor\frac{\deg_{G_Q}(x)}3\right\rfloor
       \right\rfloor.                               \tag{2}
\]

| Leave type | Orbits | Realized orbits | Primary stars | Largest extra bound |
|---|---:|---:|---:|---:|
| end | 3 | 2 | 7 | 11 |
| middle | 30 | 3 | 8 | 11 |
| triangle | 84 | 0 | 0 | — |
| total | 117 | 5 | 15 | 11 |

All fifteen realized unions have eight fixed \(b\)-words. Their
secondary candidate counts are 23--39 and their bounds (2) are seven
to eleven. Hence **\(r_b\le8+11=19\)** in every case. Cases with
seven fixed words admit no compatible primary star. This proves the
lemma without optimizing a secondary packing. The primary census
completes in **195,044** nodes, at most **5,389** for one case.

## 5. Separate replay and reproduction

`verify_single_isolate.py` constructs the first plane from rows,
columns and the twelve even permutations of four letters, then closes
four explicit permutation generators to obtain the same 36 maps.
It generates the carrier from its **degree sequence**, rather than
the three formulas: for each of all 120 pairs \(c,d\), subtract
the ten forced edges and choose every possible neighbor set of the
first point of positive remaining degree. The only forbidden edges
are pairs in the two known words. This reproduces all 3,390 actual
leaves in 12,045 states.

The replay uses mutable sparse-set Algorithm X cover/uncover
operations, reversing header ties and column order relative to the
primary integer-bitset search. Its 117 searches finish in **191,510**
nodes and produce the same fifteen covers. It generates candidates
with fixed-weight integer successors and XOR Hamming distances, and
recomputes (2) from actual neighbor bitsets.

With `--compare-primary`, the programs compare every first-star word,
raw leave, group element, required pair, candidate quadruple, completed
primary star, secondary candidate, and capacity entry. This is an
entrywise comparison. The sparse kernel also matches literal subset
enumeration for all **1,100** simple graphs of order at most five,
accepts a genuine affine-plane pair cover, rejects a zero-cap search
as `INCOMPLETE`, and rejects two malformed star inputs. Normal and
optimized Python runs agree; proof obligations do not use `assert`.

Use CPython 3.11.2 or compatible Python3, standard library, one process
and thread, from the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B constant_weight_18_6_5_equality_structure/check_single_isolate.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B constant_weight_18_6_5_equality_structure/verify_single_isolate.py --compare-primary
```

`single_isolate_expected.json` contains all 117 representatives,
orbit sizes, row and column digests, the fifteen actual primary covers,
and their secondary degree vectors and bounds. The separate summary
is `single_isolate_replay_expected.json`. Both have `status=COMPLETE`,
fifteen primary stars and maximum secondary replication upper bound
nineteen. Their SHA-256 hashes are, respectively,
`50beb3262a2b28d494f423b385bc90b68013e0cd960d4551d3fce267f2b07c5f`
and `ab30c7d6d48a220be09dd71ed95fb643b73bb3b358e6608a635b2c605f644dd5`.
Hashes authenticate compact evidence; complete regeneration
supplies the mathematical check. No large corpus or solver input is needed.

Each cover case has a 200,000-node / ten-second guard. The replay's
whole degree-sequence census has the same guards. A guard raises
`INCOMPLETE` and establishes no exclusion. All reported cases completed.
The final normal/optimized primary checks took 6.7155/6.7804 seconds;
the corresponding replay checks including entrywise primary comparison
took 33.6583/33.9707 seconds. Peak checker-child RSS was at most
28,032 KiB, within the unchanged one-CPU / 2-GiB scope.

The local lemma relies on exact enumeration, the ordinary split and
historical affine normalization proofs, the carrier and pair-cover
completeness bridges, inequality (2), CPython execution and hardware.
These interfaces are unformalized. Both implementations are by this
researcher; their agreement is not independent peer review. The new
lemma and minimum-degree-three theorem have not received independent review.

## 6. Dependencies and literature

The global corollary imports these exact graph/source premises:

* Brouwer's point cap:
  `bafkreigjhhpzojgjshtrojykwbvtxyhr4daeay5beb576uki452enqevia`.
* Prior adjacency lemma, source
  `aa24dfcdc5c3ee2509c5de0584d28f58dd236a59`:
  `bafkreidutgaz5p367nwyzmsl7glsj6i5fwy46kfb6ew5bzgpovuoyy273y`.
* Complementary absent-pair theorem, source
  `2e5f4a01e3f4e4f0983a11690d7b0df9b621c0e8`:
  `bafkreidnkqgqncmmvgx2osdci6hm5oqdjyxume6o7qa4jec6nz6mkr5exa`.
* Complementary single-pair theorem, source
  `8321eee86a06b25634651516e22d1fcbd8b76902`:
  `bafkreiatffk6cdcdpgs2esutx5ixfs4rizcw5hmfb3n3ziav3npv2hzafu`.

The [independent single-pair review](../constant_weight_single_pair_review2/REVIEW.md),
source `97325ae0e3fa8d1bde2187e38758a0aea3848b31`, confirms that input
and gives a sharp degree-20/19 absent-pair classification. It does not
review this theorem or the later degree-20/19 multiplicity-one result.
The prior SUPPORT16 geometry and theorem also have an
[independent audit](../constant_weight_18_6_5_support16_review5/REVIEW.md).

Primary literature rechecked live on 2026-09-30:

* Brouwer (1975), *A(17,6,4)=20 or the nonexistence of the scarce
  design SD(4,1;17,21)*: <https://ir.cwi.nl/pub/6883/6883D.pdf>.
* Aw--Chee--Ling (2003), *Six New Constant Weight Binary Codes*,
  Theorem 1 and Appendix A: <https://ymchee66.github.io/home/PDF/6cwc.pdf>.
* Maintained 69--72 table: <https://aeb.win.tue.nl/codes/Andw.html>.
* Historical affine uniqueness exposition, Bishnoi (2012), Theorem 3.6:
  <https://anuragbishnoi.wordpress.com/wp-content/uploads/2014/09/report21.pdf>.

The published 69-word baseline was reproduced exactly. Bounded primary
and committed-graph searches located no matching primary-anchor lemma
or minimum-degree-three theorem. This is no historical-priority guarantee.
The remaining global frontier has deficit-support minimum degree at
least three; these necessary conditions still permit size 72.
