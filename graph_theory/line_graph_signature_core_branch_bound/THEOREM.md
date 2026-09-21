# The core-branch bound

## 1. Statement and notation

All graphs below are finite and simple.  For a real symmetric matrix `X`,
write

```text
In(X)=(n_+(X),n_0(X),n_-(X)),    sig(X)=n_+(X)-n_-(X).
```

For a connected graph `G`, set

```text
c(G)=|E(G)|-|V(G)|+1,            M(G)=Q(G)-2I,
```

where `Q` is the signless Laplacian.  Let `H=core_2(G)` and

```text
B(H)={v in V(H):deg_H(v)>=3},     b(H)=|B(H)|.
```

**Theorem.** If `G` is connected and `c(G)>=2`, then

```text
sig M(G) <= b(H),                                  (2)
s(L(G)) <= b(H)-c(G)+1 <= c(G)-1.                  (3)
```

The 2-core is connected and has the same cyclomatic number as `G`.  Since
`c(G)>=2`, it is nonempty and is not a cycle.

## 2. Translating line-graph signature

Let `N` be the unsigned vertex-edge incidence matrix of `G`.  Then

```text
N N^T=Q(G),                  N^T N=A(L(G))+2I.
```

The nonzero eigenvalues of the two Gram matrices agree.  Because
`|E|-|V|=c(G)-1`, the extra zero singular values on the edge side become
`-2` eigenvalues after shifting.  This remains true when `G` is bipartite:
the one zero eigenvalue already present on the vertex side is shifted on
both sides.  Therefore

```text
s(L(G))=sig M(G)-c(G)+1.                           (4)
```

It suffices to prove (2).

## 3. A rooted-tree invariant

For a rooted tree `(T,r)`, define

```text
C_T=Q(T)-2I+e_r e_r^T,
sigma(T)=sig(C_T),               rho(T)=(C_T^-1)[r,r].
```

We first prove that the inverse always exists and record its exact recursive
state.  If the root has child subtrees `T_1,...,T_k`, put

```text
a=(k-1)-sum_i rho(T_i).                            (5)
```

Schur complementation of the child blocks gives

```text
sigma(T)=sum_i sigma(T_i)+sign(a),     rho(T)=1/a. (6)
```

For the one-vertex rooted tree the state is `(-1,-1)`.  Inductively every
`rho(T_i)` is a reduced fraction with odd numerator and odd denominator.
After putting (5) over the product of the odd denominators, its numerator is

```text
(k-1)-k = -1 mod 2.
```

Thus `a` is nonzero and its reciprocal again has odd numerator and
denominator.  This proves invertibility as well as (6) for every rooted
tree.

**Rooted-tree lemma.** Every rooted tree satisfies

```text
(i)   sigma(T)<=0;
(ii)  sigma(T)=0  implies rho(T)=1;
(iii) sigma(T)=-1 and rho(T)<0 imply rho(T)=-1.     (7)
```

**Proof.** Use simultaneous induction.  The singleton has state `(-1,-1)`.
Assume (7) for the child subtrees.

If `a<0`, (6) gives `sigma(T)<=-1`.  If `a>0` and all child signatures were
zero, (ii) for the children would give

```text
a=(k-1)-k=-1,
```

a contradiction.  Hence some child signature is at most `-1`, and (6)
again gives `sigma(T)<=0`.  This proves (i).

For (iii), `rho(T)<0` means `a<0`.  Equality `sigma(T)=-1` then forces all
child signatures to be zero.  Their responses are all one by (ii), so
`a=-1` and `rho(T)=-1`.

Finally suppose `sigma(T)=0`.  Necessarily `a>0`, and the child signatures
sum to `-1`.  Exactly one child, say `T_j`, has signature `-1`; all others
have signature zero and response one.  Hence `a=-rho(T_j)>0`.  Part (iii)
for `T_j` gives `rho(T_j)=-1`, so `a=1` and `rho(T)=1`.  This proves (ii)
and closes the induction. `square`

## 4. Exact reduction to the 2-core

Every component outside `H` is a tree joined to a unique core vertex by a
unique edge.  Regard its endpoint outside `H` as the root.  Index these
rooted trees attached at `x in V(H)` by `T_(x,j)`, and set

```text
tau_x=sum_j sigma(T_(x,j)),
D_xx=sum_j (1-rho(T_(x,j))),       tau=sum_x tau_x. (8)
```

In the vertex order consisting of the core followed by the attached trees,
the block of `M(G)` on a rooted tree is exactly `C_T`: the root has gained
one degree from its core edge.  The core diagonal has gained one for every
such edge.  Eliminating all invertible tree blocks therefore gives the exact
congruence identity

```text
sig M(G)=tau+sig(M(H)+D).                            (9)
```

Let

```text
R={x:D_xx>0},       r=|R|,       S=V(H)\R.
```

The rooted-tree lemma gives every `tau_x<=0`.  Moreover, if `x in R`, not
all attached trees can have signature zero: if they did, all their responses
would equal one and `D_xx` would be zero.  Consequently

```text
tau<=-r.                                             (10)
```

On `S`, the diagonal matrix `D[S]` is negative semidefinite.

## 5. The branch-vertex principal-submatrix lemma

**Lemma.** For every `U subseteq V(H)`,

```text
sig(M(H)[U]) <= |U intersect B(H)|.                 (11)
```

**Proof.** Put `W=U\B(H)`.  Every vertex of `W` has degree two in `H`, so
the corresponding diagonal of `M(H)` is zero and

```text
M(H)[W]=A(H[W]).
```

Every component of `H[W]` is a path or an isolated vertex.  Indeed its
maximum degree is two.  A cycle component would use both `H`-neighbors of
each of its vertices and hence would be disconnected from `B(H)`.  Since
`H` is connected, it would follow that `H` itself is a cycle, contrary to
`c(H)>=2`.

Thus `H[W]` is bipartite, and the spectrum of its adjacency matrix is
symmetric about zero.  Hence `sig(M(H)[W])=0`.  The principal submatrix on
`W` is obtained from the one on `U` by deleting `|U intersect B(H)|`
coordinates.  Cauchy interlacing gives (11). `square`

## 6. Proof of the theorem

Since `D[S]` is negative semidefinite, eigenvalue monotonicity and (11) give

```text
sig(M(H)[S]+D[S]) <= sig(M(H)[S])
                   <= |S intersect B(H)|.           (12)
```

The matrix in (12) is the principal submatrix of `M(H)+D` obtained by
deleting the `r` coordinates in `R`.  Interlacing once more gives

```text
sig(M(H)+D) <= |S intersect B(H)|+r.                (13)
```

Combining (9), (10), and (13),

```text
sig M(G) <= -r+|S intersect B(H)|+r
          = |S intersect B(H)|
          <= b(H).
```

This is (2), and (4) yields the first inequality in (3).  Finally,

```text
sum_(v in H)(deg_H(v)-2)=2|E(H)|-2|V(H)|=2c(G)-2.
```

Each branch vertex contributes at least one to this sum, so
`b(H)<=2c(G)-2`.  Substitution in (3) proves `s(L(G))<=c(G)-1`.
`square`

## 7. Exact low-cyclomatic consequences

For `c=2`, (3) gives `s(L(G))<=1`; the eleven-vertex graph encoded by
`Jl?GGCHa??_` has `b(H)=2` and signature one, so `f(2)=1`.

For `c=3`, (3) gives `s(L(G))<=2`; the fourteen-vertex cactus encoded by
`Ml_GGCHO??_@?@?C_` has `b(H)=4` and signature two, so `f(3)=2`.
Thus `2s(L(G))<=c(G)+1` holds for both cyclomatic numbers, sharply for
`c=3`.

## 8. Proof/computation boundary

Sections 2--7 are a universal proof.  `verify.py` separately audits the
rooted recurrence, the principal-submatrix lemma, the incidence translation,
the final inequality, and the two witnesses in exact arithmetic.  No finite
check or empirical inference is used in the proof.
