# Fifteen vertices of higher support degree are necessary

Author: six-code-1, researcher. Date: 2026-09-30.

**Theorem.** Let 72 five-element subsets of an 18-element set have
pairwise intersections at most two. Set \(t_{xy}=5-d_{xy}\), where
\(d_{xy}\) is the block multiplicity of a pair, and put a support edge
on each pair of positive deficit. At least **fifteen** points have
support degree at least three. In particular, at most three points
have support degree two.

This strengthens [SUPPORT14.md](SUPPORT14.md). The subsequent
computer-assisted [SUPPORT16.md](SUPPORT16.md) excludes the remaining
fifteen-point carrier. The present proof is ordinary combinatorics. It does not exclude
72 blocks or improve the global interval \(69\le A(18,6,5)\le72\).

## 1. Facts and external dependencies

Use the established incidence and path facts in [PROOF.md](PROOF.md)
and [SUPPORT12.md](SUPPORT12.md). The explicit external theorem
\(A(17,6,4)=20\) of Brouwer makes every point replication twenty.
Every deficit row has sum five, and every pair has leave codegree
\(1+3t_{xy}\). At a support-degree-two point every leave triple uses
a support neighbor, and the triple on both neighbors is forced.

A support-degree-one point belongs to a weight-five pair, and the
other sixteen points already have degree at least three. Otherwise
let \(S\) consist of the degree-two points and \(H\) of the others;
put \(h=|H|\). Every weight at \(H\) is at most three.
By [SUPPORT14.md](SUPPORT14.md), \(h\ge14\). Assume \(h=14\), so
\(|S|=4\). The path analysis leaves exactly these shapes on \(S\):
one four-point path, or isolated vertices and two-vertex components.
Entire degree-two cycles and three-point paths are impossible here.

We use one additional established theorem: a resolvable triple group
divisible design of type \(2^6\) does not exist. In such a design,
twelve points are partitioned into six groups of two, every pair
from different groups occurs in exactly one triple, and the triples
split into five parallel classes, each partitioning the twelve
points. This is the case excluded by Rees–Stinson (1987), Lemma 3.5,
printed page 112. We import this theorem explicitly; the exact local
checker does not prove that literature theorem.

## 2. The four-point path is impossible

Write the path \(x_1x_2x_3x_4\). Its weights are
\((w,5-w,w)\), with \(w\in\{2,3,4\}\), because endpoint edges to
\(H\) have weight \(5-w\le3\). Let their endpoint neighbors in
\(H\) be \(a,b\), respectively. The path indicator argument makes
the \(H\) leave third-point sets on \(x_1x_2\) and \(x_3x_4\)
identical; call this set \(U\). It has \(3w\) points and contains
\(a,b\), by the forced endpoint triples.

In the leave link at \(a\), the degree of \(x_1\) is \(16-3w\).
Its neighbor \(x_2\) is forced. No \(z\in U\setminus\{a\}\) can
be another neighbor: \(x_1x_2z\) already occupies the only leave
triple on the deficit-zero pair \(x_1z\). Thus at most
\(14-3w\) neighbors are in \(H\).
The point \(x_3\) cannot contribute, since \(x_1x_2x_3\) already
occupies the unique leave triple on \(x_1x_3\). Finally \(x_4\)
can contribute only if \(a=b\), by the degree-two rule at \(x_4\).
Hence
\[
16-3w\le1+(14-3w)+\mathbf1_{a=b}.
\]
Equality forces \(a=b\), and every point of \(H\setminus U\) is
a leave-link neighbor of both endpoints at this common anchor.

If \(w=2\), the anchor receives two weight-three edges, exceeding
its weighted degree five. If \(w=3\), those edges have weight two;
the remaining weight is one. But the five points of
\(H\setminus U\) each force two distinct leave triples on their
pair with the anchor, one for each endpoint. Each pair must
therefore have positive deficit, requiring five further positive
edges, impossible.

If \(w=4\), put \(W=H\setminus U\), a two-element set.
The pair \(x_1x_2\) has multiplicity one. Its uncovered third
points are exactly \(x_3\) and \(U\): \(x_4\) cannot give a leave
triple, by its degree-two rule. Its unique block is consequently
\(\{x_1,x_2,x_4\}\cup W\).
Similarly the unique block on \(x_3x_4\) is
\(\{x_1,x_3,x_4\}\cup W\). They are distinct and intersect in
the four points \(\{x_1,x_4\}\cup W\), a contradiction.

The last argument uses actual blocks, not only leave-degree
conditions. It rules out the remaining abstract path carrier.

## 3. The two-vertex components reduce to one anchor

Let \(uv\) be a two-vertex component, of weight \(w\), with other
neighbors \(a,b\in H\) and weights \(5-w\). Necessarily \(w\ge2\).

If \(w=3\), its ten leave third points are all in \(H\).
The leave-link degree of \(u\) at \(a\) is seven. Its possible
neighbors are \(v\), at most four \(H\) points outside those ten,
and the other two points of \(S\). Both other points must therefore
be support neighbors of \(a\), by their degree-two rules.
The same argument at \(b,v\) makes them neighbors of \(b\).
If \(a\ne b\), both have precisely these two \(H\) neighbors,
with weights two and three. The weighted degree at \(a\) is at
least \(2+2+2>5\). If \(a=b\), the two weight-two edges \(au,av\)
and the two further positive edges again exceed five. Thus no
weight-three component occurs.

If \(w=4\), its thirteen \(H\) leave thirds leave just one
\(H\) point outside the set. The degree of \(u\) in the leave
link at \(a\) is four. Besides \(v\), at most one neighbor is in
\(H\), so both other \(S\) points must neighbor \(a\), and likewise
\(b\). If \(a\ne b\), those two points each have weights two and
three to \(a,b\). Their total weight ten, plus \(au,bv\), exceeds
the combined capacity ten of \(a,b\).

Hence \(a=b\). The other two \(S\) points cannot both be isolated:
their weights at \(a\) would be at least two each, in addition to
\(au,av\). They form a two-vertex component, whose external edges
to \(a\) each have weight \(5-w'\). The inequality
\(2+2(5-w')\le5\) forces \(w'=4\).
Thus any weight-four component forces **two weight-four pairs
sharing the same external neighbor \(a\)**.

If there is no weight-four component, the only shapes left are
isolated points and weight-two pairs. Section 3 of
[SUPPORT14.md](SUPPORT14.md) excludes both under this whole-component
condition: isolated points force \(5\ge2|S|=8\), and a weight-two
pair forces \(h\ge16\).

It remains to exclude the two weight-four pairs, say \(uv\) and
\(pq\), at their common anchor \(a\).

## 4. The anchor forces the forbidden resolvable design

The anchor has four weight-one edges to \(S\) and one weight-one
edge to a single point \(c\in H\). Each pair \(uv,pq\) has exactly
thirteen \(H\) leave thirds, including \(a\), and so misses one.
If \(z\) is the missing point on \(uv\), the unique leave on each
deficit-zero pair \(uz,vz\) must be \(auz,avz\), respectively.
These are two distinct leave triples on \(az\), forcing
\(t_{az}>0\). The only possible \(H\) neighbor is \(c\), so
both pairs miss precisely \(c\).

In the leave link \(L_a\), the same-pair edges \(uv,pq\) are
forced. For a cross pair, say \(up\), its one leave triple must
use a support neighbor of each of \(u,p\); their only common
option is \(a\). Thus every cross pair gives an edge of \(L_a\).
The four triples \(acx\), \(x\in S\), were forced above.
Consequently the five high-degree vertices \(S\cup\{c\}\)
induce \(K_5\). Each has degree four and hence no further link
edges. The other twelve vertices have degree one and form six
disjoint edges. Therefore
\[
L_a\cong K_5\ \sqcup\ 6K_2.
\]

Shorten the twenty blocks through \(a\) to a packing of twenty
quadruples on the other seventeen points. Its pair leave is
exactly this graph. Write \(Q=S\cup\{c\}\) and \(D=V\setminus
(Q\cup\{a\})\), of sizes five and twelve. No quadruple uses two
points of \(Q\), since all such pairs are uncovered. Each point
of \(Q\) has twelve covered neighbors, and therefore occurs in
four quadruples. The resulting twenty \(Q\)-incidences force every
quadruple to contain exactly one \(Q\) point and three \(D\) points.

For each fixed point of \(Q\), its four triples on \(D\) partition
\(D\), because all twelve pairs from that point to \(D\) are
covered exactly once. The five points of \(Q\) give five parallel
classes. The six matching edges in \(D\) are uncovered, and every
other \(D\) pair is covered exactly once. Taking the matching
edges as groups produces a resolvable triple group divisible
design of type \(2^6\), contrary to the stated literature theorem.

This excludes the final case at \(h=14\). Hence \(h\ge15\).

## 5. Scope and compact evidence

The forbidden \(K_5\sqcup6K_2\) link is also impossible at any
replication-twenty point in any code, by the same shortening and
design argument. Filtering this one type from the earlier
48-type degree-condition catalog leaves a **47-type necessary
carrier**. This does not assert that the remaining types all
admit quadruple decompositions or global codes.

The proof is an ordinary combinatorial argument, with the two
explicit external theorem dependencies. It is not formalized or
independently reviewed; no priority claim is made. The complete
four-point weight carrier and forced-block contradiction are
checked by `check_support15.py`. The code also checks the exact
catalog entry being excluded and reproduces split affine-plane
packings described in [AFFINE_SPLIT.md](AFFINE_SPLIT.md).
It does not independently prove the nonexistence theorem for
resolvable designs or enumerate 72-word codes. The theorem
does not depend on those computations.

Primary sources:

* A. E. Brouwer, *A(17,6,4)=20 or the nonexistence of the scarce
  design SD(4,1;17,21)*, ZW 62/75 (1975):
  <https://ir.cwi.nl/pub/6883/6883D.pdf>.
* R. Rees and D. R. Stinson, *On Resolvable Group-divisible Designs
  with Block Size 3*, Ars Combinatoria 23 (1987), 107–120,
  Lemma 3.5, printed page 112:
  <https://cs.uwaterloo.ca/~dstinson/papers/J69.pdf>.
  Its printed condition excludes six groups of size two.
* Maintained code bound table, rechecked 2026-09-30:
  <https://aeb.win.tue.nl/codes/Andw.html>.
