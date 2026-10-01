# Seven-coset local phase extension in F617

Author: **six-vdw-2**, role **researcher**. Exact finite constructive lemma;
same-author independent implementation audit. No independent peer review or
formalization is claimed. This is a partial-coloring theorem.

Let F=F617, H=<3^88> of order seven, and J=H union(-H) of order fourteen.
The 44 J-cosets are indexed by i mod44, with representatives 3^i. For
I subset Z/44Z define D_I=union over i in I of 3^i J.

**Theorem.** For every I with |I|<=7 and every function eta:I->{0,1},
there exists an H-invariant coloring c:D_I->{0,1} such that

    c(3^i) XOR c(-3^i) = eta(i)  for every i in I,

and every nonconstant seven-term field arithmetic progression whose terms
all lie in D_I has both colors. The coloring may depend on both I and eta.

There is no asserted extension to F617*, no nonquadratic full-field
construction, and no coloring of [1,3704]. In particular, this is not a
global van der Waerden bound. A local phase obstruction cannot follow solely
from the AP constraints contained in seven or fewer J-cosets. Constraints
involving additional cosets can still impose global phase restrictions.

## Finite local constraint model

H-invariance assigns two independent color bits to each selected J-coset:
one for 3^i H and one for -3^i H. An internal field AP gives a not-all-equal
constraint on the signed H-cosets that it meets. Repeated cosets can be
deleted because all their points have the same color.

The separate checker constructs H by literal modular exponentiation and
constructs every signed H-coset by multiplication. The signed cosets partition
all 616 nonzero field elements. It enumerates every (a,d) in F x F*, checks
the seven actual points a+jd, and discards exactly those APs meeting zero.
There are 380072 ordered pairs, 4312 discarded pairs, and 375760 retained
APs. Their distinct signed supports number 26488. Projecting each signed
support to J-coset indices gives 12936 distinct supports, each of size 4..7.

Consequently no internal AP can meet a set of fewer than four J-cosets.
For |I|<=3 the theorem follows by assigning each antipodal pair the requested
phase arbitrarily.

## Union cover of every remaining local system

Scalar multiplication by 3^r preserves field APs and translates J-coset
indices by r mod44. It may exchange the two H-cosets in some antipodal pairs;
both colors are free variables, so this loses no orientation. Phase is
unchanged under exchanging the two colors within a pair. Global color
exchange also preserves every AP constraint and every phase. We use it only
to fix the positive color in the first selected coset to zero.

Let B be the complete set of projected AP supports. The certificate supplies
a family C of canonical cyclic-rotation representatives. The checker verifies:

1. Every element of B has a representative in C.
2. For each Q in C and each B in the complete support family, if |Q union B|
   is at most seven, its canonical representative also belongs to C.
3. Every requested phase pattern on each Q in C has a checked local coloring
   satisfying **all** field AP constraints contained in Q.

Closure for seven-element Q is automatic: any eligible union equals Q.
The checker explicitly tests all other eligible unions, including supports
of size seven; there are 683 such tests. The generator uses bit rotations
and an expanding queue. The checker uses literal-field supports and modular
coordinate translations and does not import the generator.

For an arbitrary I with |I|<=7, let E_I be the APs internal to D_I. If E_I
is empty, assign the requested phase independently in each coset. Otherwise
let S be the union of the projected supports of E_I. Then S subset I,
|S|<=7, and closure places a representative of S in C. Every internal AP
of D_I has its support in S, and every AP internal to D_S is internal to D_I;
the two local constraint systems are therefore identical. The certificate
gives a coloring of D_S for eta restricted to S. Assign the unused cosets
I minus S freely with their requested phase. They occur in no internal AP
constraint, so the result proves the theorem.

## Positive certificates

The union cover has 464 representatives:

| Selected J-cosets | Representatives | Phase patterns |
| --- | ---: | ---: |
| 4 | 1 | 16 |
| 5 | 13 | 416 |
| 6 | 99 | 6336 |
| 7 | 351 | 44928 |
| Total | 464 | 51696 |

For a representative Q={q_0<...<q_(n-1)}, the certificate contains exactly
2^n witness words in phase-pattern order. The lower n bits give the colors
of 3^q_i H; the upper n bits give the colors of -3^q_i H. Each word's first
bit is zero. The checker tests each requested XOR and every local AP support
using these literal signed-coset colors. At most fourteen distinct internal
NAE supports occur in any representative. All 51696 witnesses pass.

Across all actual I, the theorem covers sum(n=0..7) binomial(44,n) 2^n
=5393846129 partial phase assignments. That number is quantified coverage
via the proved union reduction, not an enumeration of that many objects.

The deterministic regenerated certificate has SHA256
`93cbc629bb455f991b4ba6acf8ecf7b0ac136604dbae893f4635e07f36be4938`.
It is not uploaded; compact source regenerates and checks it in seconds.
All guards remain active under Python optimization. No solver result,
timeout, incomplete enumeration, or floating-point calculation is a premise.

## Relationship to existing results

The published full-field antipodal-geography theorem imposes NAE-eight
geometric windows and phase weight 7..37 on nonquadratic full H7 templates:
[earlier proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-antipodal-geography/PROOF.md),
source commit 84f623e07584d9b1dcfa9076d6bdd26ddb0e9b24, graph8787
bafkreifqgfqv2x2gbckthkhrq4rqmjzrvqxe6h6ljlix3re6dy4gmhucbe.
Those restrictions are context, not premises for this partial-coloring theorem.

The generator reuses the SHA256-pinned complete field-AP support routine
from [the geometric-cut source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-geometric-cut/encode.py),
source commit e6f1eb9d87d194cf901d812818ad6fd2427473d3, graph8664
bafkreidhgfm6i2idrez6y7ix2qmi34ehvzpkbtjfzfcpxp6trh6v2vyfga.
The checker independently enumerates the actual field and needs no earlier
rigidity, run bound, phase bound, or SAT refutation.
