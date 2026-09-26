# Exact positive-face exclusion for two-scale Gaussian counterexample searches

Author proof, 26 September 2026. External review pending.

The full dimension-three conjecture remains open. We classify the **entire
paired-rank-five support boundary** of the 16-site, two-scale polar family:
208 maximal faces, uniformly in the distinct positive radii and invertible
polar deformation. Their distance is exactly computable from the weights.
The earlier ten isometric faces leave this much larger positive boundary
uncontrolled. Five retained failed-search packets are audited exactly.

We then consume the geometric lane's quantitative hinge theorem to obtain a
rigorous necessary condition for an actual negative hinge near any such
face, including an explicit uniform exclusion region. No Gaussian quadrature,
new integration engine, new positive geometric class, or independent
acceptance of a teammate's analytic theorem is claimed.

Write $\phi_{n,s}(z)=C_n\exp(-|z|^2/(2s))$, $C_n=(2\pi s)^{-n/2}$,
and $H_f(a)=\int(f-a)_+$. All measures have mass one; $s>0$.

## 1. The quantitative core margin is a prior team result

For a bounded core law $\mu_0$ and contraction $T$, put
$f_0=\mu_0*\phi_{3,s}$, $g_0=T_\#\mu_0*\phi_{3,s}$ and

$$
D=\mathbb E[|X-X'|^2-|TX-TX'|^2],\qquad X,X'\text{ independent with law }\mu_0.
$$

Suppose the paired support has affine rank at most five. The established
[paired-rank reduction](../gaussian_majorisation_rank_abel/PROOF.md) supplies
a continuous contraction in $\mathbb R^5$, up to endpoint congruences:
if $v=(x-x_*,Tx-Tx_*)$ and $A,B$ are the two projection Gram operators,
use $c_t=((1-t)A+tB)^{1/2}v$. Its pair distances squared interpolate
linearly between the endpoint values. This is a known positive class.

Choose an anchor $x_*$ in the source support and
$R_a\ge\sup_x|x-x_*|$. Let $0<m\le\|f_0\|_\infty$ be a certified source
peak lower bound, for example any one source density evaluation.
**Theorem H of the geometric lane**, not a theorem first proved here, states
for $0<h<m$ that

$$
H_{g_0}(h)-H_{f_0}(h)\ge\kappa(R_a,s,m,h)D/s,
\tag{1}
$$

where

$$
\kappa(R_a,s,m,h)=\frac{e^{5/2}}{96\sqrt{2\pi}}
\left(\frac{m-h}{C_3}\right)^4
\exp\left[-\left(\frac{2R_a}{\sqrt s}
+\sqrt{2\log\frac{2C_3}{h}}\right)^2\right].
\tag{2}
$$

Its proof and precise path assumptions are in
[`gaussian_axial_cone_rotations/HINGE_MARGIN.md`](../gaussian_axial_cone_rotations/HINGE_MARGIN.md),
commit `005444cfb98c1944486cdbf3b87f865c17c9da41`.
It uses the pressure identity from
[Aishwarya--Li, equation (66)](https://arxiv.org/html/2609.07041v2)
and a radial shell bound. Continuity of the motion suffices; no generic
rectifiable Gram lift or regular-level assumption is needed.
This author theorem is an explicit analytic premise of our exclusion rule.

## 2. The negative-hinge exclusion rule

Let $f_1,g_1$ be any probability densities and put
$f=qf_0+\varepsilon f_1$, $g=qg_0+\varepsilon g_1$,
where $0\le\varepsilon<1$ and $q=1-\varepsilon$.
In the application all four densities are Gaussian convolutions. No
restriction on the remainder's atom count or support extent is required.

**Lemma 1 (one-sided residual-mass budget).** For every $a>0$,

$$
H_g(a)-H_f(a)\ge q[H_{g_0}(a/q)-H_{f_0}(a/q)]-\varepsilon.
\tag{3}
$$

Indeed, $H_g(a)\ge qH_{g_0}(a/q)$ by pointwise monotonicity. The inequality
$(x+y-a)_+\le(x-a)_++y$ for $y\ge0$ gives
$H_f(a)\le qH_{f_0}(a/q)+\varepsilon$. Subtract them.

**Corollary 2 (necessary condition for a negative hinge).** Under the core
hypotheses above and $0<a/q<m$,

$$
H_g(a)-H_f(a)\ge q\kappa(R_a,s,m,a/q)D/s-\varepsilon.
\tag{4}
$$

Thus a negative hinge requires
$\varepsilon>q\kappa(R_a,s,m,a/q)D/s$.
This is a threshold-specific exclusion, not full majorisation under
arbitrary contamination. Its margin degenerates at small thresholds,
small distance loss, or near the certified source peak.

For a finite paired configuration, take any rank-five support face $F$,
let $q$ be its total weight and normalize the weights in $F$.
Compute $R_a,D,m$ for this conditional core. Every face gives one lower
bound (4); their maximum is valid. A common isometry on the face is
unnecessary. This uses the core margin directly and does not duplicate the
finite lane's integration or moment-certificate production.

**Corollary 3 (uniform exact exclusion region).** Suppose the centered source
core is supported in $B(0,R)$ with $R\le\sqrt s/4$, its paired affine rank
is at most five, and $D\ge s/16$. If $\varepsilon\le10^{-9}$ and
$a=qC_3u$ for $1/8\le u\le1/4$, then

$$
H_g(a)-H_f(a)>10^{-9}.
\tag{5}
$$

The remainder laws may be arbitrary. This excludes a continuum of actual
hinges uniformly over their support diameters and cardinalities, including
remote contamination for which a full-support high-noise bound would not
apply. The region is nonempty: a core with equal masses at
$\pm(\sqrt s/4)e_1$, mapped to zero, has $D=s/8$.

For an exact check, an anchor in the core gives $R_a\le2R\le\sqrt s/2$,
and evaluating its source density at zero gives
$m\ge C_3e^{-1/32}>31C_3/32$. Hence $(m-a/q)/C_3>23/32$.
Since $\log2<7/10$,

$$
\left(\frac{2R_a}{\sqrt s}+\sqrt{2\log(2/u)}\right)^2
< (1+12/5)^2=289/25<12.
$$

Also $e^{5/2}/\sqrt{2\pi}>4$, since $e>8/3$, $\pi<22/7$, and
$(8/3)^5>32(22/7)$. Therefore (1) gives the uniform core margin

$$
H_{g_0}(C_3u)-H_{f_0}(C_3u)
>\frac1{384}\left(\frac{23}{32}\right)^4
\left(\frac4{11}\right)^{12}
=\frac{279841}{75322281041304}.
\tag{6}
$$

Here $e<11/4$ follows from its Taylor sum through degree four, $65/24$,
and tail bound $1/100$; $\log2<7/10$ follows from the cubic lower bound
for $e^{7/10}$. All remaining comparisons are rational. Finally
$(1-10^{-9})279841/75322281041304-10^{-9}>10^{-9}$.
The exact program checks these inequalities. It does not mechanize
Theorem H or claim that any historical packet lies in this exclusion box.

## 3. All 208 rank-five faces of the two-scale polar family

Take distinct positive $r_0,r_1$ and any invertible real $3\times3$ matrix
$M$. Let

$$
\begin{split}
\alpha&=((1,0,1),(0,1,1),(-1,0,1),(0,-1,1)),\\
\beta&=((1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1)),\\
a_{ik}&=r_kM\alpha_i,\qquad b_{jk}=r_kM^{-T}\beta_j.
\end{split}
$$

The input consists of the eight $a_{ik}$ sites and eight $-b_{jk}$ sites,
with $T(a_{ik})=a_{ik}$ and $T(-b_{jk})=b_{jk}$. This is a contraction: the
within-cloud distances are unchanged, and a cross squared-distance loss
is $4r_kr_l\alpha_i\cdot\beta_j\ge0$.
Labels 0--7 are A sites (scale zero then scale one); labels 8--15 are B
sites in the same order. A mask has bit $i$ set exactly when label $i$ is
in the support. A face here means a **weight-simplex support face**, not a
face of the Euclidean convex hull.

**Theorem 4.** The maximal supports of paired affine rank at most five are
exactly 208 masks, independent of $M,r_0,r_1$ under the stated assumptions.
Their sizes are

| Support size | Number |
| --- | ---: |
| 6 | 64 |
| 7 | 96 |
| 8 | 36 |
| 12 | 12 |

**Proof.** The invertible paired-coordinate map
$(x,y)\mapsto(M^{-1}(x+y)/2,M^T(y-x)/2)$ sends the sites to
$(r_k\alpha_i,0)$ and $(0,r_k\beta_j)$. A proper affine hyperplane thus
has equations

$$
u\cdot r_k\alpha_i=c\quad\hbox{on its A sites},\qquad
v\cdot r_k\beta_j=c\quad\hbox{on its B sites}.
\tag{7}
$$

Every three distinct rays in either cloud are linearly independent. If
$c=0$ and $u=0$, all eight A sites and at most two B rays (at both scales)
are possible; these give six maximal supports of size 12. The opposite
case gives six more. If both normals are nonzero, the support is contained
in one of these twelve. Each maximal support just described has affine
rank five, since the full cloud affinely spans its three-dimensional block
and the two other rays span a two-dimensional subspace.

For $c\ne0$, normalize $c=1$. A hyperplane contains at most one scale of
each ray. Write $p=1/r_0$, $q=1/r_1$, so $p\ne q$. A maximal single-cloud
section contains at least three rays: any constraints on fewer rays extend
to three because every triple is independent. Both clouds obey
$v_0+v_2=v_1+v_3$. Choose three rays and assign each scalar product either
$p$ or $q$. The missing scalar product is of the form
$jp+(1-j)q$ with $j\in\{-1,0,1,2\}$. It equals one of $p,q$ only for
$j=1,0$, respectively, for **every** pair $p\ne q$.

There are six four-ray sections: all $p$, all $q$, and the four assignments
having one $p$ and one $q$ on each opposite pair. The other sections are
eight triples, two for each missing ray. Hence there are 14 maximal
sections in either block. The nonzero-offset faces are their independent
products, giving $14^2=196$ supports: $8^2$ of size six, $2\cdot8\cdot6$
of size seven, and $6^2$ of size eight. Each has affine rank five: its two
single-cloud affine planes have dimension two, and their join adds one
dimension. None is contained in a zero-offset face, since it uses at least
three rays in each cloud. This proves maximality and completeness.

The symbolic producer computes the 14 sections using formal coefficients
of $p,q$. Separately, `check_matroid.py` enumerates every six-row subset of
the affine matrix at $M=I,r_0=1,r_1=2$, using the rows $[1,a,0]$ and
$[1,0,b]$. It computes hyperplane closures over the prime 65537.
Each row has squared norm at most 13, so every six-row minor has absolute
value at most $13^3$ and every seven-row determinant is less than
$13^4<65537$. Hadamard's inequality therefore makes the finite-field rank
and closure tests exact over the rationals. Every maximal rank-five
support has six independent affine rows; lower-rank supports can be
extended since the whole affine matrix has rank seven. Enumeration of all
8008 six-subsets finds 5344 independent ones and exactly the 208 certified
masks, compared entry by entry. This is an independent finite-instance
check; universality in the radii follows from the proof above.

## 4. Search boundaries and an exact missed-degeneracy family

For weights $w$ on the 16 labels define

$$
\delta_5(w)=\min_{F\text{ among the 208 faces}}\sum_{i\notin F}w_i.
\tag{8}
$$

This is exactly the total-variation distance to the union of all positive
paired-rank-five support faces. Conditioning on a face attains its missing
mass as TV distance, and every law supported on that face is at least that
far away. Thus $\delta_5\ge\eta$ is a system of 208 linear constraints.

The maximum possible reserve is exactly $1/4$, attained by uniform weights.
Indeed, the two heaviest B rays carry at least half the B mass. The face
containing all A and those two B rays has missing mass at most half the B
mass. Reverse A and B to get
$\delta_5\le\min(w(A),w(B))/2\le1/4$.

The ten isometric faces from the imported minimax certificate, lifted to
both scales, are each contained in a rank-five face. Their reserve
$\delta_{\rm iso}$ therefore satisfies $\delta_5\le\delta_{\rm iso}$.
It supplies no positive lower bound on $\delta_5$, even with both scales
well populated. An exact example makes this failure quantitative.

Give each A label mass $1/16$, each B0/B1 label at both scales mass $1/8$,
and the other four B labels zero mass; call this $w^0$. Mix with the
uniform law: $w^\varepsilon=(1-\varepsilon)w^0+\varepsilon(1/16,\ldots,1/16)$.
Direct face comparison gives

$$
\delta_5(w^\varepsilon)=\varepsilon/4\quad(0\le\varepsilon\le1),
\qquad
\delta_{\rm iso}(w^\varepsilon)=3/8+\varepsilon/4
\quad(0\le\varepsilon\le1/2).
\tag{9}
$$

To verify these whole intervals, each missing mass is affine in
$\varepsilon$; the stated minimizing faces beat every other face at both
endpoints. The exact checker compares these endpoints against all masks.
Both scales always have mass $1/2$. At $\varepsilon=1/1000$, every label
has mass at least $1/16000$, the isometric reserve is $1501/4000$, and the
rank-five reserve is only $1/4000$. This family is not a Gaussian
counterexample. It explains why isometric-face and scale reserves alone
do not remove a large, already positive boundary of the actual search.

For future candidate exclusion, use each conditional face core in (4).
A reserve such as (8) is an exploration constraint, not itself a
positivity certificate. A candidate with small $\delta_5$ still needs the
explicit comparison between its missing mass and its core margin. No sign
for a historical numerical candidate is inferred merely from proximity.

## 5. Dependencies, attribution and scope

The [paired-rank result](../gaussian_majorisation_rank_abel/PROOF.md), commit
`f7c122d6a5ade217930d63da27e67f9a9e55a539`, supplies qualitative positivity
of every classified face. Theorem H, explicitly cited in Section 1, supplies
the quantitative margin. Both are prior team results. The single-residual
error in (3) is elementary; the new concrete application is its use over the
complete 208-face boundary, with exact uniform constants and search audits.

The imported ten-face certificate is
[`gaussian_majorisation_minimax_faces/CERTIFICATE.json`](../gaussian_majorisation_minimax_faces/CERTIFICATE.json),
commit `e53ad777d2aaa0556e646d4db44a2afc7235c7d0`, SHA-256
`702790f3ca82a3dfaf28ea0248536b125ab346b99388311ea6827924fc53486d`.
Its equality-face classification is used, not reimplemented. The
[spatial localization handoff](../gaussian_prior_localization/DEFECT_LOCALIZATION.md)
motivates keeping residual mass arbitrary; no localization theorem is needed
as a mathematical premise here.

The contribution does not settle rank six, yield a new full
Kneser--Poulsen class, or certify a previous floating-point candidate's sign.
No novelty for the core margin or priority beyond the checked sources is
claimed. The exact programs check
symbolic sections, rational constants, all certificate masks, and compact
historical packets. The universal geometric classification and the external
analytic margin remain unformalized mathematics. External review is pending.
