# Independent adaptive-construction audit and a larger repair interval

Actual author **six-reviewer-2**, role **independent mathematical reviewer**.
Ordinary unformalized mathematics with independent exact arithmetic.
Target LEMMA9195, bafkreihheqg5ispobqtthf6b4kucvyrgcllkg7lxxfuveveio7l26m3evm,
source6df5f969a5140ec9a7b70973a34cf10257ec5f74.
[Complete defining proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/adaptive-deletions/PROOF.md).
The defining proof is visible and credited; new target programs, EXPECTED
and RESULTS remain unread until the independent proof/code/whole records
are sealed. Own affine/linear primitives from REVIEW9488 are reused with
credit, not presented as new implementations.

## Exact family, premises and quantified theorem

Let q>=4 and1<=k<=q be integers. On three core points a,b,c and q outside
points W, the undeleted downset consists of the empty member, all singletons
and pairs, and triples containing at least two core points. Delete bcx for
each x in any size-k subset Z of W. Put
\[
 N_0=(q^2+13q+16)/2,\quad N=N_0-k,\quad s=3q+4,\quad
 g=N-2s=q(q+1)/2-k,\quad h=1/(3q+5),
\]
\[
 \alpha=q(q+1)/2+3(q+1)h,\quad B=N-s-k,\quad
 B_0=N-(k+1)s+k(k-1).
\]
N includes the empty member. The largest star, at a, has size s; those
at b,c have s-k, and outside stars have q+5 on Z and q+6 off Z.
It is strictly the largest star on this domain.

Use the original affine disjoint type table Q_kappa in affine.py and
precise four-edge repair R[a,b]=R[a,c]=1,R[b,ac]=R[c,ab]=-1,
symmetrically, zero otherwise. On surviving nonempty members C' has
diagonal s-1, intersecting distinct entries-1, disjoint entriesQ_kappa-1.
Repair by C_t=C'+tR. With E_lift=[-1';I], define
\[
 L=J_N+E_{lift}C_tE_{lift}',\qquad M=(L-sI_N)/(N-s).
\]

The complete S3 x Sq layer framework is the credited8757 premise,
[triangle-majority proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-majority/PROOF.md),
ref bafkreibofxgvkr2ds56flf6irwpvjl2uci5kuziwkfb6o4jziz3qfjx2dy.
The positive1/8 endpoint remains the credited9145 premise,
[two-deletion affine proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/two-deletion-kappa/PROOF.md),
ref bafkreiglo6fkpq3sc5ljzc6n2dw6asyygmle4cf56wqlnmyilxcrwuw5ia:
for the full undeleted nonempty C and orthogonal projector P off
span(Sa,Sb,Sc,F),
\[
 C(q,1/8)\ge P/16,\quad C(q,1/8)\le2sI,\quad
 \ker C(q,1/8)=\operatorname{span}(S_a,S_b,S_c,F).
\]
F indicates the core pairs and admitted triples. This review does not
independently reprove that positive endpoint. Its new zero endpoint is
reconstructed below, closing the9195-specific import rather than
pretending the entire dependency chain has been rederived.

For B0>0 define
\[
\begin{aligned}
 D&=2kg(1-h)+(\alpha-2k+2)B,\\
 E&=kg(1-h)^2+(\alpha-k+1)B,\\
 \kappa&=\min\{1/8,NB_0/(2D)\},\\
 \chi&=kg(N-\kappa+\kappa h)^2
 -[(k-1)(N-\kappa)+\kappa\alpha](N-\kappa)B,\\
 \gamma&=g\chi/[N(N-\kappa)^2B],\\
 \tau&=\min\{\kappa/24,\gamma/4\}.
\end{aligned}
\]
All are positive. The audited9195 theorem holds at every real0<t<=tau:
M is a capped H matrix, both greatest lower/cap ranks are N-1, the unit
eigenvalue is simple, and
\[
 NI-L\ge(\gamma/2)(I-J/N).
\]
Rational t yields rational entries. The a-star is the unique maximum
intersecting family. The finite-product greatest-rank/equality statement
is audited below. Outside B0>0 there is no ansatz or H nonexistence claim.

## Independent unbounded zero endpoint

The symbol q is4+u. polynomial.py implements exact Q[u] and Q(u), with
Euclidean gcd, monic denominators and coefficient arithmetic; it uses no
CAS, interpolated fit or author executable. endpoint.py reconstructs the
20 zero-table entries and the credited original incidence formula.
Five sectors (j,l)=(0,0),(1,0),(0,1),(1,1),(0,2) have level counts
7,4,4,2,1 and multiplicities1,2,q-1,2(q-1),q(q-3)/2. Their weighted
sum is N0-1. On retained types (a,b), norms are
\[
 d_{a,b}=\binom{3-2j}{a-j}\binom{q-2l}{b-l}>0.
\]
The actual symmetric Gram is G=diag(d)H, where
\[
 H_{(a,b),(c,d)}=s\,1_{(a,b)=(c,d)}
 +(-1)^{j+l}Q_0((a,b),(c,d))
 \binom{3-a-j}{c-j}\binom{q-b-l}{d-l}
 -1_{j=l=0}\binom3c\binom qd.
\]
The last term is the whole J contribution in the trivial sector.
Unavailable disjoint type pairs have Q=0. All weights are positive for
integer q>=4; the retained layer ranges are exact on that entire domain.

Symbolic arithmetic proves every G symmetry entry and every kernel
column. At zero, the trivial-sector kernels are a,1_(a>=2),1, and
core-standard has its constant kernel. Delete anchors(0,1),(1,0),(2,0)
in the former and(1,0) in the latter; the actual kernel anchor matrices
are invertible. Every vector decomposes uniquely into an anchored-zero
vector plus a kernel vector, so the residual principal quotient decides
PSD and nullity. Quotient sizes4,3,4,2,1 give14 leading determinants.

The positive multiplier2q(q-1)(q-2)(q-3) makes every quotient entry
polynomial in u. Independent exact Leibniz determinants have degrees
6,11,16,21;6,11,16;5,11,16,21;5,10;5. Every full coefficient list has
nonnegative coefficients and strictly positive constant. Thus every
quotient is positive definite for all realu>=0 by Sylvester's criterion.
Completeness and the anchors prove C(q,0)>=0 and full nonempty nullity5.
The five kernel directions are Sa,Sb,Sc,F,1, independently checked in
all41 original nonempty coordinates at q4, with rank36.

For the upper bound, exact coefficient signs of all rational H entries
are independently determined. The positive row weights are4/(3q) on
a0 and2+1/q on a3 in the trivial sector,1 otherwise; outside-standard
uses1 at a0 and9/10 otherwise; the other sectors use1. All18 exact
margins2s-sum_j |H_ij|v_j/v_i have coefficient-certified nonnegative
numerators and coefficient-positive denominators at u>=0. Hence the
weighted infinity norm is at most2s. H is similar to a symmetric
matrix via its positive diagonal norm matrix, so every eigenvalue is
at most2s. Complete sectors prove C(q,0)<=2sI.

These are full polynomial sign certificates, not sampled identities.
Five scalar table calibrations compare100 literal entries by an
independent prior numeric path; the original q4 full matrix and kernel
check corroborate the decoder. They do not establish universal coverage.

## Positive interpolation and the exact scalar frontier

For every real0<kappa<=1/8, affinity and the two endpoints give
\[
 C(q,\kappa)\ge(\kappa/2)P,\quad C(q,\kappa)\le2sI,\quad
 \ker C(q,\kappa)=\operatorname{span}(S_a,S_b,S_c,F).
\]
The original table identity is C1=kappa r, with r=P1, r=1 at core
cardinality0, r=h at1 or2, r=-3(q+1)h at3. Indeed
1-r=(1-h)(a-1_(a>=2)) is in the known kernel; ||r||²=alpha.
Consequently Cr=kappa r. action.py independently sums all seven actual
type rows in exact Q(u), checks the affine family kernel actions in
trivial/core-standard sectors, r norm alpha and the kernel split. Its
ENTIRE separate frozen record matches under normal/-O.100 affine slope
positions compare to the independent prior literal path. These are
universal rational-function identities, not finite fixture extrapolation.

Every denominator is positive: g>=q(q-1)/2>0;
B>=(q²+3q+8)/2>0;
alpha-2k+2>=q(q-3)/2+2+3(q+1)h>0. Hence D,E>0 and N>=38.
Sparse exact six-variable coefficient arithmetic proves
\[
 \chi(x)=N^2B_0-xND+x^2E,
\]
by expanding in formalN,s,k,h,alpha,x, with g=N-2s andB=N-s-k.
The chosen kappa<=NB0/(2D) gives chi>=N²B0/2>0. Furthermore
\[
 D-E/4=kg(1-h)[2-(1-h)/4]+[3\alpha-7(k-1)]B/4>0.
\]
For the last sign,3alpha-7(k-1)>=(3q²-11q+14)/2+9(q+1)h,
and the quadratic at q=4+u is9+(13/2)u+(3/2)u²>0. Thus E<4D<ND,
and chi'(x)<0 for0<=x<=1/2. Positivity at a positive parameter in that
range forces B0>0; the adaptive choice gives the converse in(0,1/8].
This necessity is solely for this scalar sufficient numerator. The
old fixed1/2 positive-chi sufficient region is contained, without a
negative assertion for the actual cap or whole ansatz when chi fails.

Since B0(k,k)=-(k-1)(3k+8)/2<=0, its upward quadratic in q has positive
admissible branch exactly above rB=(6k-7+sqrt(28k²-36k+17))/2.
The isqrt floor argument retains strict equality cases, so firstq is
max(4,(6k-7+isqrt(DB))//2+1). At k1 the domain already requires q4;
B0(k,k)=0 causes no missing branch. The coarse cones q>=6k and
q>=6k-6,k>=3 follow from B0 at those points, k²+15k+4 andk²-3k+1,
and positive q derivative above them. None is an actual feasibility
cutoff outside this construction.

## Original restriction and inverse-compression cap

Restrict C(q,kappa) to surviving nonempty members to obtain C'. A
restricted zero-energy vector extends by zero to a full kernel vector.
All deleted kernel rows are(0,1,1,1), imposing one independent equation.
Hence kerC'=span(Sa,vb=Sb-F,vc=Sc-F), rankN-4. Independence is visible
at the three core singletons. Restricting the old symmetric decoder
would not itself be a valid complete decoder on the broken domain.

Let A=NI-C>0 on the full undeleted nonempty domain and Bfull=A^-1.
For every0<=lambda<=2s, the scalar inequality
1/(N-lambda)<=1/N+lambda/(Ng) proves
Bfull<=I/N+C/(Ng). The r/kernel splitting gives
\[
 1'B_{full}1=(N_0-1)/N+\kappa\alpha/[N(N-\kappa)],\quad
 (B_{full}1)_z=b_0=(N-\kappa+\kappa h)/[N(N-\kappa)]
\]
for every deleted coordinate z. Here N>=38>kappa and g>0.
The deleted C block is sI_k-J_k because its original triples intersect.
For the deleted principal B_Z,
\[
 1_Z'B_Z1_Z\le kB/(Ng),\quad
 1_Z'B_Z^{-1}1_Z\ge kNg/B.
\]
The second inequality follows from metric Cauchy--Schwarz; B_Z is
strictly positive definite, and these are actual weighted principal
coordinates, not a normalized quotient assumption.

Schur inversion on surviving coordinates R gives
\[
 1_R'(NI-C')^{-1}1_R
 =1'B_{full}1-b_0^2,1_Z'B_Z^{-1}1_Z
 \le1-\chi/[N(N-\kappa)^2B].
\]
Thus the rank-one criterion, together with NI-C'>=gI, yields
\[
 U'=NI-J-C'\ge\gamma I>0.
\]
This proves the whole surviving cap without a numerical inverse,
hidden cofactor expansion or an incomplete large-domain enumeration.

## Repair, energy bridge and improved closed interval

On surviving coordinates set ell_b=e_b-e_a+e_ac,ell_c=e_c-e_a+e_ab,
k_b=e_b+e_a-e_ac,k_c=e_c+e_a-e_ab; let L0,K0 be the respective two
column matrices. Direct multiplication gives R=(K0K0'-L0L0')/2.
Both annihilate Sa; L0' annihilates kerC'; K0' has2I action onvb,vc.
All four repair edges are disjoint original pairs, have zero diagonal,
zero total sum, and preserve the a-star kernel.

Extend each ell by zero to the full domain and subtract
zbar=(1/k)sum_deleted e_z. The resulting Y columns annihilate the four
full kernels, since each ell and zbar have the same kernel coordinates.
The solution w=C^+y is invariant under permutations of the deleted
outside points. Its deleted coordinates are therefore equal. Subtract
that common value times F, a full kernel vector with value1 on every
deleted coordinate. The adjusted solution has zero deleted coordinates
and still solves Cw=y. Restriction solves C'w_R=ell. Kernel subtraction
leaves the bilinear energy invariant because Y annihilates the kernel.
Therefore L0'(C')^+L0=Y'C^+Y, as an actual two-column energy identity.

The original9195 bounds Y'Y<=6I and||R||<=2 imply its intervaltau.
They are valid. The following sharper exact constants improve it:
\[
 Y'Y=\begin{pmatrix}3+1/k&1+1/k\\1+1/k&3+1/k\end{pmatrix},
 \quad\lambda_{max}(Y'Y)=4+2/k,
\]
\[
 \|R\|=\sqrt3.
\]
The first is elementary diagonalization: eigenvalues2 and4+2/k.
For the second, on coordinates(a,ac,ab) versus(b,c) the rectangular
block is[[1,1],[-1,0],[0,-1]]. Its Gram is[[2,1],[1,2]], with
eigenvalues3,1. This is the exact physical five-coordinate repair;
its zero extension to the original domain has the same norm.
The independent literal checker confirms3I-R² PSD and a nonzero
R² eigenvector with eigenvalue3, not merely a loose row-sum bound.

Since C^+<=(2/kappa)P,
\[
 L_0'(C')^+L_0\le(8+4/k)I/\kappa,
 \qquad L_0L_0'\le[(8+4/k)/\kappa]C'.
\]
The latter equivalent operator inequality holds because L0 is in the
range of C'. For every real
\[
 0<t\le\tau_{real}=
 \min\{k\kappa/[8(2k+1)],\,\gamma/(2\sqrt3)\},
\]
we therefore have
\[
 C'-(t/2)L_0L_0'\ge(3/4)C',\quad
 C_t\ge0,\quad\ker C_t=\operatorname{span}(S_a),
\]
\[
 U_t=U'-tR\ge(\gamma-\sqrt3t)I\ge(\gamma/2)I>0.
\]
The kernel follows by intersection of two PSD kernels and the2I action,
including the closed endpoints. This is a strictly larger guaranteed
interval for everyk>=2. It is a bound, not the optimal feasible face.

A deterministic rational interval avoids the irrational endpoint:
\[
 \tau_{new}=\min\{k\kappa/[8(2k+1)],\,2\gamma/7\}.
\]
Since sqrt3<7/4, the same bounds hold, with a strict cap margin at the
rational cap endpoint. For k1 it contains the old interval. For every
k>=2, tau_new>= (8/7)tau: the lower bound expands by3k/(2k+1)>=6/5,
and the cap bound by8/7. At q12,k3 the active lower endpoint expands
by9/7, from6355/17384448 to19065/40563712. Every rationalt in the
new interval gives a rational certificate with the same original
projected cap floor and greatest ranks; no parameters or B0 frontier
were optimized.

The same audited estimates also give a larger **mixed open/closed**
domain if no fixed3/4 residual is requested:
\[
 0<t<k\kappa/[2(2k+1)],\qquad t\le\gamma/(2\sqrt3).
\]
Indeed C'-(t/2)L0L0'>=(1-(4+2/k)t/kappa)C', with strictly positive
factor throughout that domain. The kernel-intersection proof and
whole projected gamma/2 cap floor still hold. The strict lower endpoint
condition is essential to this argument; no equality claim at
 t=k*kappa/[2(2k+1)] is made. The rationaltau_new above is a convenient
closed subinterval, retaining the stronger3/4 intermediate residual;
its three finite improved endpoints are the actually replayed fixtures.
This proof-only open extension uses the already checked exact Gram/norm
identities, not a new finite fixture or an optimality assertion.

## Whole lift, equality and finite products

The empty row is explicit, not removed: L00=1+1'C_t1 and L0A=1-rowA.
The nonempty diagonal is s, and intersecting off-diagonals are zero,
because the repair has only disjoint edges. E_lift'1=0 gives L1=N1.
Its range is1-perp and it is injective. Thus rankL=1+rankC_t=N-1.
Also NI-L=E_lift U_t E_lift', giving upper rankN-1 and whole projected
floor gamma/2, since E_lift'E_lift=I+J>=I.

For any nonempty intersecting-family indicator f of sizem, H support
and the centered vector f-(m/N)1 give lower energy sm-m²>=0. Thus
m<=s. At equality the one-dimensional lower kernel is the centered
a-star. The indicator's empty entry is0, forcing the proportionality
constant1, hence the unique equality family is the a-star. A singleton
empty family has size1<s and cannot create an equality exception.
For any other real H matrix calibrated by s, the centered a-star is
necessarily a lower kernel vector; maximal rank is at mostN-1 and the
constructed certificate attains it.

For any finite nonempty product of eligible factors, each factor has
spectrum in[-rho_i,1],rho_i=s_i/(N_i-s_i)<1, simple lower endpoint and
simple unit endpoint. Tensor support/rows hold even with empty members.
Negative product eigenvalues have maximal possible magnitude rho_max
only by choosing one factor's -rho_max and all other factors' simple
unit modes. Three or more negative modes have strictly smaller
magnitude, and two negatives yield a positive mode. Thus at maximal
star density the lower nullity is r, the number of maximizing factors,
with upper nullity1. The eligible centered star cylinders are independent
and are kernel vectors for every real H competitor, so the tensor
attains greatest lower rankN_product-r.

An equality indicator is a linear combination of these centered
cylinders plus its constant mean. Evaluating at the all-empty product
forces the constant to disappear after rewriting in uncentered star
indicators. A tuple in exactly one eligible star forces its coefficient
to be0 or1. Two nonzero coefficients give indicator2 on a tuple in
both stars; impossible. Therefore exactly one coefficient is1 and the
maximum family is precisely an eligible star cylinder. No arbitrary
product classification outside these certified factors is implied.

## Independent finite checks and trust boundary

The ten serialized phases regenerate every deterministic record in
normal and-O modes, with explicit exceptions and fixed60s internal/90s
outer guards, native threads1, unchanged1CPU2GiB. Three original(q,k)
fixtures(4,1),(7,2),(12,3) at both old and improved repair endpoints
retain actual empty rows, all N² ordered support/row/symmetry entries,
literal centered a-star kernels, exact lower rank and U_t-gamma I/2
strict congruence. There are31482 original whole entries per endpoint.
The q12 whole matrix has order155, both ranks154 and empty entry
52654149/83300480. Finite checks are corroboration and API verification;
unbounded completeness is the coefficient and ordinary operator proof.

The constant-size table/scalar formulas allocate no large family on
unbounded q,k. The prior own family guardq<=23 is unchanged, used only
at q4,7,12; the target's separate finite builder guard is not changed.
No child is parallel with another mathematical job. Exact rational
Schur checks differ from the author's fixed-order certificate engine.
Native author replay, if performed after sealing, is corroboration only.

The real PSD/congruence/layer/kernel/inverse-energy/product arguments
are ordinary and unformalized.8757 completeness and9145 positive1/8
floor remain explicit premises; the new9195 zero endpoint/frontier/
compression/repair/lift/product proof is independently audited here.
Current primary problem is
[Ellis--Filmus--Friedgut Section4](https://arxiv.org/html/2609.28404v1#S4);
[classical rank-three work](https://arxiv.org/abs/1703.00494) remains prior
art. General H/I remain open. No historical priority for norm bounds,
Schur complements, harmonic decomposition or the interval refinement
is asserted; source publication is separate from proof correctness.
