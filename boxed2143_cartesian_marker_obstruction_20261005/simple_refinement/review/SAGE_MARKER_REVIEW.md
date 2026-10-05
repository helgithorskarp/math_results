# Internal full-scope check of Sage's marker obstruction

Author: Sage, literature-researcher-1. Checker: Theo, literature-researcher-4.
Date:2026-10-05. Verdict: accept Claims1–3 and the stated finite H1
counterexample/length minimality at proof SHA256
`bb901334aba7735664bfe9668a16617305e5b4834e2b0944a722eafaef2125d6`.
The immutable eleven-file packet manifest SHA256 is
`19770ba1b80858ff0e991707e0bf5894db09a6da68a50e83f067323b7eefaf4b`.
Every file's size/hash matched before and after my replay. This is internal
team checking of a partial obstruction, not external peer review, novelty
certification or a resolution of the boxed2143 growth decision410.

## Complete uniform argument

I checked the band values and positions, all occurrence cases, both tree
formulas, the prefix/availability/viability distinction and the exact entropy
limitation. Here is my reconstruction of the argument.

Write the image as X1,H1,L1,...,X_(m-1),H_(m-1),L_(m-1),Xm, with all low
values below all free X values, and all high values above them. Both marker
sequences increase in their position order. Any selected low point would
include a selected low minimum in role2. Suppose that minimum is L_j.
The first point cannot be low, because earlier lows are smaller. The final
point cannot be high: if the maximum is free, high values exceed it, while
if it is high, all later high values exceed it. Nor can the final point be
low, because it must exceed the nonlow first point. Thus the last point is
free and so is the first, since a high first point would exceed a free last
point. The maximum is free or high. If the last point is X_t, a maximum
must fit after L_j and before X_t; the immediate successor X_(j+1) leaves
no such place when t=j+1. Hence t>=j+2, and the unselected L_(j+1) lies
horizontally inside the box and vertically between the selected minimum
and maximum. This contradicts emptiness. The available indices guarantee
that L_(j+1) exists, including the end cases.

After excluding every selected low, any selected high forces a selected
high maximum H_j in role3. The last point cannot be high, since later
highs are larger, and is therefore free. Its smaller first and minimum
points must also be free. If they are X_i and X_k, their order gives
i<k<=j. Consequently j>=2 and i<=j-1. The unselected H_(j-1) lies after
the first point and before the last, with value above the selected minimum
and below H_j. It blocks the rectangle. This excludes every selected high.

Every occurrence is therefore all free. The free points have exactly the
input's relative orders, and every marker is vertically outside their box.
The old selection is boxed exactly when its free lift is boxed. Multiplying
zero-based indices by3, or taking3i-2 in one-based indexing, gives the exact
occurrence-set bijection, including multiplicities. Reading every third
position and subtracting m-1 decodes the input uniquely. The separate m=1
control is the identity; the uniform nontrivial construction uses m>=2.

For the minimum tree, the listed low right spine and X_i/H_i attachments
have the required inorder sequence, with every parent smaller than its child.
For the maximum tree, the listed high left spine and X_(i+1)/L_i attachments
likewise have that inorder sequence and the reverse heap property. An
inorder binary tree with the appropriate heap order is uniquely the
Cartesian tree: the root is the interval extremum and its two sides recurse.
Thus both explicit parent arrays hold independently of the free-value
ordering. The same uniqueness proves the generic common-linear-extension
description for a compatible tree pair. This is the known encoding context,
not a novelty claim.

After assigning ranks1,...,m-1 to the low markers, every free position's
incoming heap constraints have been assigned. Each high H_i still has incoming
constraints from X_i and X_(i+1), so no high position is available. Exactly
the m free positions are available. This is not yet viability. To certify
each free position t, take the input with its1 at t and all other entries
increasing. Every inversion ends at that same1, whereas a classical2143
requires two inversion pairs with distinct lower endpoints. This input
classically avoids and hence boxed-avoids. Its image is an avoiding complete
assignment with the common tree pair and low prefix, assigning the next
rank m at X_t. All m choices are consequently viable. This establishes
unbounded local viable branching without appealing to finite examples.

The band-restricted slice has exactly m! assignments and, by the occurrence
bijection, precisely a_m avoiding assignments at length3m-2. This preserves
the original unresolved entropy; it does not turn arbitrary inputs into
avoiders. An unbounded choice count at one prefix does not rule out an
exponential bound on entire fibers. Weighted or global encodings remain
possible. The author states these limitations correctly.

## Finite H1 obstruction and independent code checks

For4163725, the minimum parent array is(1,-1,3,5,3,1,5), and the maximum
array is(2,0,4,2,-1,6,4). After ranks1 and2 are assigned at positions1 and5,
the union of heap constraints leaves positions0,3,6 available. Rank3 is
at the interior position3. My direct rectangle and literal quadruple checks
both show this permutation avoids boxed2143. Exhaustion of all874 permutations
of sizes0..6 establishes length7 minimality. I have not independently checked
the finer claim that this is the lexicographically first length7 witness.

`check_sage_marker.py` independently builds images by zipped value bands,
builds parent arrays by iterative interval extrema, and computes available
sets from ordinary predecessor sets rather than the author's stack/bitmask
code. It imports the author functions only to compare the actual map and
formula outputs. It does not import the author verifier or another team's
expected occurrence algorithm. Direct quadruples/interior scans and my
canonical rectangle representation agree on every lifted occurrence.

The complete controls cover873 inputs of sizes1..6, their images through16,
all77 viable-position witnesses for m2..12, and the874 smaller permutations
for the H1 length assertion. Every author base stream and viable-witness
stream hash agrees. The detailed size8 fiber-audit table is not certified
by this review; it is additional author finite evidence outside the requested
uniform marker/H1 scope.

Reproduce from this directory:

```sh
python3 -B check_sage_marker.py --output sage-marker-reproduction.json
```

Use `--author-dir` for an unchanged transferred review packet. The source
manifest is checked before and after. The independent run used CPython3.11.2
and its standard library, took about1.315seconds and peaked at21576KiB Linux
RSS. No solver, external dataset, approximate mathematical comparison or
native parallel job was used. Reproduction hashes, not measured runtime,
identify the evidence.

The written arguments, inspected code, Python and the standard library form
the trust base. This acceptance supplies a precise failed bounded-branching
route and an occurrence-preserving embedding. It does not supply the missing
uniform fiber bound, persistent high-entropy family or full410 solution.
