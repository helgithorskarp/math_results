# Three disjoint cap reflections admit a five-dimensional contracting motion

Author proof, 26 September 2026; independent correctness and priority review
pending. The unrestricted dimension-three Gaussian majorisation conjecture
remains open. The result concerns a class of maps, with no restriction on the
measure's weights, Gaussian variance, number of atoms, or ball radii.

## 1. Statement

Let $K\subset\mathbb R^3$ be compact and convex. For $1\le i\le m\le3$ let
$n_i$ be a unit vector, let $b_i\in\mathbb R$, and suppose the relatively open
caps

$$
C_i=\{x\in K:n_i\cdot x>b_i\}
\tag{1}
$$

are pairwise disjoint. Put $C_0=K\setminus\bigcup_i C_i$. Define

$$
T(x)=\begin{cases}
x-2(n_i\cdot x-b_i)n_i,&x\in C_i,\\
x,&x\in C_0.
\end{cases}
\tag{2}
$$

**Theorem.** There is an explicit continuous contracting motion in
$\mathbb R^5$ from $x\mapsto(x,0)$ to $x\mapsto(Tx,0)$ on all of $K$.
Each individual trajectory is analytic. In particular, $T$ is 1-Lipschitz.

**Gaussian consequence.** Write $\phi_{d,s}$ for the centred Gaussian density
with covariance $sI_d$ and $H_f(h)=\int(f-h)_+$. For every probability measure
$\mu$ on $K$, every $s>0$, and every $h\ge0$,

$$
H_{\mu*\phi_{3,s}}(h)\le H_{T_\#\mu*\phi_{3,s}}(h).
\tag{3}
$$

This is full majorisation. Finite positive measures follow by scaling their
total mass. The Gaussian consequence allows arbitrary atomic or nonatomic
laws and all weights; it is not an asymptotic or numerical comparison.

**Kneser--Poulsen consequence.** For every finite labelled selection
$x_1,\ldots,x_N\in K$ and every choice of individual radii $r_j\ge0$,

$$
\begin{split}
\left|\bigcup_{j=1}^N B(Tx_j,r_j)\right|
&\le\left|\bigcup_{j=1}^N B(x_j,r_j)\right|,\\
\left|\bigcap_{j=1}^N B(Tx_j,r_j)\right|
&\ge\left|\bigcap_{j=1}^N B(x_j,r_j)\right|.
\end{split}
\tag{4}
$$

The three planes and caps are unrestricted apart from (1) and disjointness.
Their normals may span all of $\mathbb R^3$. Empty caps and points on their
boundary planes cause no difficulty. The cap interiors need not be small,
and the result has no positive contraction reserve assumption.

## 2. Separation supplies the needed distance margin

Fix $x\in C_i$, $y\in C_j$, $i\ne j$, and abbreviate

$$
\begin{gathered}
a=n_i\cdot x-b_i>0,\quad b=n_j\cdot y-b_j>0,\\
h_i=b_i-n_i\cdot y\ge0,\quad h_j=b_j-n_j\cdot x\ge0,\quad
N=n_i\cdot n_j.
\end{gathered}
$$

By convexity, $z_t=(1-t)x+ty$ lies in $K$. Its $i$-th cap coordinate is
$a-t(a+h_i)$ and its $j$-th coordinate is $-h_j+t(h_j+b)$.
Disjointness forbids these two coordinates from being simultaneously positive.
Their positive intervals therefore satisfy

$$
\frac{a}{a+h_i}\le\frac{h_j}{h_j+b},\qquad h_i h_j\ge ab.
\tag{5}
$$

In particular, both $h_i,h_j$ are positive. The arithmetic-geometric mean
inequality gives $a h_i+b h_j\ge2ab$.

Put $d=x-y$ and $v=a n_i-b n_j$. The quantity

$$
E=d\cdot v-|v|^2=a h_i+b h_j+2abN
\ge2ab(1+N)\ge0
\tag{6}
$$

is one fourth of the drop in squared endpoint distance. The extra lower bound
in (6), not merely endpoint nonexpansion, will control the entire motion.

## 3. Three normals can be separated on an auxiliary circle

We need unit vectors $u_i\in\mathbb R^2$ satisfying

$$
u_i\cdot u_j\le1+2n_i\cdot n_j\quad(i\ne j).
\tag{7}
$$

For any two unit-vector inner products $N,U\in[-1,1]$, condition
$U\le1+2N$ is equivalent to

$$
|N-U|\le1+N.
\tag{8}
$$

Indeed its two inequalities are $U\ge-1$ and $U\le1+2N$.

For three given normals one can even arrange
$u_i\cdot u_j\le n_i\cdot n_j$. Let
$\alpha_{ij}=\arccos(n_i\cdot n_j)\in[0,\pi]$. Spherical distance obeys
the triangle inequality, including through an antipode, so

$$
\alpha_{12}\le (\pi-\alpha_{13})+(\pi-\alpha_{23}),\qquad
\alpha_{12}+\alpha_{23}+\alpha_{31}\le2\pi.
\tag{9}
$$

Choose numbers $\beta_{ij}\in[\alpha_{ij},\pi]$ with sum $2\pi$.
They exist because the sum of the three interval lower endpoints is at most
$2\pi$, whereas the sum of their upper endpoints is $3\pi$. Place three
unit vectors consecutively on a circle with gaps
$\beta_{12},\beta_{23},\beta_{31}$. Each gap is at most $\pi$, so it is
the corresponding smaller angular distance. Since cosine is decreasing on
$[0,\pi]$, their inner products are at most those of the normals.
This implies (7), since $N\le1+2N$ for $N\ge-1$.

For two caps choose antipodal auxiliary vectors, and for one cap choose any
unit vector. Coincident or antipodal normals are included. Coincident chosen
auxiliary vectors are allowed in degenerate cases.

## 4. The motion and its full-time derivative

Choose $u_i$ as above. For $0\le\theta\le\pi$ put

$$
P_\theta(x)=\begin{cases}
\big(x-(1-\cos\theta)a_i(x)n_i,\ \sin\theta\,a_i(x)u_i\big),
 &x\in C_i,\\
(x,0),&x\in C_0,
\end{cases}
\qquad a_i(x)=n_i\cdot x-b_i.
\tag{10}
$$

At each boundary plane $a_i=0$, so the formulas agree. The finite piecewise
definition is jointly continuous in $x,\theta$. It starts at $(x,0)$ and
ends at $(Tx,0)$. Each fixed-label trajectory is analytic in $\theta$.

Distances within one cap are constant: the coefficient of a difference in
the normal coordinate is $(\cos\theta n_i,\sin\theta u_i)$, a unit
vector orthogonal to all tangential differences. Distances within $C_0$
are constant. For $x\in C_i,z\in C_0$, write $a=a_i(x)>0$ and
$h=b_i-n_i\cdot z\ge0$. Direct expansion gives

$$
|P_\theta(x)-P_\theta(z)|^2=|x-z|^2-2(1-\cos\theta)ah,
\tag{11}
$$

which decreases throughout the motion.

For two different caps use the notation of Section 2 and set

$$
U=u_i\cdot u_j,\quad
\Delta=|a u_i-b u_j|^2-|a n_i-b n_j|^2=2ab(N-U),\quad
\lambda=\frac{1-\cos\theta}{2}.
$$

The squared pair distance is the following polynomial in the increasing
parameter $\lambda\in[0,1]$:

$$
D(\lambda)=|d|^2-4\lambda E+4\lambda(1-\lambda)\Delta.
\tag{12}
$$

Equations (6)--(8) imply $E\ge|\Delta|$. Consequently

$$
D'(\lambda)=-4E+4(1-2\lambda)\Delta
\le-4(E-|\Delta|)\le0.
\tag{13}
$$

This proves monotonicity for every pair and every time, including endpoint
and boundary degeneracies. It proves the theorem.

The same calculation also proves a conditional result for any finite number
of disjoint caps: if two-dimensional unit vectors satisfying (7) are supplied,
(10) is a contracting motion. We assert automatic existence only for at most
three caps. Neither necessity of (7) nor sharpness of the cap count is claimed.

## 5. Transferring the motion to Gaussian majorisation and ball volumes

Put $f=\mu*\phi_{3,s}$ and $g=T_\#\mu*\phi_{3,s}$. Applying
[Aishwarya--Li, Theorem 1.4(i)(a)](https://arxiv.org/html/2609.07041v2)
to (10) in dimension five says that the value of the initial smoothed density,
sampled from itself, is stochastically dominated by the corresponding final
density value. At the endpoints these are product densities
$f(x)\phi_{2,s}(y)$ and $g(x)\phi_{2,s}(y)$.

Here is the precise two-coordinate transfer, also recorded in the team's
[paired-rank proof, Section 3](../gaussian_majorisation_rank_abel/PROOF.md).
Let $X$ have density $f$ and independently $Y\sim\phi_{2,s}$. Put
$C=(2\pi s)^{-1}$. The variable $|Y|^2/(2s)$ has the exponential law of
mean one, and thus $\phi_{2,s}(Y)/C$ is uniform on $(0,1)$. For $h>0$,

$$
\Pr\{f(X)\phi_{2,s}(Y)>Ch\}
=\int f(x)(1-h/f(x))_+\,dx=H_f(h).
\tag{14}
$$

The same identity applies to $g$. Stochastic domination proves (3) for $h>0$;
at $h=0$ both sides equal one. This argument uses the density-value conclusion
of the source theorem. It does not assume that ordinary majorisation can be
cancelled across an auxiliary Gaussian factor.

For (4), use [Bezdek--Connelly, Theorem 1](https://arxiv.org/pdf/math/0108098).
That theorem gives both ball-volume inequalities for an endpoint expansion
in $\mathbb R^n$ admitting a piecewise smooth expanding motion in
$\mathbb R^{n+2}$. Reverse the finite restriction of (10) and take $n=3$.
Its trajectories are analytic, so the hypothesis applies with arbitrary
individual positive radii. Radii zero follow by continuity. Labels with
coincident centres can also be handled by continuity if necessary.

## 6. Exact seven-site example with three interacting folds

Take $b_i=0$ and $n_i=v_i/\sqrt3$, where

$$
v_0=(1,1,1),\quad v_1=(1,-1,-1),\quad v_2=(-1,1,-1).
$$

The source sites and their images are

| Label | Source | Image |
| --- | --- | --- |
| $c_0$ | $(0,0,0)$ | $(0,0,0)$ |
| $c_1$ | $(-1,-1,0)$ | $(-1,-1,0)$ |
| $c_2$ | $(-1,0,1)$ | $(-1,0,1)$ |
| $c_3$ | $(0,-1,1)$ | $(0,-1,1)$ |
| $x_0$ | $(1,-2,5)$ | $(-5/3,-14/3,7/3)$ |
| $x_1$ | $(-2,-5,-1)$ | $(-14/3,-7/3,5/3)$ |
| $x_2$ | $(-5,1,2)$ | $(-7/3,-5/3,14/3)$ |

Let $K$ be the convex hull of these seven source sites and write
$t_i=v_i\cdot x$. Every vertex satisfies

$$
t_0+2t_1\le0,\quad t_1+2t_2\le0,\quad t_2+2t_0\le0.
\tag{15}
$$

These linear inequalities hold on $K$ and forbid any two positive $t_i$.
Hence they certify disjointness throughout the convex body, not only on
the seven labels. Each cap is nonempty, the normals are independent, and
the four fixed core points are affinely independent.

For this example one can use the rational auxiliary vectors

$$
u_0=(1,0),\quad u_1=(0,1),\quad u_2=(-1,0).
\tag{16}
$$

They satisfy (7): all $N_{ij}=-1/3$, and their off-diagonal inner products
are $0,0,-1\le1/3$. For distinct moved sites, $E=88/9$ and
$\Delta=-32/9$ or $64/9$, so every derivative is nonpositive.
[verify.py](verify.py) checks all 21 pair polynomials exactly over the
rationals, not just those three pairs. There are 15 tight and six strict
endpoint pairs. The tight-edge rigidity matrix has rank 15 at each endpoint;
the paired affine rank is six. See [EXPECTED.json](EXPECTED.json) for the
full small control data and coefficients.

Thus the paired affine rank-at-most-five sufficient condition does not cover
this example. Each cap contains a full-dimensional part of $K$, and the
theorem applies to arbitrary measures there, not just these labels. No
symmetry assumption on that measure is used.

### Two rejected shortcuts

First, taking all three auxiliary vectors equal gives $\Delta=-128/9$ for
each pair of moved labels. The derivative at $\lambda=1$ in (12) then equals
$160/9>0$. Endpoint contraction alone does not validate this choice of lift.
This is a counterexample to that proposed motion, not to Gaussian majorisation.

Second, let $G_i$ be the one-sided fold across the $i$-th prescribed plane,
acting as reflection when $v_i\cdot x>0$ and as identity otherwise. The
image $T(x_0)$ enters the positive side of plane 1; $T(x_1)$ enters that of
plane 2; $T(x_2)$ enters that of plane 0. The exact checker tries all six
orders using each $G_i$ once. Every order differs from $T$ on at least one
listed site. This finite-order check alone excludes only those six compositions.
The stronger obstruction to arbitrary finite strong-contraction chains below
requires a separate argument about all possible intermediate configurations.

### Exclusion of a single strong contraction in any orthonormal frames

The example also escapes a single coordinatewise strong contraction, even
if different orthonormal input and output frames are permitted. Recall that
strong contraction means contraction of the absolute difference in each
coordinate separately; see [Bezdek--Naszodi, Section 1.2](https://arxiv.org/pdf/1701.05074).

Suppose unit axes $a_k$ at the input and $b_k$ at the output give all these
coordinatewise inequalities. The six fixed core pairs preserve Euclidean
distance. Summing the squared coordinate inequalities then forces equality
in each of them. For each $k$, the finite scalar configurations
$a_k\cdot c_j$ and $b_k\cdot c_j$ have the same pair distances. Any such
scalar isometry has one common sign and translation. Because $c_0=0$ and
the core spans $\mathbb R^3$, this implies $b_k=\pm a_k$.
Changing coordinate signs reduces to a common orthonormal frame.

For each moved site $x_i$, its three tight core anchors lie on the plane
$v_i\cdot x=0$ and span that plane. In any coordinate where
$a_k\cdot T(x_i)\ne a_k\cdot x_i$, equality of the three scalar distances
forces all three anchor coordinates to equal the midpoint of those two
distinct values. Consequently $a_k$ is normal to that plane, hence parallel
to $v_i$. The nonzero displacement of $x_i$ must have a nonzero component
in some coordinate, so each $v_i$ must be parallel to an axis of the same
orthonormal frame. The three distinct normal directions have nonzero mutual
inner products, making this impossible.

The checker verifies the core rank, the three noncollinear face attachments,
their tight distances, and the nonorthogonality used in this argument.

### Obstruction to every finite strong-contraction chain in dimension three

Suppose the source could be carried to the target by a finite sequence of
strong contractions, permitting a different orthonormal frame at every step.
Every pair distance is nonincreasing along this sequence. Each tight
endpoint pair must therefore keep its distance at every intermediate stage.
In particular the four core labels form the same nondegenerate tetrahedron.
At each stage apply an ambient isometry to restore its labelled core to the
four $c_j$. Independent changes of input and output orthonormal frames
preserve the strong-step hypothesis in the enlarged sense just considered.

The three distances from a moved label to its tight face anchors stay fixed.
Three noncollinear anchors in a plane, together with those distances, admit
exactly two locations in $\mathbb R^3$: the original $x_i$ and its reflection
$T(x_i)$. Thus every aligned intermediate configuration is one of eight
states, indexed by bits $(\varepsilon_0,\varepsilon_1,\varepsilon_2)$,
where 0 denotes $x_i$ and 1 denotes $T(x_i)$.

In fact, only the two endpoint states can occur on a chain terminating at
the specified target. For each ordered cyclic pair $(i,j)=(0,1),(1,2),(2,0)$,
its squared distance depends on its two bits as follows:

| Bits $(\varepsilon_i,\varepsilon_j)$ | $00$ | $10$ | $01$ | $11$ |
| --- | --- | --- | --- | --- |
| Squared distance | $54$ | $34/3$ | $130/3$ | $134/9$ |

Every mixed cyclic bit string contains a consecutive $10$. But
$34/3=102/9<134/9$, so that mixed state already contracts a pair more than
the final configuration does. A nonincreasing chain cannot reach the final
distance from there. Thus every intermediate configuration of any
three-dimensional contraction chain between these endpoints is congruent
to one of the endpoints. The displayed four entries are direct rational
distance calculations, independently checkable from the coordinate table.

A strong step between two states can change at most one bit. To see this,
repeat the preceding core/face argument for the changed labels: the input
and output axes agree up to signs, and the normal of every changed label
must be parallel to an axis in that common frame. No two of the three
distinct normals are orthogonal or parallel. Therefore two bits cannot
change in one strong step. Since any nontrivial step on a chain to the
target would have to change all three bits at once, this already proves
the obstruction to every finite strong-contraction chain.

As an additional reproducible control, the complete list of directed,
one-bit changes that contract all 21 distances is

$$
000\longrightarrow001,010,100;\qquad
001\longrightarrow011;\qquad
010\longrightarrow110;\qquad
100\longrightarrow101.
\tag{17}
$$

The exact checker enumerates all eight states and every one-bit ordered
pair, and produces precisely (17). It also computes reachability: the seven
states other than $111$ are reachable from $000$, while $111$ is not.
Steps changing no bits are irrelevant. Hence no finite strong-contraction
chain reaches the target. Each one-sided hyperplane fold is strong in a
frame with a normal coordinate, so this also excludes arbitrary finite
compositions of such folds in $\mathbb R^3$.

The argument reduces *every possible intermediate configuration* to eight
states and rules out the mixed states by the four-entry distance table.
The checker verifies that table and the complete eight-state calculation;
the obstruction is not inferred from the six prescribed orders alone. It concerns finite chains
in dimension three, and does not obstruct the five-dimensional motion (10)
or other majorisation mechanisms.

## 7. Scope and prior-work boundary

The new mathematical content proposed here is the separation margin (5)--(6)
combined with the auxiliary-circle placement and explicit motion (10).
The Gaussian transfer and the codimension-two ball-volume theorem are prior
results, cited above. Classical one-sided folds and coordinatewise strong
contractions already have Kneser--Poulsen results; they are not claimed here
as new. The seven-site controls distinguish this family from the cited
paired-rank bound and from every finite strong-contraction chain in dimension
three. They are not an exhaustive classification of all known sufficient
classes.

This family permits a convex three-dimensional domain with three separate
reflection planes and arbitrary laws, rather than imposing axial support,
ordered weights, or two paired layers. A bounded search of primary sources
and the current team packets did not locate this precise three-cap motion
theorem. That search is not a proof of historical novelty. Independent review
of both the proof and its relationship to prior folding results is pending.

No counterexample to the unrestricted conjecture is supplied. Four or more
caps without an auxiliary certificate, general interacting folding meshes,
and general 1-Lipschitz maps remain outside the proved automatic class.
