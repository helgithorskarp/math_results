# A maximum-row upper cap for dense triple-design Hoffman matrices

Author: **six-downset-2**, role **researcher**, 2026-10-01.
Status: complete author-checked ordinary proof with exact scalar certificates;
unformalized and not independently reviewed. General Spectral Chvátal
Conjectures H and I remain open.

## 1. Quantified extension

Let U be **any existing simple 2-(v,3,l) design**. Assume integer
q=v-2-l>=0 and

```
v>=12, 2v>=5q+10, l=v-2-q.
r=l(v-1)/2, m=v(v-1)/2, b=lv(v-1)/6,
s=v+r, N=1+v+m+b, k=(v-2)(v-3)/2.
```

Existence, integrality of r,b, simplicity and constant pair multiplicity
are hypotheses; the inequalities imply l>=8. No symmetry or Steiner-system
decomposition is required. Let D consist of empty, all singletons, all pairs
and U. Use the explicit centered matrix Q_c from
[the all-orders construction](UNIFORM_LAMBDA_ALL_ORDERS.md), graph8122,
and the same credited sparse trade E. Set

```
D0=l(v^2-10v+27)-6,
t=(v-1)[l(v-3)-6]/D0, u_q=q(q-1)/2,
R1=s+l/3+t u_q v+v/3+qv/2+(3/2+2q)v,
R2=s+4/3+v/3+qv/2+v(v-4)/2,
R3=s+v^2/2+(2q+3/2)v-10,
B=max(R1,R2,R3), delta=N-B.
```

Then **delta>mk/v^2>0**, and

```
Q_c restricted to 1-perpendicular < B I.
For every real 0<eta<=1/(8v^2), Q_m=Q_c+eta E satisfies
Q_m>=0, rank Q_m=N-v,
Q_m restricted to 1-perpendicular < (N-delta/2)I.
```

The centered rank is N-v-1. Both matrices have row sum N, nonempty
diagonal s and zero distinct entries on intersecting sets. Their upper
endpoint N is simple, and both NI-Q have rank N-1. More quantitatively,
NI-Q_c-delta(I-J/N) and NI-Q_m-(delta/2)(I-J/N) have rank N-1 and
are positive definite on 1-perpendicular. The repaired kernel consists
precisely of the v independent centered coordinate stars. Rational eta,
including eta=1/(8v^2), gives a rational H matrix M=(Q_m-sI)/(N-s)
with M<=I.

The new conclusion is the **wider dense upper range and its buffered gap**.
Graph8182 [the previous dense cap](DENSE_COMPLEMENT_CAP.md) required
v>=4(q+1). That range is contained here: for q>=2 the old threshold
implies 2v>=5q+10, and q0/q1 are covered by v>=12. Keeping the singleton
diagonal bound exact and taking the maximum of the three comparison rows
avoids the previous enlargement by q^2 v in the triple row. In the old
range the new B is at most the previous bound, by its row comparisons.
The lower PSD, optimal rank and base strict-EKR conclusions are inherited,
not new all-design existence or new classical EKR results. Previously
capped sparse ranges remain available, with their own hypotheses.

For example q=3,v=13,l=8 gives N=300,s=61,
B=7289/29, delta=1411/29. The previous dense theorem excludes this
input; inserting it into that previous bound would give350>N.
At q=2,v=12 the new B is184 and delta71, improving the old B232,
delta23. At q=1,v=13 the new B is193 and delta159, improving the
old B206. The independent **six-reviewer-5**
[graph8152 review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_lambda_review5/REVIEW.md)
confirms parent8082 and separately proves a missing-STS cap; its verdict
excludes8122 and it has not reviewed this extension. The subsequently
committed **graph8204** [independent all-orders review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_all_orders_review5/REVIEW.md)
confirms8122, including the full real repair interval, lower ranks and
qualified inherited caps. It additionally proves missing-STS caps at7/9
and explicitly gives no verdict on8182. Thus the lower premise here has
independent confirmation; this new upper range remains unreviewed. The
elementary complement identities are credited, as in8182. Earlier complete-layer
constructions already cover q=0 by other matrices. No new design or
design census is claimed, and no upper assertion is made outside the
displayed range.

## 2. Inherited matrix and incidence reduction

For clarity, the unchanged weights are

```
a=-l/3,
c=[v^2-(l+3)v+11l/3]/[(v-2)(v-3)],
d=(v^2-v-4)/[(v-4)(v-3)],
w=s-(v-3)c-(r-2l)d,
h=s-(v-4)d-(r-3l)t.
```

All entries incident with empty in Q_c are one; nonempty diagonal entries
are s. All distinct intersecting entries are zero. On disjoint nonempty
sets the entries by sizes11,12,13,22,23,33 are, respectively,

```
a+t Z_l,xy, w-d*1_(union in U), h-t f_A(x), c, d, t.
```

Here T_l(p) is the set of completing points for pair p,
Z_l,xx=0 and Z_l,xy=|{p:x,y in T_l(p)}|-l(l-1)/2 for x!=y;
f_A(x) counts the three pairs in A completed by an outside point x,
with multiplicity, and is zero inside A. The constructor checks these
literal definitions; it never clamps f_A(x) to one.

Let U_q be the complement of U in all triples, allowing the empty design
at q=0. Let P be point/pair incidence and B_j,R_j,C_j be point/triple,
pair/triple and point/pair completion incidence for U_j, j=l,q.
The counting identities proved in8182 are

```
C_l+C_q=J-P, P C_q^T=C_q P^T=q(J-I),
C_j C_j^T=(r_j-u_j)I+u_j J+Z_j,
C_q R_l=3J-3B_l-H_l,
R_l R_l^T+R_q R_q^T=(v-4)I+P^T P,
r_j=j(v-1)/2, u_j=j(j-1)/2, H_l,xA=f_A(x).
```

In particular Z_l=Z_q, ||C_q||^2<=q^2(v-1)/2 and
Z_l<=u_q v I on sum-zero point vectors. These statements include q=0,1.
For L=Q_c-J_N, the layer-constant space and its orthogonal complement
are invariant. On layer constants its only positive eigenvalue is
l(v+7)/6+1<s. On the spaces with zero sum separately in point, pair
and triple layers the blocks are

```
L11=(s+l/3)I+t Z_l,
L22=(s+c)I-c P^T P,
L33=(s-t)I+t R_l^T R_l-t B_l^T B_l,
L12=(d-w)P+d C_q,
L13=(3t-h)B_l+t C_q R_l,
L23=d(R_l-P^T B_l).
```

The exact checker proves on the *new* parameter range

```
D0>0, 0<c<4/3, 0<d<2, 1<t<2,
|d-w|<1, |3t-h|<2, l(v+7)/6+1<s.
```

Thus all the norm arguments of8182 apply, now certified on the wider
range. In particular, if Pi projects pair space onto ker P and
T=Pi R_l, the complete pair Gram gives ||T||<=sqrt(v-4). For sum-zero
triple z the two outputs in

```
R_l z=Tz+2P^T B_l z/(v-2)
```

are orthogonal. Since PP^T=(v-2)I on sum-zero points,

```
||R_l z||^2-||B_l z||^2
=||Tz||^2+[4/(v-2)-1]||B_l z||^2 <=(v-4)||z||^2.
```

Consequently the diagonal bounds and off-diagonal comparisons are

```
L11 <= D1 I, D1=s+l/3+t u_q v,
L22 < D2 I,  D2=s+4/3,
L33 < D3 I,  D3=s+2(v-5),
||L12|| < a12=v/3+qv/2,
||L13|| < a13=(3/2+2q)v,
||L23|| < a23=v(v-4)/2.
```

The singleton estimate here is intentionally **nonstrict**. To recall
the cross estimates, ||P||=sqrt(v-2),
||B_l||=sqrt(l(v-3)/2), and ||R_l||<=sqrt(2v-6) on sum-zero
triple inputs. Combine these with the preceding weight bounds,
||C_q||<=q sqrt((v-1)/2), sqrt2<3/2 and sqrt(v)<=v/3.
For the last cross block use the triangle inequality applied to

```
R_l-P^T B_l=T-(v-4)P^T B_l/(v-2).
```

It yields
d[sqrt(v-4)+(v-4)sqrt(l(v-3)/(2(v-2)))]<v(v-4)/2,
because l<=v-2, d<2, sqrt(v-4)<=(v-4)/2 and
sqrt((v-3)/2)<(v-2)/4. The final strict comparison follows from
(v-2)^2-8(v-3)=v(v-12)+28>0. This is a sum of operator norms;
no orthogonality of the two input spaces is presumed.

The symmetric nonnegative3-by-3 comparison matrix with diagonals
D1,D2,D3 and cross entries a12,a13,a23 has exactly the row sums
R1,R2,R3 in Section1. Its largest eigenvalue is at most B. If the pair
or triple component of an input is nonzero, its quadratic comparison is
strict because the corresponding diagonal bound is strict. If only the
point component is nonzero, L11<=D1 I<R1 I<=B I, because
a12+a13>0. This proves strictness for every nonzero vector in the
three sum-zero layers despite the nonstrict singleton estimate.
The layer-constant estimate <s<B proves the rest of1-perpendicular.
Since J_N vanishes there, it proves Q_c<B I as claimed.

## 3. Exact gap certificates and the whole real interval

Here are polynomial certificates for all three row gaps. Put

```
A=12v+6v^2(v-1)+2vl(v-1)(v-3), P0=(v-1)(v-2)(v-3),
G1=D0[A-4vl-(22+30q)v^2-3P0]
   -6q(q-1)v^2(v-1)[l(v-3)-6],
G2=A-16v-(4+6q)v^2-6v^2(v-4)-3P0,
G3=A-6v^3-(24q+18)v^2+120v-3P0.
N-R1-mk/v^2=G1/(12vD0),
N-R2-mk/v^2=G2/(12v),
N-R3-mk/v^2=G3/(12v).
```

The following six affine domains, with x,y>=0, cover *all integer*
q>=0,v>=12,2v>=5q+10 exactly. For fixed q use y=0; for the last
two rows y is an integer. The certificates actually prove each sign
for every real x,y>=0 in those parametrizations.

| Domain | q | v | G1 constant | G2 constant | G3 constant |
|---|---|---|---:|---:|---:|
| q0 | 0 | 12+x | 13502160 | 22758 | 18918 |
| q1 | 1 | 12+x | 9124326 | 19518 | 13086 |
| q2 | 2 | 12+x | 4170060 | 16278 | 7254 |
| q4 | 4 | 15+x | 29376 | 36498 | 13788 |
| odd3plus | 3+2y | 13+5y+x | 1894968 | 20272 | 6492 |
| even6plus | 6+2y | 20+5y+x | 5496804 | 128718 | 73038 |

Every coefficient of every shifted G_i is nonnegative, with the listed
strictly positive constant. The full18 small polynomial tables are in
[dense_row_expected.json](dense_row_expected.json) and independently
regenerated by [dense_row_identities.py](dense_row_identities.py).
That checker also verifies all denominator signs and the identities above.
The q4 domain is separated because the continuous even-q quadrant
starting at q4 has a negative coefficient in G1; a negative coefficient
alone would not refute positivity. This finite partition supplies complete
integer coverage without that inconclusive sign test.
It follows that every N-R_i>mk/v^2, hence delta>mk/v^2.

The parent lower PSD and rank theorem applies since v>=12,l>=8.
The trade E annihilates constants and centered stars and has
||E||<=4mk. Thus every real0<eta<=1/(8v^2) incurs possible upper
loss at most mk/(2v^2)<delta/2, proving

```
Q_m|_(1-perp) < [B+mk/(2v^2)]I < (N-delta/2)I.
```

This completes both positive buffer ranks and the simple upper endpoint.
At q4,v15, N436,s78 the narrowest stated boundary has
B=7589/19, delta=695/19, mk/v^2=182/5 and
delta-mk/v^2=17/95>0. Its scalar certificate is exact; it is not
reported as a literal full436-by-436 elimination. At q3,v13 the corresponding
half-gap margin is8773/377>0.

The trade is credited to **six-downset-3**, graph7745
[sparse-trade proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
with its mechanism independently reviewed by **six-reviewer-1**, graph7798
[review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_sparse_trade_review1/REVIEW.md).
No new repair mechanism is claimed.

## 4. Products, checks and trust boundary

Every factor here has density s/N<1/2, since
N-2s=(v-1)[(v-2)/2+l(v-6)/6]>0. Hence the product argument in
Section5 of8182 applies without change to these newly capped factors.
For any finite list on disjoint supports, write N_*=product N_j,
p=max(s_j/N_j), and r_*=sum_(j:s_j/N_j=p) v_j.
The H slack has greatest possible rank N_*-r_* and its kernel is exactly
the r_* centered stars of greatest density. The maximum intersecting
families are precisely these coordinate stars. Mixed products with already
proved capped maximal factors having simple upper endpoint and density
below1/2 retain the same statement, with each factor's independent
maximum-star count in place of v_j. This extends the *capped factor range*;
the tensor and star-kernel arguments are credited to **six-downset-1**,
graph7578 [structural proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
and **six-downset-3**, graph7627
[criterion](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
The classical base strict-EKR conclusion is already covered by
[Czabarka--Hurlbert--Kamat, Theorems1.4--1.5](https://arxiv.org/pdf/1703.00494).

The portable scalar checker verifies **seven exact zero identities and96
strict coefficient certificates**, sixteen on each of the six domains.
Both numerator and denominator must have nonnegative coefficients and
positive constant. Its sparse Fraction rational-function backend is
[bivariate_certificates.py](bivariate_certificates.py); it needs no CAS,
numerical sampling, polynomial GCD or optimizer. The optional independent
[SymPy1.14.0 derivation](derive_dense_row_sympy.py) verifies the same
seven identities and96 signs. All18 shifted G_i tables and both boundary
values agree term for term; the compact CAS output is
[dense_row_symbolic.json](dense_row_symbolic.json).

[dense_row_lambda.py](dense_row_lambda.py) validates the enlarged cap
domain and constructs the unchanged parent matrices. The new literal input
is the complement of the retained nondecomposable simple threefold13
generator from [uniform_threefold.py](uniform_threefold.py): six seeds
{0,1,3},{0,1,9},{0,3,9},{1,3,9},{0,1,4},{0,2,7}, and all translations
modulo13. Its missing design has78 blocks; the input U has208 blocks
and pair multiplicity8. The four faces of{0,1,3,9} witness that the
missing design cannot decompose into three Steiner systems. This is a
retained validation design, not a new construction or census.

[verify_dense_row_lambda.py](verify_dense_row_lambda.py) checks every full
support, row and star equation, the ten parent incidence identities,
complement completion/Z/outside/complete-Gram identities, independent
kernel Gram ranks and matrix hashes. Four independent empty-plus-singleton
principal forms use Fraction Schur; principal forms alone do not certify
full PSD. Ten malformed controls check domain, block corruption, repair
interval, corrupted codegrees, clamped outside multiplicity and false upper/rank
certificates. Its default compact expected output records predicted full
ranks separately from the checks actually performed. No dense matrix
corpus is published.

A bounded300-second preliminary batch used the previously validated
[content-normalized integer Schur backend](content_psd.py). It completed
three full300-by-300 checks: centered rank286, repaired rank287 and
buffered centered upper rank299. It expired during the repaired upper
elimination; that incomplete fourth elimination proves nothing. Expensive
elimination was paused and no resource bound enlarged. The same three
completed full checks remain reproducible with the optional
`--full-schur` flag; the default checker avoids those expensive eliminations.
The full repaired upper form is instead checked by its exact transfer
identity in every entry:

```
NI-Q_m-(delta/2)K = [NI-Q_c-delta K]+(delta/2)K-eta E,
K=I-J/N, E=(Q_m-Q_c)/eta, E1=0,
||E||<=max_i sum_j |E_ij|=17160=4mk,
delta/2-eta*17160=8773/754>0.
```

Symmetry and E1=0 imply (delta/2)K-eta E is strictly positive on
1-perpendicular and zero on constants. Adding it to the completed centered
upper PSD certificate proves that the whole repaired upper form is PSD
with rank299. This is an ordinary operator-norm transfer, not a fourth
direct Schur elimination. The default checker verifies the full identity,
all trade row sums, the exact absolute row bound and strict margin. Its
interpretation explicitly requires the centered upper PSD theorem or
the independently reproducible centered elimination.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/verify_dense_row_lambda.py --check
```

Requires CPython3.11+ standard library, assertions enabled, one mathematical
job/thread. Appending `--full-schur` additionally checks the three full
forms above; it does not perform repaired upper elimination. The full-input
controls validate implementation; universal
coverage rests on the ordinary incidence identities, orthogonal
decomposition, norm bounds, complete affine partition, exact coefficient
certificates and inherited lower theorem. These analytic/completeness
bridges are not proof-assistant formalized. Graph8204 independently confirms
the inherited8122 lower theorem; no review verdict is asserted for this
upper extension or8182.

Primary status was reverified on2026-10-01 in
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4)
and [the version record](https://arxiv.org/abs/2609.28404), still v1.
This covers the quantified design subclass and its products; general H/I
remain conjectures.
