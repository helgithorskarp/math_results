# Theo's separate complete partial review of Quinn556

Author: literature-researcher-3. Checker: literature-researcher-4.
Verdict: accept the entire all-label three-case obstruction, its infinite
power-of-two prefix family, the conditional full-growth bridge, and both
complete finite certificate controls. This is internal team checking, not
external peer review or a novelty judgment. Full agreed target410 remains
unsolved. No earlier534/552 scope or public/graph original is extended.

The frozen eight-file manifest has SHA256
45a4024a52184fde920ab9a5ce727608c2303ae79460c0281171583a7facbc07.
The proof LEAF_BAND_OBSTRUCTION_V1.md has SHA256
eb91d9ab535aa53cc50a6d042a581fcf9e88d863c2f24d605085e4c4218678fa.
Every file and all seven named previously checked dependencies matched before
the independent replay. Original author source and certificates are unchanged.

## All-label and infinite-family proof reconstruction

For sigma2143 the eight leaves have relative order6,1,5,2,8,3,7,4. Denote
the full perfect15-node inorder word
H1,X1,L1,R12,H2,X2,L2,M,H3,X3,L3,R34,H4,X4,L4.
The high order is H2<H1<H4<H3, and each low is below every high. Heap
order gives Xi>Hi,Li; R12>X1,X2; R34>X3,X4; M>R12,R34.
Internal priorities are otherwise arbitrary, so distinctness makes the
following cases exhaustive.

If X2<H3, then L2<X2<H3<M. Positions5,6,7,8 are consecutive, hence their
2143 rectangle has no unselected interior point. If X2>H3 and X1<H3,
then H2<X1<H3<M. Select positions1,4,7,8; their unselected interior
entries are L1,R12,X2,L2. Both lows are below H2, and R12 and X2 exceed
H3. This is boxed2143. Finally if X2>H3 and X1>H3, select high leaves
at positions0,4,8,12. They have the2143 order. Every unselected low is
below H2. The unselected internal values X1,R12,X2,M are above H3 by
the case and heap inequalities, as are X3 and R34 by heap order. X4 and
L4 are after the final selected position. Thus that rectangle is empty.
These arguments do not fix internal ranks, restrict scaffolds or use a search.

For every power-of-two m>=4, sigma=(2,1,4,3,5,...,m) gives this same
configuration in the leftmost eight leaves. In a perfect tree they occupy
one whole height4 subtree, with15 consecutive inorder entries. Its first
four high leaves have the same order and all four corresponding low leaves
remain below them. Applying the preceding cases within that subtree produces
a boxed selection whose horizontal span is wholly inside it; outside entries
cannot shade it. The same argument works for any aligned four-pair block
with high order2143. Therefore omitting finitely many small powers of two
does not rescue this prescribed format. Variable shapes and other encodings
are not covered by the obstruction.

Had Hypothesis L held for every input at m=2^k, choose one standardized
completion per input. Standardizing its entries at positions0,4,8,...
recovers sigma, so distinct inputs give distinct avoiders of length4m-1.
Consequently a_(4m-1)>=m!, and (m!)^(1/(4m-1)) tends to infinity; already
the last ceil(m/2) factors, each at least floor(m/2), prove this divergence.
This is a correct conditional full-target mechanism, not a completed result.
The all-label counterexample falsifies its universal existence hypothesis.

## Independent labeled reverse certificate

The accepted reverse-merge characterization applies to shapes with original
position IDs as labels. Deleting the current maximum preserves the inorder
order of those IDs. In descending rank order, a prescribed leaf can be
deleted precisely when its relative priority is the largest among remaining
prescribed leaves. Internal nodes have no assigned relative rank; their only
heap requirement is that the next deleted node be the current root. Thus the
current named tree suffices as a state. A complete reverse history would
standardize to a valid full-rank heap labeling with the prescribed leaf order.

My check_quinn_leaf_band.py enumerates shuffle positions and reconstructs
named parents from the bottom up, rather than the author's recursive two-
branch merge generator. It checks every proposed merge against direct
nearest-greater value geometry on an independently assigned heap representative,
in addition to the already checked word grammar. It explores the reachable
named-tree DAG breadth first and compares current known-leaf ranks directly,
instead of recursive first-success search and a cached maximum-leaf function.
There is no reachable empty state. All2661 states and4784 legal branches
match the author certificate;7352 total merge candidates receive the geometry
check. Complete per-size states and the new transition stream hash are saved.
The uniform case proof independently certifies nonexistence even without this
finite search, and the search supplies a second independent derivation.

## Complete native property certificate and inspected bounds

I independently reconstruct all43 perfect size7 avoiding permutations from
all5040 labeled inputs and the boxed definition. Their order and every byte
of the native input agree. I inspect the C++ selector: it takes the eight
even-index leaves of each size15 word, sorts their distinct values, obtains
ranks1..8 and compares them to exactly6,1,5,2,8,3,7,4. This implements the
new property, not a mere count of generic perfect avoiders.

I compile and replay the pinned author native source in a fresh temporary
directory with C++20/O2 and all five requested warning options. Warnings
are empty. Every field of its full JSON matches, including all1849 pair
counts,6345768 candidates,790086 valid joins and zero target-profile
completions. All old table fields also match the independently498-checked
certificate. The join enumeration is complete by the accepted root-join
identity: restriction to either child preserves avoidance, and each root
join is specified by its two standardized child words and its unique rank
partition. The numerical candidate count is independently
43^2*binomial(14,7)=6345768. The three-case proof separately explains why
the newly selected profile has no valid word.

All input values/ranks are validated distinct. Native m is7, output length15,
mask shifts are at most14 and the proposed-bound shift is3. Every array access
has its displayed length bound. The partition, pair and sum counts are far
below uint64 capacity. The input has no trailing data or duplicate word.
Although the native executable does not itself validate each child's perfect
shape, my complete input reconstruction does; preserving child relative orders
and adding a largest root then forces the output perfect shape. No sanitizer
run or second independent native implementation is claimed in this review.
The independent reverse and uniform case proofs supply separate checks of
the zero-property claim; old numeric table fields have their prior independent
DP check plus this exact replay.

Total replay5.942seconds, native run3.441seconds. Python peak RSS24012KiB;
RUSAGE_CHILDREN peak138916KiB includes the compiler and native executable,
so it is not attributed to the native run alone. One intensive child job ran
at a time, with the Python parent waiting; native threads1. The first raw
report's resource labels were ambiguous. Its exact bytes and executed source
are preserved, and quinn-leaf-band-reproduction-v2.json corrects only those
labels, with hashes; mathematical fields are unchanged. No unnecessary
mathematical rerun was performed for this metadata correction.

## Exact scope and reproduction

Artifacts: check_quinn_leaf_band.py, quinn-leaf-band-reproduction-v2.json,
the preserved first raw report/source, compiler/native stdout/stderr and
quinn-leaf-band-native-replay.json. QUINN_LEAF_BAND_REVIEW_MANIFEST.json pins
this full review, source, evidence and complete imported own dependencies.
Reproduce with CPython3.11+ and g++ supporting C++20:

```
python3 -B check_quinn_leaf_band.py --output /tmp/theo-leaf-band-new-run.json
```

The source manifest is checked before computation; any existing output is
preserved. The full growth statement, population-average joining route and
unrestricted completion conjecture remain open. No target pivot, conclusion
from finite favorable ratios, relaxed success criterion or claim of external
peer review is accepted. Quinn owns publication of this distinct new scope.
