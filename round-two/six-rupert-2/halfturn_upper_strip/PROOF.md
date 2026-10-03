# J74: a nonlinear collar exclusion above the half-turn receiving edge

six-rupert-2, actual role **researcher**, 2026-10-03. This is a complete
ordinary conditional local proof, supported by exact finite polynomial and
geometric checks. Author checked, unformalized and independently
**UNREVIEWED**. The global standard Rupert property of J74 remains **OPEN**.

The new step is a finite two-dimensional receiving region above a known
edge. Ten exact positive contact duals control source and translation
together; a separate dual and all nonlinear Cayley remainders exclude
upward receiving motion. Translation is never assumed zero. An earlier
equal-opposite-width extension failed because this solid is asymmetric;
the present proof instead uses actual original receiving supports.

## Original solid and precise conditional statement

Let K be the convex hull of the sixty ordered unit-edge original J74
vertices in [model8551](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/model.py).
Its source is 25fc9695745b6832d068d18544452b7852b5847f and graph reference
is bafkreig4wvsmlau4koaib63i3cefofih67cczseu3hgdv2r6r54ga572aq.
The model is identified by two NONOPPOSITE cupola gyrations. Its
[ordered field](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/q5.py)
is public7140 arithmetic **code only**, not a J77 mathematical premise.

Put s=sqrt(5)>0, a=(s-1)/4, b=(s+1)/4, t=(3-s)/2, and

$$G=\begin{pmatrix}a&-1/2&-b\\-1/2&-b&a\\-b&a&-1/2\end{pmatrix},\qquad
H=\operatorname{diag}(-1,-1,1),\qquad M_y=\operatorname{diag}(1,-1,1).$$

G is an ORIGINAL proper absolute half-turn. H is an actual proper body
symmetry; M_y is an actual improper body symmetry. All sixty original
permutations, properness and the cupola identification are rebuilt.

Define the entirely CLOSED receiving rectangle by

$$x_0=(-5+4s)/11,\quad |\xi|\le\delta_x=1/1000,\qquad
0\le\eta\le\delta_y=1/100000,$$
$$r=(x_0+\xi,1,-t-\eta),\qquad n=\pm r/\|r\|.$$

Write P_r=I-rr^T/(r.r), M_r=I-2rr^T/(r.r), J_r(Q)=M_r Q M_y,
and interpret the following as a SET:

$$E(r)=\{G,GH,J_r(G),J_r(GH)\}.$$

**Conditional upper-strip lemma.** For EVERY receiver in this closed
rectangle, EVERY original Q in SO(3), EVERY physical T in r-perp and
EVERY lambda>=1, assume

$$\operatorname{tr}(Qe^T)\ge2999999/1000001
\quad\text{for SOME }e\in E(r).\tag{1}$$

Then

$$\lambda P_r(QK)+T\subseteq P_r K
\quad\Longleftrightarrow\quad
\eta=0,\quad\lambda=1,\quad T=0,\quad Q\in E(r).\tag{2}$$

Gate (1) is the CLOSED physical relative Cayley radius rho=1/1000,
equivalently squared Frobenius distance 8/1000001. It is an explicit
hypothesis: there is no arbitrary-source entry theorem outside these
collars. This rectangle covers a subsegment of the old top edge and a
small region above it; it does not cover the whole two-dimensional
receiving complement. Boundary fits touch supports and are not strict
Rupert passages. No cardinality or mirror-as-proper-source assertion is
needed for E(r).

The standard strict projection convention and the unresolved Johnson
list are in [Zeng, section1.2](https://arxiv.org/html/2604.26531#S1.SS2)
and [Gosain--Grimmer, Table4](https://arxiv.org/html/2509.08190#S3.T4).
A scoped conditional exclusion does not settle the global named-solid
problem.

## Unit reduction with the original translation retained

The actual original pairs V0/V7, V1/V6 and V2/V5 are antipodal, and
det(V0,V1,V2) is nonzero. Their octahedron puts the origin INTERIOR to K;
this uses three pairs, not whole-body centrality. For lambda>=1,
convexity therefore gives K subset lambda K. Any assumed fit in (2)
implies the unit-scale fit

$$P_r(QK)+T\subseteq P_rK\tag{3}$$

with the SAME original physical T. We prove necessity from (3), and
restore scale at the end. This is not a centering or scale-one premise.

First take Q in the physical rho collar of G. Write Q=R(c)G, with

$$\|c\|_2\le\rho,\quad N=1+c.c>0,\quad
R(c)=\frac{(1-c.c)I+2cc^T+2[c]_\times}{N}.\tag{4}$$

The gate excludes relative angle pi, so this Cayley coordinate exists.
Its trace is 3-4(c.c)/(1+c.c); this proves equivalence with (1).
All free THREE-variable orthogonality, determinant, trace and Cayley
inverse identities are checked, including the positive cleared
determinant of R+I.

Let x=x0+xi and y=t+eta. Every original physical T can be represented
by the lift L=(T_x-x T_y,0,T_z+y T_y), because T-L=T_y r, so P_r L=T.
All three identities are checked with five free variables. Introduce
the completely UNRESTRICTED translation variables

$$\tau_x=N(T_x-xT_y),\qquad \tau_z=N(T_z+yT_y),\qquad
d=(c_x,c_y,c_z,\tau_x,\tau_z).\tag{5}$$

The factor N avoids a spurious quadratic-times-translation term after
clearing the actual source rotation denominator. No initial bound on
tau, L or T is assumed.

## Actual original receiving supports and contact polynomials

For each receiving edge i->j listed in [certificate.json](certificate.json),
set

$$e_i=V_j-V_i,\quad n_i(r)=r\times e_i,\quad
h_i(r)=n_i(r).V_i.$$

There are eighteen selected edges. For EACH of the four original CLOSED
rectangle corners the checker verifies h_i>0 and

$$h_i(r)-n_i(r).V_k\ge0\quad\text{for ALL sixty originals}.\tag{6}$$

These are affine in xi and eta. The 4320 endpoint controls prove (6)
over the entire rectangle by convex interpolation. They are actual
receiving supporting halfspaces, not inherited symmetric heights.
Only necessity from these selected supports is used; a complete hull
classification or exhaustive source enumeration is unnecessary.

Let W_k=G V_k. The packet has thirty-seven actual zero contacts of the
selected supports at (xi,eta)=(0,0). These are rebuilt from all sixty
originals, with no assumed spatial preimage for each receiving corner.
All receiving-only coefficients vanish for these contacts throughout
eta=0; the full polynomials check this fact, not just the center sample.

For each packet row, the fitted unit source must satisfy

$$f_i=N h_i-n_i.R_{\rm num}(c)W_k
      -n_i.(\tau_x,0,\tau_z)\ge0.\tag{7}$$

The complete polynomials belong to Q(s)[xi,eta,c_x,c_y,c_z,tau_x,tau_z].
Let n_i^0=n_i(r0), n_i^1=(0,0,-1) cross e_i at r0=(x0,1,-t). Define

$$A_i=(2(W_k\times n_i^0)_x,2(W_k\times n_i^0)_y,
2(W_k\times n_i^0)_z,(n_i^0)_x,(n_i^0)_z),$$
$$b_i=n_i^1.(V_i-W_k).$$

The checker constructs EVERY coefficient of

$$f_i=b_i\eta-A_i.d+q_i.\tag{8}$$

The only possible monomials of q_i are: two source c coordinates;
xi times ONE d coordinate; eta times ONE d coordinate; xi times two
c coordinates; or eta times two c coordinates. Any other type is an
error. There are no unaccounted constant, receiving-only or linear
source/translation terms. Four exact fixtures, including large
unrestricted translation and one rotation outside the collar, compare
all thirty-seven full polynomials to both direct ORIGINAL spatial
constraints and independent quotient-plane determinants: 148 triple
comparisons. The fixtures check algebra; they are not the continuum
argument.

## Ten signed duals control all original source and translation variables

The compact packet supplies ten vectors nu^(k,sign)>=0 satisfying

$$\sum_i\nu_i A_i=\operatorname{sign}e_k
\quad(k=0,\ldots,4;\ \operatorname{sign}=\pm1).\tag{9}$$

Every weight and all FIFTY original coefficient identities are checked
from (8). Put beta_nu=sum nu_i b_i and q_nu=sum nu_i q_i. Equation (7)
implies

$$\operatorname{sign}d_k\le\beta_\nu\eta+q_\nu.\tag{10}$$

For each q_nu the checker sums ABSOLUTE exact coefficients separately
for the five monomial types in (8). Call these nonnegative sums
C2, Cx, Cy, Cx2 and Cy2. With

$$D=\max(|c_x|,|c_y|,|c_z|,|\tau_x|,|\tau_z|),$$

each two-c monomial is bounded by rho D, each xi-d by delta_x D,
each eta-d by delta_y D, and the two cubic types by delta_x rho D
or delta_y rho D. This remains true however large translation is.
Consequently |q_nu|<=B_nu D, where

$$B_\nu=C2\rho+Cx\delta_x+Cy\delta_y
       +Cx2\delta_x\rho+Cy2\delta_y\rho.$$

The exact maximal B and maximal nonnegative receiving coefficient are

$$B=18946199/232000000+(3500537/725000000)s<1/2,$$
$$M=\max(0,\beta_\nu)=s-3/2>0,\qquad K=2M=2s-3.$$

Because eta>=0, (10) for all ten signs gives

$$D\le M\eta+B D,\qquad\text{hence }D\le K\eta.\tag{11}$$

In particular eta=0 forces c=0 and tau=0, hence Q=G and ORIGINAL T=0.
The coercivity bound is a conclusion about the unrestricted translation,
not an assumption about it.

## A separate dual excludes every positive eta in the closed strip

The six-contact separating packet has nonnegative weights mu satisfying

$$\sum_i\mu_i A_i=0,\qquad
\beta:=\sum_i\mu_i b_i=-1179/50996-(11619/254980)s<0.\tag{12}$$

Its original source AND translation coefficients are checked separately;
the positive normalization sum mu_i h_i(r0)=1 merely fixes these weights.
It is not a unit-scale premise. From (7),

$$0\le\sum_i\mu_i f_i=\beta\eta+q_\mu.\tag{13}$$

Let C2,Cx,Cy,Cx2,Cy2 now be the five exact absolute-coefficient sums of
q_mu, and put C2eff=C2+delta_x Cx2+delta_y Cy2. Each two-c monomial is
bounded by D^2; xi-d by delta_x D; eta-d by eta D. Thus

$$q_\mu\le C2eff D^2+Cx\delta_x D+Cy\eta D.$$

Using (11) and eta<=delta_y gives

$$\beta\eta+q_\mu\le\eta E,$$
$$E=\beta+Cx\delta_x K+(C2eff K^2+Cy K)\delta_y$$
$$=-2049114251323/101992000000000
 -(117795565452007/2549800000000000)s<0.\tag{14}$$

ALL coefficient sums and the strict finite inequalities B<1/2 and E<0
are checked exactly. If eta>0, (13)-(14) contradict each other. This
finite nonlinear absorption is essential; a negative linear-program
derivative on its own would not prove the statement.

## Actual companion transport, scale closure and boundary sufficiency

J_r(Q)=M_r Q M_y is an involution on original proper sources, a Frobenius
isometry, and commutes with right multiplication by H. Since M_y K=K
and P_r M_r=P_r, it preserves the entire projected source SET with the
SAME original physical T and lambda. The checker verifies free
two-variable reflection, determinant and projection-preservation
identities; actual body permutations were checked in (6)'s geometry.
Right H also preserves source shadows. These operations transport any
collar in E(r) to the G collar, and the preceding argument applies
without changing the receiving rectangle or translation.

It follows that any assumed fit has eta=0, T=0 and Q in E(r).
At eta=0 let U=(0,t,1). Its actual positive receiving and fixed-G source
height is h=(7+s)/4>0, checked on all originals, and U.r=0. All E(r)
shadows equal the G shadow. Restoring the original lambda in the fit
requires lambda h<=h, so lambda=1.

Conversely, the boundary interval x0+-1/1000 lies strictly inside
[ell,qx], ell=(5s-9)/22, qx=(s-1)/2. The explicit prior
[fixed-G component9961](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/fixed_halfturn_component/PROOF.md),
source65f19129ef6a14e7c31e07ee3cb81c3f63707eca,
graphbafkreicf4uiglabu2wi2rpbutlucr5babhngbu643cmzd6i3yty2nyglg4,
supplies unit-scale/T0 fixed-G feasibility throughout that old edge.
The same actual body/receiving actions supply all E(r) fits. This prior
boundary sufficiency is a mathematical dependency; its large original
ray/width computation is NOT newly replayed or imported here. This
proves both directions of (2), including every closed boundary.

## Reproduction, prior scope and trust boundary

The final checker needs only model8551 and arithmetic7140 as two small
public before-import hash-pinned runtime files. Its selected supports,
literal duals and seven-variable polynomials are all new evidence for
this receiving strip. The exact private simplex used to discover the
duals is NOT a final input, solver-soundness premise or nonlinear proof.
No source forest, earlier local constant, old receiving-width tree,
failed prototype or floating generator is an input. Reproduction
commands and full mathematical record are in [README.md](README.md)
and [expected.json](expected.json).

The prior [whole top-edge collar10016](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/halfturn_branch_collar/PROOF.md)
proved radius1/8 around the full companion set on the ENTIRE old edge,
including its endpoint merger. It did not prove a receiving strip.
The present collar is smaller and its edge interval is narrower, so no
GENERALIZES or global resolution claim is made. Small geometry helpers
are adapted from9961/10016; sparse coefficient primitives are adapted
from the public [9584 ring](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/three_cube_cover/poly.py)
via10016 as code credit only. No old contact stencil or source forest
is transferred.

Normal and optimized full records, fresh minimal relocated replays,
resource measurements and false mathematical fixtures are reported in
[VALIDATION.json](VALIDATION.json) and [controls.py](controls.py). The
ordinary convexity/unit reduction, Cayley coordinate existence,
positive-combination inequalities, monomial domination and original
companion-action arguments above are part of the proof. Exact matching
author runs do not supply formalization or independent review. This
does not prove source entry outside (1) or global non-Rupertness of J74.
