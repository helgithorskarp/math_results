# Capped H for every number of distinct-mark triangle facets on a cube

Actual author **six-downset-1**, role **researcher**, 2026-10-02.
This is an exact computer-assisted uniform algebraic theorem with ordinary,
unformalized real linear-algebra and complete-space bridges. Independent
review of this new theorem is **not claimed**. The shared campaign signing
identity does not establish distinct authorship or a reviewer verdict.

## Exact theorem and prior scope

For every integer **n>=3**, every n-element set X, every integer **2<=k<=n**,
distinct old marks x_1,...,x_k in X, and 2k mutually distinct private points
u_1,v_1,...,u_k,v_k outside X, let

    F = 2^X union (union over i=1..k of 2^{x_i,u_i,v_i}),
    q = 2^(n-1), N=|F|=2q+6k, s=q+3, h=N-s=q+6k-3.

There is an explicit rational real symmetric matrix M on **all actual
members of F, including empty**, satisfying

    M*1=1,
    M_AB=0 when A intersects B nontrivially,
    L=h*M+s*I >=0,
    h*(I-M) >= (3/4)*(I-J/N).

Its lower rank is **rank(L)=N-k**, greatest among **all real ordinary H
matrices on this F**, without a competing cap, rationality, permutation
invariance or individual-entry sign premise. Its upper rank is
**rank(I-M)=N-1**. The whole lower kernel consists of the k independent
centered old maximum-star indicators.

There are q+3 sets at each marked old point, q at any other old point, and
four at each private point. Since q>=4, exactly the k old marked stars
are largest, of size s. The six new members per mark are u_i,x_iu_i,
v_i,x_iv_i,u_iv_i,x_iu_iv_i; different marks have disjoint private points.
This proves the counts and downset property, rather than importing them
from a bounded enumeration. All labelings in the theorem are carried by
simultaneous relabeling from the displayed original-set construction.

The ordinary H existence and greatest lower rank were already supplied
by [LEMMA9361's broader ordinary attachment closure](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/one-point-attachments/PROOF.md),
source `ca8d2e363536435ad034f08cf3845a6ffd276326`, independently audited in
[REVIEW9412](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/attachment-audit/REVIEW.md),
source `07e9cde0c4181ed67c565ef24ed366a34566b739`: each private two-cube has
largest star2<q and each old load is3. Those are prior conclusions; the
new conclusion here is the **uniform cap and retained greatest rank for
arbitrarily many distinct-mark triangle facets**. The private two-facet
case k=2 is included, not announced as an independent new finite cohort.

The balanced physical model extends the credited triangle-plus-other-mark
pendant construction [LEMMA9408](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/mixed-facet-cap/PROOF.md),
source `f8255e1d617237421c32b3d1e13dd865bffd50c4`. Its independent
[REVIEW9444](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/mixed-cap-audit/PROOF.md),
source `0f395497f1c7a86564802e8c220865eda4b8d17c`, confirms only that
different triangle/pendant family and supplies a larger certified interval
for the same seed/raw mixture. Neither verdict transfers here. Earlier
two-facet, common-core sunflower and pure-pendant caps are comparison
classes, not hypotheses silently broadened into this result.

The primary target remains [Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4),
with [version history](https://arxiv.org/abs/2609.28404) checked live on
2026-10-02: the displayed version is v1 of September23 and proposes H
and I as unresolved spectral conjectures. Their classical intersecting
and projection-packing conclusions do not produce this H matrix.
No general H/I solution, arbitrary private attachment cap closure,
historical priority, sharp gap or optimal perturbation is claimed.
The n=2/k=2 and k=1 cases are outside this theorem; the latter is already
within the prior two-facet class. Failure of the present candidate at
an excluded parameter is not H nonexistence.

## Complete core lift

For a symmetric nonempty Gram core C with every diagonal s-1 and
C_AB=-1 for distinct intersecting nonempty sets, put

    E=[-1'; I_(N-1)], Q=E*C*E', L=J_N+Q, M=(L-s*I_N)/h.

This credited structural lift has Q*1=0, L*1=N*1 and all required zero
entries of M, including nonempty diagonals. The actual empty vector is
the negative sum of **every actual nonempty vector**. Its loop is allowed
and determined by this sum. E is injective onto 1-perp, so
rank(L)=1+rank(C). If C>=0 then Q,L>=0.

For Euclidean Gram vectors a_A, the complete physical frame
S=sum over ALL A in F of |a_A><a_A| and Q have the same nonzero spectra,
by the RR'/R'R identity. Thus S<=(N-1)I on its exhaustive physical span
gives Q<=(N-1)P and

    h*(I-M)=N*P-Q >= P,  P=I-J/N.

The actual empty contribution is essential in that frame.

## The old cube and all omitted directions

On the 2q-1 old nonempty members, use

    C0=(q+3)I+(q-3)Pc-J,

where Pc pairs proper nonempty complements, with zero full-set row.
Initially treat this as a formal symmetric bilinear form, avoiding a
circular Euclidean assumption. Write g_A for its coefficient vectors,
G=sum old g_A, f=g_X and H_i=-sum_{x_i in A} g_A. Direct cube counting gives

    G^2=f^2=q+2, G*f=4-q,
    H_i*g_A=3(1-2[x_i in A]),
    H_i*H_j=3q*[i=j], G*H_i=f*H_i=-3.

There are q-1 proper nonempty complement pairs. Pair-constant coefficient
vectors of zero sum across pairs and zero full-set coefficient form a
q-2 dimensional eigenspace of C0, with eigenvalue2q. Pair-antisymmetric
coefficients form a q-1 dimensional eigenspace with eigenvalue6. The
remaining two-plane is spanned by

    gplus=(G-f)/2, h0=-(G+f)/2,

with diagonal Gram(q-1,3). These planes are independent and exhaustive,
proving **C0 positive definite** and rank2q-1 for every actual n>=3.

Let A_i=H_i-h0. They lie in the pair-antisymmetric space and have Gram
3(q*I_k-J_k). Since q>k for n>=3,k<=n, this is PD: its eigenvalues are
3(q-k) and3q. The A_i span k independent directions. Remove this plane
from the antisymmetric space, leaving **q-k-1** untouched directions
with eigenvalue6. The high q-2 space is orthogonal to G,f and every H_i,
because each mark occurs in exactly one member of each complement pair.
The low complement is likewise orthogonal to all changed old vectors.

The old physical frame acts on gplus,h0 with bilinear block

    [[q^2-1,3(q-1)],[3(q-1),9]],

and as6 times the Gram on the A_i plane. This follows by applying C0
to their explicit coefficient vectors: gplus maps to
(q+1)gplus+(q-1)h0 and h0 maps to3gplus+3h0. The two untouched frames
have eigenvalues2q and6. Gram and coefficient orthogonality agree on
each old scalar eigenspace.

## Marked and private vectors

Write h_i=H_i/3 and ell=3k+1. For each mark take an independent two-plane
T_i1,T_i2,T_i3 with Gram (q+3)(I3-J3/3); its sum is zero. Planes for
different marks and the old span are orthogonal. The three marked vectors
are V_ia=h_i+T_ia. They have squared norm q+2=s-1 and every required
old/marked and within-marked intersection pairing is -1. Marked vectors
at distinct marks have disjoint actual labels, so their cross entries
are permitted.

Put

    K=G+sum_i H_i, K^2=ell*q+2-6k,
    K*h_i=q-1, K*T_ia=0,
    D_i=h_i-(sum_{j!=i} h_j)/(k-1), D_i^2=q*k/[3(k-1)], K*D_i=0,
    d=3(q-3k-2)/(ell*q), a=-d/3,
    c=(a-d)q/(q+3)=-4(q-3k-2)/[ell*(q+3)].

All denominators are positive in the stated actual domain. Set

    p_i1=-K/ell+a*D_i+c*T_i2,
    p_i2=-K/ell+a*D_i+c*T_i1,
    p_i3=-K/ell+d*D_i+[c/(k-1)]*sum_{j!=i}T_j3.

The **cross-group transfer** in each full private projection is required:
the two leaves contribute -c*T_i3, supplied by the other full rows.
Sum_i D_i=0 gives sum of all3k projections =-3k*K/ell. Every contrast
is K-orthogonal. Thus every projection norm and required pairing follows
by the displayed bilinear identities, with no sign assumption on free
entries. In particular

    etaL=q+2-K^2/ell^2-a^2*D_i^2-2(q+3)c^2/3,
    etaF=q+2-K^2/ell^2-d^2*D_i^2-2(q+3)c^2/[3(k-1)],
    r=-1-K^2/ell^2-a*d*D_i^2,
    mu=(2r+etaF)/3, nu=k*mu/(k-1),
    beta=etaF-mu, alpha=2(2etaL-r-etaF).

Positivity of mu,alpha,beta is proved below. Take group means m_i with
diagonal Gram mu and off-diagonal -mu/(k-1); they span k-1 directions
and sum zero. For each group take separate orthogonal internal vectors
wA_i,wF_i of squared norms alpha,beta. All these spaces are independent
of the old and marked spans, and each other except the mean simplex.
The private residuals are

    W_i1=m_i+(wA_i-wF_i)/2,
    W_i2=m_i+(-wA_i-wF_i)/2,
    W_i3=m_i+wF_i.

They have diagonal etaL,etaL,etaF, within leaf/full pairings r, and
leaf/leaf pairing -etaL+r+etaF. Across groups every pairing is
-mu/(k-1). Their full3k Gram W has **kernel exactly span(1)** and
rank3k-1. Indeed the group-constant, zero-sum eigenvalue is3nu, each
local leaf difference has eigenvalue alpha/2, and each local
(-1/2,-1/2,1) direction has eigenvalue3beta/2. The global constant
vector is the only remaining direction.

Set U_ia=p_ia+W_ia for actual u_i,v_i,u_iv_i. Every new norm is q+2.
U_i1 meets V_i1,V_i3,U_i3; U_i2 meets V_i2,V_i3,U_i3; U_i3 meets
all three V_i's. Direct substitution yields pairing -1 for each such
case. Every other new intersection type was covered above, or is
disjoint: private rows contain no old point, and different groups have
no shared old or private point. This is the complete support partition.
The sum of all nonempty vectors is K/ell, hence the **actual empty seed
vector is -K/ell**, of squared norm K^2/ell^2.

## Exhaustive fixed-dimensional frame reduction

The changed old space has dimension k+2, the marked residuals2k,
and the private residuals3k-1. These are independent by the preceding
PD proofs, giving changed dimension **6k+1** and complete seed core rank

    6k+1+(q-2)+(q-k-1)=2q+5k-2=N-k-2.

Every untouched direction is orthogonal to every new vector and the
actual empty, because the new projections use only G,H_i,T_ia and the
new residuals. Its complete frame eigenvalue stays2q or6. No omitted
harmonic type or unbounded-dimensional direction is presumed harmless.

Local leaf exchange isolates k mutually orthogonal copies of the
two-dimensional span(tA_i,wA_i), where tA_i=T_i1-T_i2. The remaining
group-permutation action splits into the fixed5-space

    (gplus,h0,sum_i A_i,sum_i tS_i,sum_i wF_i),
    tS_i=T_i1+T_i2-2T_i3,

and k-1 copies of a standard4-space. For a zero-sum coefficient vector
z with sum(z_i^2)=2, its basis is

    (sum z_i A_i, sum z_i tS_i, sum z_i m_i, sum z_i wF_i).

For two such coefficient vectors all bilinear formulas below scale by
their dot product/2. Thus positivity of one4-block proves positivity on
the entire standard tensor space. The count 2k+5+4(k-1)=6k+1 exhausts
the changed span. Cross-sector Gram and frame entries vanish: a leaf
flip changes just its own antisymmetric block's sign, and every
fixed/standard cross is proportional to sum z_i=0. This can also be
verified directly from the following complete products.

For each basis, Gamma is its physical Gram and F its **complete** frame
bilinear matrix. The cap test is B=(N-1)Gamma-F. Let [v] denote vv'.

Antisymmetric2:

    GammaA=diag(2s,alpha),
    FA=2[(s,0)]+2[(-c*s,alpha/2)].

Fixed5:

    GammaE=diag(q-1,3,3k(q-k),6k*s,k*beta).

Its old frame has entries F00=q^2-1,F01=3(q-1),F11=9,
F22=6*GammaE22 and zero elsewhere. Set

    vL=(0,1,q-k,s,0), vF=(0,1,q-k,-2s,0),
    e=(-(q-1)/ell,-3(k-1)/ell,-3k(q-k)/ell,0,0),
    uL=e+(0,0,0,c*s,-beta/2),
    uF=e+(0,0,0,-2c*s,beta).

Then FE=Fold+k*(2[vL]+[vF]+2[uL]+[uF])+[e]. The last term is the
actual empty. These products follow because A_sum*h_i=q-k,
tS_sum*T_i1/2=s,tS_sum*T_i3=-2s, sum means=0 and the D_i fixed
projection is zero.

Standard4:

    GammaO=diag(6q,12s,2nu,2beta),
    vL=(q,s,0,0), vF=(q,-2s,0,0),
    uL=(a*k*q/(k-1),c*s,nu,-beta/2),
    uF=(d*k*q/(k-1),2c*s/(k-1),nu,beta).

Its old frame has only F00=6*GammaO00. Add2*(2[vL]+[vF]+2[uL]+[uF]).
The empty has zero standard projection. Every individual product is
the displayed vector times z_i: A_z*h_i=q*z_i,
A_z*D_i=k*q*z_i/(k-1), tS_z*T_i1/2=s*z_i,
tS_z*sum_{j!=i}T_j3=2s*z_i, mean_z*m_i=nu*z_i.
These identities prove the entire standard frame for every k, rather
than extrapolating a single k=2 block.

The standard cap also has a useful **rank-two update** identity:

    BO=D-4[uL]-2[uF],
    D=diag(6q(q+6k-7),12s(q+6k-4),2nu(N-1),2beta(N-1)).

D is PD in the domain. With U=[uL,uF], the rational2-Schur matrix

    S2=diag(1/4,1/2)-U'*D^(-1)*U

is PD iff BO is PD, by the two Schur complements of
[[D,U],[U',diag(1/4,1/2)]]. uniform.py verifies all16 entries of the
four-dimensional rank-two identity before applying the smaller test.
This is classical Schur-complement mathematics, not a new algorithm.

## Exact quadrant certificates and complete actual coverage

First take auxiliary real **k=2+r**, **q=4k-4+t**, r,t>=0. This implies
q>k. The three residual rational norms mu,alpha,beta have numerator
polynomials with nonnegative coefficients and strictly positive constants;
all denominator factors also have these properties. They are consequently
strictly positive throughout this entire quadrant.

uniform.py clears each matrix row by positive denominator factors,
then divides out known common row factors already proved positive and
normalizes its rational integer content by a positive constant. Every
division is exact. The resulting row multiplier is positive on the
whole quadrant, so it preserves each leading determinant's sign.
The cleared rows need not form a symmetric matrix; Sylvester's criterion
is applied to the original symmetric Gamma/cap/Schur matrices.

Fraction-free Bareiss gives every leading determinant polynomial.
Its exact division identities are checked. Every stored coefficient is
positive and the constant is positive. The polynomial engine uses exact
integer/Fraction arithmetic; its Kronecker multiplication is checked
against separate direct convolution. Modular probes only reject possible
divisibility; every successful division is validated exactly.

For each leading submatrix, the determinant permutation expansion gives
a separate degree bound d_r,d_t: for either variable sum each row's
largest entry degree in that variable. A **separate scalar Fraction
Gaussian determinant** checks the computed polynomial at every point
of {0,...,d_r} times {0,...,d_t}. Both polynomials obey these bounds.
Their difference vanishes on the full grid, so, by applying the univariate
root bound successively in each variable, it is identically zero.
This is an exact determinant identity proof. The subsequent coefficient
signs prove positivity on the unbounded quadrant; finite sign samples
do not prove that conclusion. RESULTS.json freezes the entire compact
coefficient/domain/identity-point record, not just a success flag.

This proves all residual norms and BA,BE,S2 positive, hence BO positive,
for all real k>=2,q>=4k-4. At actual integer n>=5,
2^(n-1)>=4n-4 by induction from equality at n5; doubling preserves it
since8n-8>=4n for n>=2. With k<=n this implies q>=4k-4.
At n3, only k3 falls outside this quadrant; at n4, only k4 does.
The exact original families **(n,k)=(3,3),(4,4)**, of sizes26 and40,
are checked directly: all residual/core/changed/full cap PSD tests and
ranks pass. All their possible labelings are permutations of these
canonical actual families. They are a complete finite exceptional
coverage argument, not a bounded approximation of the generic quadrant.

Therefore for every actual parameter in the theorem the complete seed
frame is <=(N-1)I: the changed blocks are strictly below that threshold
and the two untouched eigenvalues2q,6 are below N-1. The full actual
lift has scaled cap gap>=1, lower rankN-k-1 and upper rankN-1.

## Direct free-entry repair and greatest lower rank

The base consists of all old nonempty and3k marked rows: b=2q-1+3k.
They span rank2q-1+2k=b-k. Every private projection is a rational linear
combination of these base rows. In the base/private order, the core is

    C=[[B,B*Pi],[Pi'*B,Pi'*B*Pi+W]],

with rational Pi, B>=0 of rank b-k, and balanced W>=0 of rank3k-1.
These are the preceding independent-span results, not numerical premises.

Choose v to be the last group's full private row, and U the first
group's three private rows. Their actual sets are disjoint from v.
Delete v from W to obtain A. Since ker(W)=span(1), A is PD: a nonzero
vector with last coordinate zero cannot belong to that kernel.
For u the U-indicator put

    p=sum(u)=3, kappa=u'*A^(-1)*u=2/nu+4/beta,
    delta=1/[12*N*(1+kappa)] >0.

The inverse formula is explicit, with no large inversion needed. Extend
the solution of A*x=u by x_v=0. At the first group's three positions
take2/(3nu)+4/(3beta); at intermediate groups take1/(3nu)+4/(3beta);
at the last group's two leaves take2/beta. Substitution into the full
W gives u at every undeleted position and -3 at v, proving the formula
and sum of the first three x positions=kappa. Equivalently this follows
from W's eigenvalues3nu and3beta/2 on the group-mean and internal-full
parts of u-3e_v. It is rational and strictly positive.

Add delta only to the symmetric free private core entries (v,U).
Let W_delta denote the repaired residual. The original row-zero W has
block form [[A,-A*1],[-1'*A,1'*A*1]]. Its repaired scalar Schur is

    1'*A*1-(-A*1+delta*u)' A^(-1)(-A*1+delta*u)
      = 6delta-kappa*delta^2 >0.

Here delta*kappa<1/(12N)<6. Thus W_delta is PD of rank3k.
An invertible triangular block congruence takes repaired C to
diag(B,W_delta), giving rank(C)=b-k+3k=N-1-k. Every core diagonal and
required intersecting entry is unchanged. The **repaired actual empty**
is determined by the complete lift; it is not kept equal to -K/ell.

For the cap, the repaired full Q changes by
E*diag(0,delta*Dstar)*E', where Dstar=[[0,u],[u',0]], kills1, and has
operator norm sqrt(3)<=3. Since E'*E=I+J has top eigenvalue N,

    ||DeltaQ|| <=3Ndelta=1/[4(1+kappa)] <1/4.

The seed gap>=1 therefore gives repaired h*(I-M)>=(3/4)P. It also
gives upper rankN-1. Rationality is entrywise; a Euclidean realization
need not have rational vector coordinates.

For ANY competing real ordinary H on this F, a maximum-star indicator
sigma has sigma'*M*sigma=0 by support, L*1=N*1 and |sigma|=s. Thus
(sigma-(s/N)1)'*L*(sigma-(s/N)1)=0. PSD puts that centered indicator
in ker(L). The k marked-star centered indicators are independent:
their empty coordinate forces the sum of coefficients to be zero,
and each marked singleton then forces its own coefficient zero.
Consequently every such lower matrix has rank at mostN-k, attained
by the repaired construction. Its kernel is exactly their span.
This proof does not assume an upper cap on competing H matrices.

## Validation, failed prototypes and trust boundary

The checker builds six canonical **original** families
(n,k)=(3,2),(3,3),(4,3),(4,4),(5,5),(6,2), with N=20,26,34,40,62,76.
For every actual row it checks downset, star size, support, symmetry,
row sum, lower PSD, upper PSD, rank and cap including empty.
It compares each reduced Gram/frame entry with independent literal
original coefficient-vector products, as well as the entire6k+1 changed
Gram/frame. It checks every full untouched high/low eigenaction,
the explicit inverse action, repaired Schur, residual ranks and both
whole PSD ranks. Finite tests validate implementation; the unbounded
result rests on the written complete-space/quadrant/coverage proofs.

An initial extraction used W_i3 itself as the internal wF_i, omitting
the group mean. Literal standard-block comparisons rejected it before
any claim; the corrected extraction subtracts m_i and is retained as
a semantic damage control. The private candidate's initial k2 stage
already had a separate14-polynomial one-variable sign proof; it is
superseded here by the wider complete theorem, not another publication.

Naive four-dimensional bivariate Bareiss expansion hit the fixed512-term
guard. Exact common positive row factor removal resolved the fixed block,
and the standard rank-two Schur identity resolved the remaining expansion.
Those aborted attempts remain operational failures, not nonexistence.
Neither polynomial guard, CPU/memory/thread settings nor stage timeouts
was increased. The old unrelated multivariable native replay remains paused.

The reproducible packet needs CPython and the standard library only.
All native thread variables are1, one mathematical job is run at a time,
with unchanged1CPU2GiB scope. Individual stages have fixed60s guards;
literal validation n<=6,N<=80. No CAS, solver, floating eigenvalues,
private ledger, theorem-prover axiom, incomplete enumeration or resource
failure is a mathematical premise. Arithmetic and real linear algebra
remain **ordinary/unformalized**; the implementation is author validation,
not independent review. Semantic damages reject explicit invalid cases
in normal and optimized Python modes.

The complete replay freezes the following exact counts. The three
residual numerator polynomials are recorded separately from the
twelve leading determinant polynomials; they are not silently counted
as additional leading minors.

| Certificate block | Dimension | Leading coefficient counts | Full-grid determinant checks |
| --- | ---: | --- | ---: |
| Residual after positive factor removal | 3 | 1,1,1 | 3 |
| Antisymmetric cap | 2 | 35,92 | 165 |
| Fixed cap | 5 | 9,18,26,100,187 | 510 |
| Standard equivalent Schur cap | 2 | 45,154 | 269 |

There are **669** leading-minor coefficients, **66** additional positive
residual-numerator coefficients and **947** independent determinant-grid
evaluations. Nine scalar identity controls compare **1215** complete
Gram/frame/cap entries. Six literal fixtures check **13452** actual
positions per seed or repaired matrix, **270** reduced Gram and **270**
reduced frame positions, **2646** changed Gram and **2646** changed frame
positions, and every one of **60** untouched high plus **47** low
eigenactions. Eight direct-convolution/quotient controls and **18**
semantic damages pass. These are validation counts, not additional
finite-family discoveries. The frozen whole mathematical record is
`a2f7c6610149ebdfa4c2fff3fe4d0f7b2fcbbc560f8c5f25b3de625aa6aee710`.
