# Relabelling a rank-six ray contraction without changing its output law

Complete author proof, 26 September 2026; independent review pending.
The bounded-input Gaussian majorisation conjecture in dimension three
remains open. The result here settles an infinite class at **all** density
thresholds and positive Gaussian variances.

## 1. The class and the theorem

Let $e_1,e_2,e_3$ be the standard basis. For $i<j$, write $k$ for the
remaining coordinate, and let $\sigma,\tau\in\{-1,1\}$. Put

$$
v_{ij}^{\sigma\tau}=\sigma e_i+\tau e_j,\qquad
\mathcal C=\{0\}\cup\{r v_{ij}^{\sigma\tau}:r>0\}.
$$

Define two maps on these twelve rays, with both maps fixing zero:

$$
S(r v_{ij}^{\sigma\tau})=r\sigma\tau e_k,
\qquad
R(r v_{ij}^{\sigma\tau})=r\sigma e_k.                 \tag{1}
$$

Fix $L<\infty$. Let $\mu$ be a probability measure supported on
$\{0\}\cup\{r v_{ij}^{\sigma\tau}:0<r\le L\}$. Its mass at zero is
arbitrary. Denote by $\nu_{ij}^{\sigma\tau}$ the finite measure on
$(0,L]$ obtained by restricting $\mu$ to that ray and retaining its radial
parameter $r$. Assume the three **measure identities**

$$
\nu_{ij}^{+,-}=\nu_{ij}^{-,-}\qquad(1\le i<j\le3).    \tag{2}
$$

Equality of total ray masses alone is insufficient for this hypothesis:
the entire radial measures must agree. The two measures
$\nu_{ij}^{+,+}$ and $\nu_{ij}^{-,+}$ are unrestricted, and the three
coordinate planes may carry different masses and different radial laws.

**Theorem.** Both maps in (1) are contractions on $\mathcal C$. Under (2),
for every $s>0$ and $a>0$,

$$
\int_{\mathbb R^3}(\mu*\phi_{3,s}-a)_+\,dx
\ \le\
\int_{\mathbb R^3}((S_\#\mu)*\phi_{3,s}-a)_+\,dx,      \tag{3}
$$

where $\phi_{3,s}$ is the Gaussian density with covariance $sI_3$.
In particular this is full majorisation, rather than a comparison of only
a finite list of moments or convex polynomial energies.

The proof constructs the alternative map $R$ with

$$
R_\#\mu=S_\#\mu,
\qquad x_1=R_2(x)+R_3(x)\quad(x\in\mathcal C).         \tag{4}
$$

Thus the paired support for $R$ lies in a five-dimensional hyperplane.
On the twelve unit-ray points the paired affine ranks of $S$ and $R$
are exactly six and five, respectively.

## 2. Both maps contract at arbitrary radii

Take $x=r v_{ij}^{\sigma\tau}$ and
$x'=u v_{i'j'}^{\sigma'\tau'}$, with $r,u\ge0$.
The formulas remain consistent at zero.

If the points lie in the same coordinate plane, the deficit for $R$ is

$$
|x-x'|^2-|Rx-Rx'|^2=(r\tau-u\tau')^2\ge0.            \tag{5}
$$

For $S$, set $A=\sigma\sigma'$ and $B=\tau\tau'$. The deficit is

$$
r^2+u^2-2ru(A+B-AB)
=\begin{cases}
(r-u)^2+8ru,&A=B=-1,\\
(r-u)^2,&\text{otherwise}.
\end{cases}                                          \tag{6}
$$

If the coordinate planes differ, they share exactly one coordinate.
Let $\eta,\eta'\in\{-1,1\}$ be the signs in that shared coordinate.
The two output axes are orthogonal for either map. Consequently both
deficits are

$$
r^2+u^2-2ru\eta\eta'=(r\eta-u\eta')^2\ge0.           \tag{7}
$$

These identities prove the contraction property on the entire unbounded
cone of rays, including between unequal radii. Kirszbraun's extension
theorem gives global contractions of $\mathbb R^3$ agreeing with the maps
on the support. Only their restrictions are used in (3).

## 3. The output laws coincide

The points from plane $ij$ map to the positive or negative $k$-axis. For
the original map $S$, the radial laws on these two output rays are

$$
\nu_{ij}^{+,+}+\nu_{ij}^{-,-},
\qquad \nu_{ij}^{+,-}+\nu_{ij}^{-,+}.
$$

For $R$ the corresponding laws are

$$
\nu_{ij}^{+,+}+\nu_{ij}^{+,-},
\qquad \nu_{ij}^{-,+}+\nu_{ij}^{-,-}.
$$

They agree exactly under (2). Different coordinate planes map to different
axes, and the atom at zero is fixed, so this proves the first identity in
(4). For these two fixed maps, (2) is also necessary for equality of their
output laws away from zero. It is **not** asserted necessary for (3), or
for the existence of some other helpful relabelling.

## 4. The alternative paired rank is five

For plane $12$, $Rx=r\sigma e_3$ and $x_1=r\sigma$.
For plane $13$, $Rx=r\sigma e_2$ and $x_1=r\sigma$.
For plane $23$, $Rx=r\sigma e_1$ and $x_1=0$.
Thus $x_1=R_2(x)+R_3(x)$ in all cases, including zero. The paired affine
dimension is at most five for every measure under discussion.

For completeness, the rank is exactly five on the twelve unit-ray points.
If $\lambda\cdot x+\zeta\cdot Rx=0$ on those points, independent choices
of the two signs in the three planes give

$$
\lambda_2=\lambda_3=\zeta_1=0,
\qquad \zeta_2=\zeta_3=-\lambda_1.
$$

Hence the space of linear relations is one-dimensional. The mean of the
twelve paired points is zero, so the affine and linear dimensions agree.

For $S$, the three functions $\sigma,\tau,\sigma\tau$ on the four sign
choices are linearly independent. Applying that fact separately in each
coordinate plane shows that
$\lambda\cdot x+\zeta\cdot Sx=0$ forces $\lambda=\zeta=0$. Its paired
affine rank is six, again because the average paired point is zero.
This rank calculation does not assert that the specified map $S$ requires
six dimensions for every possible continuous motion.

## 5. Gaussian majorisation

Apply the earlier team's
[paired-rank theorem, Theorem A](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_rank_abel/PROOF.md)
to the contraction $R$ and the bounded measure $\mu$. It gives

$$
\mu*\phi_{3,s}\preceq (R_\#\mu)*\phi_{3,s}
\qquad(s>0).
$$

Section 3 identifies the second density with $(S_\#\mu)*\phi_{3,s}$,
proving (3).

The cited theorem is an explicit prerequisite, not new work claimed here.
Its mechanism is Gram interpolation of paired coordinates in dimension
five, followed by
[Aishwarya--Li, Theorem 1.4](https://arxiv.org/html/2609.07041v2).
The two auxiliary Gaussian coordinates give a Gamma$(1,1)$ variable;
the identity $\rho(1-a/\rho)_+=(\rho-a)_+$ turns their density-value
comparison into the hinge order. No cancellation of the unresolved
Gamma$(1/2,1)$ smoothing in a rank-six lift is used.

## 6. Consequences for the adversarial frontier

The following subclasses satisfy the entire conclusion:

1. In each coordinate plane, put the same arbitrary bounded radial law
   on its four rays. The laws and their total masses may differ between
   the three planes.
2. In each plane, choose arbitrary radial laws on the two rays with
   $\tau=+1$, and put any common radial law on the other two rays.
   This allows nonsymmetric weights and nonatomic input measures.
3. Add any probability mass at zero to either construction and rescale
   the remaining masses. In particular, every small-mass parameter and
   every far-tail density threshold are included.

At common radius $r=2$, equal ray weights give the twelve flap points in
the team's
[simplex-flap fixture](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_rank_abel/flap_fixture.json),
with the four tetrahedron anchors removed. Their uniform input law on
twelve cuboctahedral vertices maps to the uniform law on six octahedral
vertices. This whole Gaussian comparison is therefore settled, even
though its original label map has paired rank six.

The four fixed anchors are not in $\mathcal C$ and do not satisfy (4).
They cannot be added by the proof above. The
[earlier all-scale quartic result](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_symmetric_flap_quartics/PROOF.md)
continues to address the different class with anchors present; the full
comparison there remains open. The
[small-mass theorem](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_small_mass/PROOF.md)
addresses arbitrary fixed bounded rare laws above a threshold floor,
whereas the present balanced ray class covers every threshold and every
mass at zero. Neither theorem implies the other in its full stated scope.

The reusable mechanism is **changing the contracting realization of the
same pair of measures**. A rank-six calculation for one labelled map
does not rule out a rank-five contraction with the same pushforward.
Searches on this balanced twelve-ray class can therefore be excluded
exactly, including tests at higher polynomial degrees and extremely low
density thresholds. This does not exclude arbitrary unbalanced ray laws,
anchored flaps, or the general dimension-three conjecture.

## 7. Provenance and validation

The problem source is
[Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/abs/2609.07041).
The rank reduction and its Gaussian argument are credited to the preceding
geometric contribution. The finite classical flap fixture is background;
no new claim about its nonliftability or about historical cuboctahedral
geometry is made. Searches for Gaussian majorisation combined with
cuboctahedral, octahedral, relabelling, and paired-rank terminology did not
locate this stated measure class. That bounded literature check does not
establish historical priority.

The program checks all ordered ray pairs as exact quadratic polynomials
in two arbitrary radial variables, independently computes both affine
ranks by rational elimination, compares exact pushforwards for unequal
radii and biased balanced weights, and rejects an unbalanced control.
Those checks audit the elementary construction. The continuum theorem
uses the proof above and the cited analytic result, not numerical samples.
See [VALIDATION.md](VALIDATION.md) for commands and trust boundaries.
