# The sharp half-gap bound for two Lipschitz graphs

Let $f,g:[A,B]\to\mathbb R$ be 1-Lipschitz, with $f(A)=g(A)$, $f(B)=g(B)$, and $f(x)<g(x)$ for $A<x<B$. Set

$$
\Gamma=\operatorname{graph}(f)\cup\operatorname{graph}(g),\qquad
M=\max_{[A,B]}(g-f)>0.
$$

**Theorem.** The curve $\Gamma$ inscribes a square of Euclidean side
at least $M/2$. The constant $1/2$ is optimal.

Here inscription concerns the four vertices. Neither convexity of the
bounded region nor containment of the square's edges is assumed.
The universal lower bound is a written proof using the Greene--Lobb
theorems specified below. Sharpness is also certified by a complete,
exact finite computation in Section 7. No Floer computation is performed
by the accompanying program.

## 1. Precisely imported results

Write $T(C)$ for the area enclosed by a positively oriented Jordan curve
$C$. We use the square case $\theta=\pi/2$ of Greene--Lobb's Jordan
Floer spectral invariants $\ell_1(C),\ell_2(C)$:

1. Spectrality: a spectral value is the action of an inscribed square.
2. For a nested PL isotopy all of whose square inscriptions are elegant,
   $0\le\ell_i(C_1)-\ell_i(C_0)\le T(C_1)-T(C_0)$.
3. A curve made from two graphs of Lipschitz constant less than
   $1+\sqrt2$ has only elegant square inscriptions.

These are [Greene--Lobb, *Square pegs between two graphs*][GL2],
Theorem 1.1, Proposition 1.3, the PL extension in Section 3.4, and
Lemma 4.1. The proof of Proposition 1.3 explicitly uses PL spectrality,
including positive-dimensional inscription components. At a positive
distance from action 0 and action $T(C)$, the PL extension supplies a
nondegenerate square; equivalently use their Proposition 4.2 and the
no-shrinkout argument cited immediately afterward.

For action normalization we use [Greene--Lobb, *Floer homology and square
pegs*][GL1], Sections 2.2 and 3. In coordinates $(z,w)\in\mathbb C^2$,
the Hamiltonian is $H=|z-w|^2/4$. Its time-$\theta$ flow rotates
the two endpoints about their midpoint through angle $\theta$.
The action is Hamiltonian integral minus symplectic area of a capping
which avoids the diagonal $z=w$. We derive the needed action explicitly
below; no convention about signed caps is left implicit.

All the Floer theory, its PL extension, spectrality and monotonicity are
prior work and external mathematical dependencies. They are not proved
or formally verified by this package.

## 2. The two actions of a square

First suppose that the branches have a common Lipschitz bound $k<1$.
A branch cannot contain three vertices of a square: the three vertices
contain two perpendicular sides, whose slopes cannot both have absolute
value less than one. A common endpoint cannot be a square vertex either,
since counting membership in the two branches would then force three
members on one branch. The two same-branch pairs are sides: otherwise
they would be the two
perpendicular diagonals, whose slopes also cannot both have absolute
value less than one.

Thus every square has the cyclic labeling

$$
\begin{split}
P&=(t,y),&Q&=(t+a,y+b),\\
R&=(t+a-b,y+a+b),&S&=(t-b,y+a),
\end{split} \tag{1}
$$

where $a>0$, $|b|<a$, $P,Q$ lie on $f$, and $S,R$ on
$g$. The side squared is $a^2+b^2$. The opposite orientation would
put an upper vertex at $(t+b,y-a)$; Lipschitzness would give
$g(t)\le y-a+|b|<f(t)$, so that orientation is impossible.

Define

$$
J(Q)=\int_{t-b}^{t+a-b}g(x)\,dx-
       \int_t^{t+a}f(x)\,dx-\frac{a^2-b^2}{2}. \tag{2}
$$

**Action lemma.** The actions of the generators representing this square
are $J(Q)$ and $T(\Gamma)-J(Q)$, each repeated by exchanging the
ordered endpoints of its starting diagonal.

**Proof.** Use $\lambda=(x\,dy-y\,dx)/2$, so $d\lambda=dx\wedge dy$.
Let $\alpha$ be the ordered-pair path with its first coordinate moving
along the lower arc $P\to Q$, its second along the upper arc $R\to S$,
each linearly in its horizontal coordinate. If $u\in[0,1]$, the real
part of second-minus-first is $a-b-2au$. It vanishes once, and at
that time the imaginary part is $g(x)-f(x)>0$. Its initial vector is
$(a-b,a+b)$, in the first quadrant; its final vector is
$(-a-b,a-b)$, in the second quadrant. Its argument therefore changes
by exactly $\pi/2$, without an extra turn.

The Hamiltonian path $\tau:(P,R)\to(Q,S)$ has that same argument
change. Consequently $\tau$ followed by the reverse of $\alpha$
has winding zero in $\mathbb C^2\setminus\{z=w\}$. This complement
is homotopy equivalent to $\mathbb C^*$, by the difference coordinate,
so the loop bounds a diagonal-avoiding capping. This is a preferred
capping in the imported action definition.

Put $r^2=(a^2+b^2)/2$, the squared radius of the square. Both the
Hamiltonian integral and the integral of $\lambda\oplus\lambda$
along $\tau$ are $(\pi/2)r^2$: midpoint terms cancel between the
opposite moving endpoints. Stokes' theorem thus cancels those terms and
leaves

$$
\mathcal A(P,R)=\int_{P\to Q}\lambda+\int_{R\to S}\lambda.
$$

Using $\lambda=d(xy)/2-y\,dx$, the endpoint term in this sum is
$-(a^2-b^2)/2$. The remaining two integrals give (2).

For the other starting diagonal use the arcs $Q\to R$ through the
right common endpoint and $S\to P$ through the left one. The right
arc has horizontal coordinates at least $\min(x_Q,x_R)$, and the
left arc at most $\max(x_P,x_S)$. The former exceeds the latter by
$a-|b|>0$. Hence their difference stays in the left half-plane,
with argument changing from the second to the third quadrant by exactly
$\pi/2$. This again gives a preferred capping. The two arc pairs
together traverse $\Gamma$ positively once, so their actions sum to
$\int_\Gamma\lambda=T(\Gamma)$. These are all four ordered starting
diagonals. The same calculation applies to PL arcs. $\square$

## 3. Rifford's local integral estimate in action coordinates

The integral inequality below is prior work: it is exactly [Rifford,
Lemma 4.1, equations (4.3)--(4.4), with $\delta=0$][R], after
subtracting $(a^2-b^2)/2$ to use the action normalization (2).
We include the elementary derivation to make that identification
checkable; the chord envelope is also his equation (4.5).

If $u:[0,a]\to\mathbb R$ is 1-Lipschitz with $u(0)=c$ and
$u(a)=c+b$, its endpoint envelopes are

$$
c+\max(-x,b-a+x)\le u(x)\le
c+\min(x,b+a-x).
$$

Integrating the two affine pieces of each envelope gives

$$
\left|\int_0^a u(x)\,dx-a(c+b/2)\right|
       \le\frac{a^2-b^2}{4}. \tag{3}
$$

Apply (3) to the lower arc from $P$ to $Q$, and to the upper arc
from $S$ to $R$. Their trapezoid integrals differ by $a^2$.
Therefore (2) gives the particularly simple bounds

$$
\boxed{\quad b^2\le J(Q)\le a^2\le a^2+b^2.\quad} \tag{4}
$$

This is a local estimate for an arbitrary inscribed square. It does not
require that a point of maximum branch gap lie in its projection. It is
compatible with the previously proved failure of that localization rule.

## 4. The action of an interior diamond

Let $D_r=\{(x,y):|x-x_0|+|y-y_0|\le r\}$, with boundary $C_r$.
Its area is $2r^2$. Every square inscribed in a square boundary is
centered at the boundary's center. For completeness, unless it is the
boundary square itself, its four vertices must occur on the four sides
in cyclic order. In coordinates for $[-h,h]^2$, solving the square
equations gives

$$
(u,h),\quad(h,-u),\quad(-u,-h),\quad(-h,u),
\qquad -h\le u\le h.
$$

If two adjacent vertices occupy one boundary side, the square is parallel
to that side and the other two can lie on the boundary only for the
boundary square itself. Opposite vertices cannot occupy one side. This
also covers the corner cases of the displayed parametrization.

On each boundary side $\lambda$ is a constant multiple of its affine
parameter. Integrating either alternating pair of arcs in the displayed
family gives $2h^2$, half the boundary square's area, independently of
$u$. The action normalization in Section 2 (or its preferred-capping
calculation after rotating coordinates) then gives only that action value.
For $C_r$, therefore,

$$
\ell_1(C_r)=\ell_2(C_r)=r^2. \tag{5}
$$

This also follows by constancy of action on the connected square family
and direct evaluation at the boundary square. Degenerate inscriptions
are excluded from the action spectrum used here.

At a point $x_0$ attaining the gap $M$, set
$y_0=(f(x_0)+g(x_0))/2$. The Lipschitz inequalities show that

$$
f(x)\le y_0-M/2+|x-x_0|,\qquad
g(x)\ge y_0+M/2-|x-x_0|.
$$

Thus $D_r$ is wholly inside the bounded region of $\Gamma$ whenever
$0<r<M/2$. Its horizontal interval is inside $(A,B)$: endpoint
agreement and 1-Lipschitzness give
$M\le2\min(x_0-A,B-x_0)$.

## 5. Comparison from a prescribed interior diamond

We use the construction in [GL2, Lemma 4.3 and its proof][GL2], with
its initial square specified. The following points record precisely
what is required from that construction.

**Prescribed-diamond comparison.** Suppose the branches are PL with a
common Lipschitz bound $k<1$, and the closed diamond $D_r$ lies
strictly inside their domain. Fix $k<k'<1$. There are PL curves
$C_n$ tending to $\Gamma$, each made from two strictly separated
$k'$-Lipschitz branches with common endpoint values, such that

$$
r^2\le\ell_i(C_n)\le T(C_n)-r^2,\qquad i=1,2. \tag{6}
$$

**Alignment with the published construction.** GL2 starts its proof
with a diamond about the midpoint of the interval, chosen small enough
to be strictly interior. Smallness is used for this containment; neither
its subsequent size nor the midpoint is otherwise required. Here the
left and right vertices have abscissae $x_L=x_0-r$ and
$x_R=x_0+r$, both in $(A,B)$, and ordinate $y_0$. Strict
containment supplies weights $0<\alpha_L,\alpha_R<1$ such that

$$
y_0=\alpha_L f(x_L)+(1-\alpha_L)g(x_L),\qquad
y_0=\alpha_R f(x_R)+(1-\alpha_R)g(x_R).
$$

The left and right auxiliary paths in that proof are now PL
interpolants of $\alpha_L f+(1-\alpha_L)g$ on $[A,x_L]$
and $\alpha_R f+(1-\alpha_R)g$ on $[x_R,B]$.
Both have slopes bounded by $k$. Use increasingly fine partitions
on those intervals and on the four diamond edges. The two paths can
have different lengths and different numbers of segments.

GL2's first stage moves vertices successively along these two paths,
using close parallel guide lines. Its second stage moves branch vertices
vertically to the sampled values of $f,g$. Choose a fixed
$L$ with $1<L<1+\sqrt2$. The initial diamond has slopes of
absolute value 1, and the auxiliary paths have slopes bounded by
$k<1$. Thus the guide lines and the small adjustments giving strict
nesting can be chosen to keep every intermediate slope below $L$.
Redundant collinear vertices are inserted as in that proof, so these
are PL isotopies with a fixed number of distinct marked vertices for
each $n$. In particular we use the strictly nested version asserted
by Lemma 4.3, not the touching-curve version drawn for simplicity there.

The final branches before those adjustments interpolate samples of
$f,g$, so their slopes are at most $k$. For each finite mesh,
strictly increasing knot coordinates and the bound $k'<1$ are open
conditions on the finitely many final vertex positions. Choose the
strict-nesting adjustments small enough to retain that bound and tend
to zero with the mesh size. Consequently the final curves $C_n$
have the stated $k'$ bound and tend to $\Gamma$. This explains
why the endpoint bound can be below one even though the intermediate
diamonds require slopes of magnitude one. There is no assertion that
the entire isotopy has slopes below one.

All intermediate square inscriptions are elegant by GL2 Lemma 4.1,
since their slopes are below $1+\sqrt2$. Apply its Proposition 1.3
to each of these strictly nested isotopies starting at $C_r$, and
use $T(C_r)=2r^2$ and (5). This gives (6). This use of the existing
construction imports no continuity assertion for arbitrary Hausdorff
limits or for a clipping path with disappearing vertices. $\square$

## 6. The lower bound and the Lipschitz endpoint

Fix $0<r<M/2$. The diamond in Section 4 is strictly interior, so
(6) and PL spectrality give a nondegenerate square on each $C_n$.
The action lemma applies to its $k'$-Lipschitz branches: its spectral
value is either $J$ or $T(C_n)-J$. In either case (6) implies
$J\ge r^2$. Rifford's inequality (4) now gives

$$
a\ge r,\qquad \operatorname{side}=\sqrt{a^2+b^2}\ge r.
$$

The four vertices stay in a common compact set. A subsequence converges
to vertices of $\Gamma$. The limit is still a square and its side
is at least $r>0$. Now take $r\uparrow M/2$ and apply compactness
again. This proves the bound for PL branches of Lipschitz constant
less than one.

For general 1-Lipschitz branches, interpolate on successively finer
common finite meshes including $A,B$ and at least one interior
point, and multiply both interpolants by $1-1/n$, $n\ge2$.
Each pair has a common Lipschitz bound less than one, equal endpoint
values and strictly positive interior gap. They converge uniformly to
$f,g$, and their maximum gaps tend to $M$. The squares just proved
to exist therefore have a subsequential limit on $\Gamma$ with side
at least $M/2>0$. No smoothness, transversality or convexity hypothesis
has been added in this passage.

In fact the construction preserves a labeling (1) with $a\ge M/2$
and $|b|\le a$ in the limit. The theorem only needs the side bound.

## 7. Exact sharpness and finite completeness

Let $f=-h$, $g=h$ on $[-3/4,3/4]$, where

$$
h(x)=
\begin{cases}
1/2-|x|,&|x|\le1/4,\\
(3/4-|x|)/2,&1/4\le|x|\le3/4.
\end{cases} \tag{9}
$$

Both branches are 1-Lipschitz, agree at the endpoints, and have gap
maximum 1. The square $\{(\pm1/4,\pm1/4)\}$ has side $1/2$.
The included exact certificate proves that no square on this curve has
a larger side; it additionally verifies that this is the only nonzero
inscribed square as a vertex set.

Here is the finite-to-continuous reduction. Represent all square vertices
as $c+v,c+J_0v,c-v,c-J_0v$, with
$J_0(v_x,v_y)=(-v_y,v_x)$. There are eight polygon edges, so all
$8^4=4096$ assignments of vertices to edges are checked. Each
assignment gives four rational supporting-line equations and closed
segment inequalities in $(c_x,c_y,v_x,v_y)$. Their feasible set is a
bounded rational polytope. It is bounded because all four vertices are
on bounded segments and their average and differences recover $c,v$.

Exact row reduction finds the affine solution space. If its dimension is
$d$, solve every choice of $d$ active segment inequalities and
retain the solutions satisfying all inequalities. Every vertex of every
nonempty feasible polytope occurs this way, even when the polytope has
lower dimension than its supporting-line solution space. Squared side
is $2(v_x^2+v_y^2)$, a convex function, whose maximum on a bounded
polytope occurs at a vertex.

The exact audit finds 184 feasible assignments. Sixteen have singular
supporting-line equations. The four singular assignments admitting a
nonzero square each have just one feasible-polytope vertex, and hence
are themselves singletons. Every feasible polytope admitting a nonzero
square is a singleton; all remaining polytopes have only zero-size
vertices and therefore consist entirely of zero-size squares.
Thus no singular family, orientation, boundary contact or three/one
branch split has been omitted. The largest squared side is exactly
$1/4$, which proves optimality of $1/2$.

The program additionally checks a rational rigid motion, a rectangle with
nonzero singular square families, exact chord-envelope extremizers, and
the equality between (2) and alternating arc integrals. These are
corroboration and implementation controls; they do not prove spectral
monotonicity or replace Sections 1--6.

## 8. Attribution, status and limits

Rifford's [Theorem 1.1 and discussion on page 5][R] prove a universal
$0.018M$ bound and propose $M/2$ as the optimal value. The half-gap
problem and the fact that a larger universal constant is impossible
are therefore prior motivation, not new conjectures here. The supplied
rational extremizer makes sharpness independently reproducible.

The new conclusion relative to the searched sources is the full sharp
lower bound, obtained by identifying Rifford's existing local integral
inequality with the square action and applying Greene--Lobb's established
diamond comparison construction at the scale forced by the maximum gap.
Neither the integral inequality nor the comparison construction is new. This is not a new
Floer theory or a proof of the square-peg conjecture for arbitrary Jordan
curves. The previous affine-branch bound and the failure of maximum-gap
localization remain correct. No exhaustive historical-priority claim or
independent peer-review verdict is asserted.

[GL1]: https://arxiv.org/html/2404.05179v2
[GL2]: https://arxiv.org/html/2407.07798v1
[R]: https://arxiv.org/pdf/2106.01914
