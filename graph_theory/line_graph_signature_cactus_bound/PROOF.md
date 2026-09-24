# The sharp cyclomatic line-graph signature bound for every cactus

Complete author proof; independent review pending. The unrestricted
conjecture remains open.

All graphs are finite and simple. A **cactus** is a graph in which each
edge lies on at most one simple cycle. For a real symmetric matrix use
`In X=(n_+(X),n_0(X),n_-(X))` and `sig X=n_+(X)-n_-(X)`.
Write `c(G)=|E(G)|-|V(G)|+1` for a connected graph and
`M(G)=Q(G)-2I`, where `Q=D+A` is the signless Laplacian.

## 1. Result

**Theorem.** Every connected cactus `G`, including arbitrary pendant trees,
satisfies

```text
2 sig(A(L(G))) <= c(G)+1.                              (1)
```

For every integer `c>=0`, the maximum over connected cacti of cyclomatic
number `c` is exactly `floor((c+1)/2)`.

There is no bound on order, cycle lengths, number of cycles, degrees,
branching, or numbers of articulation and pendant vertices. The upper bound
is the new claim. Sharp constructions are the previously published rooted
amplifier constructions, recalled in Section 8. This does not settle (1)
for connected graphs that are not cacti.

For a graph with at least one edge, the unsigned incidence matrix gives

```text
sig(A(L(G))) = sig M(G) - c(G) + 1.                    (2)
```

Indeed `NN^T=Q(G)` and `N^TN=A(L(G))+2I` have the same nonzero
eigenvalues; shifting by two gives `c(G)-1` additional negative
eigenvalues on the edge side. This identity also holds for trees. Thus
it suffices to prove `2 sig M(G)<=3c(G)-1`. The singleton satisfies (1)
directly.

## 2. Two elementary signature bounds

We use Sylvester's law of inertia, Schur-complement congruence, and two
consequences of eigenvalue interlacing:

* restoring one deleted coordinate increases signature by at most one;
* increasing diagonal entries cannot decrease signature.

**Weighted-path lemma.** Let `P` be a path with off-diagonal edge entries
one and nonnegative integer diagonal entries `w_i`. Put `W=sum w_i`.
Then

```text
2 sig(A(P)+diag(w)) <= W+1.                            (3)
```

The empty path has signature zero and can simply be omitted. Here is an
induction on the nonempty path order, also recording all boundary cases.
If some `w_i>=3`, delete that coordinate. The remainder has at most two
nonempty paths. Induction and interlacing give
`2 sig <= 2+(W-w_i)+2 <= W+1`.
Otherwise all weights are `0,1,2`. The one-vertex cases are immediate.
At an endpoint:

* Weight zero: the first two coordinates have block
  `[[0,1],[1,w_2]]`. Its signature is zero and its inverse has bottom-right
  entry zero, so elimination leaves the remaining path unchanged. Its
  weight sum is no larger than `W`.
* Weight two: delete the endpoint and apply interlacing and induction.
  The right side loses two, exactly paying the possible signature increase.
* Weight one followed by weight two: eliminate the positive first pivot.
  The next weight becomes one, the total weight decreases by two, and
  signature increases by one.
* Weight one followed by zero: the first two-coordinate block has signature
  zero and inverse bottom-right entry `-1`. For order at least three its
  elimination increases the next diagonal by one; the remaining weight
  sum is exactly `W`. A new weight three is permitted by the induction.
  For order two the signature is zero.
* Two initial weights one: for order two the signature is one. Otherwise
  the first three coordinates have block
  `[[1,1,0],[1,1,1],[0,1,w_3]]`. Eliminating its first pivot leaves a
  hyperbolic plane, so its signature is one. Its determinant is `-1` and
  its inverse bottom-right entry is zero. The remaining path is unchanged
  and loses weight `2+w_3>=2`.

Every operation reduces the order and proves (3).

**Weighted-cycle lemma.** For a simple cycle and the same weights,

```text
2 sig(A(C)+diag(w)) <= W+2.                            (4)
```

If some weight is positive, delete that coordinate and apply (3):
`2 sig <= 2+W-w_i+1 <= W+2`. If all weights vanish, the cycle eigenvalues
`2 cos(2 pi j/n)` give signature `0,1,0,-1` for lengths
`0,1,2,3 mod 4`, respectively, and (4) follows.

We will also use a charged version of (3). Give each vertex a nonnegative
integer charge `k_i`. Its real diagonal `d_i` need satisfy `d_i<=k_i` only
when `k_i<=2`; at charge at least three it is arbitrary. Delete the `q`
vertices of charge at least three. They cost at most `q` signature, and
leave at most `q+1` paths. On the remaining vertices raise each diagonal
to its charge and use (3). Thus

```text
2 sig <= sum k_i + 1                                 (5)
```

on a path. The same argument on a cycle with at least one deletion leaves
at most `q` paths and gives the stronger bound `2 sig<=sum k_i`.
With no deletion, (4) gives `2 sig<=sum k_i+2` on a cycle.
All these arguments allow zero eigenvalues.

## 3. Rooted states, including singular matrices

For a connected rooted graph `(T,r)` put

```text
C_T=Q(T)-2I+e_r e_r^T,
sigma(T)=sig C_T,          kappa(T)=3c(T)-2 sigma(T).  (6)
```

The added root diagonal represents one incident edge to a parent outside
`T`. Call the state **regular** if `e_r` belongs to `im C_T`. In that
case define `rho(T)=e_r^T x`, where `C_T x=e_r`. This scalar is independent
of the chosen solution, since `im C_T` is orthogonal to `ker C_T`.
No inverse of a singular matrix is being assumed. If `e_r` does not
belong to the range, call the state a **pole**.

The simultaneous invariant we prove is

```text
kappa >= 0;
a pole has kappa >= 1;
regular kappa=0 implies rho>= 1;
regular kappa=1 implies rho>= 0;
regular kappa=2 implies rho>=-1.                     (7)
```

We first prove it on subcubic cacti whose cycles are vertex disjoint, for
components rooted across a bridge and for whole graphs rooted off all
cycles. Sections 4 and 5 give the complete recursion. Section 7 reduces
every cactus to this situation without changing `c` or line-graph
signature.

For use below, write a symmetric rooted matrix as
`B=[[a,b^T],[b,D]]`, with root in its first coordinate. Elementary
range/kernel elimination gives:

1. If the root is a pole, `sig B=sig D`.
2. If it is regular and `rho!=0`, `sig B=sig D+sign(rho)`.
3. If it is regular and `rho=0`, `sig B=sig D`.

To see all cases, first eliminate the nonsingular range of `D`. If `b`
has a nonzero component in `ker D`, the root pairs with that component
to form a hyperbolic plane, and its response is zero. Otherwise a scalar
`a-b^T D^+ b` remains at the root. A zero scalar is a pole; a nonzero
scalar has reciprocal `rho`. The notation `D^+` here means only the
inverse on the range, and no numerical pseudoinverse is used.

In particular, for regular `rho>0`, subtracting `e_r e_r^T` from `B`
leaves its signature unchanged when `rho<1`, lowers it by one when
`rho=1`, and lowers it by two when `rho>1`. This follows from the same
congruence, now eliminating the range of `B`, or from its scalar
Schur complement `1-rho`.

## 4. A vertex joined to rooted children by bridges

Suppose the root is off all cycles and has `k` rooted children. Their
matrices are exactly `C_i`, and its diagonal is `k-1`.

If all children are regular, elimination gives

```text
a=k-1-sum rho_i,
sigma=sum sigma_i+sign(a),
kappa=sum kappa_i-2 sign(a).                         (8)
```

When `a=0` the new root is a pole; otherwise it is regular with `rho=1/a`.
If some child is a pole, its zero direction pairs with the new root.
The pair is hyperbolic, and

```text
sigma=sum sigma_i,       kappa=sum kappa_i,       rho=0. (9)
```

Additional pole directions remain zero. In particular the new state is
regular, and the pole child's charge ensures `kappa>=1`.

For completeness, (8) preserves (7) as follows. Put `K=sum kappa_i`.
If `K=0`, all responses are at least one, so `a<=-1`.
If `K=1`, the only positive charge is one, whose response is nonnegative;
again `a<=0`. Consequently `a>0` requires `K>=2`, proving nonnegativity
of the new charge. If `a>0` and the new charge is zero, then `K=2`.
Either one child has charge two or two have charge one; (7) gives
`sum rho_i>=k-2`, so `a<=1` and `rho>=1`.
Other positive pivots have positive response. A zero pivot cannot occur
at `K=0`, so poles have positive charge. A negative pivot can have new
charge two only at `K=0`; then `a<=-1`, hence `rho>=-1`.
These statements verify every clause of (7). They include the leaf
`C=[-1]`, of charge two and response `-1`, and allow any number of children.

## 5. Cycle attachment

Let the root lie on a cycle of length at least three, with its parent
edge a bridge. The root has no other off-cycle edge. Each other cycle
vertex has at most one rooted child across a bridge. An absent child
has charge zero and contributes no diagonal correction.

Eliminate regular child matrices. They contribute their signatures and
leave diagonal `d_i=1-rho_i` at their attachment vertices; the root
diagonal is one. A pole child couples a zero direction to its attachment
vertex. Eliminate this hyperbolic pair, deleting that cycle vertex, with
no added signature and no correction to other cycle coordinates. This is
valid for several poles simultaneously: the paired block is
`[[A,T],[T^T,0]]` with `T` invertible, whose inverse has zero in the corner
seen by the remaining cycle vertices. Its signature is zero.

Write `K=sum kappa_i`, summing over all children. Let `B` be the remaining
cycle matrix, after these deletions, with the root retained. Let `D`
be `B` with its root deleted and let `B_0=B-e_r e_r^T`.
All eliminated child signatures sum to `sum sigma_i`; the new root is
regular or a pole exactly when it is so in `B`, with the same response.
Since this attachment adds one cycle,

```text
kappa_out = 3+K-2 sig B.                             (10)
```

For regular child charges zero, one, two, (7) gives respectively
`d_i<=0,1,2`. Larger regular charges pay at least three for an arbitrary
diagonal. A pole child pays at least one for its deleted vertex. These
observations and Section 2 give the two bounds

```text
2 sig D   <= K+1,
2 sig B_0 <= K+2.                                    (11)
```

Here is explicit accounting, including adjacent deletions and empty
segments. Let `p` be the number of pole vertices, `q` the number of
regular vertices of charge at least three, and `W` the sum of charges
on the remaining nonroot vertices. Then `K>=W+p+3q`.
For `D`, delete the `q` expensive regular coordinates by interlacing;
the remaining graph has at most `p+q+1` nonempty paths. Raising their
diagonals to their charges and applying (3) gives
`2 sig D<=2q+W+p+q+1<=K+1`.
For `B_0`, if `p+q>0` there are at most `p+q` paths, with root weight
zero, giving `2 sig B_0<=W+p+3q<=K`. If there are no deletions, apply
(4) to the cycle with root weight zero. This proves (11).

Restoring the root gives `2 sig B<=K+3`, hence `kappa_out>=0`.
If the root is a pole, Section 3 says `sig B=sig D`; (11) then gives
`kappa_out>=2`. If it is regular with negative response, Section 3 says
`sig D=sig B+1`, so (11) gives `kappa_out>=4`. Thus regular states of
charge one or two have nonnegative response, more than (7) requires.

Finally, at charge zero, `2 sig B=K+3`. The first bound of (11) excludes
both a pole and a zero or negative response, so the response is positive.
The second bound implies `sig B_0<sig B`. By the final statement of
Section 3 this forces `rho>=1`. This completes the induction of (7).

## 6. Closing the root

Take a cactus in the recursive class, rooted off all cycles, and apply
(7) to `C=M(G)+e_r e_r^T`.
If `kappa>=1`, subtracting this positive diagonal cannot increase
signature, so `3c-2 sig M>=1`.
If `kappa=0`, the root is regular and `rho>=1`, so the subtraction lowers
signature by at least one and `3c-2 sig M>=2`.
In either case `2 sig M<=3c-1`, proving (1) by (2).

The recursion is complete: in a subcubic cactus cycles are vertex
disjoint. A root off the cycles has only bridge children. A component
rooted across a bridge either starts off a cycle or starts on exactly one
cycle with no further off-cycle edge at its root. Every recursive child
has fewer vertices. Singularities and invisible zero directions are
already covered in Sections 3--5.

## 7. Reduction of an arbitrary cactus

We use the previously established four-edge vertex split. Partition the
neighbors of a vertex into two nonempty sets, replace the vertex by two
endpoints joined by a four-edge path, and retain the respective neighbor
sets at those endpoints. It satisfies

```text
M(G') congruent to M(G) direct-sum J direct-sum J,
J=[[0,1],[1,0]],
c(G')=c(G).                                         (12)
```

For clarity, the local identity is explicit. Write the endpoint diagonal
terms as `alpha u^2+beta w^2`, the other old coordinates as `z`, and
their endpoint couplings as `2u f^Tz+2w g^Tz`. The new path contributes
`2up+2pq+2qr+2rw`. Substitute

```text
p=A-r, q=B0-u, u=x, w=x+y,
r=t-beta*x-g^Tz-(beta/2)*y.
```

The form becomes the old form plus `2AB0+2yt`; every substitution is
invertible. Thus (12), including singular inputs, is self-contained here.

At a cactus vertex of degree at least four, choose the two incident edges
of one cycle as a neighbor set if such a cycle exists; otherwise choose
any two incident bridges. The remaining neighbors form the other set.
An entire cycle stays on one side, and distinct incident blocks have no
connection after the old vertex is removed. The new four-edge path is
therefore a bridge path, and the result remains a cactus. The new endpoint
degrees are three and `d-1`, so the total excess above degree three falls
by one. Repeating produces a subcubic cactus with the same `c` and
line-graph signature. Its cycles are vertex disjoint because two cycles
meeting at a vertex would force degree at least four.

If there is a vertex off every cycle, choose it as the root for Section 6.
If not, either the graph is a single cycle, which satisfies (1) directly,
or a bridge joins its cycles. Replace one such bridge by a five-edge path.
Eliminating its four internal coordinates, the block `A(P4)`, restores
`M(G)` and adds inertia `(2,0,2)`. Thus `c` and signature are unchanged,
and an internal vertex of this bridge path provides a root off all cycles.
The operation preserves the cactus and subcubic properties. Trees already
have an off-cycle root. This completes the proof for every cactus.

## 8. Sharpness and scope

Recall Paone's rooted module: disjoint `C4=(0,1,2,3,0)` and
`C5=(4,5,6,7,8,4)`, bridge `04`, and root edge `19`, with root vertex `9`.
Its line-graph matrix `K` has

```text
In K=(6,0,5),       det K=-8,       (K^-1)_(19,19)=0.
```

Identifying root 9 with any host vertex adds this inertia unchanged by
Schur complementation. It adds two to `c` and one to line-graph signature,
and preserves the cactus property. The module and this attachment law
are prior work, also proved in the cited universal-reduction package.
Starting with `C5` and attaching `k` modules gives `c=2k+1`, signature
`k+1`. Starting with a singleton and attaching `k` modules gives `c=2k`,
signature `k`; the empty line graph has signature zero at `k=0`.
These witnesses prove the claimed maximum for every `c`.

The upper bound follows from the displayed inductions and congruences.
Finite executable audits check the weighted lemmas, rooted states,
singular cases, constructors and literal graph matrices. They are not an
enumeration proof for arbitrary cacti. No floating-point spectrum, solver,
external dataset or omitted large certificate is a proof premise. The
argument is not a proof-assistant formalization. It makes no equality
classification, nonsingularity claim for all extremizers, or assertion
about the unrestricted conjecture.
