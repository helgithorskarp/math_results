# Two triangle-link deletions: the kappa=1/8 certificate for every q>=7

Author: **six-downset-3**, role **researcher**, 2026-10-01.
Status: author-checked ordinary proof and exact reproducible certificates;
unformalized and not independently reviewed. The layer-completeness,
inverse-compression, range-energy and interval arguments below are part
of the ordinary proof. General Spectral Chvátal H and I remain open.

## Family, coverage and conclusion

Take three core points a,b,c and a disjoint outside set W of integer
size q>=7. Include the empty set, every singleton and pair, and every
triple containing at least two core points, except precisely bcx for
two distinct x in W. Write this downset as D(q,Z), |Z|=2, and put

```
N0 = (q²+13q+16)/2,     N = N0-2 = (q²+13q+12)/2,
s = 3q+4,              g = N-2s = q(q+1)/2-2 > 0,
kappa = 1/8,           h = 1/(3q+5),
alpha = q(q+1)/2 + 3(q+1)/(3q+5),
chi = 2g(N-kappa+kappa*h)²
      - [(N-kappa)+kappa*alpha](N-kappa)(N-s-2),
gamma = g*chi/[N(N-kappa)²(N-s-2)],
tau = min(1/192, gamma/4).
```

Both chi and gamma are strictly positive throughout this scope.
For **every real 0<t<=tau** the explicit whole-downset construction
below satisfies

```
M = M',    M*1 = 1,    M[A,B] = 0 whenever A intersects B,
L = (N-s)M+sI >= 0,    NI-L >= (gamma/2)(I-J/N),
rank L = N-1,         rank(NI-L) = N-1.
```

Its lower and capped upper ranks are universally greatest. The only
maximum intersecting family is the a-star. The unit eigenvalue of M
is simple, with gap at least gamma/[2(N-s)] from every other eigenvalue.
All entries are rational when t is rational; the deterministic reader
formula takes the rational endpoint t=tau. The actual empty vertex
and its permitted loop are retained.

There is one permutation class for each q: permute W to take Z to its
first two points. The automorphism group on ground points is
S2 x S2 x S_(q-2), permuting b,c, the two deleted outside points and
the others. Indeed triple degrees are 2q+1 at a, 2q-1 at b,c, and
2 or 3 at outside points, respectively; these distinguish the classes.
Thus the proof covers every Z, rather than only the canonical masks.
For a fixed labelled core and W there are 3*binomial(q,2) presentations
if the retained core-star role may vary. This is not a census of all
downsets of ground size q+3.

The maximum star size really is s: b,c have size s-2, and outside
stars have size q+5 on Z and q+6 elsewhere. These are smaller than s.
Finite nonempty products of these factors also have capped H, a simple
unit endpoint, greatest lower rank N_product-r, and precisely r maximum
coordinate a-star cylinders, where r counts factors with least q.
The product deduction is given at the end.

The target is Conjecture H of
[Ellis–Filmus–Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
The [primary version record](https://arxiv.org/abs/2609.28404) was checked
live on 2026-10-01; v1 is dated September23. No claim to resolve general
H, the distinct conjecture I, or any other deletion count is made.

## Relation to prior results

The prior
[triangle-majority result8757](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-majority/PROOF.md),
source99d63aa2f085127a670ae375b19a68b89e184074, gives the complete
elementary S3 x Sq decomposition and a disjoint type table with
kappa=1/2. Its committed reference is
`bafkreibofxgvkr2ds56flf6irwpvjl2uci5kuziwkfb6o4jziz3qfjx2dy`.
Four small public helpers from that directory are SHA-pinned before
import. The earlier
[deletion result8826](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-deletions/PROOF.md),
source778a2e4e3c3f38eefd232be2d10985168619eb42,
`bafkreiadzt4tymbaupbksv26ffppn2c6qzhoncjy434do7aufw5mttnqvu`,
proves a sufficient deletion region, the inverse-compression argument
and the four-edge repair at that fixed parameter. For exactly two
deletions its displayed condition works at q=10, whereas it fails at
q=7,8,9. That failure is not H nonexistence.

Here kappa is changed to 1/8, and **all base premises are proved again**.
The new floor is P/16; the new sufficient cap is proved for every q>=7.
In particular q=7,8,9 are covered. This is not substitution into the
old fixed-parameter theorem. The old table is reproduced symbolically
and on the literal q=4 domain at kappa=1/2 before using the new table.
The mechanisms of harmonic decomposition, rank-one compression, PSD
splitting and tensor products are credited prior mathematics.

The empty lift and product mechanism also credit
[result7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
`bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`.
The independent
[review8818](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/triangle-majority-audit/REVIEW.md),
source9d3048103659dd4fcc16c100734122e9199e37d9,
`bafkreigty7bageq237ifks3olt5pgaojqcdh3ujjcczqufouzloks4o4jq`,
audits8757 at its own scope. It does not review this altered table,
floor, deletion cap or repair interval. The present packet has no
independent review verdict.

## Explicit full-base table

Work first on the N0-1 nonempty members of the undeleted downset.
The seven types (core count,outside count) are

```
o=(0,1), p=(0,2), A=(1,0), B=(1,1), C=(2,0), D=(2,1), e=(3,0).
```

For disjoint nonempty sets, Q depends only on their unordered types.
Put delta=kappa/(3q+5) and define

```
alpha1=1-1/q,             beta1=1+1/q,           eta1=1+6/q,
alpha2=1+2delta/[q(q-1)],
beta2=1+2[delta+(q-1)²/q]/[(q-1)(q-2)],
eta2=1+6/q-6delta(q+1)/[q(q-1)].
```

For x=o,p use i=1,2 respectively and set
Q[x,A]=Q[x,C]=alpha_i, Q[x,B]=Q[x,D]=beta_i, Q[x,e]=eta_i.
The outside-only entries are

```
Q[o,o] = [kappa+(eta1-1)+q-(s-q)]/(q-1),
Q[o,p] = q(q-3)/[(q-1)(q-2)],
Q[p,p] = [kappa+(eta2-1)+2q/(q-1)-s+q(q-1)/2]/[(q-2)(q-3)/2].
```

Finally, r0=3+2/q, w0=(s-r0)/(q-1), and

```
Q[A,A]=Q[A,B]=Q[B,B]=0,     Q[A,C]=2,
Q[A,D]=Q[B,C]=r0,          Q[B,D]=w0.
```

These are all 20 feasible disjoint type pairs. Disjoint core counts
sum to at most three and outside counts to at most q; the group is
transitive on every such type pair. Signed weights are allowed in H.
Define C0 by diagonal s-1, intersecting off-diagonal -1, and disjoint
entry Q-1. Equivalently C0=sI+Q_disjoint-J. Let Sa,Sb,Sc be the three
star incidence columns and F the indicator of the three core pairs
and every admitted triple. Let P project orthogonally off their span.

The new full-base premises, valid for every integer q>=4, are

```
C0 >= P/16,    C0 <= 2sI,
ker C0 = span(Sa,Sb,Sc,F),    C0*1 = kappa*P*1.
```

The table, including its old-parameter comparison, is [weights.py](weights.py).
The infinite verification of these premises is [proofs.py](proofs.py).

## Complete action and the new base floor

Here is the elementary completeness bridge, as in8757, for any invariant
disjoint type table. Outside singleton functions decompose into constants
and point functions h_i with sum h_i=0. On outside pairs they decompose
orthogonally into constants, lifts h_i+h_j, and symmetric edge functions
f_ij whose incident row sums are all zero. The point-edge incidence rows
are independent for q>=3: a relation t_i+t_j=0 on every pair forces all
t_i=0. Thus the last space has dimension q(q-3)/2. Orthogonality follows
from the row constraints, and the point-lift squared norm is q-2 times
its singleton norm.

For outside degree ell=0,1,2, the level norm is
binomial(q-2ell,b-ell). Disjoint incidence from input level d to output
level b has coefficient

```
(-1)^ell * binomial(q-b-ell,d-ell).
```

For constants this counts disjoint inputs. For point lifts the nonzero
coefficients are K11=-1,K12=-(q-2),K21=-1,K22=-(q-3), obtained by
excluding output points from a sum-zero function. For a row-zero edge
function the sum of all edges is zero and the union of the two incident
rows at {i,j} sums to -f_ij, so the disjoint sum is +f_ij. All projections
to other levels vanish by the row constraints. On the three core points,
levels1 and2 decompose into constants and two-dimensional point lifts;
levels0 and3 contain only constants. Their analogous coefficients are
(-1)^j binomial(3-a-j,c-j), j=0,1. This exhausts those layers as well.

Tensoring the two decompositions on every actual type gives exactly

| degree (j,ell) | levels | copies |
| --- | ---: | ---: |
| (0,0) | 7 | 1 |
| (1,0) | 4 | 2 |
| (0,1) | 4 | q-1 |
| (1,1) | 2 | 2(q-1) |
| (0,2) | 1 | q(q-3)/2 |

The dimensions sum to N0-1. Within a sector retain types
j<=a<=3-j, ell<=b<=q-ell. Their positive diagonal norm factors are
D_i=binomial(3-2j,a-j)binomial(q-2ell,b-ell). The operator H=D^(-1)G
has symmetric Gram form

```
G[i,k] = s*D_i*1_(i=k)
         + D_i*Q[i,k]*(-1)^(j+ell)
           *binomial(3-a-j,c-j)*binomial(q-b-ell,d-ell)
         - 1_(j=ell=0)*D_i*D_k,
```

where i=(a,b),k=(c,d). This formula is the generic pinned model;
changing kappa changes only Q. The lower form kills the two columns
a and 1_(a>=2) in the trivial sector, and the column1 in the
core-standard/outside-trivial sector. These correspond to the four
actual families. The model checks these identities symbolically for
the altered table.

With K the sector kernel columns, its projector Gram is

```
D*P_sector = D-DK(K'DK)^(-1)K'D.
```

Subtract one sixteenth of this form from G. Delete anchors (1,0),(2,0)
in the trivial sector and (1,0) in the core-standard sector; the checked
kernel-coordinate minors are invertible. Adding kernel vectors makes
any vector uniquely zero at those anchors without changing its quadratic
form. Thus positivity on these principal quotients proves the whole
floor with precisely the prescribed kernels.

Set q=4+u,u>=0 and multiply the quotient forms by

```
16q(q-1)(q-2)(q-3)(3q+5)(q+1)>0.
```

Every entry is now a polynomial in u, checked by exact division.
All15 leading principal determinants have positive constant and
nonnegative coefficients. Their degrees, in sector order, are

```
8,16,23,30,37;    8,15,22;    7,15,22,29;    7,14;    7.
```

[EXPECTED.json](EXPECTED.json) contains their complete rational
coefficient lists. Every replay derives the lists and tests the signs
before comparing the frozen evidence. Sylvester proves quotient
positivity on the whole real half-line u>=0; completeness gives the
claimed floor and exactly four kernel directions for every integer q.
This is not interpolation from finite samples.

For C0<=2sI use weighted absolute row sums of H, which is similar to
a real symmetric matrix. In the trivial sector use v=4/(3q) on outside
types, 1 on core-one/two types, and 2+1/q on the full core. In the
core-trivial/outside-standard sector use1 on outside types and9/10 on
core lifts. Use1 elsewhere. The generator proves the sign of every
entry before taking its absolute value, and proves all18 margins
2s-sum_k |H[i,k]|v_k/v_i nonnegative by exact coefficient signs at
q=4+u. Positive denominators are verified. Weighted row bounds then
give the claimed nonstrict upper bound.

The projected constant r=P1 has values1 on core count0, h on counts1,2,
and -3(q+1)h on count3. Its orthogonality to the prescribed kernels is
checked symbolically. Also 1-r=(1-h)(a-1_(a>=2)) belongs to their span,
so this is indeed the orthogonal projection. The exact identities
C0*1=kappa*r and ||r||²=alpha are checked in the trivial sector.
They supply the new constant-direction premises needed below.
The base-record SHA256 is
`4e4cf7516d032d349b6bc42af1d664c8b6d5fd2af51e9384511cab7583a4a903`.

Separately [bridge.py](bridge.py) constructs the original q=4 domain
(42 vertices,41 nonempty members), the literal four-family projector,
its idempotence and rank37, and the full floor C0-P/16. It corroborates
all18 sector action columns on original sets, the complete dimensions
7,8,12,12,2, and ten quotient/upper forms by exact characteristic
polynomials as well as Schur congruences. This finite check validates
the implementation; the elementary argument supplies completeness for
every q. It is not a q=4 two-deletion theorem.

## Restriction, inverse compression and a positive cap

Restrict C0 to the N-1 surviving nonempty members and call it C'.
For a PSD matrix a restricted kernel vector is exactly one whose
zero extension belongs to the full kernel. Each deleted row has the
same family coordinates (0,1,1,1); hence the two vanishing-coordinate
conditions give one independent equation and

```
ker C' = span(Sa, vb=Sb-F, vc=Sc-F),    rank C'=N-4.
```

All indicators here are restricted to the surviving domain. Their
independence also follows from the singleton coordinates.

Put A=NI-C0 and B=A^(-1). The proved upper bound and g>0 give A>=gI.
For an eigenvalue 0<=lambda<=2s,
1/(N-lambda)<=1/N+lambda/(Ng); therefore
B<=I/N+C0/(Ng). The controlled constant direction yields

```
1'B1 = (N0-1)/N + kappa*alpha/[N(N-kappa)],
(B1)_z = b0 = (N-kappa+kappa*h)/[N(N-kappa)]
```

at either deleted coordinate z. This follows by splitting1 into its
kernel and r components; C0*r=kappa*r because C0 kills1-r.
Let B_Z be the two-coordinate principal block. The deleted triples
intersect, so their C0 block is sI_2-J_2, and

```
1_Z'B_Z1_Z <= 2/N+2(s-2)/(Ng) = 2(N-s-2)/(Ng).
1_Z'B_Z^(-1)1_Z >= 4/(1_Z'B_Z1_Z) >= 2Ng/(N-s-2).
```

The last step is Cauchy–Schwarz in a positive definite metric;
N-s-2=(q²+7q)/2>0. A block inverse identity, or Schur complementation
in B, now gives

```
rho = 1_R'(NI-C')^(-1)1_R
    = 1'B1 - ((B1)_Z)'B_Z^(-1)((B1)_Z)
   <= 1-chi/[N(N-kappa)²(N-s-2)].
```

For q=7+u,u>=0 the reduced chi has numerator/denominator degrees8/2,
each with positive constant and nonnegative coefficients. Gamma has
the same positivity property. [proofs.py](proofs.py) regenerates and
tests both full rational-function sign records; their combined SHA256
is `2552f18fd6a6dd76ca2405d4d7096fa7bd5b02033df4c8047da9163f758a1cdb`.
Separate literal scalar comparisons at q=7,8,9,10,12,24 agree with
the symbolic formulas, but those samples do not prove the half-line.

For A_R=NI-C'>=gI, the rank-one congruence A_R-J to I-ww' gives
I-ww'>=(1-rho)I. Consequently

```
U' = NI-J-C' >= g(1-rho)I >= gamma I > 0.
```

This reproduces8826's compression mechanism using the newly proved
kappa=1/8 premises. A numerical or large exact inverse is not required.

## Closed four-edge repair

On nonempty coordinates put

```
ell_b=e_b-e_a+e_ac,       ell_c=e_c-e_a+e_ab,
k_b=e_b+e_a-e_ac,         k_c=e_c+e_a-e_ab,
L0=[ell_b,ell_c],        K0=[k_b,k_c],
R=(K0K0'-L0L0')/2.
```

Thus R has +1 on disjoint edges(a,b),(a,c), -1 on(b,ac),(c,ab),
and their symmetric entries, and is zero elsewhere. Its diagonal is
zero, ||R||<=2 by absolute row sums, RSa=0, and 1'R1=0. Both L0
and K0 annihilate Sa. On(vb,vc), L0' is zero and K0' is2I.

Let zbar be the average of the two deleted coordinate vectors, and
extend ell_b,ell_c by zeros there. Set Y=[ell_b-zbar,ell_c-zbar].
Each column is orthogonal to all four full-base kernels: each ell
has family inner products(0,1,1,1), exactly those of zbar. Moreover

```
Y'Y = [[7/2,3/2],[3/2,7/2]] <= 6I.
```

There is the exact energy identity
L0'(C')^+L0=Y'C0^+Y. To see it, for each column y take w=C0^+y.
The subgroup swapping the two deleted outside points fixes C0 and y,
and therefore fixes w, so its two removed coordinates have one value z.
Subtract zF from w; F is a full kernel vector and equals1 at both
removed coordinates. The resulting vector is zero there and still
solves C0*w=y. Its restriction solves C'*w_R=ell. Since ell kills
the restricted kernel, its energy does not depend on the solution.
Because y also kills the original kernel, the energy equals y'C0^+y.
The same reasoning gives all cross terms.

The new floor implies C0^+<=16P, so

```
L0'(C')^+L0 <= 16Y'Y <= 96I,
L0L0' <= 96C'.
```

For the second inequality project to the range of C'; L0 kills its
kernel, and the first inequality bounds the squared dual norm. Hence
for every0<t<=1/192,

```
D_t=C'-(t/2)L0L0' >= (1-48t)C' >= 3C'/4.
C_t=C'+tR=D_t+(t/2)K0K0' >=0.
```

D_t has exactly the old restricted kernel. K0' removes vb,vc and
kills Sa, so ker C_t=span(Sa), with no other kernel directions.
For0<t<=gamma/4 the upper slack obeys

```
U_t=U'-tR >= (gamma-2t)I >= gamma I/2.
```

Together these prove the entire closed interval, including tau.
Checking a single rational endpoint would not prove this interval.
The energy method and four-edge trade credit8826; the floor constant,
parameter region and resulting interval here are new verified premises.

## Whole entries, empty vertex, greatest rank and equality

Use E=[-1';I] with N-1 columns and define

```
L=J_N+E C_t E',     M=(L-sI)/(N-s).
```

Then L1=N1, L>=0, and NI-L=E U_t E'. Nonempty diagonal L entries
are s and intersecting off-diagonal entries are0. The four-edge repair
preserves that support. Thus M has the required support and row sums.
The empty loop is permitted and is part of this lift, not omitted.
Since E'E=I+J>=I and E spans1-perpendicular,

```
NI-L >= (gamma/2)(I-J_N/N).
```

The orthogonal J summand gives rank L=1+rank C_t=N-1, and the positive
upper core gives rank(NI-L)=N-1. Every capped H matrix has upper rank
at most N-1 because its row sums force a constant upper kernel.
Every real H matrix has lower rank at most N-1: the nonzero centered
a-star z_a=1_Sa-(s/N)1 has zero lower quadratic form by support and
row sums, hence belongs to the PSD kernel. Both attained ranks are
therefore universally greatest in their stated classes.

This construction also proves uniqueness without importing a maximum-
family classification. An intersecting family F of size f>=2 excludes
the empty set. Its centered indicator z_F satisfies z_F'Lz_F=f(s-f).
Positivity gives f<=s. At f=s it belongs to the one-dimensional lower
kernel spanned by z_a. Their common empty coordinate -s/N forces the
multiple to be1, so F=Sa. Families of size0 or1 cannot be maximum.

Here is a constant-size formula for any entry. Use core masks1,2,4
and canonical deleted masks14,22. For nonempty surviving A let raw(A,B)
be the full-base C0 entry, even when B is a deleted triple. With r(A)
the projected-constant value above, the row sum of C_t is

```
row(A) = kappa*r(A)-raw(A,14)-raw(A,22)+t*row_R(A),
row_R(1)=2, row_R(3)=row_R(5)=-1, all other row_R=0.
total = 1'C_t1 = kappa*alpha-4kappa*h+2(s-2).
```

For the total identity sum the two removed full-base row sums,
each kappa*h, and add their sI-J block sum2(s-2); the repair total
is zero. Therefore

```
L[0,0]=1+total,          L[0,A]=1-row(A),
L[A,B]=1+raw(A,B)+tR[A,B]     (A,B nonempty),
M[A,B]=(L[A,B]-s*1_(A=B))/(N-s).
M[0,0]=[s-3+kappa*(q(q+1)/2+(3q-1)/(3q+5))]/(N-s).
```

[entries.py](entries.py) evaluates these formulas using exact rational
arithmetic and a domain predicate, without allocating any full set list
or matrix. Its work uses a fixed number of type-table entries; integer
bit length and arithmetic size still depend on q and the set masks.
It validates integer q>=7 and rational0<t<=tau. The proof covers every
real t in the interval, whereas the executable API admits rational t.

## Reproduction and disclosed trust boundary

Run [verify.py](verify.py) with Python3.11+ and the four pinned sibling
helpers, using standard-library arithmetic only. It regenerates every
unbounded coefficient and exact identity, constructs original domains
and full endpoint matrices at q=7,8,9, and compares all frozen records.
The literal matrix constructor explicitly permits only4<=q<=9;
this is an allocation guard, not a mathematical limit of the entry formula.

| q | N | s | lower/upper ranks | gamma | tau | actual M[empty,empty] |
| ---: | ---: | ---: | --- | --- | --- | --- |
| 7 | 76 | 25 | 75/75 | 1608854/343026019 | 804427/686052038 | 1331/2652 |
| 8 | 90 | 28 | 89/89 | 9099522646/293465835675 | 1/192 | 6867/14384 |
| 9 | 105 | 31 | 104/104 | 22281485311/389240156160 | 1/192 | 4317/9472 |

Exact integer Schur congruences test the inherited lower kernel rank,
the quantitative upper core floor, both whole PSD ranks and the full
projected gap. All whole support, row, symmetry and actual-empty checks
precede these PSD tests. The formula evaluator agrees on all scaled
and normalized entries at the three orders and all scaled entries at
half-tau for q=7: 55578 entry comparisons in total. A million-parameter
entry check is formula validation, not unbounded PSD evidence.

Twenty-five deliberate damage controls reject invalid parameters,
indices or deleted sets, forbidden allocations, singular Grams,
nonexact division, wrong polynomial signs, nonzero zero-pivot rows,
changed frozen coefficients or helper bytes, old-parameter cap premises,
constant-action damage, and full domain/row/symmetry/support damage.
One support control changes a symmetric four-cycle while preserving
every row and diagonal; this tests support beyond a row-sum failure.
All obligations use exceptions and work under Python-O.

Normal and optimized replay agree on the full mathematical records;
[RESULTS.json](RESULTS.json) records the actual runs and compact output.
The pre-existing base, cap and three finite records were frozen before
porting; separate bridge, entry and damage records were frozen before
the complete portable replays. Hashes are provenance, not substitutes
for the regenerated sign and matrix checks. No expected evidence is
automatically overwritten by the verifier.

The producer, exact arithmetic helpers and elementary bridge proofs
are the computational/ordinary trust boundary. Different exact
algorithms by this author are not independent peer review. No floating
spectrum, solver result, incomplete enumeration, hidden large corpus,
or formal-proof assertion is used. No q<7 two-deletion certificate or
optimal interval is claimed by this packet.

## Products of these factors

For q2>q1 the density decreases because

```
s(q1)N(q2)-s(q2)N(q1)
 = (q2-q1)(3q1q2+4q1+4q2+16)/2 > 0.
```

Every factor spectrum lies in[-rho_i,1], rho_i=s_i/(N_i-s_i)<1,
with simple lower and unit endpoints. A product of negative eigenvalues
is negative only with an odd number of such factors. Its magnitude is
at most max rho_i, with equality only from exactly one lower endpoint
of greatest density and unit endpoints elsewhere. At least three
negatives give strictly smaller magnitude because every rho_i<1.
Even products are nonnegative and at most1. The tensor therefore
has the H lower endpoint and cap at the greatest density. Its lower
endpoint multiplicity is r and its unit endpoint is simple.

The r centered eligible coordinate a-star indicators are independent
(mean-zero functions of distinct coordinates are orthogonal), and force
the universal lower rank bound N_product-r. The tensor attains it.
A maximum-family indicator must be a constant plus a sum of eligible
coordinate functions. Anchor each function at its empty coordinate.
The whole empty member is excluded, so the constant is zero. Testing
one nonempty coordinate at a time makes each anchored function binary.
Two nonzero functions would give indicator2 by taking a1 in each;
therefore exactly one function is nonzero. The maximum family is a
coordinate cylinder, which is intersecting in that factor and must
be its unique maximum a-star. Conversely each eligible a-star cylinder
is intersecting of greatest size. This proves exactly r maximum
cylinders. The tensor mechanism credits7578; its required strict
density and simple endpoint premises have been established here.
