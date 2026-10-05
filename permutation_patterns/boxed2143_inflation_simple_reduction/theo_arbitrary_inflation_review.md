# Separate Lyra review of Theo's arbitrary-inflation packetv1

Reviewer: literature-researcher-2 (Lyra), 2026-10-05.
Author: literature-researcher-4 (Theo).
Verdict: **accept the entire stated uniform partial scope A--E**, with the
limits below. This is an internal different-researcher check, not external
peer review or a proof-assistant certificate. It does not solve target410.

Frozen author proof `ARBITRARY_INFLATION_BOUNDARIES_V1.md`:
SHA256 a577429ccb2563d53afdf81d5e20d89e882038948054a2c996c3c0f1b1bb455f.
Five-file manifest:38e79ef0acba1040cc4512501646cb642ea0392d2413ba7136ff535f650c4497.
Every manifest byte size and hash was matched before copying the packet to
`received/theo_arbitrary_inflation_v1/`. Earlier review450, publication and
graph receipt cover different bytes/scope and are not used as this acceptance.

## Uniform arguments reconstructed

**A, arbitrary nonrepair.** For each old boxed selection take last position in
its first block, global maximum in its minimum-value block, global minimum in
its maximum-value block, and first position in its final block. All bands are
disjoint and retain their old order. Residual points in the outer selected
blocks lie horizontally outside; residual points in the two extrema blocks
lie vertically outside. Every other band inside the old horizontal span lies
below the minimum band or above the maximum band. Thus the lift is boxed.
Mapping selected positions back to their block indices recovers the original
selection, proving injectivity. Arbitrary block patterns cannot repair an old
box; this argument does not assert equality of occurrence counts.

**B, anchored additivity.** Consecutive position blocks force repeated selected
blocks to occupy consecutive roles. Roles2/3 in one block or three roles in
one block force the fourth there by the nested value comparisons. The only
other repeats are roles1/2 or3/4. An anchored maximum at the end obstructs
the former and an anchored minimum at the start obstructs the latter. Four
distinct selected bands project to an old boxed selection. In this case
every point after the first selection in its band would shade the box, so it
must be last; the final selection must be first. The minimum and maximum
selected roles must be their whole-block max and min respectively. Therefore
the canonical lift is the unique cross-block occurrence for its projection.
Wholly internal occurrences are unchanged. This gives exact addition, even
for anchored blocks with internal occurrences.

**C, universal safe-block classification.** The sufficiency follows from B.
Failure to avoid is exposed already in parent1. If the first entry is not
minimum, its first later smaller entry pairs with parent213 to give a box;
all intermediate block values exceed the selected top. If the last entry is
not maximum, its last earlier greater entry pairs with parent132 to give a
box; all intermediate block values lie below the selected bottom. Both
parents avoid by length. These necessity witnesses cover every unsafe block.
For an anchored block of size r>=2 the outer1/r cannot be selected as minimum
in role2 or maximum in role3 at those positions, and cannot play another
rank. Thus all occurrences lie in its lengthr-2 interior and persist there
exactly; the safe count is a_(r-2), with empty size0 interior handled at r2.

**D, full composition identity.** The partition by selected block indices is
exhaustive: one block, four distinct blocks, repeated first descending pair,
repeated final descending pair, or both pairs repeated. Cases overlapping
middle roles or triples are forced into the one-block case. For a repeated
first pair (a,b), empty interior means every later point in that block except
b is below b. This is equivalent to b being a right-to-left record with a
greater earlier point, with a its unique nearest greater predecessor. The
dual last pair (c,d) has all earlier points except c above c; c is a left-to-
right minimum with a smaller later point, and d is its unique nearest smaller
successor. These give exactly R and L choices.

Three selected bands have parent orders132 or213 respectively; the two-band
case has order12. In each case every unselected interior parent band is
vertically interior in the inflated word iff it is interior in that smaller
boxed parent selection. Selected single-role bands have the forced extrema
or position-boundary point described in A/B. These establish each product
term and a bijection, rather than just an inequality. No count term is
missing from the displayed formula. R=0 iff the block ends at maximum and
L=0 iff it starts at minimum, so the anchored identity is its correct
special case.

**E, equivalence with simple-avoider growth.** Minimal proper nonsingleton
interval contraction is legitimate. Its standardized block is simple:
any proper nonsingleton interval inside it would be a smaller interval of
the original permutation, because both position and value bands are
consecutive. The child block avoids by contiguous-position heredity; the
contracted quotient avoids by A's contrapositive. Repeating contractions
strictly shortens length. Reversing them by leaf grafts produces a tree
with only simple avoiding labels and degree at least2. Evaluating the tree
uniquely recovers the permutation. Choosing minimum size then leftmost
position gives a deterministic encoding, so arbitrary overcount of other
labelled trees is harmless.

For n leaves, I<=n-1 internal vertices, V<=2n-1 total vertices and sum of
internal degrees V-1<=2n-2. Counting all rooted ordered shapes with v vertices
by4^(v-1) and summing v<=2n-1 is strictly below16^n. Node-label bounds
s_k<=D^k multiply to at most D^(2n), for D>=1. Hence a_n<=(16D^2)^n,
including n1. The other implication s_n<=a_n is immediate. This proof uses
interval contractions, not an unjustified arbitrary-subsequence closure of
boxed avoidance. It retains the exact bounded-exponential decision target.

The general substitution machinery is prior work. I opened the primary
Albert--Atkinson author manuscript
https://cs.otago.ac.nz/research/publications/oucs-2003-08.pdf, Section2,
Proposition2, which states the simple-quotient inflation decomposition and
the12/21 uniqueness qualifications. The new packet supplies its own elementary
tree argument and no novelty claim; the primary theorem is credited rather
than transferred wholesale to a set lacking classical containment closure.

## Independent finite controls

`check_theo_arbitrary_inflation.py` does not call the author's rectangle,
composition, inflation-offset, recursive graft or evaluation routines.
Its direct quadruple/interior checker is our current frozen reference,
SHA256 c74ccd624c909386ad151947ae5a4f9c534b58602940ba39371e214d1e5b2149.
It uses the same bounded input domains to permit exact stream comparisons.

For every inflation it independently reconstructs the **complete predicted
occurrence set**, generating valid local descending pairs by their full
one-sided point geometry. It checks record-pair equivalence, disjointness
of all five categories, canonical lift injectivity, and equality with direct
boxed enumeration, rather than comparing counts alone. It covers4545
all-block cases,3927 single-block cases and422 anchored cases. All author
streams match:

* arbitrary2f0ec6abbefa9fb7c6ffbf831f3207318c45862c0465c5ba8eda3c5ec7c7afa6;
* anchored136fe69d10648a57c563d3f0939423f06981b81e2d4d110901742470488f0095.

All873 blocks through6 were classified with839 explicit unsafe contexts.
Their safe counts1,1,1,2,6,23 match the interior shift, and both statistic
boundary equivalences pass.

For all5913 positive-length permutations through7, the checker builds a tree
from an iterative contraction log, then decodes by sorting lexicographic
root-to-leaf rank paths. This is independent of the author's recursive
graft/inflation evaluation. It verifies decoding, simple internal labels,
the leaf/vertex/degree bounds and avoidance of all labels for every avoiding
input. The exact canonical tree stream matches
90705fc4bdea4bb094a5647096dc50adfa6087827123b6588e801c8606796da4.
The simple counts and fixture531642 also match their claimed finite scope.

Replay: `python3 -B check_theo_arbitrary_inflation.py` from this directory.
Evidence: `theo_arbitrary_inflation_reproduction.json`.
Checker source SHA2560b726d924047edfb404de8f5a3c5dec6fe4e39a6a73977926bdc160b634defd3.
Python3.11.2, one process/thread, runtime2.129s, peak20916KiB. No solver,
floating-point mathematical comparison or opaque certificate is used.

## Limits

These finite controls cannot prove the uniform statements; the separate
written case/counting arguments above supply the accepted scope. No
uniform simple-label bound, unbounded-rate simple family, all-input
completion construction, full-growth solution, priority certificate or
external peer-review claim is accepted. The new source may be published with
this precise review, but cannot inherit the earlier packet's source/graph
receipt. Any reviewer-code path substitutions for portability must be pinned
separately and their deterministic output compared with this frozen replay.
