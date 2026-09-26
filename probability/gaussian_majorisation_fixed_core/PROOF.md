# A fixed tetrahedral core, balanced rays, and Gaussian majorisation

**Status:** author proof, with exact supplementary checks; independent review
pending. The full three-dimensional conjecture remains open. This contribution
gives an all-variance measure class and an all-radius, unequal-ball
Kneser--Poulsen class. Neither conclusion is an asymptotic statement.

The problem is [Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/abs/2609.07041).
The new construction is an alternative contraction that fixes an entire
tetrahedral core and preserves one coordinate. Suitable balances preserve
either the output measure or the target ball union. The Gaussian and volume
comparison principles used after that construction are consequences of prior
planar theorems. The antecedent output-law idea is credited to the team's
[balanced-ray theorem](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_ray_relabelling/PROOF.md).

## 1. Geometry and the two maps

Let

$$
u_0=(1,1,1),\quad u_1=(1,-1,-1),\quad
u_2=(-1,1,-1),\quad u_3=(-1,-1,1),
\qquad P_h=h\operatorname{conv}\{u_0,u_1,u_2,u_3\},\quad h>0.
$$

Equivalently, $a\in P_h$ if and only if $u_\ell\cdot a\ge-h$
for all four indices. In particular $|a_i|\le h$.
For $1\le i<j\le3$, $\sigma,\tau\in\{-1,1\}$, and $r\ge2h$, put
$x_{ij}^{\sigma\tau}(r)=r(\sigma e_i+\tau e_j)$.
Consider the union of these twelve rays and any compact $A\subseteq P_h$.
The core and the rays are disjoint. Simultaneous Euclidean isometries and
dilations give equivalent versions of all the statements below; the preserved
coordinate can therefore be any fixed direction.

The original map fixes $A$ and sends

$$
Sx_{ij}^{\sigma\tau}(r)=r\sigma\tau e_k,
\qquad \{i,j,k\}=\{1,2,3\}.                                      \tag{1}
$$

Define a different map, also fixing $A$, by

$$
\begin{aligned}
Rx_{12}^{\sigma\tau}(r)&=r\sigma e_1,\\
Rx_{13}^{\sigma\tau}(r)&=r\sigma e_1,\\
Rx_{23}^{\sigma\tau}(r)&=\tfrac r2\big((\sigma+\tau)e_2+
                                      (\tau-\sigma)e_3\big).
\end{aligned}                                                     \tag{2}
$$

**Geometric lemma.** Both maps are 1-Lipschitz on this entire set, including
between unequal radial parameters. Moreover

$$
(Rx)_1=x_1.                                                       \tag{3}
$$

The region $P_h$ is the largest possible set of additional fixed points
for $S$ when all twelve points at $r=2h$ are present. The largest such
fixed region for $R$ is the cylinder
$\mathbb R\times[-h,h]^2$.

*Proof.* For two ray points at parameters $r,t$, write their squared-distance
deficit as input distance squared minus output distance squared. For $S$,
points in the same coordinate plane have deficit

$$
\begin{cases}
(r-t)^2+8rt,&\sigma\sigma'=\tau\tau'=-1,\\
(r-t)^2,&\text{otherwise}.
\end{cases}                                                       \tag{4}
$$

Points in different coordinate planes have deficit
$(r\eta-t\eta')^2$, where $\eta,\eta'$ are the signs in the shared
coordinate. These are the ray identities from the preceding balanced-ray
work, also obtained directly by expanding (1).

For $R$, the complete list is

| Planes of the two points | Squared-distance deficit |
| --- | --- |
| Both 12, or both 13 | $(r\tau-t\tau')^2$ |
| One 12 and one 13 | $r^2+t^2$ |
| Both 23 | $\tfrac12[(r\sigma-t\sigma')^2+(r\tau-t\tau')^2]$ |
| One 23 and one 12 or 13 | $(r\eta-t\eta')^2$ |

For a core point $a$, the deficit against $x=r v$, with output $r w$,
is $r^2-2r\,a\cdot(v-w)$. For $S$, the vectors $v-w$ range over
$-u_0,-u_1,-u_2,-u_3$. For $R$, they range over
$e_2,-e_2,e_3,-e_3$. Thus in either case the deficit is at least
$r(r-2h)\ge0$. Core-to-core distances are unchanged. Conversely, using
all rays at $r=2h$, these same inequalities impose precisely the four
tetrahedral inequalities for $S$, or the four cylinder inequalities for
$R$. This proves maximality and also the sharpness of the cutoff. Equation
(3) follows directly from (2). $\square$

Kirszbraun's theorem extends these maps to global contractions of
$\mathbb R^3$, so they also meet the global-map formulation of the original
Gaussian question. Only their restrictions to the bounded support are used.

## 2. A planar fibre principle (a consequence of prior results)

Let $K\subset\mathbb R^3$ be compact and $R:K\to\mathbb R^3$ a
contraction with $(Rx)_1=x_1$. Then for every probability measure $\mu$
on $K$, every $s>0$, and every $a>0$,

$$
H_{\mu*\phi_{3,s}}(a)\le H_{R_\#\mu*\phi_{3,s}}(a),\qquad
H_f(a)=\int_{\mathbb R^3}(f-a)_+\,dx,                              \tag{5}
$$

where $\phi_{d,s}$ has covariance $sI_d$.

Indeed, after cancelling the first-coordinate difference in the contraction
inequality,

$$
|(Rx)_\perp-(Rx')_\perp|\le|x_\perp-x'_\perp|.
$$

Thus $(Rx)_\perp=F(x_\perp)$ for a well-defined 1-Lipschitz map on the
projected support. Extend $F$ to $\mathbb R^2$ by Kirszbraun's theorem.
For each $z\in\mathbb R$, define a finite planar measure

$$
\eta_z(B)=\int_K\phi_{1,s}(z-x_1)1_B(x_\perp)\,d\mu(x),
\qquad m_z=\eta_z(\mathbb R^2)>0.
$$

The input and output densities on the slice with first coordinate $z$
are $m_z[(\eta_z/m_z)*\phi_{2,s}]$ and
$m_z[F_\#(\eta_z/m_z)*\phi_{2,s}]$. Apply
[Aishwarya--Li, Theorem 1.2](https://arxiv.org/html/2609.07041v2)
to the planar probability measure $\eta_z/m_z$, at hinge threshold
$a/m_z$. Multiply by $m_z$ and integrate over $z$. Tonelli applies
to the nonnegative hinges, each with integral at most one. This proves (5).
No independence between the coordinates of $\mu$ is assumed.

There is a matching geometric principle. For any finite collection of centres
in $K$ and arbitrary nonnegative radii, $R$ decreases the volume of the
union of the balls and increases the volume of their intersection. At a
fixed first coordinate $z$, the active balls cut out planar disks with
radii $\sqrt{b_x^2-(z-x_1)^2}$, unchanged by $R$; their centres
contract by $F$. Apply the planar union/intersection theorem of
[Bezdek--Connelly, Corollary 1](https://arxiv.org/pdf/math/0108098)
and integrate. If any ball misses a slice, both intersections there are
empty. This is also their Corollary 3, since all displacements lie in one
two-dimensional subspace. We make **no novelty claim for this principle**.

## 3. Full Gaussian majorisation with an arbitrary fixed core

Let $\mu$ be any bounded probability measure on the core and rays above.
Fix $L\ge2h$ bounding its radial support. Denote its twelve finite radial
measures on $[2h,L]$ by

$$
A_{\sigma\tau}=\nu_{12}^{\sigma\tau},\qquad
B_{\sigma\tau}=\nu_{13}^{\sigma\tau},\qquad
C_{\sigma\tau}=\nu_{23}^{\sigma\tau}.
$$

**Theorem A.** Suppose the following are identities of measures:

$$
\begin{aligned}
C_{++}&=B_{++}+B_{--}, & C_{--}&=B_{+-}+B_{-+},\\
C_{-+}&=A_{++}+A_{--}, & C_{+-}&=A_{+-}+A_{-+},\\
A_{++}+A_{+-}&=B_{-+}+B_{--}.&&
\end{aligned}                                                     \tag{6}
$$

Then $S_\#\mu=R_\#\mu$. In particular, for **every** $s>0$ and
**every** $a>0$,

$$
H_{\mu*\phi_{3,s}}(a)\le H_{S_\#\mu*\phi_{3,s}}(a).               \tag{7}
$$

This is full majorisation, equivalently comparison of convex internal
energies whenever their integrals are defined. The mass and distribution
on $A$ are arbitrary; they need not be small, discrete, or symmetric.
Conditions (6) are also necessary for these particular two pushforwards
to agree. They are not claimed necessary for majorisation.

*Proof.* The six nonzero output rays, in the indicated order, receive

| Output ray | From $S$ | From $R$ |
| --- | --- | --- |
| $+e_1$ | $C_{++}+C_{--}$ | $A_{++}+A_{+-}+B_{++}+B_{+-}$ |
| $-e_1$ | $C_{+-}+C_{-+}$ | $A_{-+}+A_{--}+B_{-+}+B_{--}$ |
| $+e_2$ | $B_{++}+B_{--}$ | $C_{++}$ |
| $-e_2$ | $B_{+-}+B_{-+}$ | $C_{--}$ |
| $+e_3$ | $A_{++}+A_{--}$ | $C_{-+}$ |
| $-e_3$ | $A_{+-}+A_{-+}$ | $C_{+-}$ |

Equality of the last four rows gives the first four identities in (6).
After substitution, equality in either of the first two rows gives the
last identity; the other follows from conservation of total mass, as a
measure in $r$. The core is fixed by both maps and is disjoint from their
nonzero output rays. This proves the exact equivalence. Apply (5) to $R$.
$\square$

An especially simple positive subclass puts a common arbitrary radial
probability law $\rho$ on each ray, with individual ray weights

$$
\frac1{16}\quad\text{on planes 12 and 13},\qquad
\frac1{8}\quad\text{on plane 23}.                                \tag{8}
$$

Its image has individual weights $1/4$ on $\pm e_1$ and $1/8$
on $\pm e_2,\pm e_3$. Any mixture of this ray law and any probability
measure on $A$ satisfies the theorem. More generally (6) describes a
seven-dimensional positive cone at each radial parameter, with nonempty
relative interior. Whole radial measures must balance; equality only of
their total masses is insufficient. Arbitrary independent radial laws
can be combined subject to these measure identities.

## 4. Kneser--Poulsen for arbitrary cores and unequal radii

The next theorem concerns sets and balls, so it requires no choice of
probability weights.

Let $A\subset P_h$ and $E\subset[2h,L]$ be compact, with $E\ne\varnothing$.
At a core point $a$, choose a continuous positive radius $\alpha(a)$.
For each $r\in E$, assign twelve positive continuous radius functions
$b_{ij}^{\sigma\tau}(r)$ to the ray centres. In the finite case these
radii are arbitrary numbers with the conditions below.

At each fixed $r$, abbreviate these radius arrays by $A_{\sigma\tau},
B_{\sigma\tau},C_{\sigma\tau}$; **in this section they are numbers, not
the measures in (6)**. Form six effective target radii:

$$
\begin{aligned}
M_S={}&(\max(C_{++},C_{--}),\ \max(C_{+-},C_{-+}),\\
     &\max(B_{++},B_{--}),\ \max(B_{+-},B_{-+}),\\
     &\max(A_{++},A_{--}),\ \max(A_{+-},A_{-+})),\\
M_R={}&(\max(A_{++},A_{+-},B_{++},B_{+-}),\\
     &\max(A_{-+},A_{--},B_{-+},B_{--}),\ C_{++},C_{--},C_{-+},C_{+-}).
\end{aligned}                                                     \tag{9}
$$

**Theorem B.** If $M_S(r)=M_R(r)$ for every $r\in E$, then

$$
\left|\bigcup_{a\in A}B(a,\alpha(a))\ \cup\!
\bigcup_{r\in E,\,i<j,\,\sigma,\tau}
B(Sx_{ij}^{\sigma\tau}(r),b_{ij}^{\sigma\tau}(r))\right|
\ \le\
\left|\bigcup_{a\in A}B(a,\alpha(a))\ \cup\!
\bigcup_{r\in E,\,i<j,\,\sigma,\tau}
B(x_{ij}^{\sigma\tau}(r),b_{ij}^{\sigma\tau}(r))\right|.            \tag{10}
$$

There is no restriction relating the radii on different radial shells, or
relating them to the core radii. In particular, a common radius $b(r)$
on all twelve rays at each $r$, and arbitrary independent core radii,
always satisfy the hypothesis. A genuinely unequal ray-radius example,
using sign order $++,+-,-+,--$, is

$$
(A_{\sigma\tau})=(1,2,3,4),\quad
(B_{\sigma\tau})=(5,6,1,2),\quad
(C_{\sigma\tau})=(5,3,4,6).                                      \tag{11}
$$

These arrays may be multiplied by any positive continuous function of $r$.

Replacing every maximum in (9) by a minimum gives the corresponding
sufficient condition for the **reverse intersection-volume inequality**.
In particular both union and intersection conclusions hold for a common
shell radius and independent core radii.

*Finite proof.* Apply the geometric principle in Section 2 to $R$ with
exactly the given radii. At a fixed $r$, balls sent to the same signed
axis point have union equal to the ball with their largest radius. Formula
(9) says that the $S$- and $R$-target unions agree, shell by shell.
The fixed core is the same. This proves (10). For intersections, coincident
balls collapse to their smallest radius, giving the stated variant.

*Compact extension.* Choose increasing finite dense subsets of $A$ and
$E$, retaining all twelve rays at every selected radial parameter. Every
finite restriction still satisfies (9). We justify passage of union volumes
to the limit, including closed balls. For a compact parameter space, continuous
centres, and positive continuous radii, let $V$ be the union of the open
balls and $U$ the union of the closed balls. Then $\overline V=U$.
At every $x\in\partial V$, an attained closed ball has $x$ on its
sphere and its interior lies in $V$. For all sufficiently small
$\varepsilon$, a ball of radius $\varepsilon/4$ lies in
$V\cap B(x,\varepsilon)$. Thus no point of $\partial V$ has
Lebesgue density one in $\partial V$, so the density theorem implies
$|\partial V|=0$. Hence $|U|=|V|$. Continuity of centres and radii
ensures that every point of $V$ belongs to a ball from a sufficiently
large finite dense restriction. Monotone convergence proves convergence
of both union volumes. For intersections, the decreasing finite
intersections converge exactly to the full intersection, by continuity;
continuity of finite Lebesgue measure from above applies. This proves the
compact version. $\square$

**All-neighbourhood corollary.** For

$$
K=A\cup\{r(\sigma e_i+\tau e_j):r\in E,\ i<j,\ \sigma,\tau=\pm1\},
\quad
K'=A\cup\{\pm r e_i:r\in E,\ i=1,2,3\},
$$

one has $S[K]=R[K]=K'$, and for every $t>0$,

$$
|K'+tB_3|\le|K+tB_3|.                                            \tag{12}
$$

Alternatively, choose a full-support radial law in (8) and a full-support
core law when the core is nonempty,
and obtain (12) from Theorem A and Aishwarya--Li, Remark 1.9. This requires
only one full-support measure, not majorisation for all unbalanced weights.
The direct proof of Theorem B avoids that quantifier issue altogether.

## 5. Why the anchored case is a substantive extension

Take $A=\{h u_0,h u_1,h u_2,h u_3\}$ and $E=\{2h\}$. The ray
points and their $S$-images are exactly

$$
h(u_j-u_i)\longmapsto h(u_j+u_i),\qquad i\ne j,                    \tag{13}
$$

together with the four fixed tetrahedron vertices. This is the classical
sixteen-label simplex-flap contraction at depth one. Its **specified labels**
admit no continuous contraction in $\mathbb R^5$, by reversing
[Cheng--Tan--Zheng, Theorem 2.1](https://arxiv.org/pdf/1107.0140).
The paired affine ranks of the specified map $S$ and the new map $R$
are six and five respectively. Neither the classical configuration nor
its labelled nonliftability is claimed as new.

Theorem B gives its union-volume comparison with four independent anchor
radii and either a common arbitrary flap radius or the broader conditions
(9). The theorem also allows any compact additional core, continuously
many shells, and varying radii. Thus it goes beyond the unanchored twelve
points and beyond a large-radius or small-variance expansion.

The prior balanced-ray map satisfies $x_1=R_2+R_3$ and cannot fix these
four anchors. The present map instead satisfies $x_1=R_1$, and the exact
core inequalities explain why it can fix all of $P_h$. The measure
balances are different. In particular **uniform weights on all twelve
rays do not satisfy (6)**. Full Gaussian majorisation with those uniform
flap weights and an arbitrary anchored law is not proved here, even though
its ball-union case is covered by Theorem B.

There is a precise limitation here. Suppose the four anchors belong to the
support, the ray component has total mass $m>0$, and all twelve rays have
equal weights and a common radial law $\rho$. There is **no** alternative
map fixing all four anchors, having the same output law as $S$, and having
paired affine rank at most five. To see this, a hyperplane containing its
paired support has equation $v\cdot x+w\cdot Rx=c$. The four fixed,
affinely independent anchors force $w=-v$ and $c=0$, with $v\ne0$.
Consequently it preserves $v\cdot x$ and its second moment. But direct
averaging of the twelve directions and six output directions gives

$$
\int xx^{\mathsf T}\,d\mu(x)-\int yy^{\mathsf T}\,d(S_\#\mu)(y)
   =\frac{m\int r^2\,d\rho(r)}3 I_3\succ0.                       \tag{14}
$$

The unchanged core cancels. This contradicts the preserved directional
second moment. The statement excludes all core-fixing rank-five
realisations in this uniform class, not merely formula (2); it does not
exclude majorisation, a rank-six argument, or a map that moves the core.

The improvement does not make the originally labelled motion possible.
It supplies a different realization of the same balanced output law, or
of the same radius-decorated target set. The uniqueness-of-mass-label
obstruction in the team's
[nested-hull theorem](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_nested_hulls/PROOF.md)
therefore remains relevant for unbalanced configurations. The team's
[spherical-tail criterion](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_spherical_tail/PROOF.md)
and [sparse-energy theorem](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_replica_curvature_sparse_energies/PROOF.md)
address different obstructions and are not premises of this proof. The later
[high-noise hinge window](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_high_noise_window/PROOF.md)
was read before publication: it handles arbitrary bounded laws above an
explicit threshold cutoff at high variance. The present class has neither
restriction, but imposes the geometric and measure-balance conditions above.

## 6. Validation and novelty boundary

The exact verifier expands the ray deficits from coordinates, checks all
ordered sign/plane pairs as polynomial identities in two independent
radial parameters, checks the core supporting vectors and sharp cutoff,
computes the two affine ranks, and verifies the five independent additive
balances against the six output incidence rows. It also checks distinct
radial laws, a control where only total masses balance, the unequal-radius
example (11), the classical correspondence (13), and the isotropic
second-moment defect in (14).

These are supplementary algebraic checks. The planar theorems, measure
disintegration by Gaussian weighting, and compact-limit argument are
written analytic proofs, not a computer-assisted enumeration or formal
proof. There is no numerical sign test and no independent review yet.

Primary sources checked were Aishwarya--Li v2, Bezdek--Connelly's planar
theorem (especially Corollaries 1 and 3), and Cheng--Tan--Zheng's flap
construction. Targeted searches combining Kneser--Poulsen and Gaussian
majorisation with tetrahedron, cuboctahedron, fixed cores, relabelling,
and flaps did not locate this fixed-core construction or these additive
and maximum balance classes. This supports **new to the searched sources**,
not historical priority. The source version and the teammates' durable
artifacts were refreshed before publication.
