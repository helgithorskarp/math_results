# Uniform one-deficit extension and a binary boundary signature

## 1. Moore-graph setup

Let `G` be a diameter-two Moore graph of degree `k`.  Thus `G` has `k^2+1`
vertices, girth five, and every two nonadjacent vertices have exactly one
common neighbor.  Equivalently, its adjacency matrix satisfies

\[
 A^2=(k-1)I-A+J.                                      \tag{1}
\]

Assume

\[
 k=r^2+r+1                                             \tag{2}
\]

for an integer `r>=5`.  On the orthogonal complement of the all-one vector,
(1) gives the eigenvalues `r` and `-r-1`.  Hoffman's ratio bound is therefore

\[
 \alpha(G)\le
 \frac{(k^2+1)(r+1)}{k+r+1}
 =(r+1)(r^2+1)=rk+1.                                  \tag{3}
\]

## Theorem 1 (uniform one-deficit extension)

Every independent set `S` of size `rk` is contained in a unique independent
set of size `rk+1`.  More precisely, among the vertices outside `S`, the
multiset of neighbor counts

\[
 a_x=|N(x)\cap S|
\]

is

\[
 0^1,\qquad r^k,\qquad (r+1)^{kr^2}.                  \tag{4}
\]

### Moment and pointwise identities

Put `H=G-S`, `h=r+1`, and `z_x=a_x-h` for `x in H`.  Counting edges from
`S` to `H`, and then counting the unique common neighbor of every pair of
vertices of `S`, gives

\[
 \sum_H a_x=k|S|,
 \qquad
 \sum_H a_x(a_x-1)=|S|(|S|-1).                        \tag{5}
\]

Using `|S|=rk` and `|H|=k(r^2+1)+1`, direct simplification gives

\[
 \sum_Hz=-(r^2+2r+2)=:-D,
\]

\[
 \sum_Hz^2=2r^2+3r+2=:Q,
 \qquad
 \sum_Hz(z+1)=r^2+r=k-1.                             \tag{6}
\]

For `x in H`, count incidences between `N_H(x)` and `S`.  A point of `S`
adjacent to `x` contributes none, by triangle-freeness; each of the other
`|S|-a_x` points contributes its unique common neighbor with `x`.  Since
`deg_H(x)=k-a_x`, this yields

\[
 A_Hz=rz-\mathbf1.                                    \tag{7}
\]

### No positive defect

Let `P={x:z_x>0}`.  Every term `z(z+1)` is nonnegative for integral `z`, and
each positive term is at least two.  Hence (6) gives

\[
 |P|\le\frac{r(r+1)}2.                                \tag{8}
\]

Restricting (7) to `P` and moving the nonpositive neighbor terms to the
right gives

\[
 A_{G[P]}z_P\ge (r-1)z_P.
\]

Thus `rho(G[P])>=r-1`.  Every graph `F` of girth at least five satisfies

\[
 \rho(F)^2\le |V(F)|-1:                               \tag{9}
\]

indeed, in each row of `A_F^2`, returning walks and distinct nonreturning
two-walk endpoints together occupy at most all other vertices.  Consequently

\[
 |P|\ge(r-1)^2+1.                                     \tag{10}
\]

For `r>=5`, (8) and (10) conflict because

\[
 (r-1)^2+1-\frac{r(r+1)}2
 =\frac{(r-1)(r-4)}2>0.
\]

Therefore `z<=0`.

### Exact negative profile

Write `w=-z` and let `W` be its positive support, of size `m`.  Equations
(6)--(7) become

\[
 \sum_Ww=D,\qquad \sum_Ww^2=Q,
 \qquad A_{G[W]}w=rw+\mathbf1.                        \tag{11}
\]

The Rayleigh quotient and (9) imply

\[
 m-1\ge\rho(G[W])^2
 \ge\left(r+\frac DQ\right)^2>r^2+r=k-1.             \tag{12}
\]

The strict inequality is exact: after multiplying by `Q^2`, its positive
difference is

\[
 (r+1)(3r^3+8r^2+8r+4).
\]

Hence `m>=k+1`, so `E:=D-m<=r`.  Put `t_x=w_x-1`.  From (11),

\[
 \sum_Wt_x=E,
 \qquad
 \sum_Wt_x^2=r^2+r-E.                                 \tag{13}
\]

Since the `t_x` are nonnegative integers,

\[
 r^2+r-E=\sum t_x^2\le\left(\sum t_x\right)^2=E^2.
\]

Equivalently `(E-r)(E+r+1)>=0`; together with `E<=r`, this forces `E=r`.
Equality in the square-sum bound forces one `t_x=r` and every other `t_x=0`.
Thus one `w` equals `r+1`, exactly `k` further values equal one, and all
remaining values vanish.  Translating from `w` to `a` proves (4).  The unique
vertex with `a=0` is the unique extension point, and (3) makes the enlarged
coclique maximum.  QED

For `r=7`, this specializes to degree 57 and the profile

```text
0^1, 7^57, 8^2793.
```

The restriction `r>=5` is the exact threshold of the positive-support
comparison, not a claim that Moore graphs exist for other such `r`.

## 2. The sharp deficit-two branch at degree 57

Now assume `G` has strongly regular parameters `(3250,57,0,1)`, and `S` is
an independent set of size 398.  For `x in H=G-S`, put

\[
 a_x=|N(x)\cap S|,\qquad z_x=a_x-8.
\]

The accepted sharp-star branch has the following necessary structure:

- the positive support is an induced `K_(1,33)`, with center weight `z=5`
  and leaf weights `z=1`;
- it has no edge to the negative support;
- on the negative support write `w=-z`; for one `t in {0,1,2,3}`, the
  multiplicities of weights one, two, and three are

  \[
  (n_1,n_2,n_3)=(150+3t,9-3t,t);
  \]

- the negative support lies in 24 Moore branches, each of total `w`-weight
  seven, and `A_Ww=7w+2\mathbf1`.
- every weight-three vertex has exactly 23 neighbors in the negative support,
  all of weight one and exactly one in each of the other 23 active branches.

These are hypotheses inherited from the independently accepted sharp-star
theorem; the results below compress its remaining compatibility problem.

## Theorem 2 (binary even-set reduction)

Let `Q` be the union of the positive star and the negative vertices of odd
weight.  Then

\[
 (A+I)\mathbf1_Q=0\quad\hbox{over }\mathbf F_2,        \tag{14}
\]

and

\[
 |Q|=184+4t\in\{184,188,192,196\}.                    \tag{15}
\]

Moreover, the positive `K_(1,33)` is a connected component of `G[Q]`.

### Proof

The deficit-two analogues of (7) and its pointwise `S` identity are

\[
 A_Hz=7z-2\mathbf1,
 \qquad
 \sum_{x\sim s}z_x=-2\quad(s\in S).                  \tag{16}
\]

Reducing (16) modulo two says that the odd-defect characteristic vector is
fixed by `A_H` and has zero adjacency sum on every point of `S`.  Extending
it by zero on `S` gives `A1_Q=1_Q`, which is (14).  Its support size is

\[
 34+n_1+n_3=34+(150+3t)+t=184+4t.
\]

The inherited absence of positive--negative edges makes the star a component.
QED

We call a set satisfying (14) an **even closed-neighborhood set**, since
every `N[v]` meets it evenly.

## Theorem 3 (odd boundary resolutions)

Let `Q` be any even closed-neighborhood set in a degree-`k` diameter-two
Moore graph.  Suppose `G[Q]` has a star component `C=K_(1,m)`, and put
`O=Q-C`.  Then `O` has

- one resolution into `k-m` nonempty odd blocks, indexed by the external
  neighbors of the star center;
- `m` resolutions into `k-1` nonempty odd blocks, one for each leaf; and
- no unordered pair of points of `O` occurs in two boundary blocks, even
  across different resolutions.

For the sharp degree-57 branch, `m=33`, so the remaining odd support of size
`150+4t` has one resolution into 24 odd blocks and 33 resolutions into 56 odd
blocks.

### Proof

For `c in C`, let `B_c=N(c)-C`.  Girth five makes the sets `B_c` disjoint:
adjacent center--leaf pairs have no common neighbor, while two leaves already
have the center as their unique common neighbor.  Thus every `b in B_c` has
exactly one neighbor in `C`.  Since `b` is outside `Q` and `N[b]` meets `Q`
evenly, the set

\[
 R_b=N(b)\cap O
\]

has positive odd size.

Every `o in O` is nonadjacent to every `c in C`, because they lie in distinct
components of `G[Q]`.  Their unique common neighbor belongs to exactly one
`B_c`.  Hence `{R_b:b in B_c}` partitions `O`.  The center has `k-m`
external neighbors and each leaf has `k-1`, proving the block counts.

Finally, if two points of `O` lay together in two distinct boundary blocks,
they would have two common neighbors; if they were adjacent, either common
neighbor would already form a triangle.  Both alternatives contradict the
Moore parameters.  QED

## 3. Canonical branch signatures

In each of the 24 active branches, let `(a,b,c)` count negative vertices of
weights one, two, and three.  The branch weight equation is

\[
 a+2b+3c=7,                                            \tag{17}
\]

so there are exactly eight branch types:

```text
(7,0,0) (5,1,0) (3,2,0) (1,3,0)
(4,0,1) (2,1,1) (0,2,1) (1,0,2).
```

Globally `sum b=9-3t` and `sum c=t`.  Enumerating nonnegative multiplicities
of these eight types gives respectively

```text
t = 0,1,2,3:  12, 16, 11, 2
```

unlabelled branch-composition multisets.  A weight-three vertex in branch `i`
therefore meets a weight-one vertex in every other branch `j`.  Distinct
weight-three vertices in branch `i` cannot use the same vertex in branch `j`:
two vertices in one Moore branch already share the branch root, so they cannot
have a second common neighbor.  Thus the necessary capacity inequalities are
`c_i<=a_j` for every `i!=j`.  They remove three of the `t=2` multisets, leaving

```text
t = 0,1,2,3:  12, 16, 8, 2,
```

or 38 canonical signatures in all.  This is a completeness-preserving
compression, not a realizability claim.

The two `t=3` signatures are the coarse branch patterns `1+1+1` and `2+1`.
A concurrent graph contribution at height 5316 independently sharpened those
two patterns to three exact support cores.  Accordingly, the present
signature screen claims new information only for its uniform derivation and
the 36 surviving signatures with `t<=2`, not for the coarse `t=3` pair.

The odd-resolution pair budget does not yet exclude any of the four values of
`t`.  Even after maximizing the possible number of edges among the odd
support by the trivial bound on weight-two pairs, the respective numbers of
unused nonedge pairs exceed the convex minimum needed by all 34 resolutions
by `5442,5862,6262,6642`.  Thus parity alone is not a hidden contradiction;
future work must use compatibility between the boundary resolutions and the
Moore-branch perfect matchings.
