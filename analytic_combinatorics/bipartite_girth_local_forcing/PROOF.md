# Sharp local cut forcing at every bipartite girth

Let `H` be any finite simple bipartite graph containing a cycle. Isolated
vertices and disconnected components are allowed. Write

\[
m=e(H),\qquad g=\operatorname{girth}(H),\qquad
c=\#\{\text{unoriented, unrooted }g\text{-cycles in }H\},\qquad
A=\sum_{v\in V(H)}\binom{d_H(v)}2.
\]

Thus `g` is even, `g>=4`, and `A,c>0`. A cycle is counted by its edge set,
not by the number of maps from a labelled cycle. Fix `0<p<1`.

For a symmetric measurable graphon `W:[0,1]^2 -> [0,1]` of integral `p`, use
the usual homomorphism density `t(H,W)`, integrating one independent uniform
variable per vertex, and the cut norm

\[
\|F\|_\square=\sup_{S,T\subseteq[0,1]}
 \left|\int_{S\times T}F(x,y)\,dx\,dy\right|.
\]

All sets are measurable and all kernels are identified almost everywhere.
In particular, there is no extra factor of four in this definition.

## 1. Main result

For sufficiently small `r>0`, define

\[
M_{H,p}(r)=\sup_{
 \substack{\int W=p,\ 0<\|W-p\|_\infty\le rp}}
 \frac{\|W-p\|_\square}{[t(H,W)-p^m]^{1/g}}.
\]

The denominator is positive throughout this domain once `r` is sufficiently
small, as proved below. Then

\[
\boxed{\lim_{r\downarrow0}M_{H,p}(r)
 =\frac{1}{4[c\,p^{m-g}]^{1/g}}.}                 \tag{1}
\]

The exponent `1/g` is the largest possible exponent in any uniform local
bound by a power of the homomorphism-density deficit. The supremum is over
all graphons of density `p`, including irregular ones.

Section 5 also characterizes all asymptotically sharp sequences. Their
degree variance must be negligible relative to their regular `g`-cycle
moment, and their normalized regular operators must approach signed
balanced rank-one operators in Schatten `g` norm. This is a statement in
Schatten norm, not in the kernel `L^2` norm.

The neighborhood here is explicitly an `L^infinity` neighborhood of a
fixed interior density. We do not assert (1) for a cut-norm neighborhood,
as `p` tends to zero, or for nonbipartite graphs. We prove no new global
Sidorenko or global forcing case.

## 2. Signed-density input and its homogeneous consequence

We use the following prior inequalities from L. Lovász, *Subgraph densities
in signed graphons and the local Sidorenko conjecture*,
[arXiv:1004.3026](https://arxiv.org/abs/1004.3026):

* Corollary 2.7 bounds the density of a bipartite graph having two
  nonadjacent vertices of degree at least two by the four-cycle density.
* Lemma 2.22 bounds a bipartite graph of minimum degree at least two and
  girth `ell`, other than a cycle or a complete bipartite graph, by
  `t(C_ell,V)*t(C4,V)^(1/4)` when `|V|<=1`.

Absolute values on the left are valid. They follow directly from the
squared estimates in the proofs; alternatively apply the displayed
inequality to the tensor square `V tensor V` and take a square root.
The right sides are nonnegative. These external inequalities are the
main mathematical premise, not a claim established by our finite audit.

**Homogeneous domination.** If `J` is a nonempty finite simple bipartite
graph with minimum positive degree at least two and girth at least the
even integer `g`, and `U` is a bounded symmetric real kernel with
`||U||_infinity<=h`, then

\[
|t(J,U)|\le h^{e(J)-g}t(C_g,U).                    \tag{2}
\]

For `h=0` this is immediate. Normalize by `h` otherwise. For a cycle of
even length `ell>=g`, the spectral theorem and `||T_(U/h)||_op<=1` give
`t(C_ell,U/h)<=t(C_g,U/h)`. For a connected noncycle with girth at least
six, Lemma 2.22 applies, and its extra four-cycle factor is at most one.
At girth four, Corollary 2.7 applies, including to complete bipartite
graphs: two vertices in one part have the required degrees. For a
disconnected graph, use the bound on any one nonempty component and the
trivial absolute bound one on the other normalized component densities.
Rescaling proves (2). This also explains all exceptional cases in the
imported lemma.

Here `T_U f(x)=int U(x,y)f(y)dy`. It is compact and self-adjoint, and for
even `g>=4`,

\[
t(C_g,U)=\operatorname{tr}(T_U^g)
         =\|T_U\|_{S_g}^{g}\ge0.                  \tag{3}
\]

The identity follows by kernel composition and the spectral theorem for
Hilbert--Schmidt operators. Bounded kernels ensure all products are
integrable; sums of the even eigenvalue powers converge absolutely.

## 3. A uniform expansion with two nonnegative leading terms

Set

\[
\begin{split}
F&=W-p,& a(x)&=\int F(x,y)dy,& v&=\int a^2,\\
D(x,y)&=a(x)+a(y),& U&=F-D,& z&=t(C_g,U),\\
h&=\max\{\|U\|_\infty,\|a\|_\infty\},& x&=h/p,\\
X&=p^{m-2}v,&Y&=p^{m-g}z,&\delta&=t(H,W)-p^m.
\end{split}
\]

We have `int a=0`, `T_U 1=0`, and
`h<=3||F||_infinity`. For `0<=x<=1`, put

\[
B=m2^{m-1},\qquad
E_v(x)=6^m x+B x^{g/2},\qquad
E_g(x)=2^m x^2+B x^{g/2}.
\]

Then the precise uniform estimate is

\[
\boxed{|\delta-A X-cY|\le E_v(x)X+E_g(x)Y.}       \tag{4}
\]

The constants are deliberately coarse; the limiting constants are sharp.
Expand every edge factor as `p+U+D` and group the finite sum by the number
of `D` factors.

**No `D` factors.** Integrating at a leaf kills a `U`-subgraph. The first
remaining nonempty edge sets are precisely the `c` shortest cycles.
Every other surviving set has at least `g+2` edges. To check the latter
claim, a leafless graph with `g+1` edges would contain a `g`-cycle, since
its cycle lengths are even. Its one extra edge would be a chord creating
a shorter cycle, or would create a leaf. Both are impossible. Applying
(2) termwise and using `x<=1` bounds the remaining pure-`U` sum by

\[
2^m x^2Y.                                       \tag{5}
\]

**At least two `D` factors.** Suppose a coloring has `d>=2` such factors,
`u` factors `U`, and `k=d+u`. Expanding each `D` into two possible endpoint
factors gives at most `2^d` terms. Keep two factors `a` and bound all other
factors by `h`. The integral of the absolute product of the two kept
factors is at most `v`: it is `v` if they use the same variable, and is
`(int|a|)^2<=v` if they use different variables. Consequently the colored
term is bounded by `2^d h^(k-2)v`.

For `k=2`, two disjoint edges give zero and adjacent edges give exactly
`v`; their total is `AX`. All other terms have `k>=3`. There are at most
`3^m` colorings, and `2^d<=2^m`. After restoring their `p` factors their
total absolute value is at most

\[
6^m xX.                                         \tag{6}
\]

**Exactly one `D` factor.** Expanding its endpoints gives terms of the
form `int a(q) phi(q)dq`, where `phi` is the rooted density of the `u`
chosen `U` edges. If there is a nonroot leaf the term vanishes. If the
root has no incident `U` edge, it vanishes because `int a=0`.
Otherwise every nonroot vertex of positive degree has degree at least
two. The component containing the root must contain a cycle: a nontrivial
tree cannot have only one possible leaf. Thus `u>=g`.

Glue two copies of the rooted `U`-graph at the root, with every other
vertex kept distinct. The result is a simple bipartite graph with `2u`
edges, no positive degree below two, and girth at least `g`. A simple
cycle cannot cross between the copies through their sole common vertex.
The root has degree at least two after gluing. By (2) and Cauchy--Schwarz,

\[
\|\phi\|_2^2\le h^{2u-g}z,\qquad
\left|\int a\phi\right|\le h^{u-g/2}\sqrt{vz}.
\]

There are at most `m*2^(m-1)` choices of the `D` edge and the set of `U`
edges, and two endpoint terms for each. The factor after restoring `p`
is `x^(u-g/2)*sqrt(XY)`. Since `u>=g`, their total is bounded by

\[
2B x^{g/2}\sqrt{XY}\le Bx^{g/2}(X+Y).             \tag{7}
\]

Combining (5)--(7) proves (4). The argument covers disconnected `H`,
bridges, pendant trees, and any number of shortest cycles.

## 4. Cut norm, the sharp constant, and a finite-radius bound

Since `T_U 1=0`, both indicators in a cut can be centered. Their `L^2`
norms are at most `1/2`; hence

\[
\|U\|_\square\le\tfrac14\|T_U\|_{\mathrm{op}}
                 \le\tfrac14z^{1/g}.
\]

Also `|int_S a|<=sqrt(v)/2`, so `||D||_square<=sqrt(v)`. Consequently

\[
\|F\|_\square\le\tfrac14 z^{1/g}+\sqrt v.          \tag{8}
\]

Whenever `E_v(x)<A` and `E_g(x)<c`, (4) implies

\[
\|F\|_\square\le
 \frac{\delta^{1/g}}{4[c-E_g(x)]^{1/g}p^{(m-g)/g}}
 +\frac{\delta^{1/2}}{[A-E_v(x)]^{1/2}p^{(m-2)/2}}.\tag{9}
\]

It also proves strict positivity of `delta` for nonzero `F`: if both
`v,z` vanish then `a=0` and, by (3), `U=0`.

If `||F||_infinity<=rp`, `r<=1/3`, then `x<=3r`. The ordinary edge-subset
expansion, with its vanishing linear term, gives
`delta<=2^m p^m r^2`. Thus (9) yields the explicit uniform bound

\[
M_{H,p}(r)\le p^{-(m-g)/g}\left\{
\frac1{4[c-E_g(3r)]^{1/g}}
 +\frac{2^{m(1/2-1/g)}r^{1-2/g}}{[A-E_v(3r)]^{1/2}}
\right\},                                       \tag{10}
\]

provided the two bracketed denominators are positive. This proves the
upper limit in (1), with a completely explicit sufficient radius.

For the reverse inequality, take a balanced sign function `f`, equal to
`+1` and `-1` on two measurable sets of measure `1/2`, and let
`W_epsilon=p+epsilon f tensor f`. This is a graphon for sufficiently
small nonzero `epsilon`, of density `p`, and

\[
\|W_\epsilon-p\|_\square=|\epsilon|/4,\qquad
t(H,W_\epsilon)-p^m
=c p^{m-g}\epsilon^g+O_{H,p}(\epsilon^{g+2}).       \tag{11}
\]

Indeed the edge-subset expansion retains exactly the Eulerian subsets:
each vertex must have even degree. The first nonempty ones are the
shortest cycles; every Eulerian subset of a bipartite graph has an even
number of edges. This proves (11), (1), and the impossibility of any
larger exponent than `1/g`.

## 5. Characterization of asymptotically sharp sequences

Consider nonconstant graphons `W_j` of density `p` with
`||W_j-p||_infinity -> 0`; use the preceding notation with subscript `j`.
Their cut/deficit ratio tends to the value in (1) **if and only if**,
eventually `z_j>0`, the following two conditions hold:

1. `v_j/z_j -> 0`;
2. there are signs `sigma_j in {-1,1}` and balanced measurable sign
   functions `f_j` such that

\[
\left\|\frac{T_{U_j}}{z_j^{1/g}}
       -\sigma_j(f_j\otimes f_j)\right\|_{S_g}\longrightarrow0. \tag{12}
\]

The tensor in (12) denotes the rank-one operator
`h -> f_j * int f_j h`. Neither the sign nor the balanced partition
has to converge as `j` varies.

**Necessity of the variance condition.** Estimate (4) implies
`delta_j=(1+o(1))(A X_j+cY_j)`. In particular `v_j=O(delta_j)`, while
`delta_j -> 0`. Therefore
`sqrt(v_j)/delta_j^(1/g) -> 0`. Comparing (8) with an asymptotically
sharp ratio forces `cY_j/delta_j -> 1` and `X_j/delta_j -> 0`.
Thus `v_j=o(z_j)` and

\[
\frac{4\|U_j\|_\square}{z_j^{1/g}}\longrightarrow1.\tag{13}
\]

**Spectral rigidity.** This step only needs a regular self-adjoint kernel
`V` with `||T_V||_(S_g)=1` and `4||V||_square>=1-eta`, where `eta->0`.
There is an eigenvalue `lambda` with `|lambda|>=1-eta`. Its real normalized
eigenfunction `f` is orthogonal to the constants. Write
`T_V=lambda f tensor f+R`. Then `R` is regular and

\[
\|R\|_{S_g}\le[1-(1-\eta)^g]^{1/g}=:\tau\to0.
\]

For a mean-zero rank-one profile the exact cut norm is
`|lambda|*||f||_1^2/4`. Applying (8)'s centered operator inequality to
`R` gives

\[
1-\eta\le|\lambda|\|f\|_1^2+\tau.
\]

Since `|lambda|<=1` and `||f||_1<=||f||_2=1`, it follows that
`||f||_1 -> 1`. The sign function `q=sign(f)` (arbitrary sign at zero)
satisfies
`||f-q||_2^2=2(1-||f||_1) -> 0`. Moreover `int q -> 0`.
By changing `q` on a set of measure `|int q|/2`, one obtains a balanced
sign function `q_0` with `||q-q_0||_2 -> 0`. This uses nonatomicity of
Lebesgue measure. Finally

\[
\|f\otimes f-q_0\otimes q_0\|_{S_g}
 \le2\|f-q_0\|_2\to0.
\]

Since `|lambda| -> 1`, this proves (12) from (13).

**Sufficiency.** Condition (12), Schatten domination of the operator norm,
and the exact cut norm of a balanced rank-one kernel give (13).
The variance condition and (4) give
`delta_j ~ c p^(m-g) z_j`. The term `D_j` is negligible at scale
`z_j^(1/g)`, since
`sqrt(v_j)/z_j^(1/g)=sqrt(v_j/z_j)*z_j^(1/2-1/g) -> 0`.
Together these yield the ratio in (1).

The same argument also shows that the full normalized operator
`T_(W_j-p)/z_j^(1/g)` has the limit description (12): the two nonzero
singular values of `T_D` are `sqrt(v)`, so
`||T_D||_(S_g)=2^(1/g)*sqrt(v)`. However, approximation by a rank-one
operator at that scale alone is **not sufficient** for sharpness.

## 6. Why the separate degree condition matters

For any bounded regular kernel `U` and bounded mean-zero `b`, put

\[
W_\epsilon=p+\epsilon U+
             \epsilon^{g/2}[b(x)+b(y)].
\]

For small positive `epsilon` these are graphons, and (4) gives

\[
t(H,W_\epsilon)-p^m=
\epsilon^g\left[A p^{m-2}\int b^2
                 +c p^{m-g}t(C_g,U)\right]+O_{H,p,U,b}(\epsilon^{g+1}).\tag{14}
\]

Thus the regular cycle contribution and the degree contribution can live
at the same leading order, even when `g` is large. For `U=f tensor f`
with balanced `f` and nonzero `b`, the normalized perturbation converges
to the balanced rank-one profile, but the limiting cut/deficit ratio is
strictly smaller than (1). This verifies that the first condition in
Section 5 cannot be omitted.

For comparison, a forest has `t(H,W)=p^m` for every `p`-regular graphon,
by successively integrating leaves. Thus no deficit-only cut bound of
this type is available for forests. This qualitative boundary is prior
local-forcing theory, not a novelty claim here.

## 7. Evidence and boundaries

The theorem is an analytic proof with the explicitly cited Lovász
inequalities as external premises. The program `verify.py` audits signed
domination, cycle normalizations, centered cut bounds, two-scale
coefficients, finite-radius remainders, and the sharpness construction
using exact rational arithmetic. Its complete finite scope is in
`expected.json` and the README. Finite checks do not establish the
universal theorem or independently verify the cited infinite inequalities.

All sums over edge subsets are finite. Fubini applies to bounded kernels;
spectral arguments use compact self-adjoint Hilbert--Schmidt operators.
There is no floating-point premise, external dataset, solver certificate,
or claimed proof-assistant formalization. Independent mathematical review
of this general theorem remains pending.
