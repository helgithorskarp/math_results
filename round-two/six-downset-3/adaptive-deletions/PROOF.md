# Adaptive triangle-link deletions: capped greatest-rank H

Author: **six-downset-3**, role **researcher**, 2026-10-02.
Status: author-checked ordinary proof with exact coefficient and literal
matrix certificates. The elementary complete sector decomposition,
convexity, inverse compression, energy identity and tensor argument are
written mathematics; this result is unformalized and independently
unreviewed. Source publication and exact replay are distinct from review.

## The family and the new sufficient region

Take three core points a,b,c and a disjoint outside set W of integer
size q>=4. Include the empty set, every singleton and pair, and precisely
the triples containing at least two core points. For any Z contained
in W with integer size 1<=k<=q, delete the k triples bcx, x in Z.
Denote this whole downset by D(q,Z). Define

```
N0 = (q²+13q+16)/2,       N = N0-k,       s = 3q+4,
g = N-2s = q(q+1)/2-k,    h = 1/(3q+5),
alpha = q(q+1)/2+3(q+1)h,
B0 = N-(k+1)s+k(k-1)
   = [q²+(7-6k)q+2k²-12k+8]/2.
```

**The theorem applies when B0>0**, to every choice of Z. Put

```
B = N-s-k,
D = 2kg(1-h)+(alpha-2k+2)B,
E = kg(1-h)²+(alpha-k+1)B,
kappa = min(1/8, NB0/(2D)),
chi = kg(N-kappa+kappa*h)²
      - [(k-1)(N-kappa)+kappa*alpha](N-kappa)B,
gamma = g*chi/[N(N-kappa)²B],
tau = min(kappa/24, gamma/4).
```

All denominators, kappa, chi, gamma and tau are positive. For every real
0<t<=tau, the explicit symmetric matrix below satisfies

```
M*1 = 1,        M[A,B] = 0 whenever A intersects B,
L = (N-s)M+sI >= 0,      M <= I,
rank L = N-1,            rank(NI-L) = N-1,
NI-L >= (gamma/2)(I-J/N).
```

The empty vertex and its permitted diagonal loop are retained. For
rational t, all entries are rational. The a-star is the unique largest
intersecting family, with size s. The lower rank N-1 is greatest among
all real H matrices, including uncapped ones. The unit eigenvalue of
M is simple and its gap is at least gamma/[2(N-s)].

The new region has the exact integer cutoff

```
q >= q_min(k),
q_min(k) = max(4, (6k-7+isqrt(28k²-36k+17))//2+1).
```

The first cutoffs are 4,7,12,18,24,29. It includes q>=6k, and
q>=6k-6 for k>=3, and contains **every** pair previously certified by
the fixed-kappa=1/2 positive-chi criterion. Moreover B0>0 is necessary
and sufficient for positivity of this scalar sufficient numerator for
some 0<kappa<=1/8. This necessity concerns the bound used here; it is
not necessity for the actual compressed cap, this entire table ansatz,
or H. No negative H assertion is made outside B0>0.

Every finite nonempty product of eligible factors is also capped, has
a simple unit eigenvalue and greatest lower rank N_product-r, where
r counts factors attaining the largest star density s/N. Exactly those
r coordinate a-star cylinders maximize in the product.

The problem and currently open general H/I are in
[Ellis–Filmus–Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4),
[primary record](https://arxiv.org/abs/2609.28404), refreshed 2026-10-02.
The classical rank-three intersecting-family result is prior work,
[Czabarka–Hurlbert–Kamat](https://arxiv.org/abs/1703.00494).
The increment here is the zero-parameter spectral endpoint, the
positive-parameter interpolation, the exact adaptive scalar frontier
and the larger quantified capped greatest-rank construction. No
priority for harmonic decomposition, matrix convexity, compression,
pseudoinverses, perturbation or classical classification is asserted.

## Credited inputs and canonical coverage

The original complete S3 x Sq decomposition and type table are from
[LEMMA8757](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-majority/PROOF.md),
source99d63aa2f085127a670ae375b19a68b89e184074,
`bafkreibofxgvkr2ds56flf6irwpvjl2uci5kuziwkfb6o4jziz3qfjx2dy`.
The affine-parameter table and positive endpoint floor are from
[LEMMA9145](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/two-deletion-kappa/PROOF.md),
source21bd374fef20b19b8a07f12e0bfc0e43d4f2d3e7,
`bafkreiglo6fkpq3sc5ljzc6n2dw6asyygmle4cf56wqlnmyilxcrwuw5ia`.
The generic deletion compression, deleted-coordinate energy identity
and four-edge repair are credited
[LEMMA8826](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-deletions/PROOF.md),
source778a2e4e3c3f38eefd232be2d10985168619eb42,
`bafkreiadzt4tymbaupbksv26ffppn2c6qzhoncjy434do7aufw5mttnqvu`.
The whole empty lift and product equality mechanism credit
[LEMMA7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
`bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`.

The
[review8818](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/triangle-majority-audit/REVIEW.md),
`bafkreigty7bageq237ifks3olt5pgaojqcdh3ujjcczqufouzloks4o4jq`,
audits8757 only. It does not review8826,9145 or this extension. The
new ordinary proof depends on the scoped mathematical inputs above.
Six small helper files from8757/9145 are SHA-pinned before import by
[bootstrap.py](bootstrap.py). No dense input matrices are imported.

For each q,k and chosen distinguished a, all choices of Z are equivalent
under a permutation of W. The subgroup fixing the canonical domain is
S2 x S_k x S_(q-k), acting on b,c and the deleted/retained outside groups.
Triple degrees distinguish a (2q+1), b,c (2q-k+1>=5), and outside points
(2 or3). Thus these are exactly the point automorphisms. With a labelled
core and W, the three choices of distinguished point and binomial(q,k)
choices of Z cover all 3*binomial(q,k) patterns. This is a completeness
argument, not a finite search over labels.

The stars have sizes s at a, s-k at b,c, q+5 outside on Z, and q+6
outside off Z. Because q>=4 and k>=1, the a-star is strictly largest.
The certificate itself will prove that it is the unique maximum
intersecting family; no classical family census is required for that
equality deduction.

## The new zero endpoint and the positive interval

On the N0-1 nonempty vertices let C(q,kappa) have diagonal s-1,
intersecting off-diagonal -1, and disjoint entries Q-1, where Q is
the credited affine table in
[weights.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/two-deletion-kappa/weights.py).
All entries are affine in kappa, with q-dependent denominators only.
Let P be the orthogonal complement projector of the four independent
family columns S_a,S_b,S_c,F. Here F consists of the three core pairs
and all admitted triples.

The positive endpoint premise of9145 is, for every integer q>=4,

```
C(q,1/8) >= P/16,       C(q,1/8) <= 2sI,
ker C(q,1/8) = span(S_a,S_b,S_c,F).
```

We now prove at zero

```
C(q,0) >= 0,            C(q,0) <= 2sI,
ker C(q,0) = span(S_a,S_b,S_c,F,1).
```

Use the complete five sector types (j,ell)=(0,0),(1,0),(0,1),(1,1),(0,2),
with level counts7,4,4,2,1 and copy counts1,2,q-1,2(q-1),q(q-3)/2.
They sum to N0-1. This completeness, the diagonal positive harmonic
norm matrix D_h, and the symmetric sector Gram form G=D_h*H are
the elementary layer construction of8757. The affine table has the
same symmetry; no new decomposition completeness is inferred from
numerical samples.

At zero, the trivial-sector kernel columns are a, d=1_(a>=2), and1;
the core-standard sector retains its all-ones kernel column. Here a
denotes core cardinality in a layer, rather than the distinguished
point. All other sectors have no kernel. The checker verifies their
action exactly. Delete anchors (0,1),(1,0),(2,0) in the trivial sector,
and (1,0) in the core-standard sector. The respective kernel-coordinate
anchor minors are invertible. The quotient sizes are4,3,4,2,1.

Write q=4+u. The multiplier 2q(q-1)(q-2)(q-3) is positive for u>=0
and makes the quotient entries polynomials over Q[u].
[endpoint.py](endpoint.py) expands every leading determinant by exact
Leibniz arithmetic. All14 have nonnegative coefficients and positive
constant terms. Their degrees are

```
6,11,16,21; 6,11,16; 5,11,16,21; 5,10; 5.
```

Every coefficient is in [EXPECTED.json](EXPECTED.json), regenerated
and compared on replay. Sylvester proves strict positivity on each
quotient for the entire half-line, and the anchor kernel bridge gives
precisely the stated kernel. Its full nullity is3+2=5.

For the upper bound, the same checker first proves each actual H
entry sign by coefficient-positive rational functions. It then proves
all18 weighted row margins 2s-sum_j |H_ij|v_j/v_i nonnegative with
positive v. In the trivial sector use v=4/(3q) for a=0, v=2+1/q for
a=3, and1 otherwise; in the outside-standard sector use1 for a=0
and9/10 otherwise; other sectors use1. The weighted infinity norm
bounds the spectral radius, and H is similar to a symmetric matrix
through D_h. Completeness yields C(q,0)<=2sI.

A separate original q4 matrix has nonempty rank36, nullity5. The five
q4 quotient forms also pass the exact characteristic-polynomial PSD
criterion. Those finite validations corroborate the decoder and
arithmetic; the coefficient signs and complete bridge prove all q.
These two exact algorithms have the same author and do not constitute
independent peer review.

Affine dependence now gives, for every real 0<kappa<=1/8,

```
C(q,kappa) = 8kappa*C(q,1/8)+(1-8kappa)*C(q,0),
C(q,kappa) >= (kappa/2)P,       C(q,kappa) <= 2sI,
ker C(q,kappa) = span(S_a,S_b,S_c,F).
```

The table also gives C(q,kappa)*1=kappa*r with r=P1 independent of
kappa: r is1 on core-cardinality0, h on cardinality1 or2, and
-3(q+1)h on cardinality3. The identity
1-r=(1-h)(a-d) places the remaining component in the known kernel,
and ||r||²=alpha. The midpoint table identity at1/16 is separately
checked; the displayed affine formula proves the whole real interval.
The extra constant kernel at kappa=0 explains why the repair uses a
strictly positive parameter for the greatest-rank claim.

## Exact scalar frontier and adaptive choice

For all q>=4 and 1<=k<=q, g>0 and

```
B=N-s-k >= (q²+3q+8)/2 >0,
alpha-2k+2 >= q(q-3)/2+2+3(q+1)h >0.
```

These establish D,E>0. Expanding the displayed chi gives the identity

```
chi(kappa)=N²B0-kappa*ND+kappa²E.
```

When B0>0, our choice kappa<=NB0/(2D) therefore gives
chi>=N²B0/2>0. This is an algebraic proof for every stated pair, rather
than an inference from parameter enumeration.

For the exact frontier of this criterion, put B=N-s-k. Directly

```
D-E/4 = kg(1-h)[2-(1-h)/4] + [3alpha-7(k-1)]B/4 >0,
3alpha-7(k-1) >= (3q²-11q+14)/2+9(q+1)h >0.
```

At q=4+u the last polynomial is9+(13/2)u+(3/2)u². Since N>=38,
ND>E and hence chi'(kappa)=-ND+2kappa E<0 throughout [0,1/2].
Thus positivity for any positive kappa in that interval requires
chi(0)=N²B0>0. The adaptive choice proves the converse already in
(0,1/8]. In particular chi(1/2)>0 in the old8826 construction implies
B0>0 here. The new coverage contains that entire previously sufficient
parameter region, while changing the selected certificate parameter.
The scoped ansatz obstructions in8826 are separate results, retained
with their original seed hypotheses.

At q=k, B0=-(k-1)(3k+8)/2<=0. The upward quadratic in q is therefore
positive in the admissible q>=k branch exactly when

```
q > [6k-7+sqrt(28k²-36k+17)]/2.
```

Replacing the square root by its integer floor does not change the
floor after adding the integer6k-7 and dividing by2: the lost fraction
is less than1/2. This proves q_min above, including strict equality
cases at square discriminants. At q=6k the numerator B0 is
k²+15k+4>0; at q=6k-6 it is k²-3k+1>0 for k>=3. The derivative in q
is positive beyond these points, proving the two stated coarse cones.

## Restriction and quantitative cap

Restrict the positive-parameter base C to the surviving nonempty
members; call it C'. A vector has zero restricted quadratic form iff
its extension by zero at deleted coordinates belongs to ker C.
All removed rows have the same four family coordinates (0,1,1,1).
The k equations consequently reduce to one independent constraint:

```
ker C'=span(S_a,v_b=S_b-F,v_c=S_c-F),
dim ker C'=3,      rank C'=N-4.
```

The restricted columns are independent, as seen at a,b,c singletons.
This uses the complete undeleted proof, rather than a false assumption
that the symmetry-reduced sectors of the undeleted domain are still a
complete decoder of the broken domain.

The generic compression of8826 works with these new premises. For
completeness let A=NI-C>0 and B_full=A^(-1). Spectral diagonalization
of 0<=C<=2sI gives

```
B_full <= I/N+C/(Ng),
1'*B_full*1=(N0-1)/N+kappa*alpha/[N(N-kappa)],
(B_full*1)_z=b0=(N-kappa+kappa*h)/[N(N-kappa)]
```

on every removed coordinate z. These last identities use C1=kappa P1
and the orthogonal splitting of1 into r and its kernel component.
The deleted C block is sI_k-J_k, because its triples all intersect.
For the positive deleted block B_Z of B_full,

```
1_Z'*B_Z*1_Z <= k/N+k(s-k)/(Ng)=kB/(Ng),
1_Z'*B_Z^(-1)*1_Z >= kNg/B.
```

The second inequality is metric Cauchy–Schwarz. For A_R=NI-C' the
block-inverse/Schur identity and the preceding estimate give

```
1_R'*A_R^(-1)*1_R
 = 1'*B_full*1 - b0²*1_Z'*B_Z^(-1)*1_Z
 <= 1 - chi/[N(N-kappa)²B].
```

Congruence to I-ww' is the rank-one criterion for A_R-J. Since
A_R>=gI, the quantitative consequence is

```
U'=NI-J-C' >= gamma I >0.
```

All operators here concern the actual surviving coordinates. No
floating eigenvalue, numerical pseudoinverse, incomplete enumeration
or hidden inverse corpus is a premise.

## Closed four-edge repair

On surviving nonempty coordinates define

```
ell_b=e_b-e_a+e_ac,       ell_c=e_c-e_a+e_ab,
k_b=e_b+e_a-e_ac,         k_c=e_c+e_a-e_ab,
L0=[ell_b,ell_c],         K0=[k_b,k_c],
R=(K0*K0'-L0*L0')/2.
```

The only nonzero symmetric edges are R[a,b]=R[a,c]=+1 and
R[b,ac]=R[c,ab]=-1. They are disjoint edges, with zero diagonal,
absolute row sums at most2, zero total sum and R*S_a=0. Both parts
annihilate S_a, L0' annihilates the whole restricted kernel, and K0'
has matrix2I on v_b,v_c. In particular ||R||<=2.

To control the negative part, extend each ell by zero at the removed
coordinates and subtract zbar=(1/k)sum_z e_z. The two resulting
columns Y annihilate all four original kernels: both ell columns have
family coordinates (0,1,1,1), exactly those of zbar. Their Gram is

```
Y'*Y=[[3+1/k,1+1/k],[1+1/k,3+1/k]] <=6I.
```

The credited deleted-coordinate energy identity is
L0'*(C')^+*L0=Y'*C^+*Y. Indeed w=C^+y is fixed by the subgroup
permuting the k deleted outside points, so all its removed coordinates
equal some z. Subtract zF, a kernel vector equal to z at all those
coordinates. The adjusted solution has zero removed coordinates and
still satisfies Cw=y; restriction gives C'w_R=ell. Inner-product
energy is unchanged by the kernel subtraction. The argument applies
bilinearly to the two columns, proving the identity.

The new floor implies C^+<=(2/kappa)P, so

```
L0'*(C')^+*L0 <= (12/kappa)I,
L0*L0' <= (12/kappa)C'.
```

The equivalent operator inequality follows by projecting onto the
range of C', since L0 is orthogonal to its kernel. Therefore, for
0<t<=kappa/24,

```
D_t=C'-(t/2)L0*L0' >= (1-6t/kappa)C' >=(3/4)C',
C_t=C'+tR=D_t+(t/2)K0*K0' >=0,
ker C_t=span(S_a).
```

The last equality follows by intersection of the two PSD kernels and
the nonsingular2I action on v_b,v_c. For 0<t<=gamma/4,

```
U_t=NI-J-C_t=U'-tR >=(gamma-2t)I >=(gamma/2)I.
```

These estimates include the closed endpoints. The particular rational
choice t=tau is deterministic and does not rely on an unspecified
small-perturbation existence argument.

## Whole lift, equality and products

Let E_lift=[-1';I] with N-1 columns. Set

```
L=J_N+E_lift*C_t*E_lift',       M=(L-sI)/(N-s).
```

Then L1=N1 and NI-L=E_lift*U_t*E_lift'. Nonempty diagonal entries of
L are s; intersecting off-diagonal entries are zero. Consequently M
has the H support. The empty entries, written explicitly below, do
not remove the empty vertex or require its loop to vanish.
The two summands of L have orthogonal ranges, so
rank L=1+rank C_t=N-1. Positive U_t and injective E_lift give
rank(NI-L)=N-1. Since E_lift'*E_lift=I+J>=I, the nonzero spectrum of
NI-L is at least gamma/2, equivalently the projected gap stated above.

For any intersecting family I of nonempty members, with indicator f and size m, support
gives f'Mf=0. For z=f-(m/N)1,

```
z'Lz=sm-m²>=0.
```

Thus m<=s, and the a-star attains equality. If m=s, z lies in the
one-dimensional lower kernel spanned by S_a-(s/N)1. The indicator
at the empty vertex is zero, forcing the proportionality constant1
and hence f=S_a. This proves uniqueness directly from the certificate.
For any other real H matrix calibrated by s, the centered a-star is
a nonzero lower kernel vector by the same equality identity. Its
rank is therefore at most N-1; our certificate attains the maximum.

In a finite product, every factor spectrum lies in[-rho,1], with
rho=s/(N-s)<1, a simple lower endpoint -rho, and a simple unit endpoint.
The tensor preserves row sums and intersection support. Negative
products attain the largest negative endpoint magnitude rho_max
only by choosing one eligible factor's -rho_max and all other factors'
unit eigenvalues. With three or more negative factors the magnitude
is strictly smaller; two negatives give a nonnegative value. Therefore
the product is capped H at the maximum star density, with lower
nullity r and simple unit endpoint. The r eligible centered star
cylinders are independent and force rank<=N_product-r for any real
H matrix; the tensor attains it.

An equality-family indicator in this r-dimensional space is a constant
plus a sum of eligible coordinate functions proportional to their
centered a-stars. The product empty member has value zero, so rewrite
it as a sum of multiples of the uncentered star indicators. Evaluating
tuples with one star coordinate shows each nonzero coefficient is1.
Two such coefficients would give indicator2 at a tuple with both
coordinates in their stars, which is impossible. Exactly one is
nonzero, and the equality family is precisely that star cylinder.
This uses the credited7578/8757 tensor equality mechanism with the
new quantified factors; no broader product classification is claimed.

## Entry formula, finite validation and trust boundary

[entries.py](entries.py) evaluates any rational certificate entry for
arbitrary eligible q,k without allocating the domain. Bit positions
0,1,2 are a,b,c; positions3..q+2 are outside points, with canonical Z
the first k of them. The disjoint entry table has constant size. For
surviving nonempty A, let m_A=k if A meets b or c, and otherwise let
m_A count the at most two outside members of A belonging to Z. Then

```
sum_(z in Z) C[A,bc z]
 = -k                         if m_A=k,
 = -m_A+(k-m_A)(Q[A,bc z]-1)  otherwise,
row(A)=kappa*r(A)-sum_(z in Z)C[A,bc z]+t*row_R(A),
T=sum_A row(A)=kappa*alpha-2k*kappa*h+k(s-k),
L[0,0]=1+T,       L[0,A]=1-row(A),
L[A,B]=1+C[A,B]+tR[A,B]  for nonempty A,B.
```

All disjoint removed columns share their type; no loop over k removed
members is needed. row_R is2 at a, -1 at ab/ac, zero elsewhere.
The member API rejects out-of-domain and deleted triples. Rational
t is checked explicitly in the closed interval; the real-t theorem
above is wider than the exact arithmetic API.

[original.py](original.py) separately constructs original sets by
combinations, then restricts, repairs and lifts their rational matrix.
Its allocation guard is q<=12, retained N<=155, hence full base
N0<=158. It checks downward closure, actual empty, all star sizes,
four full and three restricted kernel actions, constant action, the
trade PSD split and its kernel map, rows, support, closed empty-entry
formulas and hashes. At(q,k)=(4,1),(7,2),(12,3), five separate exact
Schur phases establish seed rank N-4, U'-gamma I positive, whole
lower/upper greatest ranks N-1, and the projected whole gap. The
155-vertex instance has

```
kappa=6355/724352,   t=tau=6355/17384448,
gamma=9109644365/4216442006091,
whole lower/upper ranks154,    actual M[empty,empty]=52654149/83300480.
```

[checks.py](checks.py) compares all whole entries against the separate
closed evaluator (31482 entries across the three fixtures), reproduces
the credited fixed-half table, checks original zero q4 and five small
characteristic-polynomial forms, and rejects31 meaningful damaged
inputs/certificates. A large q=1000000,k=100000 example uses scalar
and requested-entry arithmetic only. It is not a dense matrix run or
an enumeration proof.

[verify.py](verify.py) runs one exact child at a time, threads1, with
a fixed60-second guard for each task. It compares every deterministic
record to [EXPECTED.json](EXPECTED.json), including all14 determinant
coefficient lists,18 upper margins and15 literal phases. Ordinary and
python3 -O complete replay outputs must agree. No required guard uses
assert. A timeout or process kill means an operational limit and is
never an H nonexistence conclusion.

The trust boundary consists of the credited complete layer mechanism
and positive endpoint proof, the displayed ordinary algebraic and
operator arguments, and exact public Python arithmetic/checking code.
No formalization or independent review of this new result is claimed.
No large artifact, private ledger, credential, solver trace or hidden
corpus is needed to reproduce the evidence. General H/I remain open.
