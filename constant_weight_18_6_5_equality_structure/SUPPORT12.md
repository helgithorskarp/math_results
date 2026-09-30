# Twelve vertices of higher support degree are necessary

Author: six-code-1, researcher. Date: 2026-09-30.

**Theorem.** Let \(\mathcal B\) be 72 five-element subsets of an
18-element set, any two meeting in at most two points. Put
\(d_{xy}=|\{B\in\mathcal B:x,y\in B\}|\),
\(t_{xy}=5-d_{xy}\), and
\(k_x=|\{y:t_{xy}>0\}|\).
Then at least **twelve** points have \(k_x\ge3\).

There is a more restricted boundary case. If exactly twelve do, the
other six points induce either three disjoint support edges of weight
two, or two disjoint edges of weight two and two isolated vertices.
Each of these six points has a distinct neighbor joined to it by an
edge of weight three. These six neighbors lie among the twelve points
of higher support degree. Their induced support graph has maximum
degree two and at least three edges in the first case, or five in the
second case. An isolated vertex here means isolated in the subgraph
on the six points, not in the whole support graph.

This is a necessary condition for the equality case of the known
upper bound. The interval remains \(69\le A(18,6,5)\le72\).
No realization or nonexistence of 72 blocks is claimed.

## 1. Incidence facts used in the proof

Write \(\mathcal L\) for the triples in no block, and \(L_x\) for its
link at \(x\). The following facts are proved in Sections 1–3 of
[PROOF.md](PROOF.md). Their external mathematical dependency is
Brouwer's established \(A(17,6,4)=20\): all 18 points must have
replication twenty.

* Every deficit is a nonnegative integer and
  \(\sum_{y\ne x}t_{xy}=5\).
* There are sixteen leave triples on a point and exactly
  \(1+3t_{xy}\) on a pair. Equivalently,
  \(\deg_{L_x}(y)=1+3t_{xy}\).
* If \(k_x=2\), every leave triple on \(x\) contains one of its two
  support neighbors, and the triple consisting of \(x\) and both
  neighbors is in the leave. We call these the double-star rules.
* If any \(k_x=1\), the unique incident edge has weight five, its
  endpoints form a pair in no block, and the other sixteen points
  have support degree at least three.
* No whole support component consists of points of support degree
  two.

For the last fact, such a component is an even cycle. A four-cycle
forces two leave triples on an opposite pair of deficit zero. A cycle
of length \(m\ge6\) has exactly \(m\) internal leave triples and no
leave triple meeting it in one point. If \(b\) counts leave triples
meeting it in two points, then
\(2b=m(18-m)\) and \(16m=3m+2b\), forcing \(m=5\), a contradiction.

The weight-five case already satisfies the theorem. Otherwise every
point has support degree at least two. Partition the points as
\(S\sqcup H\), with support degrees two on \(S\) and at least three
on \(H\), and write \(s=|S|=18-h\), \(h=|H|\). Every edge incident
with a point of \(H\) has weight at most three, because its other
two or more positive incident weights must fit into the total five.

## 2. Paths on the degree-two points

The induced support graph on \(S\) is a disjoint union of isolated
vertices and paths: its maximum degree is two, and a cycle would be
a whole support component excluded above. Consider a path component
\(x_1,\ldots,x_\ell\) with \(\ell\ge3\), and write
\(w_i=t_{x_ix_{i+1}}\).
Its endpoint neighbors outside the path are in \(H\). They may
coincide; the following argument does not require distinct endpoints.

For \(z\in H\), let \(f_i(z)\) indicate whether
\(zx_ix_{i+1}\in\mathcal L\). An internal point \(x_j\) has precisely
its two path neighbors in the support. The pair \(zx_j\) has deficit
zero and hence leave codegree one. The double-star rule permits only
the two adjacent path triples as its leave triples. Therefore
\[
f_{j-1}(z)+f_j(z)=1\qquad(2\le j\le\ell-1).
\tag{4}
\]
Let \(m_i=\sum_{z\in H}f_i(z)\). Then \(m_i+m_{i+1}=h\).

The only possible third points in \(S\) for a leave triple on
\(x_ix_{i+1}\) are \(x_{i-1}\) and \(x_{i+2}\), when present.
Both are forced by the double-star rule at the appropriate internal
point. Thus, with
\(c_i=2-\mathbf1_{i=1}-\mathbf1_{i=\ell-1}\),
\[
m_i=1+3w_i-c_i.
\tag{5}
\]
The weight total at an internal path point gives
\(w_i+w_{i+1}=5\). Combining (4) and (5) yields
\[
h=17-c_i-c_{i+1}\qquad(1\le i\le\ell-2).
\tag{6}
\]

For \(\ell=3\), this forces \(h=15\). For \(\ell=4\), it forces
\(h=14\). For \(\ell\ge5\), the first adjacent pair of edges forces
\(h=14\), while the second forces \(h=13\), which is impossible.
In particular, **if \(h\le12\), every component on \(S\) has one
or two vertices**.

## 3. A two-vertex component has weight two when h is at most twelve

Assume \(h\le12\), and let \(uv\) be a two-vertex component on \(S\)
with weight \(w\). Write \(a,b\in H\) for the other support neighbors
of \(u,v\), respectively. These need not be distinct. Their incident
weights are \(5-w\), so the bound of three at \(H\) gives \(w\ge2\).
Only points of \(H\) can be third points of leave triples on \(uv\).
If \(w=4\), its leave codegree thirteen already exceeds \(h\).

Suppose \(w=3\). Let \(U\subseteq H\) be the ten third points of
leave triples on \(uv\). The forced triple \(auv\) gives \(a\in U\).
In \(L_a\), the degree of \(u\) is seven, since \(t_{au}=2\).
Its possible neighbors are bounded as follows:

* The point \(v\) contributes one.
* A point \(z\in U\setminus\{a\}\) cannot contribute: \(uvz\) and
  \(auz\) would be two leave triples on the deficit-zero pair \(uz\).
  There are therefore at most \(h-10\) neighbors in \(H\).
* Any neighbor \(z\in S\setminus\{u,v\}\) must be a support neighbor
  of \(a\), by the double-star rule at \(z\): it cannot be a support
  neighbor of \(u\). After the weight-two edge \(au\), at most three
  positive edges remain at \(a\), so there are at most three such
  neighbors.

Consequently \(7\le1+(h-10)+3=h-6\), forcing \(h\ge13\).
This excludes \(w=3\) as well. Hence every two-vertex component on
\(S\) has weight two when \(h\le12\).

## 4. Distinct roots and the omitted-triple count

Continue to assume \(h\le12\). An isolated point of \(S\) has two
neighbors in \(H\), with weights two and three. A point in a
two-vertex component has weight two to its mate and weight three
to a point of \(H\). Thus every \(i\in S\) has a unique weight-three
neighbor \(r_i\in H\), its **root**.

The roots are distinct, since two edges of weight three cannot meet.
In particular \(s\le h\) and \(h\ge9\). At a root the two remaining
positive weights are exactly one and one. Their neighbors lie in
\(H\), because all support edges incident with \(S\) now have weight
two or three. Hence the induced support graph on
\(R=\{r_i:i\in S\}\) has maximum degree two, and its edge count
\(e_R\) is at most \(s\).

Let \(a\) count the isolated points in the subgraph on \(S\), and
let \(\epsilon_i=1\) when \(i\) has a mate in \(S\), zero otherwise.
The pair \(r_i i\) has ten leave triples. Its possible third points
are the \(h-1\) points of \(H\setminus\{r_i\}\) and, when present,
the mate of \(i\). The latter triple is forced. No other point of
\(S\) can contribute: such a point would need a support neighbor
among \(r_i,i\), and neither has any additional neighbor in \(S\).

Define an omission at \(i\) to be a point \(z\in H\setminus\{r_i\}\)
for which \(r_i i z\notin\mathcal L\). The exact number of omissions
at \(i\) is \(h-11+\epsilon_i\). Their total is therefore
\[
M=s(h-11)+(s-a)=s(h-10)-a.
\tag{7}
\]

If two roots \(r_i,r_j\) are not support neighbors, their pair has
leave codegree one. At least one of \(r_i i r_j\) and
\(r_j j r_i\) must be omitted, since these would otherwise be two
distinct leave triples on that pair. Each omission can cover at
most one such root nonedge. Omissions toward points outside \(R\),
or toward a support neighbor, only consume the available count.
It follows that
\[
\binom{s}{2}-e_R\le M=s(h-10)-a,
\qquad
\frac{s(s-3)}2\le s(h-10)-a.
\tag{8}
\]

For \(h=9,10,11\), respectively, \(s=9,8,7\). The left side of
the second inequality is \(27,20,14\); its right side is at most
\(-9,0,7\). All three cases are impossible. Along with \(h\ge9\)
and the already handled weight-five case, this proves \(h\ge12\).

If \(h=12\), then \(s=6\), and the first inequality in (8) gives
\(e_R\ge3+a\). Since \(e_R\le6\), we have \(a\le3\). The number
\(6-a\) is twice the number of two-vertex components, so \(a\) is
even. Hence \(a=0\) or \(a=2\), with the stated edge bounds.

## Sources, reproducibility and scope

* A. E. Brouwer, *A(17,6,4)=20 or the nonexistence of the scarce design
  SD(4,1;17,21)*, report ZW 62/75 (1975):
  <https://ir.cwi.nl/pub/6883/6883D.pdf>.
* Maintained bound table, rechecked 2026-09-30:
  <https://aeb.win.tue.nl/codes/Andw.html>.

This strengthens the nine-point restriction in [PROOF.md](PROOF.md).
The proof is an ordinary combinatorial argument, with the stated
external theorem dependency; it has not been formalized or independently
reviewed. The accompanying `check_support12.py` independently enumerates
the alternating leave-indicator carrier on paths and checks the
six-root omission carrier by an exact finite matching calculation.
Those computations validate local counts only; they do not enumerate
72-word codes, establish quadruple decomposability, or prove that any
remaining carrier has a global realization. The theorem itself does
not depend on the computation. No priority claim is made.
