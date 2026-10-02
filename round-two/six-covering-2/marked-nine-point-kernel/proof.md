# A sharp nine-point kernel after original sixteen is spent

Actual author: **six-covering-2, researcher**, 2026-10-02. Complete elementary
arguments with literal same-author checks; no independent review or
formalization. This is a conditional capacity lemma for minimum EXACTLY8,
all original moduli dividing10080. It supplies no numerical L_min(8)
improvement and asserts no complete BASE-stage realization of the kernel.
The actual LCM may be a proper divisor of10080.

Consider either original prefix

    H1=(8:0,9:0,10:1,14:0,12:10,16:1),
    P1=(8:0,9:0,10:1,14:1,12:10,16:1).

All six resources are already present. In particular original16 is spent;
original32 remains available. Put D=Div(315), E=D minus{1}. The remaining
original resources partition into36 BASE labels dividing2520 and23 TAIL
labels

    {16d:d inE} union {32d:d inD}.

These are23 distinct original moduli, not a pooled multiplicity of
cofactor labels. The prescribed six,36 BASE and23 TAIL labels partition
all65 divisors of10080 at least8. Every phase at the four TOP resources
288/1440/2016/10080 remains free.

## Explicit obstruction and BASE clause

On the315 cofactor choose

    K2=K3=K4=K5={3,5}, K6={3}, K0=K1=K7=empty.

Let W contain ALL physical x modulo10080 with x mod8=r and x mod315 inKr.
The nine cofactor points give36 physical points: the CRT period is2520,
so each point has four lifts. They avoid every prescribed original class
in BOTH H1 and P1. They also avoid original15:2. This can be seen directly
from the stated residues, and the checker verifies every physical point.

For every d inE the two distinct cofactor points3 and5 differ modulo d.
Thus an original16d phase hits at most two points of W (one cofactor
point at one of two16 children), and a32d phase hits at most one. These
maxima are attained separately. Original32, with d=1, hits at most two.
The sum of individual maximum capacities is therefore

    11*2 + 11*1 + 2 =35 <36=|W|.                     (1)

No35-point simultaneous union attainment is asserted. Even the sum of
maxima is insufficient, so the23 tails cannot cover W. Omitting resources,
wasting phases or overlapping classes cannot increase this upper bound.
The checker scans every actual physical tail progression, including
all29936 phases and the zero-gain ones.

Consequently any covering extending H1 or P1 must use a BASE class
hitting W. Write K0'=W modulo2520. The necessary phase clause is

    OR_(n inBASE, a in{x modn:x inK0'}) X_(n,a).       (2)

It has225 terms. If original15:2 is additionally prescribed, its resource
is spent and its class avoids W; the same clause reduces to223 terms
over35 remaining BASE labels. The canonical clause hashes are in
[expected.json](expected.json). Neither clause by itself excludes either
root. They can be added to an appropriately marked BASE/TAIL search;
the claim does not import the peer's numerical P BASE fixture.

## Nine is sharp in the specified product-kernel class

Here a product kernel means arbitrary finite Kr subsets of Z/315Z with
ALL four physical lifts at each r modulo8, avoiding the prescribed8:0
and16:1 classes. Assume exactly the above23 TAIL labels remain available,
and compare unit demand with the sum of individual phase maxima.
This is a restricted notion of obstruction, not minimality among all
weighted witnesses, physical subsets, conditional states or coverings.

Take any nonempty such kernel, with k total cofactor points and
M=max_r|Kr|. Avoiding8:0 forces K0 empty. Avoiding16:1 forces K1 empty,
because any cofactor point at r=1 would include two forbidden16 lifts.
There are at most six nonempty parents, hence M>=ceil(k/6).

At any one cofactor point every remaining16d resource has a phase
covering two of its four physical lifts. Thus the11 such resources have
individual maximum capacity at least2. Every nontrivial32d resource
has a phase covering at least one point. Original32 has a phase covering
all M cofactor points of a largest parent at one32 prefix. Therefore

    total unit tail capacity >=22+11+M
                             >=33+ceil(k/6).         (3)

For1<=k<=8 this is at least4k, so no strict unit-capacity obstruction
exists. The displayed nine-point kernel achieves35<36, proving the
limited minimum is exactly9. This universal lower argument uses no
bounded search or undocumented finite reduction.

## Every ordinary common-q erasure cut accepts this kernel

Credit the general unequal-pool inequality of
[six-covering-3, contribution9241](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/few-class-erasers/proof.md)
and the prescribed-resource bookkeeping of
[six-covering-2, contribution9172](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/prescribed-sixteen-allocation/proof.md).
Here the restricted point kernel has five nonempty parents, each with
two16 targets. Hence T=10, p=2, k1=11, k2=12. The first cofactor pool is
E, and the last is D. Spent16 and free32 must remain different resources.

For B subsetD let R=|B|, epsilon=1_(1 inB), L=|E minusB|. Let Aq(B)
count parents having a cheap support of fewer than q distinct labels
disjoint from B, contained entirely in E OR entirely in D. All copies
of such a parent must belong to C; otherwise its cheap support would
miss the hypergraph cover. Other parents can have both copies omitted.
Thus the minimum exceptional-target count is c=2Aq(B).

Using b1=R-epsilon, b2=R and
max(0,T-floor(k2/p))=4 in the credited inequality, divide by q-1>0.
The resulting minimum-cost test is

    4q Aq(B)+(2q-1)R >=8q-10+2(q-1)epsilon.          (4)

If1 is NOT in B, the last-pool support{1} erases EVERY parent: Aq=5.
This support is legal at original32 even though original16 is spent.
If1 is in B, only E minusB remains. A single such label erases K6 but
none of the four two-point sets, since3 and5 differ at every label inE.
Any two distinct remaining labels can erase any two-point set, by using
one class per point. Consequently

    q=2: Aq=5 if epsilon=0; otherwise Aq=1_(L>=1).
    q>=3: Aq=5 if epsilon=0 or L>=2;
          Aq=1 if epsilon=1,L=1; Aq=0 if epsilon=1,L=0.

These formulas apply to EVERY integer q>=3: with at most two points
there are no new distinctions at larger thresholds. They are not an
extrapolation from finitely many q values.

For q=2 the minimum slack in(4), over all4096 B, is3, attained at B={1}.
For q>=3 the four regimes have their least possible slack respectively

    epsilon=0:          12q+10        (B=empty),
    epsilon=1,L>=2:     12q+11        (B={1}),
    epsilon=1,L=1:      16q+1,
    epsilon=1,L=0:      14q           (B=D).

Therefore the exact minimum slack is min(12q+10,14q)>0 for q>=3;
at q=3 it is42. Every ordinary common-q hypergraph-cover cut accepts
the kernel, despite its strict35<36 physical capacity obstruction.
The exact checker reconstructs actual first/last single/two-class
supports separately, enumerates all4096 B, and verifies the affine
regimes. It never treats first-only supports as the true cover cost.

This separation concerns the restricted point kernel. Actual complete
BASE residuals may contain more holes and may fail erasure cuts. No
complete residual realization is claimed, and the hierarchy's failure
here does not constitute an impossibility result for all BASE choices.

## Prior art, reproduction and trust boundary

This develops the point-capacity versus erasure distinction of
[six-covering-3's contribution9369](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/tail-capacity-kernel/proof.md),
source c3dd66e6298f7eded8a5dcf9c23664da76783ca7. That source has24 free
tails and a limited twelve-point minimum. Here original16 is already
spent: the tail pool and the sharpness statement are different. Its
12-point kernel, BASE fixture and numerical tables are not asserted
as new or imported as proof premises. The necessary BASE clause format
also relates to the peer's
[shared-BASE reduction9309](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/cardinality-cores/proof.md).

Primary context remains [Zhang--Zhang](https://arxiv.org/html/2607.19029)
and [Harrington--Klein--Lowrance--Trifonov](https://arxiv.org/html/2605.18644).
Their reported minimum-seven LCM and restricted-prime construction are
prior art, not premises. The global exact-eight candidates remain
10080/15120/20160, only20160 witnessed in credited prior work.

From the repository root, with Python3.11 or later and no external packages:

    python3 -B round-two/six-covering-2/marked-nine-point-kernel/check.py --expected round-two/six-covering-2/marked-nine-point-kernel/expected.json
    python3 -O -B round-two/six-covering-2/marked-nine-point-kernel/check.py --expected round-two/six-covering-2/marked-nine-point-kernel/expected.json
    python3 -B round-two/six-covering-2/marked-nine-point-kernel/check.py --controls

All substantive certificate data are compact and public. The elementary
CRT, union-capacity, product-kernel lower bound and credited inequality
specialization are written proof steps. The checker scans every physical
tail phase and6235 actual cofactor phase masks, using integer sets and
distinct original labels. It imports no producer, discovery normalizer,
solver, peer fixture or large proof corpus. Same-author algorithmic
checks and14 rejecting damages are not independent review.
