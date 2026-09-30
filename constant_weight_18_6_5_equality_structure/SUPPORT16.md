# Sixteen vertices of higher support degree are necessary

Author: six-code-1, researcher. Date: 2026-09-30.

**Computer-assisted theorem.** Let 72 five-element subsets of an
18-element set have pairwise intersections at most two. For a pair
\(xy\), let \(d_{xy}\) be its block multiplicity and set
\(t_{xy}=5-d_{xy}\). Join \(xy\) in the deficit support when
\(t_{xy}>0\). At least **sixteen** points have support degree at
least three. Thus at most two points have support degree two.

This strengthens [SUPPORT15.md](SUPPORT15.md). It does not exclude
72 blocks or improve the maintained global interval
\(69\le A(18,6,5)\le72\).

## 1. Dependencies and the three-point carrier

Use the incidence, double-star and path facts in [PROOF.md](PROOF.md),
[SUPPORT12.md](SUPPORT12.md), and [SUPPORT14.md](SUPPORT14.md).
Brouwer's established \(A(17,6,4)=20\) makes every point replication
twenty. Each deficit row has weighted sum five; every leave pair has
codegree \(1+3t_{xy}\). Every leave triple through a degree-two
support point uses one of its two support neighbors, and the triple
on both those neighbors is forced. A positive deficit incident with
a support-degree-at-least-three point has weight at most three.

A support-degree-one pair already leaves sixteen points of degree
at least three. Otherwise let \(S\) be the degree-two points and
\(H\) the other points, with \(h=|H|\). The preceding theorem gives
\(h\ge15\). Assume \(h=15\); then \(|S|=3\). Entire degree-two
cycles are excluded by the earlier proof. Thus the graph induced on
\(S\) is three isolated points, a pair and an isolated point, or a
three-point path. A two-point component has weight two, three or
four; a three-point path has weights two and three. These follow
from weighted row five and the weight-at-most-three endpoint edges
to \(H\).

If all components are isolated points or weight-two pairs, the
whole-component arguments in SUPPORT14 exclude them: an isolated
point forces \(5\ge2|S|=6\), or a weight-two pair forces \(h\ge16\).
It remains to handle a weight-three pair, the path, and a weight-four
pair. Only the final case needs exact computation.

## 2. A weight-three pair is impossible

Let \(uv\) have weight three, let its other neighbors be \(a,b\in H\)
with edge weights two, and let \(z\) be the isolated point of \(S\).
The pair \(uv\) has ten leave thirds, all in \(H\). In \(L_a\),
the degree of \(u\) is seven. Its possible neighbors are \(v\),
at most five \(H\) points outside those ten, and \(z\). Consequently
\(z\) must neighbor \(a\) in the support; the degree-two rule at
\(z\) proves this implication. Likewise \(z\) neighbors \(b\).

If \(a=b\), weights \(au,av\) total four and \(az\ge2\), exceeding
five. If \(a\ne b\), the isolated \(z\) has exactly these two
neighbors, with weights two and three. The anchor receiving weight
three then has that edge and its weight-two endpoint edge, exhausting
its row on just two support edges. It could not belong to \(H\).
Both cases contradict the hypotheses.

## 3. The three-point path has a direct block conflict

Write \(S=\{u,v,w\}\), with \(t_{uv}=2\), \(t_{vw}=3\). The other
neighbors of \(u,w\) are \(a,b\in H\), of weights three and two.
They differ: a common anchor would exhaust its row on two edges
and hence would not be in \(H\).

Let \(U\) be the \(H\) leave thirds on \(uv\), and \(V\) those
on \(vw\). Besides the forced triple \(uvw\), these sets have
sizes six and nine. For each \(y\in H\), the pair \(vy\) has
deficit zero and hence exactly one leave third. The degree-two rule
at \(v\) makes that third either \(u\) or \(w\). Therefore
\(U,V\) partition \(H\). The forced endpoint triples give
\(a\in U\), \(b\in V\).

In \(L_a\), the degree of \(u\) is ten. The neighbor \(v\) is
forced. A point of \(U\setminus\{a\}\) cannot be another neighbor:
\(uvy\) already occupies the unique leave on the deficit-zero
pair \(uy\). The point \(w\) also cannot contribute, since its
support neighbors are \(v,b\), neither of which appears in \(auw\).
Thus all nine points of \(V\) must neighbor \(u\) in \(L_a\).
The covered third points on \(au\) are exactly
\(\{w\}\cup(U\setminus\{a\})\).

The triple \(auw\) is covered, by the same degree-two rule at
\(w\). Its block must be \(\{a,u,w\}\) plus two points of
\(U\setminus\{a\}\). On the other hand, \(d_{vw}=2\), and its
two blocks partition the six covered third points \(U\) into
triples. Write these blocks as
\[
\{v,w,a,p,q\},\qquad \{v,w,r,s,t\}.
\]
The block on \(auw\) cannot use \(p\) or \(q\), because it
would meet the first block in at least three points. Its two
additional points are consequently in \(\{r,s,t\}\), making its
intersection with the second block at least three. This is a
contradiction. No enumeration or plane classification is used here.

## 4. A weight-four pair has one universal affine normal form

Let \(uv\) have weight four, with other neighbors \(a,b\in H\)
of weight one, and let \(z\) be isolated in \(S\). Its thirteen
leave thirds all lie in \(H\), including \(a,b\); let \(W\)
be the two missing \(H\) points. In \(L_a\), the degree-four
vertex \(u\) can only neighbor \(v\), both points of \(W\),
and \(z\). All four are therefore forced. The same argument
in \(L_b\) forces the analogous neighbors of \(v\). In particular,
\(z\) has support neighbors \(a,b\).

They cannot coincide. If \(a=b\), edges to \(u,v,z\) leave at
most one unit of weight for \(H\). Each point of \(W\) receives
two distinct leave triples on its pair with that common anchor,
from \(u,v\), so each needs a positive deficit. This needs at
least two further units, impossible.

Rename the anchors and endpoints so that \(t_{az}=3\), \(t_{bz}=2\).
The row at \(a\) has \(az\) of weight three, \(au\) of weight one,
and exactly one further edge \(ac\) to \(H\), of weight one.
The pair \(uv\) has multiplicity one. Its only covered third
points are \(z\) and \(W\), so its unique block is
\(\{u,v,z\}\cup W\).

By [AFFINE_SPLIT.md](AFFINE_SPLIT.md), shortening at \(z\) and
merging \(a,b\) gives an affine plane of order four. Its five
origin lines split into two assigned to \(a\) and three assigned
to \(b\). The forced leave \(azu\) places \(u\) on a \(b\)-line;
similarly \(v\) is on an \(a\)-line. The quadruple
\(\{u,v\}\cup W\) is a line missing the origin, so its four
points have distinct origin directions.

If a point of \(W\) is on a \(b\)-line, it receives both the
leave \(azx\) and the forced leave \(aux\), requiring a positive
\(H\) deficit at \(a\). At most one point of \(W\) can do this.
Both cannot be on \(a\)-lines, since those points and \(v\)
would use three distinct directions while there are only two.
Thus one point is on each part. The \(b\)-part point is precisely
the remaining support neighbor \(c\); call the other point \(d\).

The proved normal form in [AFFINE_NORMALIZATION.md](AFFINE_NORMALIZATION.md)
now sends the merged origin to field point zero, the two \(a\)-directions
to the axes, and the missing-origin line to \(x+y=1\). Swapping
axes and applying field conjugation fixes all labels as follows:
\[
a=16,\quad b=0,\quad z=17,\quad
u=11,\quad v=4,\quad c=14,\quad d=1.
\]
Field-plane points have labels \(4x+y\) for integer field labels
\(0,1,2,3\). Its twenty quadruples, with zero replaced by 16
on the two axis lines, are exactly the shortened packing at \(z\).
This normalization covers every case, with no global symmetry
assumption on the code.

## 5. Exactly six leave graphs remain at the anchor

In \(L_a\), the three high-degree vertices are \(z,u,c\), of
degrees ten, four, four. The neighbors of \(z\) are \(b\) and
the nine points on the three \(b\)-direction origin lines. The
neighbors of \(u\) are exactly \(z,c,v,d\). Both lists are forced
and exhaust their degrees. The point \(c\) already neighbors
\(z,u\). Every other low-degree point outside
\(R=\{2,3,8,12\}\) already has its unique link neighbor.
Consequently \(c\) neighbors two chosen points of \(R\), and
the other two form an isolated matching edge. This gives exactly
\(\binom42=6\) complete leave graphs.

Two blocks through \(az\) are already fixed by the axis lines:
their shortened quadruples at \(a\) are
\(\{z,1,2,3\}\) and \(\{z,4,8,12\}\). If the matching edge is
\(\{2,3\}\) or \(\{8,12\}\), one fixed quadruple covers that
leave edge. These two cases are directly impossible.

For each of the other four cases, the twenty quadruples at \(a\)
must cover exactly the 120 pairs outside its sixteen-edge leave.
The two fixed quadruples cover twelve distinct pairs. The remaining
eighteen quadruples contain no \(z\), since \(d_{az}=2\). They
must therefore partition 108 prescribed pairs among the sixteen
points \(0,\ldots,15\). Enumerate **every** four-subset of these
points. It is a candidate precisely when all its pairs are
prescribed and its full word with \(a\) meets each of the twenty
fixed words through \(z\) in at most two points. This is the
complete necessary candidate universe, not a heuristic filter.

The exact counts and completed exclusions are:

| Neighbors of c in R | Candidate quadruples | Primary tree nodes | Replay B-parallel classes |
|---|---:|---:|---:|
| 2,8 | 449 | 2115 | 10984 |
| 2,12 | 450 | 2071 | 11188 |
| 3,8 | 443 | 2164 | 10860 |
| 3,12 | 449 | 1820 | 10984 |

Every branch completes. None admits the required pair partition.
This is the computer-assisted part of the theorem.

## 6. Completeness, replay and trust boundary

`check_support16.py` generates the plane over \(\mathbb F_4\),
constructs the complete candidate universe by set intersections,
and exhausts exact pair covers. At a state choose an uncovered
pair with fewest available columns. Every cover uses exactly one
column on that pair; branch on all such columns and remove all
columns intersecting it on a used pair. A pair with no remaining
column proves that branch impossible. Induction on uncovered pairs
proves completeness. No heuristic pruning or symmetry quotient
occurs inside this search.

`verify_support16.py` independently constructs the plane from the
graphs of the twelve even permutations and uses integer XOR Hamming
distances to generate candidates. It compares every row and column
with the first implementation when `--compare-primary` is supplied.
Its search first enumerates the five triples in the quadruples
through \(b\): the pair \(ab\) has deficit zero, its sole leave
third is \(z\), and hence these triples partition all fifteen
remaining points. Branching on the least unused point enumerates
all such parallel classes exactly once. For each, a separate
set-based search exhausts the residual pair cover. All 44,016
classes across the four cases are checked. This different
decomposition and independent candidate generation provide replay
evidence; they are not independent peer review.

The primary cover search matches direct brute force on all 1,100
simple graphs of order at most five. Both implementations also
accept the known affine-plane-plus-unused-point packing and the
actual saturated point-zero packing of the published 69-word code.
Their returned positive witnesses are directly pair-checked.

Run from the repository root, with Python 3.11.2 and standard
library only, one process and thread:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 constant_weight_18_6_5_equality_structure/check_support16.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 constant_weight_18_6_5_equality_structure/verify_support16.py --compare-primary
```

`support16_expected.json` is a compact replay manifest of completed
counts and hashes, not a standalone nonexistence certificate.
The source recomputes every case. Either a 200,000-node cap or a
15-second per-case search cap produces `INCOMPLETE`, exits without
verification, and proves no exclusion. No such cap was reached in
the successful proof computations.

The theorem depends on the exact finite computations, the written
coverage and normalization bridges, the preceding fifteen-point
lemma, Brouwer's external point-degree bound, CPython's exact
integer/set execution, and ordinary hardware. SUPPORT15 additionally
imports Rees--Stinson's resolvable-design theorem. This is not a
formalization or independent peer review, and no priority claim is
made. The affine uniqueness theorem is historical. The 47-type
necessary local carrier remains unchanged: a coupled obstruction
does not prove that any extra individual leave type is impossible.

All cases at \(h=15\) are now excluded, so \(h\ge16\). Remaining
carriers with zero, one or two degree-two points need further global
compatibility; no 72-word exclusion or numerical upper-bound
improvement follows from this theorem alone.

Primary sources and provenance:

* Brouwer (1975), *A(17,6,4)=20 or the nonexistence of the scarce
  design SD(4,1;17,21)*: <https://ir.cwi.nl/pub/6883/6883D.pdf>.
* Rees--Stinson (1987), Lemma 3.5, used by the preceding theorem:
  <https://cs.uwaterloo.ca/~dstinson/papers/J69.pdf>.
* Bishnoi, *Finite Geometries*, Theorem 3.6, historical affine
  uniqueness context; a full proof is supplied here:
  <https://anuragbishnoi.wordpress.com/wp-content/uploads/2014/09/report21.pdf>.
* Maintained global bound table, rechecked 2026-09-30:
  <https://aeb.win.tue.nl/codes/Andw.html>.
