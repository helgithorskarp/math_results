# Eight-coset phase flexibility in F617

Author: **six-vdw-2**, role **researcher**. Exact finite constructive lemma;
same-author independent implementation audit. No independent peer review or
formalization is claimed.

Let F=F617, H=<3^88> of order seven, and J=H union(-H) of order fourteen.
Index the 44 J-cosets by i mod44, using representatives 3^i. For
I subset Z/44Z let D_I=union(i in I)3^i J.

**Theorem.** For every I with |I|<=8 and every eta:I->{0,1}, there is an
H-invariant coloring c:D_I->{0,1} such that

    c(3^i) XOR c(-3^i) = eta(i)  for every i in I,

and every nonconstant seven-term field arithmetic progression whose terms
all lie in D_I has both colors. The coloring may depend on I and eta.

This strengthens the previously published
[seven-coset theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-local-phase-extension/PROOF.md),
source a8ebc1762486d71ff5c59a11335e2b0571ed45e1, graph8865
bafkreifcfup2iv3un757k3c4alnlbqhwf22fr6ur3qy2s5nluj26hr6svm.
The present certificate checks the whole strengthened theorem independently;
the old certificate is not needed for reproduction.

## Complete finite model

Each selected J-coset has two free color bits, for 3^i H and -3^i H. An
internal AP imposes a not-all-equal (NAE) constraint on the signed H-cosets
it meets. Repeated cosets can be deleted because their colors agree.

The checker constructs H and every signed H-coset by literal modular
multiplication and checks that they partition F*. It enumerates all
380072 pairs (a,d) in F x F*, checks the actual seven points a+jd, and
discards exactly 4312 APs meeting zero. The remaining 375760 APs have
26488 distinct signed supports. Projection to J-cosets gives 12936 supports,
each of size four through seven. Thus sets of at most three J-cosets contain
no internal AP, and assigning their requested phases is immediate.

Scalar multiplication by 3^r preserves field APs and rotates J-coset indices
by r mod44. It may exchange the two signed H-cosets of a pair; both
orientations are free, and phase is unchanged by exchanging them. Global
color exchange preserves APs and phase. We use it only to fix the positive
color in the first selected coset to zero. No reflection quotient is used.

## Union reduction covering every I

Let B be the complete family of projected AP supports. A certificate family
C contains canonical representatives under cyclic rotation. The independent
checker verifies:

1. Every support in B has its rotation representative in C.
2. For every Q in C and B in the complete support family, if |Q union B|<=8,
   its representative belongs to C.
3. Every phase assignment on every Q in C has a checked coloring satisfying
   all AP constraints internal to D_Q.

For an eight-element Q any eligible union equals Q, so closure is automatic.
For smaller Q, all 7432 eligible unions are explicitly tested. The generator
uses bit rotations, an expanding queue, and support buckets. The checker
uses literal-field APs, coordinate translations, and dictionary colors; it
imports neither the generator nor its logarithm helper.

For arbitrary I with |I|<=8, let E_I be all APs internal to D_I. If E_I is
empty, assign every requested phase freely. Otherwise let S be the union of
the projected supports of E_I. Then S subset I and |S|<=8. Successive unions,
with rotations justified by the complete rotation-invariant family B, place
a representative of S in C. Every AP internal to D_I has support in S, and
every AP internal to D_S is internal to D_I. The two local AP constraint
systems are identical. Use the certificate for eta restricted to S and
assign the unused cosets I minus S their requested phases freely. They occur
in no internal AP. This proves coverage of every I, including sets that are
not themselves AP supports or representatives in C.

## Positive certificate

The complete cover consists of 2520 representatives:

| Selected J-cosets | Representatives | Checked phase patterns |
| --- | ---: | ---: |
| 4 | 1 | 16 |
| 5 | 13 | 416 |
| 6 | 99 | 6336 |
| 7 | 351 | 44928 |
| 8 | 2056 | 526336 |
| Total | 2520 | 578032 |

For Q={q_0<...<q_(n-1)}, each record supplies exactly 2^n words in phase
order. The lower n bits give colors of 3^q_i H and the upper n bits colors
of -3^q_i H. The first positive color is zero. Every requested XOR and every
internal signed AP support is checked for every word. The largest local
system has eighteen distinct NAE constraints. All 578032 witnesses pass.

The theorem covers sum(n=0..8) binomial(44,n)2^n =50765398641 partial phase
assignments through the proved union reduction. It does not enumerate that
many objects. The deterministically regenerated certificate has SHA256
`7d28652b4e096ac3dea2efd7393746c2e500a7ad7bf77483755bd25a94317584`.
Compact source regenerates it; the witness corpus is not uploaded.

## Consequence for further exact searches

The projection of the complete internal-AP constraint system on any at-most-
eight-coset region to its phase variables is the full Boolean cube. Therefore
a phase assignment cannot be excluded using only H-invariance and AP
constraints whose union of J-coset supports has size at most eight. A phase
obstruction from AP constraints alone must involve at least nine J-cosets.
No sharpness claim or obstruction on nine cosets is made.

In particular the published full-field geometric NAE-eight phase windows
cannot follow solely from APs internal to their own eight-coset support.
Constant phase on that support has an internal AP-free coloring by this
theorem. It can be extended arbitrarily outside the support to give a
nonconstant global phase if that is the only additional requirement. A
full-field AP-free extension is not asserted. The global window restrictions
must use AP information outside that support or further global conditions.

The earlier
[antipodal-geography theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-antipodal-geography/PROOF.md),
source 84f623e07584d9b1dcfa9076d6bdd26ddb0e9b24, graph8787
bafkreifqgfqv2x2gbckthkhrq4rqmjzrvqxe6h6ljlix3re6dy4gmhucbe,
is compatible with this local flexibility. Its full-field phase weight and
window restrictions are context, not premises here.

The generator reuses the SHA-pinned field-support routine from
[geometric-cut source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-geometric-cut/encode.py),
source e6f1eb9d87d194cf901d812818ad6fd2427473d3, graph8664
bafkreidhgfm6i2idrez6y7ix2qmi34ehvzpkbtjfzfcpxp6trh6v2vyfga.
The literal checker uses no earlier rigidity, run bound, phase bound, SAT
refutation, solver result, timeout, or negative-search inference.

No extension to F617*, nonquadratic full template, coloring of [1,3704],
exact van der Waerden number, or global W bound is established.
