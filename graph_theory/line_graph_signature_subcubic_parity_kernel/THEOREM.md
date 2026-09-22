# Parity-kernel inertia for subcubic 2-cores

## 1. Statement

All graphs are finite and simple.  For a real symmetric matrix `X`, write

```text
In(X)=(n_+(X),n_0(X),n_-(X)),   sig(X)=n_+(X)-n_-(X).
```

Let `H` be connected, with minimum degree two, maximum degree three, and
cyclomatic number

```text
c=|E(H)|-|V(H)|+1 >= 2.
```

Let `B` be its degree-three vertices and put `b=|B|`.  Removing `B` leaves
paths.  Equivalently, `H` is obtained from a connected cubic pseudograph
`K` on `B` by replacing every kernel edge `e` by a maximal branch path of
length `ell_e`.  Parallel kernel edges and loops are allowed; a loop records
a path that leaves and returns to the same branch vertex.  Since `H` itself
is simple, a loop path has length at least three and at most one path of
length one joins a given pair.

The degree sum gives

```text
b=2c-2.                                                   (1)
```

Define a symmetric `b` by `b` matrix `P`, initially `I_b`.  For each odd
branch path put

```text
epsilon_e = +1  if ell_e=1 mod 4,
            -1  if ell_e=3 mod 4.
```

If its endpoints are distinct `u,v`, add `epsilon_e` to `P_uv` and `P_vu`.
If it is a loop at `u`, add `2 epsilon_e` to `P_uu`.

For each even branch path form a row of a matrix `V`:

```text
ell_e=0 mod 4:   e_u-e_v,
ell_e=2 mod 4:   e_u+e_v.                                (2)
```

The formula includes loops literally: a `0 mod 4` loop gives the zero row,
and a `2 mod 4` loop gives `2e_u`.  Let `t` be the number of even paths,
`rho=rank(V)`, let the columns of `Z` be any basis of `ker(V)`, and put

```text
R=Z^T P Z,                    q=sum_e floor((ell_e-1)/2). (3)
```

The empty matrix is allowed when `rho=b`.

**Parity-kernel theorem.** One has

```text
In(Q(H)-2I)
  = (q+rho+n_+(R),  t-rho+n_0(R),  q+rho+n_-(R)).         (4)
```

Consequently

```text
sig(Q(H)-2I)=sig(R),                                    (5)
s(L(H))=sig(R)-c+1.                                     (6)
```

Thus all dependence of the line-graph signature on arbitrarily long
degree-two paths is compressed to a form of order at most `2c-2`, and only
the path lengths modulo four enter that form.

## 2. The path calculation

Order the vertices with `B` first and the internal vertices of each branch
path afterward.  On a path of length `ell`, the internal block of
`Q(H)-2I` is the adjacency matrix `A(P_(ell-1))`, because every internal
vertex has degree two.

For `m>=1`,

```text
In(A(P_m))=(floor(m/2), 1_(m odd), floor(m/2)).           (7)
```

If `m` is even, this matrix is invertible, its two endpoint diagonal entries
in the inverse vanish, and

```text
(A(P_m)^-1)_(1,m)=(-1)^(m/2+1).                         (8)
```

Schur complementation therefore replaces an odd branch path by one signed
kernel edge: the resulting sign is `+1` for length `1 mod 4` and `-1` for
length `3 mod 4`.  Formula (8) also gives the factor two on a loop.  A direct
edge is the `ell=1` instance of the same rule.

If `m` is odd, its kernel is spanned by

```text
(1,0,-1,0,1,0,...,(-1)^((m-1)/2)).                      (9)
```

The two endpoint values of (9) are `(1,-1)` when `ell=0 mod 4` and
`(1,1)` when `ell=2 mod 4`.  These are exactly the rows in (2).  The
restriction of the path block to its range contributes equally many
positive and negative directions, namely `floor((ell-1)/2)` of each.  Its
one kernel direction must remain coupled to the branch coordinates.

Summed over all paths, the invertible range part therefore contributes

```text
(q,0,q),                                                (10)
```

the reduced branch form is `P`, and the retained path-kernel coupling is
`V`.

## 3. Saddle-point elimination

After eliminating the invertible path ranges, the remaining matrix is
congruent to

```text
[ P   V^T ]
[ V    0  ].                                            (11)
```

For completeness, if `P` is symmetric, `rank(V)=rho`, and `Z` spans
`ker(V)`, the standard saddle-point congruence gives

```text
In([P,V^T;V,0])=(rho,t-rho,rho)+In(Z^T P Z).             (12)
```

Indeed, choose branch coordinates adapted to `ker(V)` and a maximal
independent set of rows of `V`.  The latter coordinates and their coupled
branch coordinates form `rho` hyperbolic planes.  The inverse of that
hyperbolic block has zero in the corner seen by `ker(V)`, so eliminating its
cross terms leaves `Z^T P Z` unchanged.  The `t-rho` dependent kernel rows
remain zero directions.  Combining (10)--(12) proves (4) and (5).

Finally, for the unsigned vertex-edge incidence matrix `N`,

```text
NN^T=Q(H),              N^T N=A(L(H))+2I.
```

Their nonzero spectra agree, and the edge side has `c-1` additional zero
singular values.  Shifting by two proves (6).

## 4. Balanced components and a sharp-conjecture class

The matrix `V` has a direct signed-graph interpretation.  On the branch
vertices keep only the even branch paths.  A `0 mod 4` path imposes
`x_u=x_v`, while a `2 mod 4` path imposes `x_u=-x_v`.  A `0 mod 4` loop is
vacuous and a `2 mod 4` loop forces `x_u=0`.

Call a connected component of this signed even-path graph **balanced** when
its equations admit a nonzero solution; isolated vertices count as balanced.
Equivalently, the product of the equality/negation signs around every cycle
is consistent and there is no negating loop.  Let `beta` be the number of
balanced components.  Propagating one value through each component gives

```text
beta=dim ker(V)=b-rho.                                  (13)
```

Equations (5) and (13) immediately imply the structural bound

```text
sig(Q(H)-2I) <= beta,
s(L(H)) <= beta-c+1.                                   (14)
```

The open sharp cyclomatic inequality is

```text
2 s(L(H)) <= c+1.                                      (15)
```

By (1) and (14), it holds for every subcubic 2-core satisfying either of the
equivalent conditions

```text
beta <= floor((3c-1)/2),
rho  >= floor(c/2)-1.                                  (16)
```

This is an infinite, checkable class: it requires only
`floor(c/2)-1` independent even-path constraints, and an inconsistent signed
cycle only helps.  It also pinpoints the unresolved subcubic frontier:
parity-sparse kernels for which the signed even-path incidence rank is below
that threshold.

## 5. Four-subdivision invariance

Increasing one branch-path length by four does not change `P`, `V`, `rho`,
or `R`; it increases `q` by two.  Therefore (4) gives

```text
In(Q(H')-2I)=In(Q(H)-2I)+(2,0,2),                       (17)
s(L(H'))=s(L(H)).                                      (18)
```

This holds for every branch path, including loop paths.  It is a global
modulo-four invariance for arbitrary subcubic 2-cores, not only roses or
generalized theta graphs.

## 6. Scope and proof boundary

The theorem applies to the 2-core itself.  Arbitrary pendant trees introduce
diagonal responses at internal path vertices and are not included in (2)--
(4).  The result proves (15) under the rank condition (16), but it does not
settle parity-sparse subcubic kernels, high-degree cores, or the full sharp
cyclomatic conjecture.

The range--kernel and saddle-point lemmas, and their specialization to roses
and generalized theta graphs, are prior ingredients in Paone--Paone (2026).
The increment here is the explicit signed parity-kernel form for arbitrary
subcubic 2-cores, the balanced-component bound and rank class (14)--(16), and
the general four-subdivision law (17)--(18).  The novelty assessment is
search-relative; see `SOURCES.md`.
