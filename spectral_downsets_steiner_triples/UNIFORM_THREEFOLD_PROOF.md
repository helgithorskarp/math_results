# Uniform capped maximal-rank H for simple threefold triple designs

Author: **six-downset-2**, role **researcher**, 2026-09-30.
Status: complete author-checked written proof, unformalized and not independently
reviewed. The input designs, base strict EKR, sparse trade and tensor mechanism
are prior ingredients. General Spectral Chvátal Conjectures H and I remain open.

## 1. Quantified input and conclusion

Let U be **any simple 2-(v,3,3) design with v>=13**: every unordered pair
of points is in exactly three distinct triples, and triples are not repeated.
Such an input necessarily has odd v. No symmetry, bijective completion map,
or decomposition into three Steiner triple systems is assumed. Let D consist
of the empty set, all singletons and pairs, and U. Write

```
m=b=v(v-1)/2,   r=3(v-1)/2,   N=|D|=v^2+1,
s=v+r=(5v-3)/2,  delta=N-25v/2=(2v^2-25v+2)/2>0.
```

Every coordinate star has size s. There are explicit rational symmetric
matrices Q_c and Q_m, with nonempty diagonal s, zero distinct-intersection
entries, Q1=N1, and 0<=Q<=NI, satisfying

| Matrix | Rank | Constant-complement upper gap | Rank of NI-Q |
|---|---:|---:|---:|
| centered Q_c | N-v-1 | delta | N-1 |
| maximal Q_m | N-v | 3delta/4 | N-1 |

Here an upper gap g means Q restricted to 1-perpendicular is **strictly**
below (N-g)I. Accordingly M=(Q-sI)/(N-s) satisfies Conjecture H and M<=I.
Rank N-v is greatest possible for any real H matrix on D, including ones
without an upper cap. The kernel of Q_m is exactly the v-dimensional
centered-star span. This also supplies a spectral proof that only coordinate
stars are maximum intersecting families; that base strict-EKR conclusion
already follows from the classical rank-three result cited below.

Every finite product of these downsets on disjoint coordinate supports has
capped H. For products of the maximal matrices, write N_* for the product
order, p=max_j(s_j/N_j), and r_*=sum_(j:s_j/N_j=p) v_j. Their H matrix has
rank N_*-r_* and only those r_* largest coordinate stars as equality cases.
Mixed products allow any previously established capped maximal-rank factor
with simple upper endpoint and 0<s_j/N_j<1/2, replacing v_j by its number
of independent maximum coordinate stars. The density restriction matters.

The [twofold theorem](UNIFORM_TWOFOLD_PROOF.md) is the degree-two predecessor,
not a theorem about this input class. The earlier
[three-STS9 theorem](THREE_STS9_PROOF.md) treats a finite decomposable
nine-point subclass outside the present order range. The new increment is
the uniform degree-three spectral formula, its complete incidence/Schur/cap
argument and maximal rank on **all** inputs in the stated range. No census,
new design construction or historical-priority claim is made.

## 2. Formula and complete incidence identities

For a pair p let T(p) be its three distinct completing points. For distinct
x,y put Z_xy=|{p:x,y in T(p)}|-3; set Z_xx=0. For a triple A and x outside
A put f_A(x)=|{p subset A:|p|=2, x in T(p)}|, counting multiplicity across
the three pairs. Define the rational weights

```
a=-1,
w=(v^3-6v^2+23v-36)/((v-4)(v-3)(v-2)),
c=(v^2-6v+11)/((v-3)(v-2)),
d=(v^2-v-4)/((v-4)(v-3)),
h=(v^2+2v-11)/((v-5)(v-3)),
t=(v-1)/(v-5).
```

Set all empty entries of Q_c to one, every nonempty diagonal entry to s,
and distinct intersecting entries to zero. On disjoint nonempty sets use

| Sizes | Entry |
|---|---|
| 1,1 | a+t Z_xy |
| 1,2 | w-d if their union is in U, otherwise w |
| 1,3 | h-t f_A(x) |
| 2,2 | c |
| 2,3 | d |
| 3,3 | t |

Let P,B,R be point/pair incidence, point/triple incidence and pair/triple
containment. Let C_xp=1_(x in T(p)) and H_xA=f_A(x) outside A, zero inside.
Dimensions are v by m, v by b, m by b, v by m, v by b respectively.
Use J of the indicated rectangular size. Direct counting gives

```
PP^T=(v-2)I+J,             BB^T=(r-3)I+3J,
CC^T=(r-3)I+3J+Z,         PC^T=CP^T=3(J-I),
PR=2B,                    RB^T=3P^T+C^T,
CR=B+H,                   BH^T=HB^T=9(J-I)+Z.
```

Every row of C has r ones: a point completes its opposite pair in each
of its r blocks. Thus CC^T has diagonal r, agreeing with the definition
Z_xx=0. Off-diagonal entries are exactly the defining codegrees. C has three
ones per column, so CC^T1=3r1; since r=3(v-1)/2 this also proves Z1=0.
For x!=y, (PC^T)_xy counts the three triples through x,y, using their pair
containing x and excluding y; its diagonal is zero. Each pair's three
blocks give RB^T=3P^T+C^T. The three pairs of A each contribute their
third point inside A once, proving CR=B+H. Finally

```
BH^T=B(R^TC^T-B^T)=3PC^T+CC^T-BB^T=9(J-I)+Z.
```

P,C,B,H have row sums v-1,r,r,2r and column sums 2,3,3,6, respectively.
R has row and column sums three. All entries are nonnegative, including
the multiplicity-valued H. Therefore the nonnegative row/column norm
bound gives ||C||^2<=3r, ||H||^2<=12r and ||R||^2<=9. On sum-zero point
vectors, Z<=3vI follows from CC^T=(r-3)I+Z and 3r-(r-3)=3v.

The six scalar row/star equations are

```
h+(v-4)d+(r-9)t=s,
1+s+(v-3)h-6t+(v-3)(v-4)d/2+(b-3r+8)t=N,
w+(v-3)c+(r-6)d=s,
1+s+(v-2)w-3d+(v-2)(v-3)c/2+(b-2r+3)d=N,
a+(v-2)w-3d+(r-3)h-9t=s,
1+s+(v-1)a+(v-1)(v-2)w/2-rd+(b-r)h-2rt=N.
```

For an outside point x, the numbers of triples in its star disjoint from
a pair p or a triple A are r-6+1_(p+x in U) and r-9+f_A(x), respectively.
These follow by inclusion-exclusion using pair multiplicity three. Their
completion corrections cancel those in the 1,2 and 1,3 entries, giving
the third and first equations. At a singleton indexed x and another star
coordinate y, the 1,1 correction tZ_xy cancels the -tZ_xy supplied by
BH^T in the triple sum. Z1=0 removes its row correction. The point row
uses C1=r1 and H1=2r1. The remaining row counts of disjoint triples are
b-2r+3 for a pair and b-3r+8 for a triple. This proves every displayed
equation's interpretation. Substitution proves all six over Q(v).
Star coordinates inside the indexed set follow from support and diagonal;
the empty row and star sums are N and s. Hence Q_c1=N1 and Q_c x_i=s1
for every star indicator x_i.

## 3. Lower PSD, exact kernel and rank

Let L be the nonempty principal matrix of Q_c-J_N. Its star identities give
L[I_v;P^T;B^T]=0. Consequently L=FKF^T, with full-column-rank F and

```
F=[-P -B; I_m 0; 0 I_b],
K22=(s+c)I-cP^TP+(c-1)J,
K23=dR-dP^TB+(d-1)J,
K33=(s-t)I+tR^TR-tB^TB+(t-1)J.
```

Indeed K is the bottom principal block; the star annihilation determines
the other blocks. The disjointness identities are J-P^TP+I on pairs,
J-P^TB+R on pair/triple coordinates, and J-B^TB+R^TR-I on triples.
Simplicity ensures two distinct triples share at most two points, proving
the last identity. Thus no unverified incidence spectrum is being assumed.

Regular row/column sums separate normalized layer constants from vectors
having sum zero in both layers. Since m=b, the constant block of K is

```
[ 4 -2 ]
[ -2 1 ],
```

PSD of rank one, with kernel (1_m,2*1_b). The identities giving its entries
are s+c-2c(v-1)+(c-1)m=4, 3d-2dr+(d-1)b=-2, and
s+8t-3rt+(t-1)b=1. In particular F^T1=(-1_m,-2*1_b) and L1=0.
The six row/star equations initially leave t free; selecting this constant
triple entry to equal one gives t=(v-1)/(v-5). This is the algebraic
parameter choice, followed by the independent positivity proof below.

On sum-zero pairs the eigenvalues of K22 are

```
alpha1=s-c(v-3)=(3v^2-v-16)/(2(v-2))>v,
alpha2=s+c=(5v^3-26v^2+33v+4)/(2(v-3)(v-2))>2v.
```

The first acts on the image under P^T of sum-zero points; the second acts
on ker(P). For sum-zero triples z, PRz=2Bz, so the projection of Rz onto
the former space is 2P^TBz/(v-2). Resolving K23 along these two orthogonal
spaces gives the exact Schur complement

```
S=(s-t)I+beta R^TR-gamma B^TB,
beta=t-d^2/alpha2,
gamma=t-4d^2/(alpha2(v-2))+d^2(v-4)^2/((v-2)alpha1).
```

The positive weights obey 1<t<=3/2 and d<=2, whence
beta>1-2/v>0. The same projection gives R^TR>=4B^TB/(v-2).
Since BB^T=(r-3)I on sum-zero points, B^TB<=(r-3)I on sum-zero triples.
The bracket below is positive for v>=13, so both inequality directions are
justified:

```
S >= (s-t)I-[t(v-6)/(v-2)+d^2(v-4)^2/((v-2)alpha1)]B^TB
  >= mu I,
mu=2v(v^3-5v^2+v+13)/((v-3)(v-2)(3v^2-v-16))>1/2.
```

For z=v-13>=0 the numerator of mu-1/2 is
19076+6660z+855z^2+48z^3+z^4, over the positive denominator
2(v-3)(v-2)(3v^2-v-16). The numerators of alpha1-v and alpha2-2v
are 192+29z+z^2 and 1304+360z+33z^2+z^3 over
2(v-2) and 2(v-3)(v-2). Also 3v^2-v-16=478+77z+3z^2>0.
All divided factors v-2,v-3,v-4,v-5,alpha1,alpha2 are positive.

K is positive definite on the sum-zero pair/triple space and rank one
on constants, so rank K=m+b-1. Extend L by an empty zero row/column.
Because L1=0 and Q_c=J_N+L, Q_c is PSD of rank m+b=N-v-1. Its kernel
is exactly the span of the v centered stars x_i-(s/N)1 and
e_empty-(1/N)1. Independence follows by comparing empty, singleton and
pair coordinates; the number of these vectors matches the proved nullity.

## 4. Uniform strict upper cap

L preserves the three nonempty layer-constant space and its orthogonal
complement of vectors with sum zero on every layer. On the constant space
it has rank one and trace (v-1)/2+4+1=(v+9)/2<25v/2. On the complement
the following positive weight bounds hold:

```
w<=3/2, c<1, d<=2, h<=5/2, t<=3/2.
```

For w use w=1+3d/(v-2)>0; positivity of c,d,h,t follows directly from
their numerators. The respective bound-minus-weight numerators, after
multiplying by their positive denominators, are

| Bound | Numerator | Positive denominator |
|---|---|---|
| 3/2-w | v(6+11z+z^2) | 2(v-4)(v-3)(v-2) |
| 1-c | 8+z | (v-3)(v-2) |
| 2-d | 28+13z+z^2 | (v-4)(v-3) |
| 5/2-h | 32+34z+3z^2 | 2(v-5)(v-3) |
| 3/2-t | z | 2(v-5) |

The diagonal blocks are bounded above by

```
L11=(s-a)I+tZ<7vI,
L22=(s+c)I-cP^TP<(5v/2)I,
L33=(s-t)I+tR^TR-tB^TB<=(5v/2+21/2)I.
```

Use Z<=3vI and ||R||<=3; all J terms vanish on this complement.
The off-diagonal norms satisfy

```
||L12||<=w sqrt(v-2)+d sqrt(9(v-1)/2)<=6 sqrt(v),
||L13||<=h sqrt(3(v-3)/2)+t sqrt(18(v-1))<=(19/2)sqrt(v),
||L23||<=d[3+sqrt(3(v-2)(v-3)/2)]<=(5/2)v+6.
```

Here L12=-wP-dC, L13=-hB-tH, L23=dR-dP^TB after J terms vanish.
Use sqrt(9/2)<9/4, sqrt(3/2)<5/4, sqrt18<17/4; P and B have norm
sqrt(v-2) and sqrt(3(v-3)/2) between their sum-zero spaces. On each layer
the row/column regularity ensures the relevant maps preserve sum zero.
For the last inequality, sqrt((v-2)(v-3))<v. A nonnegative symmetric
three-by-three comparison matrix bounds the full quadratic form; its top
eigenvalue is at most its largest row sum. Since sqrt(v)<=v/3 for v>=13,
its three row sums are bounded by

```
(73/6)v,     7v+6,     (49/6)v+33/2.
```

Their differences from 25v/2 are v/3, (11v-12)/2 and
(26v-99)/6, all strictly positive. Thus L<25vI/2. Finally
2delta=15+27z+2z^2>0. On 1-perpendicular, Q_c=L, so
NI-Q_c-delta(I-J_N/N) is PSD with only the constant vector in its kernel,
and rank N-1. This proves the asserted centered cap and strict buffer.

## 5. Maximal rank by the credited sparse trade

The full-two-skeleton trade below is prior work of **six-downset-3**,
[KERNEL_TRADE_PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
graph7745, with an independent general-mechanism review by **six-reviewer-1**,
[REVIEW.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_sparse_trade_review1/REVIEW.md),
graph7798. The present increment is its rigorous uniform degree-three
specialization, with an explicit perturbation margin for the new input core.
Neither that review nor reviews of other input classes verify this theorem.

Put k=(v-2)(v-3)/2, eta=delta/(16mk), and Q_m=Q_c+eta E. E has nonempty
diagonal zero, vanishes on distinct intersecting sets, and its nonzero entries
are exactly

| Position | Entry of E |
|---|---:|
| empty,empty | mk |
| empty,singleton | -(v-1)k |
| empty,pair | k |
| disjoint singleton,singleton | 2k |
| disjoint singleton,pair | -(v-3) |
| disjoint pair,pair | 1 |

All triple rows vanish; use symmetry. Row sums cancel using 2m=v(v-1).
For star sums, the empty row gives -(v-1)k+(v-1)k=0. A singleton in
the star has zero sum by support. An outside singleton gives
2k-(v-2)(v-3)=0. A pair in the star likewise has zero sum by support;
an outside pair gives -(v-3)+(v-3)=0. Triple rows vanish.
Thus E1=0 and Ex_i=0. Symmetry, support, prescribed nonempty diagonal,
row sum and centered-star kernel are preserved. The absolute row sums of
E on empty, singleton, pair and triple rows are 4mk, 4(v-1)k, 4k and zero.
Consequently ||E||<=4mk, preserving a strict upper buffer 3delta/4.
This norm bound alone would not establish positivity at a singular Q_c.

For the lower proof extend F by one independent empty column:

```
F_0=[1 0 0; 0 -P -B; 0 I_m 0; 0 0 I_b].
```

Q_m-J_N annihilates every uncentered star, so it equals F_0 K_0 F_0^T,
where K_0 is its principal block on empty, pairs and triples; F_0 has full
column rank. Its normalized constant block is the centered rank-one PSD
block of Section3 with an empty zero row, plus

```
eta*k [sqrt(m);1;0][sqrt(m);1;0]^T.
```

These independent rank-one directions give PSD of rank two. Its kernel
is F_0^T1=(1,-1_m,-2*1_b), or (1,-sqrt(m),-2sqrt(b)) in normalized
constant coordinates. On the sum-zero pair/triple space only K22 changes,
by eta(I-P^TP); its eigenvalues become alpha1'=alpha1-eta(v-3) and
alpha2'=alpha2+eta. Write

```
A=(r-3)d^2(v-4)^2/(v-2)<6v^2,
mu'=mu-A(1/alpha1'-1/alpha1).
```

The same projection/Schur proof works, since beta'=t-d^2/alpha2'>beta>0.
It gives mu' as a lower bound. To check the perturbation quantitatively,

```
eta=(2v^2-25v+2)/(8v(v-1)(v-2)(v-3))<1/(2v^2).
```

Indeed delta<v^2 and 8mk-v^4=v(443+217z+27z^2+z^3)>0, so
16mk>2v^4. The numerator of 6v^2-A over 2(v-3)(v-2) is
153768+54108z+7113z^2+414z^3+9z^4>0. Since alpha1>v, we have
alpha1'>alpha1/2, and the Schur loss satisfies

```
A(1/alpha1'-1/alpha1)
 =A eta(v-3)/(alpha1 alpha1')
 <2*(6v^2)*(1/(2v^2))*v/v^2=6/v.
```

Thus mu'>1/2-6/v>0 for every v>=13. K_0 is positive definite on
sum-zero pairs/triples and rank two on constants, giving rank K_0=m+b.
Since Q_m-J_N is PSD and annihilates constants, Q_m is PSD of rank
m+b+1=N-v. Its kernel is precisely the v centered-star span. The upper
endpoint is simple by the strict 3delta/4 buffer; Q_m(empty,empty)=1+delta/16.

## 6. Rank, equality and product bridges

The star-kernel/rank/equality criterion is prior work of **six-downset-3**,
[REGULAR_SIX_PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md),
graph7627. Briefly, support makes an intersecting indicator of size a have
centered Q quadratic form a(s-a), hence a<=s. At maximum size the centered
indicator belongs to every H kernel. The v centered maximum stars are
independent by empty and singleton coordinates, giving rank<=N-v. If the
kernel is their span, comparison of the empty coordinate forces its star
coefficients to sum to one; singleton coordinates make each coefficient
zero or one. Precisely one star is selected. A maximum family cannot contain
the empty set since s>1. The classical base conclusion is also covered by
[Czabarka--Hurlbert--Kamat, Theorems1.4--1.5](https://arxiv.org/pdf/1703.00494);
in particular s>=31, so Theorem1.5 applies directly.

The capped tensor rule is prior work of **six-downset-1**,
[structural proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
graph7578. Here N>25v/2>2s, so rho_j=s_j/(N_j-s_j)<1. Each normalized
capped factor has spectrum in [-rho_j,1]. Their tensor product preserves
symmetry, support and row sums. A negative product eigenvalue has magnitude
at most max_j rho_j, giving H with the largest star density. For maximal
factors the endpoint one is simple; reaching the largest negative endpoint
requires exactly one factor at a tied largest negative endpoint and every
other factor at one. Any additional eigenvalue of absolute value below one
decreases the magnitude. The negative multiplicity is therefore sum_(ties)
v_j. The product star-kernel criterion proves the rank and equality claims.
Centered products satisfy capped H but have extra negative-endpoint directions
and are outside the maximal-rank product claim.

## 7. Exact reproduction and scope of evidence

[uniform_threefold.py](uniform_threefold.py) checks simplicity and every
pair multiplicity before constructing Q_c and Q_m. Its three literal inputs
are two developed 13-point designs and a union of three block-disjoint STS(15).
The second 13-point fixture develops, modulo13, seeds

```
{0,1,3}, {0,1,9}, {0,3,9}, {1,3,9}, {0,1,4}, {0,2,7}.
```

Its 78 triples are all distinct and every pair occurs three times. All four
three-element faces of {0,1,3,9} occur. Any two of those faces share a pair,
so an STS contains at most one face: this input cannot be a union of three
Steiner triple systems. The obstruction is a four-clique verified literally,
not a failed colouring search. These fixtures are validation examples,
not a classification, and their designs are not claimed new. This particular
input has Z=0, while the other two inputs have nonzero Z: balanced completion
codegrees do not imply a three-STS decomposition.

[threefold_identities.py](threefold_identities.py) verifies 38 rational-function
identities by integer polynomial coefficient comparison over Q(v), including
the six row/star equations and all scalar factorizations used above. It checks
17 strict positive-coefficient certificates in z=v-13, one weak certificate
for t<=3/2, and the exact radical bounds. No CAS is required.
The optional [derive_threefold_sympy.py](derive_threefold_sympy.py) uses
SymPy1.14.0 over Q(v) to reproduce that affine parameter selection and the
Schur expression; its output is [threefold_symbolic.json](threefold_symbolic.json).
That derivation is outside the portable verifier's dependency boundary.
[verify_uniform_threefold.py](verify_uniform_threefold.py) regenerates all
inputs and checks every support, row, star and incidence identity. It checks
four **full** matrices for each input by exact integer Schur congruence:
centered/maximal lower PSD and their claimed buffered uppers. For cyclic13
it independently checks both lower forms with rational Schur. The compact
output is [uniform_threefold_expected.json](uniform_threefold_expected.json).
No symmetry reduction or numerical eigenvalue enters these checks.

The 13-point cases have N=170,s=31, centered/maximal ranks156/157, upper
rank169, delta=15/2 and maximal gap45/8. At15, N=226,s=36,
ranks210/211, upper rank225, delta=77/2 and maximal gap231/8.
Six rejection controls cover excluded small/even weight parameters, a missing
or duplicate input block, removal of the singleton completion correction,
and an indefinite matrix with zero diagonal. The previous smaller-order
twofold verifier was also reproduced unchanged as a baseline.

Run from repository root with CPython3.11+ (tested3.11.2), assertions enabled,
standard library, one process/thread:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/threefold_identities.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/verify_uniform_threefold.py --check
```

Universal scope rests on the ordinary written incidence, Schur, invariant-layer,
norm and equality/tensor bridges, not on the finite examples or polynomial
checker alone. The proof is author-checked, unformalized and not independently
reviewed. No floating fitting, solver status, private corpus or omitted large
certificate is required.

The complete expected-output replay passed in267.48s with43,848KiB maximum
RSS and one thread; the expanded initial run took337.64s/43,376KiB. The
old four-input smaller-order twofold baseline passed unchanged in16.25s.
These are measured costs, not performance guarantees.

The primary target remains
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4);
its [arXiv record](https://arxiv.org/abs/2609.28404) was checked2026-09-30
and lists v1. H and I remain conjectures in that version. The earlier
[seven-weight obstruction](TEMPLATE_OBSTRUCTION.md) does not exclude this
completion-sensitive template. The distinct peer families include complete
rank-three truncations, degree v-2, in
[six-downset-3's theorem](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three/PROOF.md),
graph7930, and all complete rank-four truncations v>=6 in
[its rank-four theorem](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md),
graph7980. Those results are credited context, not a review of this formula.
The predecessor degree-two core at v>=13 has now been independently
verified and strengthened by **six-reviewer-1**,
[twofold review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_twofold_review1/REVIEW.md),
graph8010. Its smaller-order extension and this degree-three formula are
explicitly outside that verdict. Its cap improvement is a separate result.
