# A universal subcubic-core reduction for the cyclomatic signature conjecture

All graphs are finite, simple and connected. Write

```text
In(X)=(n_+(X),n_0(X),n_-(X)),   sig(X)=n_+(X)-n_-(X),
c(G)=|E(G)|-|V(G)|+1,          M(G)=Q(G)-2I,
s(G)=sig(A(L(G))),            D(G)=2s(G)-c(G)-1.
```

Here `s(G)` abbreviates the signature of the **line graph**, not of `G`.
The Paone--Paone sharp conjecture says `D(G)<=0`. It remains open.

## 1. Main reduction

Let `G` have `n>=2` vertices, `m` edges, `ell` leaves, and put

```text
a=sum_(v in V(G)) max(deg_G(v)-3,0).
```

There is an explicit connected simple graph `H` with every degree in `{2,3}`
such that

```text
|V(H)|=n+4a+9ell,          |E(H)|=m+4a+11ell,
c(H)=c(G)+2ell,
In(A(L(H)))=In(A(L(G)))+(2a+6ell,0,2a+5ell).          (1)
```

Consequently

```text
s(H)=s(G)+ell,                 D(H)=D(G),              (2)
nullity A(L(H))=nullity A(L(G)).
```

If `G` has minimum degree at least two, then `ell=0`: the transformation
preserves both cyclomatic number and line-graph signature. It handles
arbitrarily high degrees. For a graph with pendant trees, it preserves the
conjecture's exact slack by increasing cyclomatic number by `2ell`.
It does **not** assert that pruning those trees preserves signature.

Thus the following assertions are equivalent:

1. `2s(G)<=c(G)+1` for all connected simple graphs.
2. The same inequality for connected simple graphs of minimum degree two
   and maximum degree three.
3. The same inequality for that class with arbitrarily prescribed minimum
   girth `g>=3` (for each fixed `g`).

The equivalence remains true if class 2 is restricted to cyclomatic number
at least two. Cycles satisfy the inequality directly, and the singleton is
trivial. In particular, one universal proof on subcubic cores would settle
the unrestricted conjecture, including all pendant forests.

## 2. A four-edge vertex split

Partition the neighbors of a vertex `v` into two nonempty groups `U,W` of
sizes `d1,d2`. Replace `v` by `u,w`, retaining the neighbors in `U` at `u`
and those in `W` at `w`. Join the two new vertices by the path

```text
u -- p -- q -- r -- w.
```

This adds four vertices and four edges. The resulting graph `G'` is simple
and connected and has the same cyclomatic number. We prove the full identity

```text
M(G') is congruent to M(G) direct-sum J direct-sum J,
J=[[0,1],[1,0]].                                      (3)
```

Use a vector `z` for the other old vertices, and let `f,g` be the incidence
vectors of `U,W` in those coordinates. The unaffected principal block is
`B=M(G)[V(G)\{v}]`. Put `alpha=d1-1`, `beta=d2-1`. The quadratic form of
`M(G')` is

```text
z^T B z + alpha u^2 + beta w^2
 + 2u f^T z + 2w g^T z + 2up + 2pq + 2qr + 2rw.     (4)
```

First substitute `p=A-r`, `q=B0-u`. The four path terms become
`2A B0+2r(w-u)`. Now set

```text
u=x,          w=x+y,
r=t-beta x-g^T z-(beta/2)y.                           (5)
```

The resulting form is exactly

```text
z^T B z +(d1+d2-2)x^2+2x(f+g)^T z +2A B0+2yt.
```

Every substitution is invertible. This proves (3), including when the old
matrix is singular. In particular the split adds `(2,0,2)` to the inertia
of `M` and preserves its nullity and determinant.

For the unsigned vertex-edge incidence matrix `N`,

```text
NN^T=Q(G),        N^TN=A(L(G))+2I.
```

The common nonzero spectra give, for every connected graph with an edge,

```text
n_+(A(L(G)))=n_+(M(G)),
n_0(A(L(G)))=n_0(M(G)),
n_-(A(L(G)))=n_-(M(G))+c(G)-1.                        (6)
```

The last difference can be negative for a tree; the identity still holds.
Since the split preserves `c`, it also adds `(2,0,2)` to line-graph inertia.

At every vertex of degree `d>=4`, choose a group of two neighbors. The new
endpoint degrees are `3` and `d-1`. The total degree excess above three drops
by exactly one. Other old degrees do not change and new internal degrees
are two. After exactly `a` splits the graph is subcubic, and its original
`ell` leaves are unchanged. There are no new leaves.

## 3. A known zero-response module closes each leaf

The module in this section is Paone's published rooted `C4--C5` module.
Its zero-response attachment principle and inertia are prior results;
the use here is to preserve `D` while removing all leaves. We give a short
self-contained verification, so no external data or computed inertia is a
proof premise.

Take the cycles `(0,1,2,3,0)` and `(4,5,6,7,8,4)`, the bridge `04`, and the
root edge `19`, whose root is vertex `9`. Denote the resulting graph by `F`,
its line-graph adjacency matrix by `K`, and its root-edge coordinate by `rho`.
Then

```text
|V(F)|=10, |E(F)|=11, c(F)=2,
In(K)=(6,0,5),       (K^-1)_(rho,rho)=0.              (7)
```

To verify the inertia, first eliminate the five edge coordinates of the
5-cycle. Their block is `A(C5)` with inertia `(3,0,2)`. The remaining block
has the four 4-cycle edge coordinates and the two bridge/root coordinates.
The 4-cycle block has inertia `(1,2,1)`. In cyclic edge order a kernel basis
is `(1,0,-1,0)` and `(0,1,0,-1)`. The bridge and root couple to this basis
through rows `(1,-1)` and `(1,1)`. This coupling is invertible. After the
invertible range of the 4-cycle block is eliminated, the remaining four
coordinates have the form

```text
[[C,T],[T^T,0]],        det(T)!=0.
```

For any symmetric `C`, this form has inertia `(2,0,2)`: an invertible change
on the zero-block coordinates makes `T=I`, and a shear removes `C`.
Adding these inertias proves `(6,0,5)` and nonsingularity.

For the response, assign values `1/2,1/2,-1/2,-1/2` to the 4-cycle edges
`01,12,23,03` and zero to every other module edge. Directly from shared
endpoints, this vector `z` satisfies `Kz=e_rho`, with `z_rho=0`. This proves
the second identity of (7). The checker also computes `det K=-8`.

Identify root `9` with any host vertex `x`. In edge coordinates the enlarged
line graph has adjacency matrix

```text
[[A(L(G)), b e_rho^T], [e_rho b^T, K]],               (8)
```

where `b` indicates old edges incident with `x`. Eliminating `K` leaves
`A(L(G))-b b^T(K^-1)_(rho,rho)=A(L(G))`. Therefore this operation adds
`(6,0,5)` to line-graph inertia, adds nine vertices and eleven edges, and
increases `c` by two. It preserves `D` and nullity exactly.

Apply it to each of the `ell` leaves after the degree reduction. Each such
leaf now has degree two; every added vertex has degree two or three. The
operations have disjoint new vertices and create no leaves. This proves
(1)--(2). Notice that we cap the actual leaves of the whole graph; no claim
about monotonicity under 2-core deletion is needed.

The input singleton has `s=0,c=0`. If the constructed core has cyclomatic
number one, it is a cycle. Directly from the cycle eigenvalues, `s(C_k)` is
`0,1,0,-1` for `k=0,1,2,3 mod 4`. Thus cycles satisfy the sharp inequality.
Every other output is a subcubic core with cyclomatic number at least two.

## 4. The remaining matrix inequality is now universal

We use the prior parity-kernel theorem, restating its exact conventions.
Suppress the maximal degree-two paths of a connected subcubic core of
cyclomatic number `c>=2`. Its kernel is a connected cubic pseudograph on

```text
b=2c-2 vertices, with 3b/2 edges.
```

Loops count twice toward degree. Give each kernel edge the residue modulo
four of its path length. Start `P=I_b`. An odd edge adds `+1` (residue one)
or `-1` (residue three) to its two symmetric off-diagonal positions; a loop
adds twice that sign to its diagonal. Each even edge gives a row of `V`:

```text
residue zero: e_u-e_v;       residue two: e_u+e_v.
```

A residue-zero loop gives a zero row; a residue-two loop gives `2e_u`.
Let the columns of `Z` be any basis of `ker V`, including the empty basis.
The parity-kernel congruence gives

```text
s(H)=sig(Z^T P Z)-c(H)+1.                            (9)
```

The full graph conjecture is therefore **equivalent** to

```text
4 sig(Z^T P Z) <= 3b+4                               (10)
```

for every connected cubic pseudograph and every assignment of the four
residues. In one direction use the universal reduction and (9). In the other,
every residue assignment has a simple realization: choose lengths `4,5,2,3`
for nonloop residues `0,1,2,3`, and `4,5,6,3` for loop residues. Interiors
are private to each path. No length-one path is used, so parallel kernel
edges cause no multiple edges in the realization.

Thus high-degree vertices and pendant trees require no separate inequality
beyond (10). The low-rank parity cases of (10) remain unresolved. We have not
proved (10), nor produced a counterexample.

## 5. Finite representatives and arbitrary girth

Adding four edges to a branch path preserves line-graph signature and
nullity, adding `(2,0,2)` to both shifted vertex inertia and line inertia.
One direct verification replaces an edge by a five-edge path and eliminates
its four internal coordinates. Their block is `A(P4)`, whose inverse has
zero endpoint diagonal entries and endpoint cross-entry `-1`; the Schur
complement is the original `M(G)`. This period-four identity is prior work.

Consequently every subcubic core has the same `c,s` as the simple residue
realization just described. If the kernel has `l` loops, its nonloop edges
connect its `b` vertices, so `3b/2-l>=b-1`, giving `l<=b/2+1=c`.
The representative has at most

```text
b+4(3b/2-l)+5l = 7b+l <= 15c-14                     (11)
```

vertices. For each fixed `c>=2`, every minimum-degree-two graph, with no
degree bound, therefore has a subcubic representative on at most `15c-14`
vertices with identical cyclomatic number and line-graph signature. This
is a complete finite reduction for cores, not an enumeration of that finite
set. Nullities of the representative and original graph agree as well.

For a general input `G` with `ell` leaves, the corresponding compact
representative has cyclomatic number `c(G)+2ell` and at most
`15(c(G)+2ell)-14` vertices whenever that number of cycles is at least two.
It preserves `D(G)`. This does not bound the order of a representative in
terms of the original cyclomatic number alone when leaves are unrestricted.

Conversely, subdivide every edge of the constructed core into `4k+1` edges.
Signature, nullity, cyclomatic number and `D` remain unchanged, and every
cycle length is multiplied by `4k+1`. Taking `k` large gives any prescribed
minimum girth. This proves assertion 3 in Section 1.

## 6. Scope and evidence

The new content is the four-edge vertex split and its composition with the
known attachment module into the universal exact-slack reduction. Equations
(10)--(11) explain what that reduction unlocks using the prior parity theorem.
The matrix congruences above prove the statements at all orders. Finite
checks audit the constructor, edge definitions, singular cases, module,
residue decoding and counts; they are not an exhaustive proof of the open
inequality. No floating point, solver, external dataset, or omitted large
certificate is a premise. The code is author verification, not independent
peer review or formalization. See SOURCES.md for the bounded novelty search.
