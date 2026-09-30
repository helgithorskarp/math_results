# A necessary structure for a 72-word code

Author: six-code-1, researcher. Date: 2026-09-30.

The current strongest support-size consequence in this directory is
the computer-assisted [SUPPORT17.md](SUPPORT17.md): at least seventeen
points have support degree at least three. It excludes the two-isolate
carrier using the preceding adjacency result and the complementary
six-code-3 pair theorems, whose additional dependencies are explicit there.
The original incidence proof and local catalog below remain valid.

The at-least-nine conclusion below is strengthened to at least sixteen
in the computer-assisted [SUPPORT16.md](SUPPORT16.md), via the ordinary
[SUPPORT15.md](SUPPORT15.md), [SUPPORT14.md](SUPPORT14.md) and
the intermediate result
[SUPPORT12.md](SUPPORT12.md). They use the incidence facts and component
exclusion established here. The original proof and local catalog remain valid.

[ADJACENT_LOW.md](ADJACENT_LOW.md) supplies stronger local restrictions:
degree-two points in a 72-word code cannot share an edge of deficit two or
three. Combined with SUPPORT16 and the separate six-code-3
[saturated single-pair theorem](../coding_theory/a18_6_5_saturated_single_pair/PROOF.md),
the degree-two vertices form an independent set of size at most two.
The distinct-anchor weight-three exclusion
uses complete link enumeration and an elementary pair-capacity bound.

Let \(\mathcal B\) be 72 distinct five-element subsets of an 18-element
set \(V\), with two different blocks meeting in at most two points.
Write \(r_x\) for the number of blocks containing \(x\), and \(d_{xy}\)
for the number containing the pair \(\{x,y\}\). Define
\[
t_{xy}=5-d_{xy},\qquad
N_T(x)=\{y\ne x:t_{xy}>0\},\qquad k_x=|N_T(x)|.
\]
The **support graph** has vertex set \(V\) and edge \(xy\) exactly when
\(t_{xy}>0\); its edges carry the positive integer weights \(t_{xy}\).
Let \(\mathcal L\) be the triples contained in no block (the triple leave).

**Lemma.** At least nine vertices have \(k_x\ge3\). If some pair is in no
block, its endpoints have \(k_x=1\), and all other sixteen vertices have
\(k_x\ge3\). In particular, there is at most one pair in no block.

This is a necessary condition for equality in the known upper bound 72.
It does not prove nonexistence of a 72-word code, and does not improve
the known interval \(69\le A(18,6,5)\le72\).

## 1. Incidence and local leaves

The blocks through a point, with that point deleted, form a packing of
four-element subsets of a 17-set in which each pair is in at most one
block. The established result \(A(17,6,4)=20\) of Brouwer therefore gives
\(r_x\le20\). Since \(\sum_x r_x=5\cdot72=360\), every \(r_x=20\).
This use of Brouwer's theorem is an explicit external dependency.

The blocks through a pair have disjoint three-element remainders, so
\(d_{xy}\le\lfloor16/3\rfloor=5\). Thus the deficits are nonnegative and
\[
\sum_{y\ne x}t_{xy}=5\cdot17-4r_x=5.                 \tag{1}
\]
There are \(\binom{18}{3}-10\cdot72=96\) leave triples. Exactly
\(\binom{17}{2}-6r_x=16\) contain any given vertex \(x\), and exactly
\[
16-3d_{xy}=1+3t_{xy}                                \tag{2}
\]
contain a given pair \(xy\).

For each \(x\), let \(L_x\) be the graph on \(V\setminus\{x\}\) whose
edges \(yz\) mean \(xyz\in\mathcal L\). It has sixteen edges, and the
degree of \(y\) is \(1+3t_{xy}\). Its high-degree vertices are precisely
\(N_T(x)\); all other vertices have degree one. If \(H_x\) is its graph
induced on \(N_T(x)\), and \(p_x\) is the number of edges between two
degree-one vertices, then
\[
|E(H_x)|-p_x=k_x-1.                                \tag{3}
\]
Indeed the sum of degrees of high-degree vertices is \(15+k_x\), the
sum for the other vertices is \(17-k_x\), and subtracting cancels the
edges between the two sets.

If \(k_x=1\), (3) gives \(p_x=0\), and \(L_x\) is a star. If
\(k_x=2\), (3) forces the two high-degree vertices to be adjacent and
\(p_x=0\): \(L_x\) is a double star. Consequently:

* If \(k_x\le2\), every leave triple containing \(x\) contains a
  neighbor of \(x\) in the support graph.
* If \(k_x=2\) with support neighbors \(a,b\), then \(xab\in\mathcal L\).

## 2. A zero pair forces sixteen vertices of support degree at least three

If \(d_{xy}=0\), then \(t_{xy}=5\), and (1) makes every other deficit
incident with either \(x\) or \(y\) zero. All sixteen triples \(xyz\)
are in the leave. For any other vertex \(z\), the edge \(xy\) in \(L_z\)
joins two degree-one vertices. Thus \(p_z\ge1\), which is impossible
when \(k_z\le2\), by (3). Hence every such \(z\) has \(k_z\ge3\).

Conversely, (1) shows that any support-degree-one vertex belongs to
such a zero pair. This also proves uniqueness of a zero pair.

## 3. No support component consists entirely of degree-two vertices

Suppose such a component is a cycle \(C\) of length \(m\). Summing (1)
over its vertices gives \(5m=2\sum_{e\subset C}t_e\), so \(m\) is even.
If \(m=4\), its two opposite vertices force two distinct leave triples
on the same other opposite pair. That pair has deficit zero and leave
codegree one by (2), a contradiction.

For \(m\ge6\), the internal leave triples are exactly the \(m\)
consecutive three-vertex paths around the cycle. Each is forced by its
middle vertex. No other internal triple is possible, because each of
its three degree-two vertices must have a support neighbor in it.
There is no leave triple having exactly one vertex of \(C\), for the
same reason. Every pair between \(C\) and its complement has leave
codegree one. If \(b\) counts leave triples with exactly two vertices
of \(C\), counting cross pairs and then vertex incidences gives
\[
2b=m(18-m),\qquad 16m=3m+2b=m(21-m).
\]
It follows that \(m=5\), contradicting evenness.

## 4. At least nine vertices have support degree at least three

The zero-pair case is already proved. Otherwise there are no
support-degree-one vertices. Partition \(V=S\sqcup H\), where
\(k_x=2\) for \(x\in S\) and \(k_x\ge3\) for \(x\in H\); put
\(h=|H|\). Assume for contradiction that \(h\le8\).

An edge \(uv\) with both endpoints in \(S\) cannot have weight four.
In a leave triple \(uvz\), a vertex \(z\in S\) must be one of the
other support neighbors of \(u,v\). There are at most two such
vertices, so the pair \(uv\) has leave codegree at most \(h+2\le10\),
whereas weight four would give thirteen by (2).

Weight three would give leave codegree ten. It is impossible if
\(h\le7\). If \(h=8\), the two other support neighbors \(a,b\) of
\(u,v\) must be distinct elements of \(S\), and every vertex of \(H\)
must occur in a leave triple with \(uv\). Both edges \(ua,vb\) have
weight two by (1). Let \(c\) be the other support neighbor of \(a\).
The double-star rule forces \(acu\in\mathcal L\). If \(c\in H\),
then \(cuv\in\mathcal L\) also. These are distinct triples on the
pair \(cu\), which has deficit zero since the only support neighbors
of \(u\) are \(a,v\). This contradicts (2). Therefore \(c\in S\),
and \(ac\) has weight three. Repeating in both directions extends
alternating weight-three and weight-two edges entirely through
degree-two vertices, making a whole support component a cycle in
\(S\). Section 3 excludes this. Thus no edge within \(S\) has weight
at least three when \(h\le8\).

Each vertex of \(S\) has two positive incident weights summing to
five, so exactly one is at least three. It therefore meets a vertex
of \(H\). A vertex of \(H\) cannot receive two such edges, since its
total incident weight is five. They give an injection \(S\to H\),
so \(18-h\le h\), contradicting \(h\le8\). Hence \(h\ge9\).

## 5. Forty-eight abstract local leave types

The positive deficits at any saturated point form a partition
\((t_1,\ldots,t_k)\) of five. Given its high-degree core graph \(H\),
equation (3) determines the number of isolated edges among the
degree-one vertices as \(p=|E(H)|-k+1\). High vertex \(i\) has
\(1+3t_i-\deg_H(i)\) degree-one neighbors. These data determine the
entire graph up to isomorphism. Conversely they construct a graph
with seventeen vertices, sixteen edges and the required degrees,
provided the leaf counts and \(p\) are nonnegative and fit the
remaining vertices.

There are at most five high vertices, so enumerating at most
\(2^{\binom52}=1024\) core graphs per partition is exhaustive.
The accompanying exact program quotients only by permutations
preserving the deficit values. It returns the following counts:

| Positive deficits | Abstract local types |
|---|---:|
| 5 | 1 |
| 4+1 | 1 |
| 3+2 | 1 |
| 3+1+1 | 3 |
| 2+2+1 | 3 |
| 2+1+1+1 | 13 |
| 1+1+1+1+1 | 26 |
| Total | 48 |

These are abstract leave graphs satisfying the incidence conditions.
We do **not** assert that all 48 admit the requisite packing of
twenty quadruples, or that they can all extend to a 72-word code.
The at-least-nine lemma does not depend on this enumeration.

## Sources and evidence boundary

* A. E. Brouwer, *A(17,6,4)=20 or the nonexistence of the scarce design
  SD(4,1;17,21)*, report ZW 62/75 (1975),
  <https://ir.cwi.nl/pub/6883/6883D.pdf>.
* H. K. Aw, Y. M. Chee and A. C. H. Ling, *Six New Constant Weight
  Binary Codes*, Ars Combinatoria 67 (2003), 313–318, Theorem 1 and
  Appendix A: <https://ymchee66.github.io/home/PDF/6cwc.pdf>.
* Maintained bound table, checked 2026-09-30:
  <https://aeb.win.tue.nl/codes/Andw.html>.

The proof is an ordinary combinatorial argument, not a proof-assistant
formalization. The code checks the known 69-word baseline, the finite
local degree-condition carrier, and the local leaves at all twelve
saturated points of that baseline. It does not enumerate 72-word codes
or certify a global exclusion. A targeted search of the cited sources
found no statement of the at-least-nine restriction; no priority claim
is made.
