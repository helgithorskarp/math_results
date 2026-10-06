# Whole independent reconstruction of the Bell-leaf obstruction

Sage/literature-researcher-1,2026-10-06,normal workday12. Internal review of
ENTIRE Theo888 under fresh901/author902, AFTER actual whole author882
alignment909. Independent hand proof and one manually reconstructed literal
example; ZERO native mathematical jobs. All three author files/manifest
were read completely and frozen unchanged. No858 checker result or code
supplies the following theorem.

## Position inverse and the exact source population

Let k>=1 and sigma be any permutation of[k]. Root i is paired with leaf
k+sigma_i. Its S component at positions4i-3 through4i is
(i,k+sigma_i,k+sigma_i,i). The complete position table is therefore
root i:(4i-3,4i), its leaf:(4i-2,4i-1).

E lists these pairs in descending LABEL order2k,...,1, using one-based
positions as VALUES. Every S position occurs once; E is a permutation
of[4k]. Put p(v)=sigma^{-1}(v). Its halves are explicitly

 E_leaf=(4p(k)-2,4p(k)-1,...,4p(1)-2,4p(1)-1),
 E_root=(4k-3,4k,4(k-1)-3,4(k-1),...,1,4).

For q_i=k+1-sigma_i, leaf i occupies E positions(2q_i-1,2q_i);
root i occupies(4k-2i+1,4k-2i+2). These cover EVERY output point.
Conversely assign label2k-r+1 to S positions E_(2r-1),E_(2r),
r=1,...,2k. This recovers S uniquely, hence each root's leaf and sigma.

For a Bell input, list each block decreasingly and blocks in increasing
minimum order. A block's last element is its minimum, strictly below the
first element of the next block. Exactly the boundaries are ascents;
maximal descending runs recover the blocks. Thus input->sigma->S->E is
injective and output length is4k. T_k counts ONLY these Bell inputs whose
E actually avoids full boxed2143, equivalently their distinct safe images.

## Exhaustive mixed rectangle for arbitrary sigma

Suppose an ascent sigma_i<sigma_(i+1) has an earlier smaller value,
2<=i<=k-2. Choose the LAST j<i with sigma_j<sigma_i. All entries indexed
j<t<i exceed sigma_i, as does sigma_(i+1). Decreasing leaf-label order
places all their pairs before leaf i, whereas leaf j is after it.
In particular q_i<q_j. Select, in horizontal order,

 A: leaf i high, position2q_i, value4i-1;
 B: leaf j high, position2q_j, value4j-1;
 C: root i+2 low, position4k-2i-3, value4i+5;
 D: root i+1 low, position4k-2i-1, value4i+1.

All leaf positions are<=2k, and i<=k-2 gives C_position>=2k+1.
Hence A_position<B_position<C_position<D_position. Since j<i,
4j-1<4i-1<4i+1<4i+5. This is2143 with open vertical band(4j-1,4i+5).
The four selected points are exemptions from the box test.

Account for EVERY possible unselected point strictly between A and D.
The following disjoint cases exhaust all leaves:

* t<j: both values<=4j-5, below the bottom;
* t=j: its low4j-2 is below the bottom, its high B is selected;
* j<t<i: the whole pair is before A by the choice of j;
* t=i: its low is immediately before A, its high A is selected;
* t=i+1: the whole pair is before A by the ascent hypothesis;
* t>=i+2: both values>=4i+6, above the top.

This includes every leaf between B and C. In descending root order the
only roots appearing up to D have t>=i+1. For t>i+2 even the low is
at least4i+9, above the top. Root i+2 contributes selected C and high
4i+8, above the top. Root i+1 contributes selected D; its high is AFTER
D. All smaller roots are after D. No blocker remains; the rectangle is
empty and boxed avoidance fails.

Contrapositively, EVERY ascent i<=k-2 in an avoiding image has ALL earlier
values larger than sigma_i: its lower value is a LEFT-TO-RIGHT minimum.
For i=1 this condition is vacuous; no earlier smaller j exists. For
i=k-1 root i+2 does not exist, so that ascent is excluded from the
statement. Small k with no qualifying index are covered vacuously.
No condition on the final ascent is inferred.

## Bell's second boundary and necessary shapes

Let the ordered blocks be B1,...,Bb. If b>=3, the boundary after B2 is
an ascent whose lower value min B2 exceeds1, while1 occurs earlier in B1.
It is not a prefix minimum. Its index i=|B1|+|B2|>=2. If b>=4, the later
blocks contain at least two elements; if b=3 and |B3|>=2, again at least
two remain. Either case gives i<=k-2, so the mixed rectangle rejects it.

Therefore any surviving input has b<=2, or b=3 with final B3 a singleton.
This condition is NECESSARY ONLY. The earlier858 fifth input
{1,4},{2,5},{3} meets it but fails through its separately checked leaf
rectangle. That historical input is not rerun as another native control
and does not supply the new uniform proof.

## Exact count through a distinguished singleton

For k>=2, choose Q subset{2,...,k} as the block not containing1.
Q empty gives the unique one-block input; Q nonempty gives exactly one
two-block input. This bijection has2^(k-1) choices, with no symmetry factor.

For three blocks with final singleton{r}, choose r in{2,...,k}. The other
two blocks partition[k] minus{r}. Anchor B1 by1; its complement is Q=B2.
To precede{r} in minimum order Q must meet{2,...,r-1}, ensuring Q is
nonempty. B1 is nonempty because it contains1. Of the2^(k-2) subsets Q
of[k] minus{1,r}, exactly2^(k-r) use only{r+1,...,k} and are forbidden.
The exact number of necessary shapes for this r is

                         2^(k-2)-2^(k-r).

Q may itself be a singleton. For r=2 the count is zero. Even if other
blocks are singleton, the final block in minimum order is unique, so r
creates no double count. Conversely each admitted Q gives exactly one
ordered three-block input. Summing r=2,...,k uses

 sum_(r=2)^k 2^(k-r)=1+2+...+2^(k-2)=2^(k-1)-1.

The three-block count equals(k-1)2^(k-2)-(2^(k-1)-1)
=(k-3)2^(k-2)+1. Adding one/two-block shapes gives
U_k=(k-1)2^(k-2)+1. At k=2 the three-block count is0 and U_2=2, so the
formula covers this boundary. At k=1 there is only one input and T_1<=1;
no negative-power counting convention is used. All counts concern the
NECESSARY allowed superset, never certified survivors. Thus

                       T_k<=U_k for EVERY k>=2.

Since U_k<=k2^(k-2),
T_k^(1/(4k))<=k^(1/(4k))2^((k-2)/(4k)). The first factor tends to1 by
log(k)/k->0 and the second to2^(1/4); the limsup is at most2^(1/4).
Every pruning within this injective length4k rule satisfies the same
finite exponential output-root bound. It cannot prove the negative
alternative of410. This says nothing about all a_n, other encodings or
a different source population, and does not give a safe lower bound.

## Complete literal k4 reconstruction and trust boundary

Partition{1},{2},{3},{4} gives sigma=(1,2,3,4). The four components are
(1,5,5,1),(2,6,6,2),(3,7,7,3),(4,8,8,4). The entire position table is

 1:(1,4),2:(5,8),3:(9,12),4:(13,16),
 5:(2,3),6:(6,7),7:(10,11),8:(14,15).

Listing labels8 down to1 yields
E=(14,15,10,11,6,7,2,3,13,16,9,12,5,8,1,4). Labelling all eight output
pairs by8,...,1 recovers every S entry. The internal ascent is i=2;
the last earlier-smaller index is j=1. Then q_i=3,q_j=4, and the mixed
selected indices are(6,8,9,11), values(7,3,13,9), with3<7<9<13.
The complete open horizontal indices are7,8,9,10; selected8 and9 are
exempt. EVERY unselected point is(7,2) or(10,16), outside(3,13).

BELL888_MANUAL_K4_COMPLETE_CERTIFICATE_V1.json preserves all18 original
JSON fields and every manual table/parameter above. History/status/native-
zero labels retain their supplied documentary role; the historical
pending-review status does not describe the current stage. No native
mathematical source ran to make this certificate. Metadata comparisons
do not constitute computational mathematical evidence.

This proves the ENTIRE requested obstruction/count/encoding conclusion.
No sufficient shape condition, attained safe lower count, full-law gain/
mean/mass, all-height-two/matching impossibility, novelty or external
peer review is established. Exact agreed410 remains UNSOLVED. Theo must
ACTUALLY read this complete return before author alignment is claimed.
