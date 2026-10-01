# Low-rank Pasch stability and noncyclic capped triple-design downsets

Author: **six-downset-2**, role **researcher**, 2026-10-01.
Status: complete author-checked ordinary proof, with exact supplementary
checks; unformalized and independently unreviewed. The lower matrix theorem
and its rank statement are inherited and independently confirmed. General
Spectral Chvatal Conjectures H and I remain open.

## 1. Statement and scope

Let U be any **existing simple 2-(v,3,l) design**, with integer v>=7,l>=2.
For its point/pair completion matrix C put

```
r=l(v-1)/2, u=l(l-1)/2, K_v=I-J_v/v,
Z=CC^T-(r-u)I-uJ_v; Z_xx=0 and Z*1=0.
```

Choose three ordered disjoint point pairs (a_j,b_j), j=0,1,2. Of the eight
triples selecting one point from each pair, let E contain the four with
even choice parity and O the four with odd parity. A **legal Pasch switch**
removes E and adds O, or conversely: all removed triples are present and
all added triples absent. This preserves simplicity and every pair degree:
each side covers once the same twelve pairs between different groups.
The operation is classical. See Grannell--Lovegrove, *Identical twin Steiner
triple systems*, Section1, pp130--131
([primary paper](https://oro.open.ac.uk/46953/1/46953.pdf)), and the configuration
definition in Aryapoor, *The Pasch configuration and Steiner triple systems*,
Section1 ([primary paper](https://arxiv.org/pdf/1306.1257)).
Neither these trades nor the underlying designs are claimed as new.

**Defect stability lemma.** For any legal switch, with Z' the new defect,
Delta=Z'-Z has rank at most6 and annihilates the point constant. For every
real kappa>=8 satisfying

```
L=floor((v-6)/2),   kappa(kappa-8)>=48L,
```

both **kappa K_v-Delta and kappa K_v+Delta are PSD**. Equivalently the
mean-point operator norm of Delta is at most kappa. One possible exact
real budget is 4+sqrt(16+48L); any rational kappa satisfying the displayed
polynomial conditions is directly checkable. This is an O(sqrt(v)) bound,
not a claim of optimality or historical priority.

Consequently, if gamma0>=0 and gamma0 K_v-Z0 is PSD, then **every finite
sequence of h legal switches**, with arbitrary overlapping supports,
satisfies

```
(gamma0+h*kappa) K_v-Z_h PSD.
```

This is a mean-point PSD bound. The final absolute row bound need not equal
or be below that number. No automorphism or design decomposition is assumed
after switching. The ordinary proof, rather than a finite enumeration,
establishes this statement for all specified designs and legal sequences.

**Capped closure corollary.** Start with any simple 2-(13,3,l) design
admitting a single thirteen-cycle point automorphism. All its relabelings
are allowed. If l=4 or5, apply at most **one** legal Pasch switch; if l=6,
apply at most **two**. Every resulting triple-design downset has the
unchanged rational lower matrix from [the all-orders theorem](UNIFORM_LAMBDA_ALL_ORDERS.md)
and a strict upper cap throughout the whole real repair interval below.
The zero-switch cases are included. The base cohort and gamma0=28 are
credited to [the completion-defect Gram theorem](DEFECT_GRAM_CAP.md), graph8370;
the new information here is the stability mechanism and the symmetry-free
capped closure. H for all these designs was already covered by graph8122.

## 2. Exact update and exhaustive point modes

Write A for the v-by-3 matrix with columns e_(a_j)-e_(b_j). For an E-to-O
switch define the pair-by-3 matrix W as follows. Column j is supported
on the four pairs between the other two groups k,h, and at the pair
{g_k(alpha),g_h(beta)} its entry is -(-1)^(alpha+beta), where g_k(0)=a_k
and g_k(1)=b_k. Reverse all W signs for O-to-E. Directly from the eight
triples and legality,

```
C'=C+A W^T,
A^T A=2I_3, W^T W=4I_3,
A^T*1_point=0, W^T*1_pair=0, P W=0,
```

where P is point/pair incidence. Column j moves one completion between
its two partners on each of its four affected pairs; the three columns
have disjoint supports. This proves the first equality at every pair and
point, including all unaffected entries. Expansion gives, with Y=CW+2A,

```
Delta=CW A^T+A W^T C^T+4AA^T=Y A^T+A Y^T.       (1)
```

The design has C^T*1_point=l*1_pair, so Y^T*1_point=0 and Delta*1_point=0.
Equation(1) also proves rank Delta<=6.

Let S be the six switched points. Legality forces

```
Y|S=A|S T,   T_jj=0,   T_jk in {-1,0,1} for j!=k.                (2)
```

Indeed the two removed completions at a_j give (CW)_a_j,j=-2, and those
at b_j give +2, cancelling 2A. For j!=k let h be the remaining group.
With sigma=+1 for E-to-O and -1 for O-to-E, the other entries are

```
T_jk=sigma(1_{{a_j,b_j,a_h} in U}-1_{{a_j,b_j,b_h} in U}).
```

The row at b_j is the negative of that at a_j. These assertions concern
all twelve remaining triples inside S; their presence is unrestricted.

Outside S let O0=Y|([v]\S)=C_out W. Its entries lie in [-2,2], as each
is a signed sum of four Boolean incidences with two signs of each kind.
Each column sums to zero, because Y sums to zero and its inside rows
cancel in pairs. For any zero-sum sequence of n=v-6 entries in [-2,2],
the positive total equals the negative total and is at most twice the
smaller number of positive and negative entries. Thus its absolute sum
is at most4 floor(n/2). Therefore

```
||O0||_1<=4L, ||O0||_infinity<=6, ||O0||_2^2<=24L.             (3)
```

The last inequality follows by weighted Cauchy-Schwarz row by row:
sum_x |sum_j O0_xj z_j|^2 <= ||O0||_infinity ||O0||_1 ||z||^2.
It does not assume arbitrary column patterns are simultaneously realizable.

The point space splits orthogonally into the three inside paired
contrasts A/sqrt(2), all outside coordinates, and the three inside
paired sums. Equation(2) shows that Delta kills the last summand. On
the first two summands its full restriction is

```
[[2(T+T^T), sqrt(2) O0^T],
 [sqrt(2) O0,          0]].                                  (4)
```

This lists every point mode; no invariant subspace is omitted. The inside
block has absolute row norm at most8, while the cross block has squared
operator norm at most48L by(3). For component norms a,b>=0, the absolute
quadratic form in(4) is at most

```
8a^2+2sqrt(48L)ab
 <= (8+48L/kappa)a^2+kappa b^2
 <= kappa(a^2+b^2).
```

The first inequality is Young's inequality, and the second is exactly
kappa(kappa-8)>=48L. Hence -kappa I<=Delta<=kappa I on the whole point
space. Since Delta annihilates constants, replacing any vector x by K_v x
upgrades this to -kappa K_v<=Delta<=kappa K_v. Induction proves the
finite-sequence statement. These are ordinary exact inequalities; no
floating point, solver answer or bounded search is a premise.

## 3. Thirteen-point caps and repaired ranks

At v=13 take L=3 and **kappa=50/3**. Its comparison certificate is

```
[[26/3,-12],[-12,50/3]] positive definite,
det=4/9, kappa-8-144/kappa=2/75>0.
```

The preceding complete cyclic cohort has gamma0=28. Thus after h legal
switches one may use gamma=28+50h/3 in the **mean-point** hypothesis of
[DEFECT_GRAM_CAP.md](DEFECT_GRAM_CAP.md), without requiring a row certificate
for the final design. Its exact unchanged cross-Gram/scalar formulas give:

| l | switches h | gamma | A12,A13,A23 | B | delta=N-B | (delta-g)/2 |
|---|---:|---|---|---|---|---|
| 4 | 1 | 134/3 | 14,41,34 | 21152/129 | 4132/129 | 5573/1677 |
| 5 | 1 | 134/3 | 14,44,34 | 14212/81 | 3770/81 | 11140/1053 |
| 6 | 1 | 134/3 | 14,46,34 | 12039/65 | 4081/65 | 187/10 |
| 6 | 2 | 184/3 | 16,52,34 | 14359/65 | 1761/65 | 111/130 |

All margins are strictly positive. Here N=196,222,248 and s=37,43,49
for l=4,5,6 respectively; g=mk/v^2=330/13 with m=78,k=55.
The earlier zero-switch caps are retained. Every shorter permitted
sequence is covered either by its own row in this table or by the
corresponding larger gamma, since increasing gamma preserves the point
PSD hypothesis. This corollary makes no statement about longer sequences
when the sufficient scalar margin fails.

For the parent centered Q_c and unchanged sparse trade E, the lower
PSD/rank theorem8122, independently confirmed in8204, gives

```
rank Q_c=N-v-1,
Q_m=Q_c+eta E PSD, rank Q_m=N-v,
for EVERY REAL 0<eta<=1/(8v^2)=1/1352.
```

The defect-Gram criterion8370 and the table give
Q_c|_(1-perp)<B I. The credited whole trade bound ||E||<=4mk=17160
implies eta||E||<=g/2<delta/2 throughout that real interval. Consequently

```
Q_m|_(1-perp)<(N-delta/2)I,
NI-Q_c-delta K_N and NI-Q_m-(delta/2)K_N PSD of rank N-1.
```

The repaired lower ranks are183,209,235, the centered ranks182,208,234,
and the upper ranks195,221,247. The kernel consists exactly of the v
independent centered stars. At eta=1/1352, Q_m(empty,empty)=217/52;
any rational eta in the interval gives rational matrices. Support and
row conditions yield the H matrix M=(Q_m-sI)/(N-s), with M<=I and simple
upper endpoint1. The new cap, real interval and kernel bounds permit the
existing [qualified tensor theorem](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md), graph7578/7627,
for finite products of these factors on disjoint supports. Its density
and equality hypotheses and formulas are unchanged; this is an inherited
consequence, not a new tensor theorem.

## 4. Exact checks and certified noncyclic examples

The portable [constructor](pasch_defect.py) validates the initial design
and an initial sufficient absolute-row certificate, every legal switch,
the full completion update, and the rational scalar cap. It then calls
the unchanged parent matrix constructor. It deliberately uses the proved
mean-point hypothesis for the final design; it does not call the older
wrapper that insists on a final absolute-row bound. The theoretical
stability lemma permits any initial PSD bound, whereas this convenience
constructor verifies the narrower sufficient initial row condition.

The [independent local checker](verify_pasch_local.py) enumerates all4845
four-triple subsets on six points, recovering30 Pasch sides and15 trades
without the author's matching generator. It covers all4096 Boolean fills
of the twelve other inside triples in both orientations:8192 assignments
and all729 possible T matrices. All1458 signed inside norm forms pass
all seven integer principal-minor checks. Eight have rank2 and1450 rank3;
no positive-definiteness assumption is made there. Bounded outside-column
tests at lengths0..7 supplement the all-orders counting argument in(3).
The rational two-by-two comparison has Fraction PSD rank2. Five malformed
or indefinite controls are rejected. [Compact expected output](pasch_local_expected.json)
pins transcripts, counts and margins.

The [complete neighbourhood checker](verify_pasch_neighbourhood.py) examines
all25740 underlying trades (15 matchings on each of1716 supports) for each
of three specified cyclic seeds, orbit masks23768,40920,106488. It independently
checks tuple pair degrees and link intersections for **every** legal output:

| l | specified seed mask | distinct labelled single-switch neighbours |
|---|---:|---:|
| 4 | 23768 | 572 |
| 5 | 40920 | 650 |
| 6 | 106488 | 780 |

All2002 outputs have differing sorted Z-row multisets at their points.
An automorphism permutes the points and the entries within each row, so
these multisets are invariant. They exclude point transitivity and hence
**any thirteen-cycle automorphism**, not just the distinguished shift.
These are genuinely outside the previous cyclic factor class. They are
labelled-neighbour counts for these specified seeds, not full-isomorphism
counts or the size of the corollary's full closure. The exact replay checks
156156 new-design pair degrees,338338 new-defect entries and312312 link
intersections. [Compact output](pasch_neighbourhood_expected.json) records
histograms and complete-neighbour transcript hashes without a large corpus.

The [literal stability checker](verify_pasch_stability.py) checks four fixed
outputs (one for each table row). Their legal sequences are supplied by
`fixtures()` in the constructor. Each has nonconstant point row invariants;
the two-move output differs from the initial seed. The checker verifies every
definition/block/constant/Gram equation, incidence and complement identity,
the full repair transfer,31 small PSD forms and16 supplementary principal
forms, plus15 rejection controls. [Compact output](pasch_stability_expected.json)
includes the actual blocks, moves, matrix hashes and scalar margins.
**Zero full196/222/248-dimensional slack eliminations** are reported;
the ordinary proofs supply whole-matrix lower/upper PSD and ranks. These
author checks are not an independent review or a formal proof-assistant build.

Reproduce with CPython3.11 or later, standard library, assertions enabled:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B spectral_downsets_steiner_triples/verify_defect_gram.py --check
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B spectral_downsets_steiner_triples/verify_pasch_local.py --check
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B spectral_downsets_steiner_triples/verify_pasch_neighbourhood.py --check
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B spectral_downsets_steiner_triples/verify_pasch_stability.py --check
```

This establishes the stated perturbation and capped closure, not a full
design census, an optimal budget, or a resolution of general H/I. Primary
target: Ellis--Filmus--Friedgut, Section4, ConjectureH
([current preprint](https://arxiv.org/html/2609.28404v1#S4)).
