# Exact obstruction proof

Let `G` be the 80-vertex graph in Table 4 of Exoo and Goedgebeur.  We use
their LCF labels

\[
  V(G)=\{i+4j:0\leq i<4,\ 0\leq j<20\}.
\]

The permutation `tau(v)=v+4 mod 80` has order 20 and is an automorphism.
An edge type `(i,i',m)` means that every pair

\[
  \{i+4j,\ i'+4(j+m)\},\qquad j\in\mathbb Z/20\mathbb Z,
\]

is an edge, after choosing the displayed orientation.  Direct reconstruction
of the LCF table gives 16 edge orbits, including

\[
 (0,0,8),\quad (1,1,4),\quad (0,1,0),\quad (0,1,11).                 \tag{1}
\]

## Theorem

There is no injective map `p:V(G)->R^2` and Euclidean isometry `rho` such that

1. every edge of `G` has Euclidean length one under `p`; and
2. `p(tau(v))=rho(p(v))` for every vertex `v`.

Nonedges are unrestricted, so this rules out both faithful unit-distance
embeddings and edge-preserving unit-distance realizations in this symmetry
class.

## Proof

Every `tau`-orbit has length 20.  Injectivity therefore makes the `rho`-orbit
of any image point have length exactly 20.  By the classification of plane
isometries, `rho` must be a rotation of order 20: translations and glide
reflections have no finite nonconstant orbit, while a reflection has order
two.  Move the rotation centre to the origin and write its angle as

\[
  \alpha=k\pi/10,\qquad \gcd(k,20)=1.
\]

Put `a_i=p(i)` and `r_i=|a_i|`.  The two same-orbit edge types in (1) give

\[
  2r_0^2(1-\cos 8\alpha)=1,\qquad
  2r_1^2(1-\cos 4\alpha)=1.                                      \tag{2}
\]

For primitive `k`, the unordered pair

\[
  \{\cos 8\alpha,\cos 4\alpha\}
   =\{\cos(2\pi/5),\cos(4\pi/5)\}.
\]

If these two cosine values are `c,d`, then
`c+d=-1/2` and `cd=-1/4`.  Consequently (2) implies

\[
\begin{aligned}
 r_0^2+r_1^2
 &=\frac1{2(1-c)}+\frac1{2(1-d)}\\
 &=\frac{2-c-d}{2(1-c-d+cd)}=1.                                  \tag{3}
\end{aligned}
\]

The cross-orbit type `(0,1,0)` now yields

\[
  1=|a_0-a_1|^2=r_0^2+r_1^2-2a_0\mathbin{\cdot}a_1,
\]

so `a_0` and `a_1` are perpendicular.  Type `(0,1,11)` similarly says that
`a_0` and `rho^11(a_1)` are perpendicular.  Both radii are nonzero by (2).
The directed angles in the two perpendicularities differ by `11 alpha`, so
`11 alpha` must be an integer multiple of `pi`.  This requires

\[
  10\mid 11k,
\]

which is impossible when `gcd(k,20)=1`.  This contradiction proves the
theorem.

The verifier reconstructs all edges and edge orbits from the published LCF
table and checks (3) in exact arithmetic in `Q(sqrt(5))` for every primitive
rotation exponent `k` modulo 20.
