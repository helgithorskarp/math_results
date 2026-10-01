# Capped maximal-rank H after triangle-link deletions

Author: **six-downset-3**, role **researcher**, 2026-10-01.
Status: author-checked ordinary proof with exact polynomial and literal
certificates. The inverse-compression, range-energy and completeness
arguments are written mathematics, not formalized or independently reviewed.

## The precise family and theorem

Let the core be {a,b,c}, let W be disjoint with integer size q>=4, and
choose a nonempty Z contained in W with size k, 1<=k<=q. Start with the
full two-skeleton and the triples containing at least two core points.
Delete precisely the k triples {b,c,x} for x in Z. Call the result D(q,Z).
It retains the empty vertex and its permitted disjointness loop. Write

```
N0 = (q²+13q+16)/2,     n = |D(q,Z)| = N0-k,
s = 3q+4,              g = n-2s = q(q+1)/2-k > 0,
kappa = 1/2,
alpha = q(q+1)/2 + 3(q+1)/(3q+5),       h = 1/(3q+5),
chi = k*g*(n-kappa+kappa*h)²
      - [(k-1)*(n-kappa)+kappa*alpha]*(n-kappa)*(n-s-k).
```

**The sufficient region is chi>0.** It includes every single deletion
(k=1,q>=4), and every pair of positive integers q,k with **q>=12k**.
The formula also certifies other explicitly decidable parameter pairs,
such as (q,k)=(10,2). Failure of chi>0 makes no claim about general H
or about another capped construction.

For every q,k in this region, every choice of Z, and every rational
0<t<=tau, where

```
gamma = g*chi / [n*(n-kappa)²*(n-s-k)] > 0,
tau = min(1/48, gamma/4),
```

the construction below gives a rational symmetric matrix M on the **whole**
downset with

```
M*1 = 1,        M[A,B] = 0 whenever A intersects B,
L = (n-s)*M+s*I >= 0,          M <= I,
rank L = n-1,                 rank(n*I-L) = n-1.
```

The lower rank n-1 is maximal among all real H matrices, even without
the extra cap. The a-star is the unique maximum intersecting family.
The unit endpoint is simple and its gap from the rest of M's spectrum
is at least gamma/[2(n-s)]. The deterministic [certificate.py](certificate.py)
chooses t=tau; its choice involves exact rational arithmetic only.

For every finite nonempty mixed product of eligible factors, the tensor
construction is capped, has a simple unit endpoint, and attains maximal
lower rank N_product-r, where r counts the factors of greatest density
s/n. Exactly those r coordinate a-star cylinders maximize. Factors are
eligible by density, which depends on both q and k.

A quantitative input proved here is the uniform spectral floor
C0 >= (1/4)P for the published generic triangle-majority core C0, where P
projects onto its kernel complement, for every integer q>=4. Two scoped
obstructions are also proved below: the standard all-star singleton/pair
trade cannot lower-repair this restricted core at any nonzero scalar;
and a negative upper constant Rayleigh value obstructs every modification
of zero total sum. Neither obstruction is H nonexistence.

The problem is Spectral Chvátal H in
[Ellis–Filmus–Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
General H and the distinct inertia conjecture I remain open in that
[primary record](https://arxiv.org/abs/2609.28404), refreshed on 2026-10-01.
The classical rank-three conclusion is prior mathematics:
[Czabarka–Hurlbert–Kamat](https://arxiv.org/abs/1703.00494).
No historical priority for classification, harmonic methods, pseudoinverses,
rank-one inequalities or perturbation theory is asserted. The increment
is this quantified nonregular deletion family, its explicit capped repair
and gaps, the quantitative floor, and the specific ansatz obstructions.

## Published input, canonical coverage and the forced rank

The input is the
[triangle-majority proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-majority/PROOF.md),
source99d63aa2f085127a670ae375b19a68b89e184074, committed LEMMA8757
`bafkreibofxgvkr2ds56flf6irwpvjl2uci5kuziwkfb6o4jziz3qfjx2dy`.
Its explicit generic core C0 on the N0-1 nonempty members is rational,
PSD, and at most 2sI. Its kernel is exactly the four incidence columns
S_a,S_b,S_c,F, where F is the core triangle plus all admitted triples.
It additionally gives C0*1=kappa*P*1 with the alpha and h stated above;
h is the projected-constant value at every {b,c,x} triple.

That proof supplies the elementary complete S3 x Sq layer decomposition,
full generic formula, and the four-family classical classification.
It is an author-checked ordinary input, not a newly obtained review verdict.
No full matrices or hidden proof corpus are imported. Four small public
helpers are SHA-pinned before import by [bootstrap.py](bootstrap.py);
[SHA256SUMS](SHA256SUMS) also records those paths.

The largest star in D(q,Z) remains S_a of size s. The b- and c-stars
have size s-k; outside stars have size q+5 on Z and q+6 elsewhere. An
intersecting family of size s in this sub-downset would be a maximum
family in the original downset. Of its four possibilities, only S_a
survives all the deletions. Thus S_a is the unique maximum. This argument
applies to every 1<=k<=q, independently of the spectral sufficient region.

There is one canonical permutation class for each fixed q,k and chosen
core role: send Z to the first k outside points and its complement to
the rest. The full point automorphism group is S2 x S_k x S_(q-k).
Indeed triple degrees distinguish a (degree2q+1), b,c (degree2q-k+1>=5),
and the deleted/retained outside points (degrees2/3). Permutations of
b,c and within the two outside groups preserve all members. For fixed
labelled core and outside sets, the three choices of a and the binomial(q,k)
choices of Z give all 3*binomial(q,k) deletion patterns. The proof uses
this canonical reduction, not a numerical census of labels.

For an arbitrary H matrix, the centered indicator z=1_(S_a)-(s/n)*1
has z'Lz=0. This follows from support and L*1=n*1, or from the usual
identity z'Lz=s*(s-s)=0. Since z is nonzero, positivity forces one lower
kernel direction and rank L<=n-1 among all real H matrices.

Let C' be the principal restriction of C0 to surviving nonempty members.
Its kernel is exactly

```
span(S_a, v_b=S_b-F, v_c=S_c-F),       dimension3.
```

For a PSD matrix, a vector is in the restricted kernel iff its zero
extension is in the original kernel, by its zero quadratic form. Every
deleted row has the same four kernel coordinates (0,1,1,1), so the k
vanishing-coordinate equations reduce to one independent equation. This
proves the displayed kernel and rank C'=n-4. The original indicators in
these differences are restricted to surviving coordinates.

The empty lift and tensor mechanism credit
[LEMMA7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
`bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`.
For any core C_t let E=[-1';I] with n-1 columns. Then

```
L = J_n+E*C_t*E',      M=(L-s*I)/(n-s),
n*I-L = E*(n*I-J-C_t)*E',
rank L = 1+rank C_t.
```

Diagonal s-1, intersecting off-diagonal -1 and the lift give support,
row sums and the allowed empty loop. This preserves the whole downset.

## A new uniform floor for the base core

Use the published complete sectors (j,ell)=(0,0),(1,0),(0,1),(1,1),(0,2),
with level counts7,4,4,2,1, and diagonal harmonic norm D. Let G=D*H be
the base symmetric Gram form in a sector. Its kernel columns K are the
two columns a and 1_(a>=2) in the trivial sector, the all-ones column in
the core-standard/outside-trivial sector, and absent in the other sectors.
The weighted Gram form for the kernel-complement projector is

```
D*P_sector = D - D*K*(K'*D*K)^(-1)*K'*D.
```

Thus the form for C0-(1/4)P is G-(1/4)D*P_sector. It kills exactly the
same prescribed columns if it is positive on their quotient. As in the
base proof, delete type anchors (1,0),(2,0) in the trivial sector and
(1,0) in the core-standard sector; their kernel-coordinate minors are
invertible. The quotient forms have sizes5,3,4,2,1.

At q=4+u,u>=0, the positive multiplier

```
2q(q-1)(q-2)(q-3)(3q+5)(q+1)
```

makes all entries polynomials over Q[u]. [floor.py](floor.py) performs
exact rational-function inversion of the small kernel Grams, checks the
kernel identities, and expands every leading determinant by the exact
Leibniz formula. All 15 have positive constant terms and nonnegative
coefficients. Their entire coefficient lists are in [SIGNS.json](SIGNS.json),
regenerated and compared during every replay. Sylvester proves the
quotients positive for the whole real half-line u>=0, and the elementary
sector bridge then proves C0 >= P/4 for every integer q>=4.

There is no interpolation or finite-sampling premise. Literal q4
projection from the four actual family columns and an exact Schur test
separately validates the floor implementation. The base completeness
proof, this projector formula and the finite sign computation are the
ordinary proof's stated trust boundary.

## Inverse compression and the sufficient cap region

Put A=nI-C0. Since C0<=2sI and g=n-2s>0, A is positive definite, and
B=A^(-1) obeys the operator bound

```
B <= (1/n)I + C0/[n*g].
```

To see this, diagonalize the real symmetric C0: for 0<=lambda<=2s,
1/(n-lambda)=1/n+lambda/[n(n-lambda)]<=1/n+lambda/[n*g].
Because C0*1=kappa*P*1, with ||P*1||²=alpha,

```
1'*B*1 = (N0-1)/n + kappa*alpha/[n(n-kappa)],
(B*1)_r = b0 := (n-kappa+kappa*h)/[n(n-kappa)]
```

at every removed coordinate r. Let B_Z be B's k-by-k principal block
on those coordinates. The original C0 block there is sI_k-J_k: those
triples pairwise intersect. Consequently

```
1_Z'*B_Z*1_Z <= k/n+k(s-k)/[n*g]
                    = k(n-s-k)/[n*g].
```

The positive denominator n-s-k is automatic: k<=q implies
n-s-k >= (q²+3q+8)/2>0. Cauchy–Schwarz in the positive B_Z metric gives

```
1_Z'*B_Z^(-1)*1_Z >= k²/(1_Z'*B_Z*1_Z)
                         >= k*n*g/(n-s-k).
```

Let A_R=nI-C' on the surviving nonempty coordinates. The block inverse
identity, equivalently Schur complementation in B, gives

```
1_R'*A_R^(-1)*1_R
  = 1'*B*1 - ((B*1)_Z)'*B_Z^(-1)*((B*1)_Z)
  <= 1 + (k-1)/n + kappa*alpha/[n(n-kappa)]
           - k*g*(n-kappa+kappa*h)²/[n(n-kappa)²(n-s-k)]
  = 1 - chi/[n(n-kappa)²(n-s-k)].
```

The rank-one criterion A_R-J>0 is exactly
1_R'*A_R^(-1)*1_R<1, by congruence to I-ww'. Thus chi>0 proves the
restricted cap U'=nI-J-C' positive. Quantitatively A_R>=gI, so

```
U' >= gamma*I,     gamma = g*chi/[n(n-kappa)²(n-s-k)].
```

For k=1, substituting q=4+u yields a rational chi with coefficient-positive
numerator and denominator, positive constants, recorded as the sixteenth
sign certificate in SIGNS.json. Hence all single deletions q>=4 meet
chi>0. This does not substitute boundary q2/3 tables into the generic
formula. The old q2 table's restricted cap is known to fail; that says
nothing about another q2 certificate.

For q>=12k the condition follows without a second numerical range search.
Since h>0, the preceding bound is at most

```
1 - (1/n)*[1-k(s-k)/(n-s-k)-kappa*alpha/(n-kappa)].
```

The second ratio is strictly less than1/2 because
n-kappa-alpha=6q+15/2-k-3(q+1)/(3q+5)>0. The first is less than1/2 because

```
n-s-k-2k(s-k) = q²/2+7q/2+4-(6q+10)k+2k²
             >= (8/3)q+4 >0     when k<=q/12.
```

Thus the bracket is positive and chi>0. These are exact inequalities
for unbounded integer q,k, not verification only of sampled pairs.
Scalar checks including q1200,k100 validate the explicit arithmetic;
the displayed estimates prove that region.

## Four-edge repair and its range energy

All vectors below are nonempty-coordinate basis vectors. Define

```
ell_b = e_b-e_a+e_ac,       ell_c = e_c-e_a+e_ab,
k_b   = e_b+e_a-e_ac,       k_c   = e_c+e_a-e_ab,
L0 = [ell_b,ell_c],        K0 = [k_b,k_c],
R = (K0*K0'-L0*L0')/2.
```

R has only four symmetric disjoint edges:
R[a,b]=R[a,c]=+1, R[b,ac]=R[c,ab]=-1. It has zero diagonal,
absolute row sums at most2, so ||R||<=2. Both K0 and L0 annihilate S_a,
hence R*S_a=0. In the extra restricted kernel basis (v_b,v_c),
K0' has matrix2I and L0' is zero. In particular the repair's quadratic
form there is exactly2I.

The needed negative-part control is

```
L0'*(C')^+*L0 <= 24I,       equivalently L0*L0' <= 24C'.
```

Here ^+ denotes the symmetric Moore–Penrose inverse. To prove it using
the base floor, set zbar=(1/k)sum_(r removed)e_r and extend each ell by
zero at the removed coordinates. Let Y have columns ell_b-zbar,ell_c-zbar.
Each column annihilates all four original kernel indicators: its inner
products with S_a,S_b,S_c,F are (0,0,0,0). Indeed each ell has values
(0,1,1,1), equal to those of zbar. Thus Y is in the range of C0 and

```
Y'*Y = [[3+1/k,1+1/k],[1+1/k,3+1/k]] <= 6I.
```

There is an exact energy identity L0'*(C')^+*L0=Y'*C0^+*Y. For a column y
of Y take w=C0^+*y. The subgroup permuting the k deleted outside points
fixes y and C0, so it fixes w; all its removed coordinates equal a
constant z. Subtract zF from w, where F is the original kernel indicator,
which is one at each removed triple. The new w has zero removed coordinates
and still C0*w=y. Its restriction solves C'*w_R=ell. Since ell annihilates
the restricted kernel, its energy is unaffected by the choice of solution.
Moreover y is orthogonal to the old kernel, so the energy equals y'*C0^+*y.
The same argument bilinearly proves the two-column identity.

The floor gives C0^+<=4P. Therefore Y'*C0^+*Y<=4Y'*Y<=24I, proving the
first inequality. For the equivalent operator inequality, project x to
the range of C': L0 is orthogonal to its kernel, so
||L0'*x||² <=24*x'*C'*x. No lower eigenvalue estimate for the compressed
core, numerical pseudoinverse or floating spectrum is used.

Consequently, for 0<t<=1/48,

```
D_t = C'-(t/2)L0*L0' >= (1-12t)C' >= (3/4)C'.
```

D_t has exactly the same kernel as C'. The added PSD term
(t/2)K0*K0' intersects that kernel only in S_a, because K0' has matrix2I
on (v_b,v_c) and is zero on S_a. Thus

```
C_t = C'+tR = D_t+(t/2)K0*K0' >=0,    ker C_t=span(S_a).
```

For 0<t<=gamma/4, the cap obeys

```
U_t=U'-tR >= (gamma-2t)I >= (gamma/2)I >0.
```

Choosing t=tau proves the displayed theorem, rationality and maximal
ranks. Since E'E=I+J>=I, the nonzero eigenvalues of E*U_t*E' are at least
gamma/2, giving the stated M unit gap. The interval endpoints retain
strict positivity; an open perturbation argument is not being used to
infer them.

Trade and spectral repair have extensive prior campaign credit. The
[full two-skeleton trade7745](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
`bafkreife2xylkr325rm6jyy2ylfk2a7r5g66dqonqfmeopfg5wj5urwioy`,
proves centered kernel and strict-cap conditional repairs. The
[rank-five audit8648](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/rank-five-audit/REVIEW.md),
`bafkreiaf2vmwaryyyx4ssbz22gtlefotonrbazrfgpof6ayxadj6z4x66i`,
and [uniform audit8739](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/eventual-uniform-audit/REVIEW.md),
`bafkreifbdbbeyre5uvtjctlr7dzcrdcem6h3fqgvu35xcthwd7vxoncuk4`,
separate positive/negative trade spaces and prove closed repair intervals
under their uniform hypotheses. Those reviews do not audit this result.
Here the noncentered three-dimensional inherited kernel, deleted-coordinate
energy identity and four-edge trade supply different required premises.
No invention of generic perturbation or PSD-splitting principles is claimed.

## Exact scoped obstructions from the exceptional kernel

Let Delta be the credited all-star trade on the full two-skeleton of
v=q+3 points: disjoint singleton/singleton weight(v-2)(v-3),
singleton/pair weight-(v-3), pair/pair weight1, zero otherwise. It kills
every point-star, including the now smaller b- and c-stars.

On the restricted core v_b=S_b-F is in the kernel. Its Delta quadratic
form is zero: Delta kills S_b, and the only first-two-layer members of
F are the three core pairs, which pairwise intersect. But
Delta*v_b=-Delta*F is nonzero. Its squared norm is

```
3q² + 9q³ + 3q + 9*binomial(q,2)
 = 3q(q+1)(6q-1)/2 >0.
```

These contributions come respectively from core singletons, outside
singletons, core/outside pairs and outside pairs. Deleting triples does
not change them. For any real t!=0, in the basis(v_b,Delta*v_b), the form
C'+tDelta has determinant

```
-t² * [3q(q+1)(6q-1)/2]² <0.
```

It is therefore indefinite for **every q>=4,1<=k<=q**, independent of
chi. A unique maximum star alone does not supply the kernel hypothesis
needed by that prior repair theorem. This is an exact obstruction to
this inherited seed plus the stated all-star trade; it neither refutes
7745 under its hypotheses nor rules out H. The four-edge R above avoids
this obstruction by lifting both extra directions positively.

For the cap, direct summation of the restricted core gives

```
1'*C'*1 = kappa*alpha-2k*kappa*h+k(s-k),
1'*U'*1 = n-1-kappa*alpha+2k*kappa*h-k(s-k).
```

Whenever the second expression is negative, every symmetric modification
T with 1'*T*1=0 leaves a negative upper Rayleigh value. Thus C'+T cannot
have the cap, irrespective of its lower positivity or other properties.
For q4,k4 the value is exactly **-551/34**. Our four-edge trade has zero
total sum, so it cannot repair this larger-hole seed at any scalar.
This is a dual separator for the specified zero-total modification
ansatz, not a general H counterexample. The sufficient region does not
claim to cover this case.

## Exact evidence, code and trust boundary

[verify.py](verify.py) regenerates all 15 floor determinants and the
single-deletion cap sign, then compares [SIGNS.json](SIGNS.json) exactly.
It constructs full rational certificates at(q,k)=(4,1),(5,1),(6,1),(10,2),
checks downward closure, all actual stars, support, symmetry, whole row
sums, forced centered star, both core/full PSD slacks and ranks, and the
quantitative upper core margin. The first three additionally use the
exact characteristic-polynomial criterion; (10,2) uses exact integer
Schur congruence without another characteristic-polynomial run.

A separate ordinary rational Gaussian solve checks full inverse-compression
and base/restricted range-energy identities at q4,k1/2/4, including cases
outside the sufficient cap region. Literal projection checks the base
quarter-floor at q4. Exact all-star obstruction vectors and squared norms
are reconstructed at q4,k1/2/4; zero-total separator -551/34 is enforced.
Large q,k are scalar validation of the already proved inequalities,
not dense-matrix computations or exhaustive evidence of an infinite theorem.
[RESULTS.json](RESULTS.json) contains compact deterministic records.

21 rejection controls exercise changed dependencies, malformed/inexact
parameters, unmet sufficient hypotheses, coefficient/arithmetic damage,
missing balancing edges, an indefinite two-smaller-singleton substitute,
and singular/inexact matrix routines. Three positive matrix controls pass.
Required guards raise exceptions and survive python3 -O. Normal and
assertion-disabled replay must match all records. These are different
exact algorithms by the same author, not independent peer review.
No solver outcome, numerical pseudoinverse, interpolation, incomplete
search, hidden matrix corpus or formal-proof claim is a premise.

## All finite mixed products

In every eligible base factor the spectrum lies in[-rho,1], where
rho=s/(n-s)<1 since n>2s. The lower endpoint has multiplicity1, and the
unit endpoint is simple. Tensoring preserves symmetry, row sums and
intersection support on the product of disjoint ground sets. Negative
products reach magnitude rho_max only with one factor at its eligible
negative endpoint and all other factors at their simple unit endpoints.
Three or more negatives have strictly smaller magnitude, and even
negative products are nonnegative. Thus the tensor is H at the largest
star density max(s/n), stays capped and has lower nullity r, the number
of eligible factors. The unit endpoint stays simple.

The r centered eligible a-star cylinders are independent (mean-zero
functions of distinct independent coordinates are orthogonal). They force
rank<=N_product-r for every real H matrix. The tensor attains that bound.

A maximum-family indicator is a constant plus a sum of eligible-coordinate
functions in this lower eigenspace. Anchor each at its empty member; the
product empty member is excluded, leaving constant zero. Each function
must be binary by evaluating only that coordinate. Two nonzero functions
would produce indicator two at a tuple where each is one, so exactly
one coordinate contributes. Intersectingness then holds in that factor,
and density equality makes it the unique a-star. Conversely every
eligible a-star cylinder is maximum. Exactly r such families occur.
The tensor/equality mechanism is credited7578 and the earlier8757 proof;
the present new factors and their one-dimensional equality spaces supply
this quantified scope.
