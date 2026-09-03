# Conformal complement constraints at the Albertson \(r=27\) frontier

## Result

Let \(G\) be a \(k\)-critical graph, let \(H=\overline G\), and suppose
that \(H\) is connected.  A triangle \(T\) of an odd-order graph is called
**conformal** here if \(H-T\) has a perfect matching.  A four-vertex diamond
is called conformal if deleting its four vertices leaves a perfect matching.

The two orders adjacent to \(2k\) have sharply different complement
normal forms.

### Odd order \(2k-1\)

Suppose \(|G|=2k-1\).  Then:

1. \(H\) is factor-critical and has no conformal triangle.
2. Let \(v\) have \(d_G(v)=k-1\), and put
   \[
       A=N_H(v),\qquad B=V(H)\setminus(A\cup\{v\}).
   \]
   Thus \(|A|=|B|=k-1\).  Every perfect matching of \(H-v\) lies
   entirely in the bipartite graph \(H[A,B]\).
3. Fix any such matching and write it as
   \(M=\{a_i b_i:1\leq i\leq k-1\}\), with \(a_i\in A\) and
   \(b_i\in B\).  For every distinct \(i,j\),
   \[
       a_i a_j\in E(H)\quad\Longrightarrow\quad b_i b_j\notin E(H).
   \]
   Equivalently, under the matching bijection, the two internal shadow
   graphs \(H[A]\) and \(H[B]\) are edge-disjoint subgraphs of
   \(K_{k-1}\).  In particular,
   \[
       e_H(A)+e_H(B)\leq \binom{k-1}{2}.
   \]
4. Moreover, \(H[B]\) is nonempty.

At the order-53 Albertson frontier, write
\(x=e_H(A)\), \(y=e_H(B)\), and \(z=e_H(A,B)\).  For every degree-26
vertex of \(G\), the preceding conclusions and \(\Delta(H)\leq26\) give:

| \(m=|E(G)|\) | number of such vertices | \(x+y+z\) | \(z\) lower bound | bounds on \(x-y\) |
|---:|---:|---:|---:|---:|
| 713 | at least 5 | 639 | 314 | \(-37\leq x-y\leq11\) |
| 714 | at least 3 | 638 | 313 | \(-38\leq x-y\leq12\) |
| 715 | at least 1 | 637 | 312 | \(-39\leq x-y\leq13\) |

In every row, additionally \(x+y\leq325\), \(y\geq1\), and the
bipartite graph \(H[A,B]\) has a perfect matching.  These constraints hold
for **every** perfect matching of \(H-v\), not just for the one obtained
from a selected coloring.

### Even order \(2k\)

Suppose \(|G|=2k\).  For every vertex \(v\), there is a triangle \(T\)
of \(H-v\) such that
\[
                 H-(T\cup\{v\})
\]
has a perfect matching.

If in addition \(d_G(v)=k-1\), the triangle can be labelled
\(T=\{a,a',b\}\) so that
\[
 a,a'\in N_H(v),\qquad b\in N_G(v).
\]
Consequently \(H[\{v,a,a',b\}]\) is exactly a diamond
\(K_4-vb\), and this diamond is conformal.  The other \(2k-4\) vertices
are paired by a perfect matching.

For the order-54 survivor \((|G|,m)=(54,726)\), at least six vertices
of \(G\) have degree 26 and hence root such a conformal diamond.  For each
such root \(v\), put \(A=N_H(v)\), \(B=N_G(v)\), and again write
\(x=e_H(A)\), \(y=e_H(B)\), \(z=e_H(A,B)\).  Then
\[
 |A|=27,\quad |B|=26,\quad x+y+z=678,
 \quad |x-y|\leq24,
\]
and the displayed coloring supplies \(x\geq1\) and \(z\geq27\).

These are necessary conditions only.  They neither classify the surviving
graphs nor prove Albertson's conjecture for \(r=27\).

## Proof

Stehlik proved that for every vertex \(v\) of a \(k\)-critical graph with
connected complement, \(G-v\) has a \((k-1)\)-coloring in which every
color class has at least two vertices.  A color class of \(G-v\) is a
clique of \(H-v\).

If \(|G|=2k-1\), all \(k-1\) classes in Stehlik's coloring are pairs.
Hence \(H-v\) has a perfect matching for every \(v\), so \(H\) is
factor-critical.  Also \(H\) cannot have a conformal triangle \(T\): the
triangle together with a perfect matching of \(H-T\) would partition
\(V(G)\) into one independent triple and \(k-2\) independent pairs,
giving a \((k-1)\)-coloring of \(G\).

Now let \(d_G(v)=k-1\).  Then \(|A|=|B|=k-1\).  Consider an arbitrary
perfect matching \(M\) of \(H-v\).  If \(M\) contained an edge
\(aa'\) of \(H[A]\), then \(vaa'\) would be a triangle and
\(M-aa'\) would be a perfect matching of \(H-\{v,a,a'\}\), contrary to
the absence of conformal triangles.  Thus \(M\) contains no edge of
\(H[A]\).  Since the two sides have equal size, it also contains no edge
of \(H[B]\), and therefore it is a perfect matching of \(H[A,B]\).

Fix the resulting labelling \(a_i b_i\in M\).  If both
\(a_i a_j\) and \(b_i b_j\) were edges of \(H\), replacing
\(a_i b_i,a_j b_j\) in \(M\) by those two internal edges would produce a
perfect matching of \(H-v\) containing an edge of \(H[A]\), which was
just shown impossible.  Thus the internal shadows are edge-disjoint and
their total number of edges is at most \(\binom{k-1}{2}\).

Finally choose any \(a\in A\) and a perfect matching of \(H-a\), which
exists by factor-criticality.  The vertex \(v\) is matched to some vertex
of \(A-a\).  After deleting that matching edge, the vertices still to be
matched comprise \(k-3\) vertices of \(A\) and \(k-1\) vertices of
\(B\).  If the matching uses \(p_A\) further edges inside \(A\),
\(p_B\) edges inside \(B\), and \(c\) cross edges, then
\[
 2p_A+c=k-3,\qquad 2p_B+c=k-1.
\]
Hence \(p_B=p_A+1\), proving that \(H[B]\) has an edge.

For \(|G|=2k\), Stehlik's coloring of \(G-v\) has one class of size
three and \(k-2\) classes of size two.  This proves the first even-order
statement.  If \(d_G(v)=k-1\), criticality says that every color class
contains a neighbor of \(v\); otherwise its color could be assigned to
\(v\).  There are exactly \(k-1\) neighbors and \(k-1\) classes, so each
class contains exactly one neighbor.  The triple therefore contains one
vertex \(b\in N_G(v)\) and two vertices \(a,a'\in N_H(v)\).  All three
are mutually adjacent in \(H\), while \(v\) is adjacent in \(H\) exactly
to \(a,a'\) among these three.  This is the asserted conformal diamond.

It remains only to check the numerical specializations.  At order 53,
\(e(H)=1378-m\) and a degree-26 root has 26 incident complement edges, so
\(x+y+z=1352-m\).  The paired-shadow bound gives
\(z\geq1352-m-325\).  Since \(\Delta(H)\leq26\), summing degrees in
\(H-v\) over \(A\) and over \(B\) gives
\[
 2x+z\leq650,\qquad 2y+z\leq676,
\]
which yields the tabulated bounds on \(x-y\).

At order 54, \(e(H)=1431-726=705\), and a degree-26 root has complement
degree 27, whence \(x+y+z=678\).  Here \(\Delta(H)\leq27\), so
\[
 2x+z\leq702,\qquad 2y+z\leq702,
\]
and therefore \(|x-y|\leq24\).  The triple contributes one edge inside
\(A\) and two cross edges, while the other 25 color pairs contribute 25
more cross edges.  Thus \(x\geq1\) and \(z\geq27\).

In either order, the number of degree-26 vertices is at least the order
minus the total degree excess \(2m-26|G|\), giving respectively
\(5,3,1\) and \(6\).

## Reproduction

Run:

```sh
python3 verify.py
```

The dependency-free script checks the color-class size distributions,
matching balance identities, all exact frontier arithmetic, and the local
edge-count inequalities.  The matching and coloring arguments above are
deductive; the script does not enumerate critical graphs or certify that a
survivor exists.

## Sources and novelty scope

* A. Sadhu, *Albertson's Conjecture Holds for \(r\) at Most 26*,
  arXiv:2609.01682 (2026): <https://arxiv.org/abs/2609.01682>.
* M. Stehlik, *Critical graphs with connected complements*, J. Combin.
  Theory Ser. B 89 (2003), 189--194:
  <https://doi.org/10.1016/S0095-8956(03)00069-8>.
* A. V. Kostochka, *Color-critical graphs and hypergraphs with few edges:
  a survey*, Bolyai Soc. Math. Stud. 15 (2006), 175--197:
  <https://kostochk.web.illinois.edu/docs/2008/book06.pdf>.

The factor-critical/perfect-matching starting point was recorded in the
preceding frontier note.  The contribution here is the next parity-sensitive
layer: exclusion of conformal triangles at order 53, the resulting
all-perfect-matchings and paired-shadow constraints with exact cut bounds,
and the conformal-diamond normal form at every low vertex at order 54.  A
targeted search of the cited sources, current Albertson literature, and the
committed Discovery Net found no prior statement of this combined frontier
specialization.  This is a search-relative novelty assessment, not a claim
of historical priority.
