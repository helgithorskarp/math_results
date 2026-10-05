# Theo's separate review of Sage's simple-marker refinement

Reviewer: literature-researcher-4 (Theo), 2026-10-05.
Author: literature-researcher-1 (Sage).
Verdict: **accept the complete stated uniform partial scope S1–S3**, with
the exclusions below. This is internal different-researcher checking,
not external peer review or novelty certification. Target410 is unsolved.

New proof `MARKER_SIMPLE_REFINEMENT_DRAFT.md`:
SHA25620875be828aab1516dc15b988bad0d70be99cfc6d5f6142ec9f53e984c460e5d.
Eight-file packet manifest:
4071acf23136510a8d1d621dc333b90163f120289025e686816288df12d09eb9.
All files were byte-matched before copying to `received/sage_simple_marker_v1/`
and rehashed after the check. Review473 of the older marker map is a stated
dependency for its uniform occurrence bijection and common tree pair; it
does not preaccept simplicity, padding or the new simple viability claim.

## Uniform proof reconstruction

For M>=2, every three successive entries of Phi contain exactly one low
marker, one free point and one high marker. Any contiguous segment of
length at least three therefore contains values below M and above2M-1.
Consecutive values in such an interval would contain the entire free band
M..2M-1. In particular it would contain X1 and XM, which are at the first
and last positions, so the segment must be the whole permutation. This
excludes all proper intervals of length>=3 without assumptions on sigma.

Adjacent X_i,H_i have difference M+i-sigma_i>=i; equality1 is possible
exactly at i=1,sigma_1=M. Adjacent H_i,L_i have difference2M-1>=3. Adjacent
L_i,X_(i+1) have difference M-1+sigma_(i+1)-i>=M-i; equality1 is possible
exactly at i=M-1,sigma_M=1. Hence the two asserted endpoint conditions are
necessary and sufficient for simplicity. This also handles M2, where Phi
has length4 and both endpoint intervals are proper.

For padding tau=(1,pi+1,m+2), the new minimum is first and cannot play
selected role2; no other role has minimum rank. The new maximum is last
and cannot play selected role3; no other role has maximum rank. These
points are also horizontally outside every old selection. Thus padding
preserves the complete boxed occurrence set, with old indices shifted by1.
Its first/last ranks avoid the two forbidden endpoints of S1. Applying the
accepted Phi correspondence gives a simple extension of length3m+4,
with old selected indices mapped to3(i+1). Reading every third point,
removing the padding and subtracting the known offsets recovers pi.
The old common-pair theorem applies at M=m+2, independently of the input.
Consequently this is an injection into one simple tree-pair fiber and
s_(3m+4)>=a_m. Its band-restricted avoiding image is exactly a_m; arbitrary
nonavoiding inputs retain their occurrences and are not repaired.

For S3, the separately checked pair and low-marker prefix make exactly the
M free positions heap-available. At every t<M, taking sigma with1 at t and
all other ranks increasing gives a classical2143 avoider: every inversion
ends at the same1, so two descending selected pairs cannot exist. It also
satisfies S1: for M>=3 its first value is1 or2, its last value is M; for
M2 the sole t=1 witness is12. Each image is a simple avoiding completion
sharing the same pair and prefix and placing rank M at X_t.

The last free position cannot be viable in any simple completion, even
outside the image: the fixed preceding low marker at the penultimate
position already has rank M-1. Placing M at the last position forces an
adjacent consecutive-value interval of length2, which is proper because
3M-2>=4. Together with the exact heap availability this proves precisely
M-1 viable next positions for every M>=2, without an upper bound inferred
only from the constructed witnesses.

## Independent exact controls

`check_sage_simple_marker.py` imports no author executable. It uses Theo's
previous independently constructed zipped-band map, iterative extrema
trees and set-valued predecessor availability from `check_sage_marker.py`.
Every proper interval is checked by sorting its actual value set, rather
than invoking the author's endpoint criterion or running min/max scan.
Complete occurrence sets use both direct quadruple/interior geometry and
the separately checked value-interval rectangle scanner.

All872 inputs M2..6 reproduce the full proper-interval classifications,
simple counts and exact interval streams. All153 extensions m1..5 reproduce
padding and final complete occurrence sets, decoding, common pairs and every
extension stream. All66 positive simple-branch witnesses through M12 are
checked, along with exact heap availability and the final interval obstruction.
All author deterministic control fields match.

Additional exhaustive controls enumerate every remaining rank assignment
after the fixed prefix at M2,3,4, including assignments outside the
band-restricted image. There are6,120,5040 total assignments respectively,
of which2,8,48 have the common tree pair and1,3,15 are simple avoiders. The
sets of viable next positions are exactly {0}, {0,3}, {0,3,6}, matching S3.
These finite checks support the uniform exclusion of the final position;
they do not supply an asymptotic multiplicity bound.

Replay from this directory:

```sh
python3 -B check_sage_simple_marker.py --output /tmp/theo-sage-simple-marker.json
```

Evidence: `sage-simple-marker-reproduction.json`, Python3.11.2,
one process/thread,0.683seconds,20964KiB peak RSS. The source snapshot and
all reviewer dependencies are pinned in the review manifest.

## Limits

Neither the occurrence-preserving simple extension nor the M-1 local
viability count gives factorial growth or an exponential upper bound.
No arbitrary-input repair, universal132 completion, constant-fiber bound,
global history-count estimate or novelty assertion is accepted. This is a
separate partial review from473 and from Theo's inflation/simple-count
equivalence. Sage owns publication of these exact new bytes; the earlier
public marker source and its pending graph original remain unchanged.
