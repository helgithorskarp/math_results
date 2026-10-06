# All-size obstruction and exponential survivor bound for the Bell leaf rule

Theo/literature-researcher-4,2026-10-06,normal workday12.
NEW AUTHOR HAND theorem, after completed independent858 return882. It is a
separate claim, not in858 preregistration/source/job/return, and not yet
independently checked. ZERO new author native mathematical jobs, no partition
census/complete box sets/fitted mean. This gives negative evidence for one
existing proposed full-target construction, not a replacement target.
The full exact410 remains unchanged ACTIVE/UNSOLVED. No novelty/publication
priority, external peer review, full avoiding-class bound or completion claim.

## Definition and exact theorem

For k>=1 and sigma in S_k, put the increasing roots1,...,k in that order,
and pair root i with leaf k+sigma_i. Its height-two Stirling word is

 S(sigma)=(1,k+sigma_1,k+sigma_1,1,2,k+sigma_2,k+sigma_2,2,...,
           k,k+sigma_k,k+sigma_k,k).

E pairs FIRST/SECOND ONE-BASED positions of labels2k,2k-1,...,1.
Its length is4k. Define a Bell leaf sigma from a set partition P of[k]
by listing each block decreasingly, with blocks in increasing order of
minimum. Let T_k be the number of these INPUT partitions whose E avoids
the exact full boxed2143 rectangle. The map is injective: E recovers S by
assigning label2k-r+1 to its rth pair of positions, S recovers each root's
leaf/sigma, and maximal descending runs of sigma recover the Bell blocks.
Thus T_k also counts distinct avoiding images from this specified rule.

THEOREM (author hand proof, separate entire internal check requested):

(A) For arbitrary sigma, if E(S(sigma)) avoids, then every ascent
    sigma_i<sigma_(i+1) with1<=i<=k-2 has its lower point a LEFT-to-RIGHT
    minimum: sigma_j>sigma_i for ALL j<i. No such constraint on the last
    possible ascent i=k-1 is asserted.
(B) A surviving Bell partition has at most TWO blocks, or exactly THREE
    blocks whose final block in minimum order is a singleton.
(C) T_1<=1. For EVERY k>=2,

             T_k <= (k-1)*2^(k-2)+1.

    In particular limsup_(k->infinity) T_k^(1/(4k)) <= 2^(1/4).
    Optimal pruning within this EXACT Bell leaf rule still has finite
    exponential growth; its unrestricted Bell count cannot prove the full
    negative410. No claim for different encodings or all avoiding inputs.

The conditions are NECESSARY, not sufficient; the original858 fifth witness
has three blocks/final singleton, yet a separate leaf rectangle rejects it.
No actual avoiding-family lower bound or full law/mass transport is implied.

## 1. Position formula, with one-based indices throughout

For root i, the S positions are(4i-3,4i) and its leaf positions(4i-2,4i-1).
The FIRST2k entries of E consist of the leaf pairs, in decreasing leaf-label
order. Set q_i=k+1-sigma_i. The two E indices of leaf i are2q_i-1,2q_i,
with values4i-2,4i-1. All leaf pairs occur exactly once.

The FINAL2k entries consist of root pairs i=k,k-1,...,1. Root i's E indices
are2k+2(k-i)+1 and2k+2(k-i)+2, with values4i-3,4i.
These formulas explicitly cover every point of E, with no imported checker.

## 2. A mixed empty rectangle for a nonminimum internal ascent

Suppose2<=i<=k-2, sigma_i<sigma_(i+1), and an earlier smaller value exists.
Choose

               j=max{t<i: sigma_t<sigma_i}.

Then1<=j<i; for every j<t<i we have sigma_t>sigma_i. Also
sigma_(i+1)>sigma_i. In the leaf prefix, ALL pairs for labels t in
{j+1,...,i-1,i+1} therefore occur strictly BEFORE pair i. This uses that
q_t<q_i is equivalent to sigma_t>sigma_i, not any guessed prefix law.
The leaf pair j occurs after pair i, since sigma_j<sigma_i.

Select the high of leaf i, the high of leaf j, the core of root i+2,
and the core of root i+1. Their ONE-BASED indices and values are

 indices=(2q_i,2q_j,4k-2i-3,4k-2i-1),
 values =(4i-1,4j-1,4i+5,4i+1).

They are strictly ordered indices:2q_i<2q_j<=2k<4k-2i-3<4k-2i-1.
The roots exist because i<=k-2. The selected second<first<fourth<third
inequality follows from j<i. Thus they form2143 with open band
(4j-1,4i+5). Check EVERY unselected horizontal point as follows.

* In the leaf prefix, labels t<=j give values<=4j-1, and labels t>=i+2
  give values>=4i+6. They are outside the open band. All potentially
  in-band pairs j<t<i or t=i+1 lie before the FIRST selected point,
  as proved above. Leaf i's low also precedes its selected high; leaf j's
  high is selected and its low is below the band. This exhausts all leaf
  pairs, including all points after the second selected point.
* In the root suffix up to root i+2, labels t>i+2 have even their lower
  endpoint>=4i+9, above the band. The lower endpoint of root i+2 is the
  third selected point. Its high, the only point between the third and
  fourth selected roots, is4i+8, above the band. The next root's lower
  endpoint is the selected right boundary. Its high and all later roots
  occur AFTER that boundary.

The strict rectangle is empty. No endpoint is omitted, and selected
exceptions/open boundary inequalities are explicit. This contradicts
boxed avoidance and proves(A). The case i=1 always has a prefix minimum,
so it needs no obstruction. The case i=k-1 genuinely lacks root i+2 and
is deliberately excluded, including the original k5 fifth hand witness.

## 3. Consequence for ordered Bell blocks

Write the Bell blocks as B_1,...,B_b in increasing minimum order.
Within each block sigma decreases. Every block boundary is an ascent,
because its lower point is min B_s and the next block's maximum is at
least min B_(s+1)>min B_s. All earlier blocks have smaller minima.
In particular, the SECOND boundary (after B_2) has lower value min B_2>1,
while an earlier entry1 is present in B_1. It is not a prefix minimum.
Its index is i=|B_1|+|B_2|>=2. If b>=4, at least two entries remain,
so i<=k-2 and(A) rejects the input. If b=3 and |B_3|>=2, the same holds.
Consequently any surviving input must have b<=2, or b=3 and |B_3|=1.
This proves(B). It does NOT assert all partitions meeting(B) survive.

## 4. Exact count of the necessary surviving shapes

For k>=2, partitions into one or two blocks number2^(k-1): the one-block
case plus every nonempty subset of{2,...,k} as the block not containing1.
For a three-block partition with final singleton{r}, r must be at least2.
The other two blocks have minima less than r. Anchor the first by1.
Its complementary block Q is a subset of[k] minus{1,r} and must meet
{2,...,r-1}. Thus exactly

                   2^(k-2)-2^(k-r)

choices correspond to this r, including zero for r=2. There is no double
count: the singleton is uniquely the last block and Q is uniquely the
non1 nonsingleton-order block (Q itself may be a singleton). Summing r=2..k:

 sum_r (2^(k-2)-2^(k-r)) = (k-3)*2^(k-2)+1.

Adding the one/two-block shapes gives (k-1)*2^(k-2)+1. This counts a
necessary allowed superset, NOT a safe-input table. For k=1 there is only
one input. Taking4k-th roots gives(C); the polynomial factor disappears
and the exponential factor contributes2^(1/4). Thus no pruning of THIS
specified rule can have unbounded output roots, even without identifying
which of its permitted shapes actually avoid. It gives no upper bound on
a_n for all permutations, no estimate on a different source population,
and no justification to mark full410 solved or replace the agreed target.

## 5. A new hand-selected falsifiable control at k4, no native job

Take P={{1},{2},{3},{4}}, sigma=(1,2,3,4). Its second boundary i2 has
sigma_2=2, sigma_3=3 and largest earlier-smaller index j1. Here
S=(1,5,5,1,2,6,6,2,3,7,7,3,4,8,8,4) and
E=(14,15,10,11,6,7,2,3,13,16,9,12,5,8,1,4).
The formula selects ONE-BASED indices(6,8,9,11),values(7,3,13,9).
ALL unselected horizontal points are(7,2),(10,16), outside(3,13).
This is hand-derived after858's one independent job, not a preregistered
native experiment or partition census. Any different reviewer may use
hand reasoning or a proportionate prospectively bounded exact check.
The uniform proof is required even if this small example agrees.

No source executable for this NEW author theorem has run. The existing
858 reviewer source/control tests different original five inputs only,
and supplies NO acceptance or finite test of this new theorem. Preserve
that separation, chronology, all qualifications and any objections.
