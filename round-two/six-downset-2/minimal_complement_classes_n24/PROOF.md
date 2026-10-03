# Five complement-deficit classes and sharp constrained rank at order 24

Actual author **six-downset-2**, role **researcher**, 2026-10-03.
Status: ordinary author proof with a reproducible exact rational certificate.
Independent review of this new order is pending. The original lift, real
harmonic decomposition and completeness bridges are unformalized mathematics.

## The original problem and the finite theorem

Fix **n=24** and write

```
D={A subset[24]: |A|<=22}, F=D\{empty},
N=16777191, s=8388584, h=N-s=8388607, N-2s=23.
```

An ordinary H matrix is a real symmetric matrix M on **all** of D with
`M1=1`, `M[A,B]=0` if `A intersects B`, and `L=sI+hM>=0`.
An original capped H matrix additionally satisfies `L<=NI`.
The actual empty vertex, its row and its allowed loop are part of M.
Entries may have either sign. The cap is an extra hypothesis beyond H.

For a noncentral size a in **2,...,11**, call its complement-deficit class
present if **some** unordered pair `{A,[24]\A}` with sizes a and 24-a
has `L[A,A^c]<s`. This definition is for the original full ground set;
it imposes no invariance or equality between different pairs in a class.
The middle size12 is excluded from this count.

**Theorem.** Among all real original capped H matrices on D, the minimum
number of present noncentral complement-deficit classes is **five**.
At that minimum the greatest possible rank of L is **16587141**.
Both optima are attained by the rational invariant matrix specified in
[CERTIFICATE.json](CERTIFICATE.json) and the formulas below. Its five
present classes are **7,8,9,10,11**, and all classes **2,3,4,5,6** are
exactly saturated. It has q=190026 saturated unordered complementary
pairs, `rank(NI-L)=16777190=N-1`, and a simple unit eigenvalue for M.
Every other eigenvalue of M is at most
`1-1/838860700000000`. This conservative gap is not claimed optimal.

More precisely, any five-class cap must have exactly those five absent
noncentral classes. At the greatest constrained rank its lower kernel
is exactly the span of the 24 centered star indicators and the 190026
saturated pair differences. No other pair, including a middle pair,
can be saturated at that rank. The same rank ceiling applies among
ordinary H matrices required to saturate all pairs in classes2..6,
even without the cap or invariance, and the witness attains it there.

The new point is attainment of the count and rank bounds at **this one
order**. The count bound is credited to
[9942](https://github.com/helgithorskarp/math_results/blob/034e8aadfe9b9409d506cd910ce3abaf8190497f/round-two/six-downset-2/saturated_complement_count/PROOF.md).
The earlier n12/n16 constructions and generic exact model are
[10008](https://github.com/helgithorskarp/math_results/blob/07a1ed55f9ae998d000be2bd197b5b574c289fa7/round-two/six-downset-2/minimal_complement_classes/PROOF.md).
Their independent
[10030 audit](https://github.com/helgithorskarp/math_results/blob/137da10649c5edc34b58974758093a4f76ace71c/round-two/six-reviewer-4/class-rank-audit/PROOF.md)
already supplies the generic necessary rank/equality argument; it does
not audit or supply the present n24 certificate. Unrestricted n24 cap
existence is also prior art, via9556. There is no general H/I theorem,
all-order count sufficiency, optimal-gap assertion, classification of
maximum intersecting families or historical-priority assertion here.

## Count optimality over every real cap

The ordinary two-by-two PSD minor on a complementary pair gives
`L[A,A^c]<=s`. Consequently an absent deficit class is saturated on
**every** pair in that class. The credited original saturated-count
theorem9942 gives

```
q <= s/(N-2s) = 8388584/23,
integer q <= 364721.
```

The population of class a<12 is `C(24,a)`; the middle population is
`C(24,12)/2`. The ten noncentral populations increase strictly with a.
If at most four classes are present, at least six are absent, giving

```
q >= sum(a=2..7,C(24,a)) = 536130 > 364721.
```

Thus at least five classes are necessary. If exactly five are present,
there are five absent classes. Their least possible population is

```
q0 = sum(a=2..6,C(24,a)) = 190026.
```

Any different five-element set of absent classes has largest element
at least7 and its other four elements at least2,3,4,5 respectively, so

```
q >= sum(a=2..5,C(24,a))+C(24,7) = 401534 > 364721.
```

It follows that classes2..6 are the unique possible absent set at
the minimum. Some additional individual pairs in other classes could
still be saturated; the rank argument below excludes them only at
the greatest rank. The rational witness gives attainment. For an
additional finite arithmetic control, the verifier checks all1024
subsets of the ten size classes against this necessary count bound.
This is not an enumeration of original vertices or a solver proof.

## The rank ceiling and its equality case

For any original ordinary H matrix on D, `L1=N1`. Write
`C=L[F,F]-J_F`. Since L is PSD and acts by N on span(1), `L-J_N`
is PSD, hence C is PSD. Its diagonal is s-1.

Let w_i be the indicator of the size-s star at point i. Every two
members of the star intersect, so `w_i' L w_i=s^2`. The centered
vector `v_i=w_i-(s/N)1` therefore has zero L energy, and PSD implies
`Lv_i=0`, equivalently `Lw_i=s1`.

For a saturated pair `{A,A^c}`, the diagonal and cross entries of C
are all s-1. Thus `C(e_A-e_Ac)=0`. It also gives a full original
lower-kernel vector: the difference has coefficient sum zero.
The 24 centered stars are independent: a relation evaluated at the
empty vertex gives `sum_i c_i=0`, and evaluation at singleton i
then gives `c_i=0`. All pair differences vanish at empty and singleton
vertices. Their unordered pair supports are disjoint, so they are
independent of one another and of the star span. Hence, for **any**
q saturated pairs,

```
dim ker(L) >= 24+q,
rank(L) <= N-24-q.
```

Every five-class cap has `q>=q0=190026`, so its rank is at most
`16777191-24-190026=16587141`. The witness has exactly this rank.
At equality there are no additional saturated pairs and no additional
lower kernels, proving the stated equality profile. This is the
generic necessary argument of10030 applied at an attained new order.

The same killed pair difference implies a support constraint useful
for construction. For any other nonempty X, at least one of A,A^c
intersects X. That corresponding L entry is zero; equality of the C
columns, and hence of the two L cross entries, makes the other zero
as well. Thus **every proper nonempty coupling incident to a saturated
pair vanishes**, including singleton couplings.

## A complete invariant face with 36 exact coordinates

Use active classes7..11, their complements13..17, and middle12.
Set the symmetric nonempty disjoint coefficient table B as follows.
Its six deficits `d7,...,d12` are

```
12333549/2500000, 45850983/6250000, 79402731/12500000,
23321691/6250000, 21130569/6250000, 2404857/3125000.
```

For `2<=a<=12`, set `B[a,24-a]=s-d_a`, with d_a=0 on classes2..6.
There are thirty remaining proper nonsingleton orbits
`2<=a<=b`, `a+b<24`, both sizes in7..17. Assign their exact rational
values from the named ordered table in [CERTIFICATE.json](CERTIFICATE.json).
All other proper nonsingleton orbits and all entries with `a+b>24`
are zero. Finally recover the singleton coefficients uniquely by

```
B[1,a] = [(24-a)s-sum(b=2..22,b B[a,b] C(24-a,b))]/(24-a),
B[1,1] = [23s-sum(b=2..22,b B[1,b] C(23,b))]/23.
```

These are the credited star-only decoder9365/9639, without a zeroth
moment or centering condition. Every divisor is nonzero. They imply
all22 star equations
`sum_b b B[a,b] C(24-a,b)=(24-a)s`. The verifier checks every affine
coordinate against an independent full star-system RREF, and checks
all recovered original in-point, out-of-point and empty-row star sums.

This parametrization loses no invariant coordinate in the saturated
face: the support argument just proved forces every incident proper
coupling to vanish, and the singleton equations are uniquely solvable.
Moreover permutation averaging preserves the real original H and cap
conditions and preserves which deficit classes are absent/present,
since every pair deficit is nonnegative. It therefore reduces the
all-real five-class feasibility problem to this complete invariant
36-dimensional face. It does **not** force competitors to be rational,
entrywise positive, centered or strictly attenuated at middle12. The
particular rational witness happens to have all six deficits positive.

## Actual completion on all original vertices

For A,B in F set

```
C[A,B]=s*1_(A=B)-1+B[|A|,|B|]*1_(A disjoint B),
E=[-1_F'; I_F],
L=J_N+E C E', M=(L-sI_N)/h,
U=N I_F-J_F-C.
```

The nonempty original diagonal of L is s; distinct intersecting entries
vanish. Since `E'1=0`, `L1=N1` and `M1=1`. For size a put

```
c_a=s-(N-1)+sum(b=1..22,B[a,b] C(24-a,b)),
L[empty,A]=1-c_a,
L[empty,empty]=1+sum(a=1..22,C(24,a)c_a).
```

The actual empty loop is **2238275691119621/4468750000**; all22 empty
row entries are recorded in the certificate and regenerated exactly.
Every original size-row, empty-row and point-star equation is checked.
Several supported entries are negative, which is permitted in H.
The identity `NI-L=EUE'` retains the entire empty row and loop.
E has full column rank with range `1-perp`, so `L>=0` iff `C>=0`,
`NI-L>=0` iff `U>=0`, and `rank L=1+rank C`. This is the original
lift credited to7578; no altered vertex set is used.

## All thirteen physical degrees and the original mean metric

Use the complete real Boolean harmonic decomposition credited to
[9639](https://github.com/helgithorskarp/math_results/blob/82271e4d09ca65afa426f917e885a558d1145867/round-two/six-downset-2/near_full_low_degree_reduction/PROOF.md).
For j=0,...,12 let

```
I_j={max(1,j),...,min(22,24-j)},
g_ja=C(24-2j,a-j), G_j=diag(g_ja),
K_j[a,b]=s*1_(a=b)-1_(j=0)C(24,b)
         +(-1)^j B[a,b] C(24-a-j,b-j),
U_j[a,b]=N*1_(a=b)-1_(j=0)C(24,b)-K_j[a,b].
```

The symmetric physical forms are `H_j=G_j K_j` and `V_j=G_j U_j`.
Each copy has multiplicity `C(24,j)-C(24,j-1)`, with `C(24,-1)=0`.
Their weighted dimensions sum to `N-1`; every lower and upper degree
is included, including j=0 and the highest middle parity j=12.
The credited binomial disjoint-action and norm formulas give these
operators on all real harmonic copies. This is an ordinary analytic
bridge, not an inference from a floating computation or an omitted
irreducible component. The source agrees entry-for-entry with the
unchanged independently checked generic10008 harmonic implementation.

To state an upper gap in the **original** Euclidean metric, the entire
mean block needs its actual empty coordinate. Put

```
b_a=C(24,a), a=1,...,22, P=I+1 b',
G_original=diag(b)+bb'.
```

An original mean vector w_z has layer constants z and empty coordinate
`-b'z`, so `1'w_z=0`, `||w_z||^2=z'G_original z`, and `E'w_z=Pz`.
Its original lower and upper forms are therefore
`H_original=P'H_0P`, `V_original=P'V_0P`. Since `1+sum_a b_a=N`,
P is invertible with `P^-1=I-1 b'/N`; and
`H_original+V_original=N G_original`. All j>0 copies have zero layer
sum and empty coordinate zero, retaining metric G_j. Thus these forms
describe the **entire** original space `1-perp` with its actual metric.

The row-sum congruence assembly is checked against independent generic
dense P multiplication on all38 affine probes (zero,36 units and a
signed probe), on both endpoints, and on the certificate itself. The
new mean coordinate formula is also compared with direct energies of
the credited n8 original matrix8319, using all61009 literal entries.
These checks are validation of the coordinate formula, not new n8
mathematics or an independent-person review of n24.

## Exact positivity, complete ranks and the gap

The known core lower kernels are cardinality `(a)_a` at j=0, constants
`(1)_a` at j=1, and `e_a-(-1)^j e_(24-a)` for every saturated class
a in2..6 present in that degree. They are independent. In the original
mean coordinates these are mapped by `P^-1`: the cardinality vector
becomes `(a-24s/N)_a`, and equal-population pair differences are unchanged.
Every full kernel identity is checked exactly. Their counts by degree
are `(6,6,5,4,3,2,1,0,0,0,0,0,0)`.

For each degree the verifier first checks both full raw physical forms
using **two exact algorithms**, integer Bareiss and rational Schur
elimination. Their ranks must agree. The lower has exactly its listed
kernel; every full upper block is positive definite. Weighted lower
nullity is `24+190026=190050`, giving core rank16587140 and original
rank16587141. Weighted cap rank is N-1=16777190.

Set `epsilon=1/100000000`. On each complete **original** upper sector,
both algorithms check that `V_original-epsilon G_original` (j=0) or
`V_j-epsilon G_j` (j>0) is positive definite. No mean direction is
dropped. The decomposition therefore gives

```
NI-L >= epsilon (I-J_N/N),
M on 1-perp <= (1-epsilon/h) I,
epsilon/h = 1/838860700000000.
```

The unit eigenvalue is simple. Point-star kernels force the minimum
eigenvalue of M to be `-s/h`, so its weighted Hoffman value is exactly s.
For lower-rank validation, the verifier also subtracts epsilon times
the actual metric on each retained principal coordinate plane after
deleting RREF kernel pivots. This lower floor applies **only to the
chosen complementary plane**, not to every vector perpendicular to the
kernel in the full original metric. PSD reversibility follows because
every full vector has a representative on the kept coordinates modulo
the verified kernel span. No positivity direction is lost by this
principal restriction.

The certificate's six deficits are positive and every other pair class
is saturated, so it has exactly five noncentral classes and no further
saturated pairs. The exact existence and the preceding all-real count
and rank bounds prove the theorem.

## Reproduction and trust boundary

[verify.py](verify.py) uses only this directory and the Python standard
library. The acceptance calculation regenerates every coefficient,
complete sector, original row and star, both exact PSD algorithms,
original floors and all1024 class subsets. The compact expected output
is compared **after** this calculation, never used as its mathematical
premise. Semantic damaged inputs must reject in ordinary and optimized
isolated executions. No `assert` is an acceptance condition.

The ordinary statements linking the original downset, real harmonic
copies, lifted ranks and all-real competitors remain unformalized.
Two author algorithms, runtime modes and literal controls provide
reproducibility, not independent-person review. Source credits and
the exact prior dependencies are listed in [CREDITS.md](CREDITS.md).

The primary problem remains Ellis--Filmus--Friedgut's
[Conjecture H, Section4](https://arxiv.org/html/2609.28404v1#S4).
The live [submission history](https://arxiv.org/abs/2609.28404), checked
2026-10-03, still lists v1 of2026-09-23; the paper proposes spectral H/I.
This finite capped result neither closes those conjectures nor derives
a certificate from the announced proof of classical Chvatal.
