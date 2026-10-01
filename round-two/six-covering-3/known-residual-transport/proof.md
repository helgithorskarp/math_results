# Known-residual transport refinement of the primitive covering budget

Author: **six-covering-3, researcher**, 2026-10-01. This is a necessary-bound
refinement, not a new covering, a global exclusion, or a claim of historical
priority for transportation duality. It addresses the exactly-eight problem
through literal prescribed classes containing modulus8. A general lemma below
also applies to covers whose actual LCM merely divides the ambient period.

## 1. The local bound

Write the six primitive points as `j mod6`, with grid coordinates
`(j mod2,j mod3)`. Let V be the additive space of functions
`f(e,c)=x(e)+y(c)`. Define the balanced transportation polytope

\[
 \Omega=\{\omega_{0c}=1+h_c,\ \omega_{1c}=1-h_c:
                    -1\le h_c\le1,\ \sum_c h_c=0\}.
\]

All arrays are nonnegative, each row has sum3, each column has sum2, and the
total is6. Hence `sum omega*f = sum f` for every `f in V`. Its six vertices
are the permutations of `h=(-1,0,1)`: a vertex of the plane section of the
cube must have two coordinate bounds active, and feasibility forces those
bounds to be opposite. Thus no floating-point LP is involved.

For a point set A put

\[
 M(A)=\max_{\omega\in\Omega}\sum_{j\in A}\omega_j.
\]

The prior sharp primitive charge is
`kappa(H)=min_(omega in Omega) mass_omega(H)`.
If a,c count columns marked only in binary row0,row1 respectively, and d
counts doubly marked columns, its formula is

\[
 \kappa(H)=2d+\max(0,2\max(a,c)-3).
\]

This is the charge and additive signed-function bound proved in
[the four-top publication](../four-top-block-dp/proof.md), source
`2d195230df390e3f7483a00e7c4782a7ddf5fddf` (graph8604).
Alternatively evaluate the six vertices directly: a doubly marked column
contributes2 and the singly marked column coefficients of h are +1 or -1;
their minimum over the six permutations gives the formula. The symmetry
`omega -> 2-omega` and the total mass6 imply

\[
 M(A)=2|A|-\kappa(A)=6-\kappa(A^c).                 \tag{1}
\]

**Sharp local lemma.** For nonnegative `F in V` with `F>=1_A`,
`sum F>=M(A)`, and equality is attained by an additive function.
Indeed `sum F=sum omega*F>=mass_omega(A)` for every balanced omega. For
attainment take the sharp prior signed function for `H=A^c` and add1.
It has total `6-kappa(A^c)`, is nonnegative everywhere, and is at least1
on A. For completeness, that signed function can be constructed as follows.
Let D be doubly marked columns of H and S_r the columns marked only in row r.
Start with `f=-1_D(column)`. If the larger of `|S_0|,|S_1|` is at least2,
choose a row r attaining it and add
`-1_{row=r}+1_{column not in S_r}`. The resulting function is in V, is
at least-1 on H, at least0 off H, and its total is `-kappa(H)`.

Sharpness here concerns arbitrary nonnegative additive functions. It does
not assert that the equality function is attainable by a set of distinct
modulus resources. The local residual bound could therefore be sharpened
further by additional resource constraints.

There is also an elementary row/column-cover formula. If a,c,d now count
the singly/doubly marked columns of **A**, then

\[
 M(A)=\min\{2(a+c+d),\ 3+2(c+d),\ 3+2(a+d),\ 6\}.       \tag{1a}
\]

These are the costs of covering A by its marked columns, row0 plus columns
marked in row1, row1 plus columns marked in row0, or both rows. For the
matching lower bound, represent a nonnegative additive function as
`r_e+y_c` and shift `min(r_0,r_1)` to zero. All y_c are then nonnegative.
If `r_0=0,r_1=t>=0`, the least allowed objective is
`3t+2[(a+d)+c*max(0,1-t)]`. Its minimum occurs at t=0 or t=1.
Reverse the rows for the other two-row ordering. The two cases give (1a);
the cost6 is also available (and redundant when all marked columns suffice).
This row/column derivation was shared by **six-covering-2, researcher**, in
the live covering-eight discussion (message596,2026-10-01), and is included
with an independent exact64-shape check. It is mathematical input, not a
reviewer judgment or a separate priority assertion.

For a fixed residual set U define

\[
 \delta_U(H)=M(U)-M(U\setminus H).                 \tag{2}
\]

It is nonnegative, vanishes for empty H, and is monotone in H, because M
is monotone under point inclusion. A singleton can have positive delta
despite `kappa(singleton)=0`. For example a known binary row and a known
ternary column have indicator-count mass5; their union leaves two points
in the opposite row. That U has `|U|=2`, `M(U)=3`, and removing one of
those points has delta1.

## 2. The known-residual global inequality

Let `B=2^alpha*3^beta`, `alpha,beta>=1`, `gcd(B,C)=1`, `N=BC`,
`T=B/6`, and `b|T`. Use actual CRT coordinates `(t mod B,z mod C)`,
with each primitive block labelled by the **actual** pair `(q,z)`,
`0<=q<T`, `0<=z<C`, and points `t=q+Tj`.

Let P be prescribed congruences with distinct moduli dividing N. Let R
contain every free outside modulus allowed in the problem; these have
`gcd(n,B)<B`. The complete top resource set is
`S={Bd:d|C}`. Tops in P are fixed to their actual prescribed phases.
Every remaining top is allowed an arbitrary phase for the necessary-bound
maximum. If a completion omits some available outside or top resource,
adjoin it with any phase: covering is preserved. This is an upper-bound
relaxation, not a claim that an omitted class occurs in a minimal cover.

Let u be nonnegative on the N physical residues and vanish on every class
in P. Let v be a nonnegative weight of physical period `bC`. On a primitive
block it is constant; denote its value by `v(q mod b,z)`. We permit positive
v on known classes.

Define **U(q,z) to be the points not covered by any prescribed OUTSIDE
class**. Prescribed TOPS are excluded from this definition. For a complete
top assignment let H(q,z) be the actual distinct set of primitive points
marked by its active tops, including the fixed tops. Let `Phi_(Bd)(u)`
be the u-footprint of the assigned top phase. Define

\[
 K_U(u,v)=\max_{\text{legal complete top phases}}
 \left[\sum_{d\mid C}\Phi_{Bd}(u)+
        \sum_{q,z}\delta_{U(q,z)}(H(q,z))v(q\bmod b,z)\right].       \tag{3}
\]

The phases in this maximum keep actual q labels and resource identities.
For a modulus n write `C_n(w)=max_a sum_(x mod n=a) w(x)`.
Every completion of P to a distinct cover whose moduli divide N satisfies

\[
 \sum_x u(x)+\sum_{q,z}M(U(q,z))v(q\bmod b,z)
       \le \sum_{n\in R} C_n(u+v)+K_U(u,v).          \tag{4}
\]

**Proof.** Restrict the free outside indicator-count function to a primitive
block. The B-component of any outside modulus omits a full binary or
ternary exponent, so its induced j-period is1,2, or3. Consequently its
indicator, and their nonnegative sum F, lie in V. Covering forces
`F>=1_(U\H)`: known outside classes cover none of U, and top classes
cover none of U\H. The local lemma gives
`sum_j F(j)>=M(U\H)`. Multiply by the block weight v and sum. Independently,
since u vanishes on all known classes, ordinary covering gives
`sum u <= sum_freeoutside footprint(u)+sum_top footprint(u)`.
Add these inequalities and rearrange using (2). Replace each outside
footprint of u+v by its phase maximum and the top expression by (3).
Prescribed top u-footprints are zero. Monotonicity of delta justifies
adjoining any missing top; adjoining an outside adds nonnegative
footprints. This proves (4). No actual-LCM-equals-N assumption is used.

## 3. Fractional outside groups still work

The exact group capacities and resource-incidence rules in
[mixed-outside-groups](../mixed-outside-groups/proof.md), source
`2918961832e06c9ee371779ed19650fadfdea272` (graph8674), can be reused
without alteration. In detail let nonempty groups `G subset R` have
nonnegative coefficients lambda_G with
`sum_(G contains n) lambda_G=1` for each n. On each phase assignment let
`I_G` be the group union indicator. For the v-part choose either
`g_G=sum_(n in G) I_n`, or `g_G=I_G` when that union has a proper primitive
period. A sufficient condition for the latter, valid for all its phases,
is `lcm_(n in G) gcd(B,n)<B`.

Put `M_G=max_actual group phases [sum u*I_G + sum v*g_G]`.
Then the right side of (4) can be replaced by
`sum lambda_G*M_G + K_U`. To see this, the function
`F=sum lambda_G*g_G` is nonnegative additive on every primitive block.
If a free resource n covers a point, every group containing n has
`g_G>=I_n`; the incidence condition implies `F>=1` there. Thus it covers
U\H for the local argument. The same incidence argument with I_G supplies
ordinary u-counting. The exact pair phase maxima are unchanged from graph8674.
An unrestricted union for the v-part is still invalid when it has full
primitive period; the published 12-period counterexample remains applicable.

## 4. Comparison with the old known-cost budget

On each block let k be the **actual integer indicator count** of prescribed
outside classes, let `S=sum_j k(j)`, and `U={j:k(j)=0}`. The old effective
periodic demand is `(6-S)v`. The new one is `M(U)v`. Put

\[
 c_0=6-S-M(U),\qquad c_H=6-S-M(U\setminus H)=c_0+\delta_U(H).
\]

For every H,

\[
 c_H\le\kappa(H),\qquad c_0\le0.                 \tag{5}
\]

Take the sharp nonnegative additive g covering U\H, with total M(U\H).
The signed function `g+k-1` lies in V. Off H it is nonnegative: if k=0,
g is at least1; if k is positive, its integer indicator-count nature
gives k>=1. On H it is at least-1. The old sign lemma therefore gives
`sum(g+k-1)>=-kappa(H)`, proving the first inequality. Set H empty for
the second. This proof uses actual class counts; an arbitrary positive
real function with values below1 would not suffice.

Let `K_kappa` be the old complete-top maximum, with exactly the same
u/v vectors and prescribed tops, and let `c=sum c_0*v`. Maximizing the
pointwise comparison gives

\[
 c+K_U\le K_\kappa.
\]

If D_old and D_new are the two effective demands, then
`D_old-D_new=c`. The outside singleton or fractional-group capacities
are identical. Consequently
`D_new-outside-K_U >= D_old-outside-K_kappa`.
The refinement holds for all such vectors, including cases with negative
old effective demand. Comparing delta alone to kappa would be incorrect;
the generally negative baseline c must be retained.

## 5. Exact computation and the extended quotient

The subset DP of graph8604 applies with local charge `delta_U(H)` in place
of kappa. At each actual q, maximize over the six j choices of precisely
the resource subset assigned there; fixed tops retain both their q and j.
Then partition the top resources across all actual q labels by subset DP.
Table[empty] is zero because delta_U(empty)=0. This gives the exact finite
maximum (3), not a covering-existence test.

For C=35 the resources are labelled d=1,5,7,35, with cofactor phases
`(0,r5,r7,s)`. Let A be the point of resource1 if present, R add resource5,
L add resource7, E be the coarse/row/column set active at s, and F add
resource35 there. Precompute, for every point mask H, the weighted
delta base sum over all z, its five row sums, seven column sums, and35
point values. The local profile is exactly

```
base(A) + row(R,r5)-row(A,r5) + col(L,r7)-col(A,r7)
+ point(R union L,cross)-point(R,cross)-point(L,cross)+point(A,cross)
+ point(F,s)-point(E,s).
```

Here cross is the CRT residue of r5,r7. This is pointwise
inclusion-exclusion and retains repeated primitive j as set unions.
The `base(A)` term is essential: a singleton now can have positive charge.
It gives O(1) local evaluation after the profile is built for each actual q.

The coordinate-fiber quotient of
[cofactor-orbits](../cofactor-orbits/proof.md), source
`cc7f49b401ad050e5347cf4aea1d72ea58122f34` (graph8713), extends provided
the tested signatures include **every U(q,z) mask**, alongside every u
and v fiber. Fixed top cofactor values remain singleton classes. Products
of permutations within equal fiber classes preserve all three arrays,
fixed phases, and the actual q/j labels. They therefore preserve (3).
Represent the ordered pairs `(r5,s mod5)` and `(r7,s mod7)` by distinct
class pairs, equal elements in a class, or unequal elements in that class,
then combine the representatives by CRT. The published orbit proof
establishes completeness, unchanged after adding the mask invariant.
Using the old u/v-only signatures for this new charge is not justified.

`coefficient_row` unfolds a witnessed maximum to linear coefficients on
the original u/v coordinates. A cutting-plane implementation can insert
that row without averaging the master weight variables. Recompute the
signature classes for each oracle input, including when any weights change.

## 6. Target controls and current scope

The literal adapter reconstructs every known class, the full residual,
every unused divisor >=8, and prescribed tops. At ambient10080, with
u equal to the uncovered indicator and v its projection to period1680,
the current normalized prefix01d4 gives old/new K=174 and identical
gap -9297. Thus this vector supplies no exclusion there.

A former peer search prefix
`[(8,0),(9,0),(10,0),(14,0),(12,10),(16,1),(15,2),(32,9),(18,6)]`
has4591 residual points. For the same projected vector, outside capacities
total35462 and old/new K=192. The old demand28388 becomes28528, improving
the gap -7266 to -7126, exactly140. The U-aware quotient has50 tuples
instead of1225. This is a reproducible strict budget improvement on a
literal minimum-eight prefix, not an exclusion or a new viable branch.
That branch's older root was subsequently excluded by a peer ordinary tree.

Peer source for the currently committed modulus12/phase disjunction is
`b1d33a7c2b7ab8091d58508033107e0f88e61c80`,
[twelve-class-exclusion](../../six-covering-2/twelve-class-exclusion/proof.md),
graph8728. It leaves16 canonical10080 forms. We inspected its source and
actual graph commitment but did not independently replay its trees.
The global remaining candidates stay **10080,15120,20160**, with a
published20160 witness. This artifact changes none of those global bounds.
The pure235 restricted question remains separate.

Primary literature checked2026-10-01: Zhang--Zhang,
[arXiv2607.19029](https://arxiv.org/html/2607.19029), on the claimed
minimum-seven LCM10080; and Harrington--Klein--Lowrance--Trifonov,
[arXiv2605.18644](https://arxiv.org/html/2605.18644), for the restricted
235 minimum-eight construction/exponent frontier. These are prior art,
not numerical conclusions of the present computation. See README for
source dependencies, reproduction, validation, and operational caps.
