# A scalar defect absorbed by pairwise contraction

Author proof; independent review pending. All Euclidean norms are ordinary
norms, and $\gamma_s^{(d)}$ denotes the density with covariance $sI_d$.

## 1. Endpoint theorem

Let $K\subset\mathbb R^3$ and $T:K\to\mathbb R^3$. Suppose fixed unit vectors
$e,f$ satisfy

$$
 d(x,x'):=|x-x'|^2-|T(x)-T(x')|^2
 \ \ge\
 |e\cdot(x-x')-f\cdot(T(x)-T(x'))|^2                            \tag{3}
$$

for every pair. In particular, $T$ is a contraction.

**Theorem.** For every bounded probability measure $\mu$ supported on $K$,
every $s>0$, and every $a>0$, put
$p=\mu*\gamma_s^{(3)}$ and $q=(T_\#\mu)*\gamma_s^{(3)}$. Then

$$
 \int(p-a)_+\,dx\le\int(q-a)_+\,dx.                            \tag{4}
$$

For every finite list $x_i\in K$ and all radii $r_i\ge0$,

$$
 \left|\bigcup_i B(Tx_i,r_i)\right|
 \le \left|\bigcup_i B(x_i,r_i)\right|,\qquad
 \left|\bigcap_i B(Tx_i,r_i)\right|
 \ge \left|\bigcap_i B(x_i,r_i)\right|.                        \tag{5}
$$

These are three-dimensional volumes. Atom weights, number of sites,
thresholds, and variances have no additional restriction. The Gaussian
assertion includes nonatomic bounded laws.

## 2. The exact interpolation identity

Apply separate orthogonal changes of coordinates at the endpoints so
that $x=(u,r)\in\mathbb R^2\oplus\mathbb R$,
$Tx=(v,s_0)\in\mathbb R^2\oplus\mathbb R$, with
$r=e\cdot x$ and $s_0=f\cdot Tx$. The letter $s_0$ here is a position
coordinate, not Gaussian variance.

For $0\le t\le1$, define in $\mathbb R^2\oplus\mathbb R^2\oplus\mathbb R$

$$
 Z_t(x)=\big(\sqrt{1-t}\,u,\sqrt t\,v,(1-t)r+ts_0\big).        \tag{6}
$$

For one pair, write $X=|x-x'|^2$, $Y=|Tx-Tx'|^2$, and
$b=(r-r'-(s_0-s_0'))^2$. Direct expansion gives

$$
 |Z_t(x)-Z_t(x')|^2=(1-t)X+tY-t(1-t)b.                       \tag{7}
$$

Its derivative is

$$
 -(X-Y)+(2t-1)b\le -(X-Y)+b\le0.                            \tag{8}
$$

Thus (3) is sufficient, and is also necessary for monotonicity of this
particular interpolation: its largest derivative occurs at $t=1$.
It is not a necessary condition for other motions or for majorisation.

Use $t=\sin^2\theta$, $0\le\theta\le\pi/2$, to obtain smooth trajectories
through both endpoints. The initial and final copies of $\mathbb R^3$
are different subspaces of $\mathbb R^5$. A rigid rotation of the first
four coordinates sends the final copy to the initial copy without
changing any pair distance. Append it when endpoints in one fixed
subspace are required. Separate endpoint isometries used above do not
change the Gaussian or ball-volume quantities.

The map (6) is a continuous contraction on the entire domain, rather than
a motion constructed separately for each finite subset. Joint continuity
on bounded subsets follows from the Lipschitz property of $T$.

## 3. Gaussian cancellation and the volume consequence

Apply Aishwarya--Li, Theorem 1.4(i)(a), to this motion in dimension five.
It compares the density values sampled from the two endpoint densities.
At either endpoint the density factors as its three-dimensional density
times $\gamma_s^{(2)}$ in the orthogonal complement.

Set $C_2=(2\pi s)^{-1}$. If $X$ has density $p$ and $W$ independently has
density $\gamma_s^{(2)}$, then $|W|^2/(2s)$ is exponential of mean one.
Consequently

$$
 \Pr\{p(X)\gamma_s^{(2)}(W)>aC_2\}
 =\int p(x)\left(1-\frac{a}{p(x)}\right)_+dx
 =\int(p-a)_+\,dx.                                         \tag{9}
$$

The same identity holds for $q$. The five-dimensional stochastic
comparison therefore proves (4). This cancellation is already used in
the team's paired-rank and simplicial-cone results; it is repeated to make
the precise endpoint transparent.

Reverse the piecewise-smooth motion from Section 2 and apply
Bezdek--Connelly, Theorem 1, in dimension $3+2$. This gives (5). Zero
radii follow by continuity. Neither transfer theorem is new here.

## 4. A quantitative perturbation class

Suppose $F:K\to\mathbb R^3$ is 1-Lipschitz and

$$
 e\cdot(x-x')=f\cdot(Fx-Fx') \quad(x,x'\in K),                 \tag{10}
$$

where $e,f$ are unit vectors. Let $T=q_0F+E$, with
$0\le q_0\le1$ and $\operatorname{Lip}(E)\le\epsilon$. Constants in
$E$ are unrestricted. The triangle inequality gives

$$
 |\Delta T|\le(q_0+\epsilon)|\Delta x|,\qquad
 |e\cdot\Delta x-f\cdot\Delta T|
 \le(1-q_0+\epsilon)|\Delta x|.
$$

The sum of the squared bounds is at most $|\Delta x|^2$ exactly when

$$
 (q_0+\epsilon)^2+(1-q_0+\epsilon)^2\le1
 \quad\Longleftrightarrow\quad
 \epsilon^2+\epsilon\le q_0(1-q_0).                          \tag{11}
$$

This proves the stated class. The endpoint case is included. At
$q_0=1/2$, any $\epsilon\le(\sqrt2-1)/2$ suffices. If the inequality is
strict, the hypotheses tolerate further perturbations in Lipschitz norm.
The constant is sufficient, not asserted optimal over all constructions.

## 5. An exact example beyond paired rank and strong coordinates

On all of $\mathbb R^3$ define

$$
 T(x,y,z)=
 \left(\frac{|x|}{2}+\frac y{20},
       \frac{|y|}{2}+\frac z{20},
       \frac z2+\frac{|x+2y+2z|}{60}\right).                 \tag{12}
$$

Here $F(x,y,z)=(|x|,|y|,z)$ preserves $e_3$, $q_0=1/2$, and

$$
 E=\frac1{20}\left(y,z,\left|\frac{x+2y+2z}{3}\right|\right).
$$

The vector $(1,2,2)/3$ has norm one, so
$|\Delta E|^2\le|\Delta x|^2/200\le|\Delta x|^2/100$.
We may use $\epsilon=1/10$ in (11). Its squared-bound sum is $18/25$,
leaving margin $7/25$. In particular (12) is a contraction on the whole
space, and every bounded law on it satisfies (4).

Consider the seven input sites

$$
 0,\ e_1,\ -2e_1,\ e_2,\ -2e_2,\ e_3,\ -2e_3.                \tag{13}
$$

Their targets are all distinct:

$$
 0,\ (1/2,0,1/60),\ (1,0,1/30),\
 (1/20,1/2,1/30),\ (-1/10,1,1/15),\
 (0,1/20,8/15),\ (0,-1/10,-14/15).
$$

The paired vectors $(x_i,Tx_i)$ span all of $\mathbb R^6$.
Indeed, twice the positive-axis paired vector plus the negative-axis
paired vector has zero input part. The three resulting output vectors
are $(2,0,1/15)$, $(0,2,2/15)$, and $(0,0,2/15)$, which are independent.
Together with the three independent input directions this gives rank six.
Thus this fixture does not meet the paired-affine-rank-five hypothesis.
Its displacement vectors also span three dimensions, as the checker
verifies; the two-dimensional-displacement corollary does not apply
directly to these endpoint coordinates.

There is no choice of separate orthonormal input and output coordinates
making the global map (12) a strong contraction. Such coordinates would
force each output coordinate to depend only on the corresponding input
coordinate, so all Jacobians would become diagonal under the same two
orthogonal matrices. In the open sign regions of $x,y,x+2y+2z$, changing
only the sign of $x$ changes the Jacobian by $E_{11}$; changing only the
sign of $y$ changes it by $E_{22}$. Every such sign region is nonempty.
For a rank-one matrix to become diagonal its two defining directions
must be corresponding coordinate axes. These two differences therefore
fix the first and second axes, up to matching permutation and signs;
orthogonality fixes the third. The nonzero entry $J_{12}=1/20$ of every
Jacobian cannot then become diagonal, a contradiction.

These are distinctions from specific sufficient criteria. They do not
exclude every possible factorization or earlier motion construction.
The result is presented as a usable criterion with endpoint consequences,
not a claim of a new general Kneser--Poulsen transfer theorem.

## 6. The nonsimplicial frontier is still outside this condition

Suppose the domain contains zero, fixed vectors $a_i$ spanning
$\mathbb R^3$, and vectors $-b_j$ mapped to $b_j$, with the $b_j$ also
spanning $\mathbb R^3$. Every pair with zero preserves its distance.
Condition (3) would force

$$
 (e-f)\cdot a_i=0,\qquad (e+f)\cdot b_j=0.
$$

Hence $e=f$ and $e=-f$, impossible for unit vectors. This applies to
researcher7's square-cone nine-point example, and also to spanning
simplicial-cone examples already resolved by a different motion.
The new criterion and that theorem are complementary, not nested.
The later axial-cone theorem also follows norm-preserving spanning
clusters, so it is complementary for the same reason.

Researcher8's common-target decomposition settles a different,
merged-output class and cannot enlarge finite injective deterministic
targets. Neither that decomposition, entropy rigidity, nor the
high-variance endpoint is used to infer (4) here.
The latest asymmetric square-cone covariance certificate further rules
out the martingale sufficient route for an open set of weights, even
after common Gaussian smoothing. This is incorporated as a restriction
on the next analytic target, not as an argument against majorisation.

The next analytic obligation for the square cone remains an integrated
hinge or a stochastic comparison after smoothing. This note hands the
positive estimate (11) to the geometric lane and does not propose
another scalar-coordinate search on that closed boundary obstruction.

## 7. Validation

The standard-library rational checker verifies (7) and (8) as polynomial
identities, the perturbation boundary including equality, all 21 fixture
pairs, paired rank six, displacement rank three, the explicit target
list, and the two spanning conditions in Section 6. An intentional
false certificate must be rejected. Normal and optimized Python agree.

These finite checks audit algebra, constants, and the example. The
universal conclusion is the analytic proof above with the two primary
transfer theorems identified in SOURCES.md. No finite numerical
experiment, formalization, or independent mathematical review is claimed.
