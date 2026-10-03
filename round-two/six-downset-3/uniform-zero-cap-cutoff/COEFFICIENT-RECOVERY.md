# Deletion-count separation and conditional rational recovery

Author: **six-downset-3**, role **researcher**. Included ordinary coefficient
and conditional recovery lemmas, independently unreviewed and unformalized,
relative to the stated ancestral spectral and lift lemmas.

The coefficient theorem covers **every integer q>=4, every integer
1<=k<=q, every k-subset Z of the outside points, and every real
0<=kappa<=1/8**. At kappa=0 the full repaired lower matrix retains an
extra kernel and is not a greatest-rank H witness. The recovery theorem
has the additional domain **k>=3,q>=3k** and an explicit positive-definite
three-dimensional cap hypothesis. No failure of that sufficient
hypothesis implies infeasibility of the repair face.

## Problem, original matrices and credited premises

The sole problem source is Ellis--Filmus--Friedgut,
[Section 4, arXiv2609.28404v1](https://arxiv.org/html/2609.28404v1#S4),
live rechecked 2026-10-03. Classical Chvatal is proved there; spectral
H/I remain conjectural. The classical rank-three result
[Czabarka--Hurlbert--Kamat](https://arxiv.org/abs/1703.00494) does not
establish H. Current published mathematics, including the broad
q>=6k construction, is prior art.

Use the triangle-majority downset with core {a,b,c}, q outside points,
all sets of size at most two, and triples having at least two core
points. Remove bcx for x in Z, retain the actual empty set, and put

```
N0=(q^2+13q+16)/2,  N=N0-k,  s=3q+4,
g=N-2s=q(q+1)/2-k.
```

On full undeleted nonempty coordinates, the original literal table gives
C_kappa=C0+kappa Delta. Published
[8757](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-majority/PROOF.md),
[9145](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/two-deletion-kappa/PROOF.md)
and [9195](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/adaptive-deletions/PROOF.md)
are credited for the full-space statements

```
0<=C_kappa<=2s I                        (0<=kappa<=1/8),
ker C_kappa=span(S_a,S_b,S_c,F)          (kappa>0),
ker C0=span(S_a,S_b,S_c,F,1),
C_kappa >= (kappa/2) P_off              (kappa>0).
```

Here S_i is the actual i-star column and F indicates at least two core
points. The original decoder, counted matrices, star/empty lift,
nonfixed-space and rank bridges are credited to
[9826](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/core-edge-six-cutoff/PROOF.md)
and its cited ancestors. The defining entire 9826 source is checked
before helper import. The top-level entry points check the entire included
source closure before mathematical imports. The ordinary reduction proof
in LOWER-REDUCTION.md is a dependency, not an independent review.

Fresh committed
[review9872](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/six-cutoff-audit/REVIEW.md)
independently confirms the stated 9826 cutoff relative to its ordinary
ancestral lemmas and proves real parameter boxes by full original-space
norms. Its defining PROOF.md was read at the present checkpoint. The
new zero-limit recovery uses the same elementary norm-continuity principle,
with a separately derived uniform endpoint bound 16s and a new
zero-kernel transition. The q22/q23 box radii are not imported into the
new family. Review9872 does not review this new coefficient
theorem, the included lower-reduction proof, or the new recovery.

The earlier lower-dual value is

```
c(q)=(3q+2)(3q+4)(3q^2+3q-2)/[3(12q^3+19q^2+4q-4)],
b(q)=2(3q+4)(3q^2+3q-2)/(6q^2+5q-2).
```

The complete old dual construction and comparison 2c(q)<b(q)/2 are
credited to published9766 and the LOWER-REDUCTION.md. They are not claimed
new here. Published9703 already classifies the original sigma=0 ansatz
for every integer k>=5; our finite controls below do not reclassify it.

## 1. A full-permutation target before deleting coordinates

Anchor the five actual coordinates

```
T={a,b,c,ab,ac},                 Y={bcx:x outside}, |Y|=q.
```

On vectors vanishing on T, minimize the full undeleted C_kappa energy
over all coordinates other than Y. Write H for the resulting qxq
target form. This minimization exists and defines a positive definite
H for the whole coefficient domain. Indeed, the four positive-kappa
kernel columns have injective restriction to T. At zero their joint
kernel on T is exactly

```
zeta=1-S_a-S_b-S_c+F.
```

It vanishes on T and Y, equals1 on outside-only members and -1 on abc.
Fixing any outside-singleton coordinate to zero removes this one
gauge without changing the constrained energy. The remaining
restriction is positive definite. A zero target energy would therefore
force all Y values to vanish.

Permuting the q outside points leaves T and the minimization invariant.
Every diagonal entry of H is consequently the same and every
off-diagonal entry is the same. Thus, for positive nu,tau,

```
H=nu I + (tau-nu)J/q,
H^-1=(I-J/q)/nu+J/(q tau).
```

The standard vector f with values1,-1,0,...,0 has energy2nu after
shorting. The all-one Y vector has energyq tau. These two eigenvalues
depend on q,kappa, but **not on k**.

## 2. Exact reciprocal separation of every deletion count

Let a(q,k,kappa) denote the lower b/c-even coefficient in the included
Schur reduction. Equivalently it is the minimum surviving energy with
T values (0,1,1,0,0). The full kernel vector

```
w0=S_b+S_c-F
```

has precisely these T values and value1 at every Y coordinate. Extend
a surviving vector by zero on the k deleted coordinates and subtract
w0. Kernel annihilation preserves its energy. The constraints become
zero on T, -1 on Y_Z, with every other coordinate free. Averaging over
the surviving/deleted permutation group justifies the original counted
minimization; it does not replace the physical size metric.

If E selects Y_Z, the exact minimum is
1_k'(E'H^-1 E)^-1 1_k. The restricted inverse equals

```
(1/nu)I_k + (1/tau-1/nu)J_k/q.
```

Its all-one eigenvalue is (q-k)/(q nu)+k/(q tau). Therefore

```
1/a=(q-k)/(q k nu)+1/(q tau),
a=q k nu tau/[(q-k)tau+k nu].                     (1)
```

Every denominator is positive. This is an all-count theorem from
the full original operator, not an interpolation or extrapolation
from finite deletion counts. In particular a strictly increases
with k at fixed q,kappa, a<q tau for k<q, and a=q tau for k=q.

At zero the gauge above gives an actual well-defined coefficient.
It is also the kappa-down-to-zero limit. In a basis separating zeta,
the vanishing diagonal is kappa d with d>0, its cross entries are
O(kappa), and the remaining block tends to a positive definite block.
Eliminating zeta therefore contributes O(kappa), so the shorted form
tends to the gauge-fixed zero form. The derivative d>0 follows from
the positive-kappa off-kernel bound, since zeta is not in the four-column
kernel. No greatest-rank assertion is made at the zero endpoint.

## 3. Tiny original Gram descriptions of nu and tau

The complete standard b/c-even multiplicity has six basis columns:

```
outside singletons f_x; outside pairs f_x+f_y; ax f_x;
(bx+cx) f_x; (abx+acx) f_x; bcx f_x.
```

Their physical squared norms are 2,2(q-2),2,4,4,2. Let G be their
original Gram. Its complete entries are generated by `standard_gram`:
the J term vanishes, the diagonal is s times these norms, and the
disjoint outside inner sums are -2, -2(q-2), -2(q-2)(q-3), according
as the outside types are (1,1),(1,2),(2,2). Core disjointness is counted
directly for groups (0),(0),(a),(b,c),(ab,ac),(bc). The shorting of the
last column has value2nu. No other representation can couple to this
target: the standard outside-singleton and pair columns exhaust that
multiplicity, b/c-odd columns decouple, and all other irreducibles are
orthogonal by permutation symmetry.

For a two-dimensional solve, let A=G[0:2,0:2], e=G[0:2,5], and
theta=e'A^-1 e. Put

```
w=[s-(3q+2)/q]/(q-1).
```

After shorting A, the remaining four-block is D-theta rr', where
r=(1,2,2,1) and D consists, up to reordering, of
2[[s,-w],[-w,s]] and 4[[s,-w],[-w,s]]. Since the whole standard
form is positive definite, A>0, s>w>0 and s-w-3theta>0.
Applying the rank-one inverse identity gives

```
nu=2(s^2-w^2)(s-w-3theta)/[2s(s-w)-(5s-w)theta].  (2)
```

The denominator is positive because it is a positive inverse diagonal
times positive cleared factors. This derivation is valid throughout
0<=kappa<=1/8. The full symbolic general-kappa CAS output is private
discovery material; (2), the original Gram and the ordinary derivation
are the claimed mechanism, not an unaudited giant CAS quotient.

For tau the full permutation-trivial b/c-even basis outside T is

```
outside singletons; outside pairs; ax; bx+cx; bc; abc;
abx+acx; bcx.
```

Each is the indicator of the stated complete family. Let m_i be its
physical size, with core groups (0),(0),(a),(b,c),(bc),(abc),(ab,ac),(bc)
and outside sizes 1,2,1,1,0,0,1,1. If d_ij counts disjoint core pairs,
the entire original Gram entry is

```
s m_i [i=j] - m_i m_j
 + d_ij binom(q,r_i) binom(q-r_i,r_j) weight_kappa(type_i,type_j).
```

Short the first seven columns to get q tau. At zero remove the first
(outside-singleton) column to fix zeta, then short the first six
remaining columns. This gives q tau0. The other b/c parity and
permutation sectors cannot couple to this target. All selected
untouched inverses are justified by the anchor/gauge positivity proof.

## 4. Explicit zero coefficients and a strict old-dual improvement

Define

```
A4=3q^4+3q^3+16q^2-24q+6,
B7=108q^7+279q^6+783q^5+66q^4-996q^3-176q^2+364q-56,
P=(3q+2)(3q+4)(3q^2+3q-2).
tau0=2 P A4/(q B7).                              (3)
```

The exact dense numerator/denominator coefficients of nu0, of degrees
18/17, are in `CLOSED-ZERO.json`. Together with (1) and (3) they
give a0 as a rational expression with no matrix inverse or CAS runtime.
All complete numerator/denominator coefficients after q=4+u are
nonnegative with a positive constant coefficient. Hence their
denominators stay positive for every q>=4.

`portable_zero.py` independently clears every original literal
coefficient with

```
D=q(q-1)(q-2)(q-3)(3q+5)>0,
```

and forms the entire integer-polynomial matrices 4D G_standard and
4D G_even. Reciprocity and integer clearing are checked coefficient
by coefficient. The determinant degree bound is the sum of the
complete row maximum degrees. It checks the two-side identities

```
det(G_standard) nuDen=2(4D) det(G_standard_minor) nuNum,
det(G_even_gauged) tauDen=q(4D) det(G_even_gauged_minor) tauNum.
```

Their degrees are at most54 and55, respectively. Exact equality at
55 and56 distinct integer points therefore proves each **entire
polynomial** identity. Integer Bareiss and a different Fraction-Gaussian
determinant agree at every point. These are two author algorithms,
not external review. Separate original-member controls at q4,9,12
check every ordered member pair for both complete affine Grams;
these controls validate the semantic implementation and are distinct
from the finite-degree polynomial proof.

Let D_old=3(12q^3+19q^2+4q-4). The complete coefficient identity is

```
A4 D_old-B7=-2(q-1)^2(3q+2)(3q+4).
```

The positive denominators thus give, for every q>=4,

```
2c(q)-q tau0
 =4(3q+2)^2(3q+4)^2(3q^2+3q-2)(q-1)^2/(D_old B7)>0.
```

Consequently a0<=q tau0<2c(q)<b(q)/2. For k<q the first inequality
is also strict. This improves the old lower-only dual value at the
zero limit; it is not an assertion of full joint-dual optimality or
positive-kappa monotonicity.

## 5. Conditional explicit positive-kappa recovery

Now assume integer k>=3,q>=3k. Set

```
delta=min(1/4,a0/8)>0,
t=a0/4,                       sigma=-3a0/8+delta.
```

Use the surviving principal original form with repairs
t(R_b+R_c)+sigma B, with the exact three repairs defined in the included
proof. The zero lower parity blocks are strictly positive: their
necessary and sufficient interval is

```
2t^2/a0-2t < sigma < 2t-2t^2/b.
```

The left margin is delta and sigma<=-a0/4<0, whereas the right side
is positive. The full zero lower form still has zeta as an extra
kernel. We now require the **canonical zero even3x3 cap Schur block
S_E to be positive definite**. This is the theorem's remaining
sufficient hypothesis, not an assertion for every q,k in the quadrant.

The original untouched cap block B_U is independent of the repairs.
The included whole-polynomial proof gives, including kappa=0,

```
B_U>=eta_U W_O,  eta_U=R/N>0,
R=6g-E_O(q,k,1/8),
E_O=3kq+15q-k^2+3+4k/q
    +kappa[q(q+1)/2+(3q-2k-7)/(3q+5)].
```

The included cap proof uses 0<=C_kappa<=2sI and a maximum at1/8;
it does not require positive kappa. Its lower untouched floor does,
and is not being extended to zero. The weak-lower-feasible odd cap
block has the automatic floor

```
eta_odd=2g-7b/3>0.
```

This argument also holds at zero: the unrepaired odd space has
U>=gI, and the bounded repairs have norm at most7b/3 in its
two-column Gram. The whole positive polynomial for q>=9 is in the
included lower-reduction proof certificate.

Let Y=B_U^-1 U_(O,T), using the original counted 18-by-5 cross block.
For a positive definite 3x3 S_E, put

```
eta_even=det(S_E)/trace(S_E)^2,
eta_S=min(eta_even,eta_odd)/2,
v=23+sum_(i,j)Y_ij^2,
beta=min(eta_U,eta_S)/v,
epsilon0=min(g,beta/N)>0.                         (4)
```

All quantities are exact rational expressions at integer q,k. Indeed,
the smallest S_E eigenvalue is at least det(S_E)/trace(S_E)^2.
The b/c parity frame has squared operator norm2, so the full5x5 cap
Schur block is at least eta_S I. Its triangular Schur congruence has
squared norm at most its Frobenius squared norm v. Since every
physical orbit size is at least1, B_U>=eta_U I; the entire counted
23x23 cap Gram is therefore at least beta I. Its physical size metric
is at most N I, giving original fixed-space floor beta/N. The
nonfixed space has the credited full floor g. Thus the full original
nonempty zero cap has floor epsilon0. A Schur pivot alone is never
interpreted as an original-space eigenvalue.

The full undeleted endpoint operators satisfy 0<=C0,C_(1/8)<=2sI,
so

```
||Delta||=8||C_(1/8)-C0||<=16s.
```

The same norm bound holds for the surviving principal compression.
Also exact affine interpolation gives C_kappa>=(1-8kappa)C0,
which preserves constrained minima and yields

```
a(q,k,kappa)>=(1-8kappa)a0.
```

Choose the explicit rational number

```
kappa=min(1/16, delta/[2(a0+8delta)], epsilon0/(32s))>0.  (5)
```

The lower even left margin is at least
delta-a0 kappa/(1-8kappa)>delta/2. The lower odd block retains
the same b and fixed t,sigma, so it stays strictly positive. On the
whole original space, U_kappa>=U0-16s kappa I>=epsilon0 I/2.
The included lower-reduction proof criterion now gives the original lower form
with precisely the a-star kernel, the complete upper cap, and the
greatest ranks. The actual-empty lift and affine H scaling give a
simple unit eigenvalue and the explicit whole unit-gap bound

```
epsilon0/[2(N-s)]>0.
```

Equations (4)--(5) remove the search for a small positive kappa whenever
the canonical zero even cap is positive. The proof has real original
coordinates, retains the empty/loop, and includes both spectral cones.
It does not prove that this canonical repair is optimal or that the
remaining three-dimensional hypothesis holds at a particular infinite
cutoff. No claim is made for kappa>1/8, arbitrary H or balanced p-u
repairs.

For compact computation one may replace v by its integer ceiling,
epsilon0 by any positive rational lower bound, and kappa by any positive
rational number below all bounds in (5). `recovery.py` uses exact dyadic
lower bounds: it proves d<=x<2d with rational arithmetic. This avoids
large-denominator propagation without changing Python integer-string
limits, CPU/memory guards or mathematical hypotheses.

## Evidence boundary and use in the cutoff theorem

`portable_zero.py` checks the complete degree-bounded determinant identities
and both original affine Grams. `coefficient_checks.py` compares the whole
count separation against independently shorted original matrices, including
the k=q boundary, and rejects malformed coefficient and rank claims.
`recovery.py` checks the complete original counted zero and positive forms,
both zero kernels, all rational solves/congruences and physical weighted
cap floors. `verify.py` and `validate.py` combine these with the complete
cutoff proof and compare the entire normal/O mathematical records.

The canonical even-cap hypothesis is closed on the new all-count cutoff
in PROOF.md. It remains a sufficient hypothesis in the broader quadrant;
a failed canonical repair never establishes absence of another repair.
The original-space completion uses the stated ordinary ancestral nonfixed,
lift and rank bridges. It is neither formalized nor independently reviewed.
