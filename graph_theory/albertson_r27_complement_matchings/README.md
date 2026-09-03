# Complement matching normal forms at the Albertson \(r=27\) frontier

## Claim

Let \(G\) be a \(k\)-critical graph and put \(H=\overline G\).  Assume that
\(H\) is connected.

1. If \(|G|=2k-1\), then \(H\) is factor-critical.  If in addition
   \(d_G(v)=k-1\), then
   \[
       H[N_H(v),N_G(v)]
   \]
   has a perfect matching (both sides have size \(k-1\)).
2. If \(|G|=2k\), then \(H\) has a perfect matching.  If in addition
   \(d_G(v)=k-1\), then \(|N_H(v)|=k\), \(|N_G(v)|=k-1\), and
   \(H[N_H(v),N_G(v)]\) has a matching saturating \(N_G(v)\).  Together
   with the edge from \(v\) to the one unused vertex of \(N_H(v)\), this
   matching is a perfect matching of \(H\).

Consequently, let \(G\) be a hypothetical counterexample at \(r=27\), after
passing to the 27-critical subgraph supplied by Sadhu's frontier theorem.
Write \(m=|E(G)|\).

* If \((|G|,m)=(53,713+s)\), where \(s\in\{0,1,2\}\), then \(H\) is
  factor-critical and has at least \(5-2s\) vertices \(v\) for which the
  balanced bipartite graph \(H[N_H(v),N_G(v)]\) has a perfect matching.
* If \((|G|,m)=(54,726)\), then \(H\) has a perfect matching and has at
  least six vertices \(v\) for which
  \(H[N_H(v),N_G(v)]\) has a 26-edge matching saturating \(N_G(v)\).

These are necessary conditions, not a proof of Albertson's conjecture at
\(r=27\).

## Proof

Stehlik proved that, for every vertex \(v\) of a \(k\)-colour-critical graph
whose complement is connected, \(G-v\) has a \((k-1)\)-colouring in which
every colour class has at least two vertices.

Suppose first that \(|G|=2k-1\).  The \(2k-2\) vertices of \(G-v\) are
therefore partitioned into \(k-1\) independent pairs.  Every pair is an edge
of \(H-v\), so these pairs form a perfect matching of \(H-v\).  This holds
for every \(v\), proving that \(H\) is factor-critical.

Now suppose that \(|G|=2k\).  For every \(v\), the colour classes of
\(G-v\) consist of one triple and \(k-2\) pairs.  In \(H-v\) they span a
vertex-disjoint \(K_3\) and \(k-2\) copies of \(K_2\), hence \(H-v\) has a
matching of size \(k-1\).  We show that \(H\) has a perfect matching.  If
not, Tutte's theorem gives a set \(S\) with
\(o(H-S)>|S|\).  Since \(|H|\) is even, parity gives
\(o(H-S)\ge |S|+2\).  Connectedness and the even order of \(H\) imply
\(S\ne\varnothing\); choose \(v\in S\).  But \(H-v\) has a matching that
misses only one vertex.  For any vertex set \(T\), such a matching forces
\(o((H-v)-T)\le |T|+1\): apart from possibly the component containing the
one unmatched vertex, every odd component must send a matching edge to a
distinct vertex of \(T\).  Applying this with \(T=S\setminus\{v\}\) gives
\[
  o(H-S)\le |S\setminus\{v\}|+1=|S|,
\]
a contradiction.

It remains to prove the local assertions.  If \(d_G(v)=k-1\), criticality
forces \(v\) to have a neighbour in every colour class of every
\((k-1)\)-colouring of \(G-v\); otherwise that class's colour could be
assigned to \(v\).  There are exactly \(k-1\) neighbours, so there is exactly
one in each class.

At order \(2k-1\), each colour pair therefore contains one vertex of
\(N_G(v)\) and one vertex of \(N_H(v)\).  Its \(H\)-edge gives the asserted
perfect matching between those two sets.

At order \(2k\), the same holds for the \(k-2\) colour pairs.  In the colour
triple, one vertex lies in \(N_G(v)\) and two lie in \(N_H(v)\).  Match the
former to either of the latter in \(H\), use the \(k-2\) pair edges, and
match \(v\) to the remaining vertex of the triple.  This proves both local
assertions.

For the numerical consequences, every 27-critical graph has minimum degree
at least 26.  At order 53 this gives \(\Delta(H)\le26\), and
\[
 \sum_x(26-d_H(x))=26\cdot53-2\left(\binom{53}{2}-m\right)
 =48+2s.
\]
Thus at most \(48+2s\) vertices have degree below 26, leaving at least
\(5-2s\) vertices of degree 26 in \(H\), equivalently degree 26 in \(G\).
At order 54, \(\Delta(H)\le27\) and
\[
 \sum_x(27-d_H(x))=27\cdot54-2\left(\binom{54}{2}-726\right)=48,
\]
so at least six vertices have degree 27 in \(H\), equivalently degree 26 in
\(G\).  The local assertions apply to all of them.

## The displayed order-\(2k\) equality family is excluded

Kostochka and Stiebitz exhibit the following order-\(2k\), excess
\(2(k-3)\) family.  Its vertices are four nonempty disjoint sets
\(A,S_1,S_2,S_3\), with \(|A|=k-2\) and
\(|S_1|+|S_2|+|S_3|=k-1\), and three vertices \(c_1,c_2,c_3\).  The sets
\(A\) and \(S_1\cup S_2\cup S_3\) are cliques, there are no edges between
them, and
\(N_G(c_i)=A\cup S_i\).

Every graph in this displayed family contains a subdivision of \(K_k\).
Indeed, take branch vertices \(A\cup\{c_1,c_2\}\).  All branch pairs are
edges except \(c_1c_2\).  For arbitrary \(s_i\in S_i\), replace that missing
edge by the path
\[
                 c_1s_1s_2c_2.
\]
Its internal vertices are not branch vertices.  Thus the order-54 survivor
cannot belong to this family, because a graph containing a subdivision of
\(K_{27}\) has crossing number at least that of \(K_{27}\).  This does not
classify all order-\(2k\) equality graphs: the cited paper asserts only that
the displayed family is contained in the extremal class.

## Reproduction and trust boundary

Run:

```sh
python3 verify.py
```

The script checks the exact deficit arithmetic and, for all 300 ordered
positive triples \((|S_1|,|S_2|,|S_3|)\) summing to 26, constructs the
displayed equality graph and verifies its order, size, minimum degree,
excess, connected complement, and the explicit topological \(K_{27}\)
certificate.  The structural proof itself is deductive; the script does not
verify criticality or enumerate all critical graphs.

## Sources and novelty scope

* A. Sadhu, *Albertson's Conjecture Holds for \(r\) at Most 26*, arXiv:2609.01682
  (2026): <https://arxiv.org/abs/2609.01682>.
* M. Stehlik, *Critical graphs with connected complements*, J. Combin.
  Theory Ser. B 89 (2003), 189--194:
  <https://doi.org/10.1016/S0095-8956(03)00069-8>.
* A. V. Kostochka and M. Stiebitz, *Excess in Colour-Critical Graphs*,
  Bolyai Society Mathematical Studies 7 (1999), 87--99:
  <https://old.renyi.hu/bolyai_archivum/BJMT-7.PDF>.

The ingredients about colourings and matchings are classical.  The claimed
contribution is their explicit specialization to all four surviving
\((n,m)\) pairs at the September 2026 \(r=27\) frontier, including the local
matching normal forms and exact low-degree multiplicities, together with the
explicit exclusion of the displayed order-\(2k\) equality construction.  A
search of the cited sources, later edge-bound literature, and the local
Discovery Net found no prior statement of this combined reduction.  No claim
is made that each ingredient is new or that all equality cases have been
classified.
