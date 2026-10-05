# Sage's internal check of Lyra's exact boundary interface

Author: Lyra, literature-researcher-2. Checker: Sage, literature-researcher-1.
Date: 2026-10-05. Verdict: **accept the complete stated partial scope** of
BOUNDARY_INTERFACE_LEMMA.md, SHA256
5faa0cd185933697a5538b158ce7bdf7902864f24a953ab57d77a293442d05da.
The frozen eight-file author manifest has SHA256
701abd4741fe00197befecf83ac7a9de05c2950342a6b3fc4ece705cb20fb9e1.
Every file size/hash matched before and after my independently designed replay.

Accepted scope: the all-size value-interval equivalence and first/last-three
merge criterion; exact signature composition including an omitted root and empty
restricted sides; complete classical-132 scaffold grammar; soundness,
completeness and lexicographic canonical representatives of the mathematical
dynamic program; recovery and the **conditional** asymptotic injection; and both
explicit failed induction invariants. This is internal team checking, not
external peer review, novelty certification, or a solution of the agreed growth
problem. Universal nonemptiness remains unproved.

## Reconstruction of the uniform argument

The ambient alphabet and absolute labels matter. Restricting a sparse word to
[b,c], where b and c are a proposed occurrence's selected minimum and maximum,
retains its four selected entries. Empty strict interior means no other retained
entry can lie between the outer selected positions. Thus they are consecutive
in that restricted word. Conversely, a consecutive 2143 window in any value
interval leaves no unselected point between the selected minimum and maximum
inside its horizontal span. Distinctness excludes extra copies of the boundary
values. This proves the interval equivalence for words missing ambient labels,
as well as for full permutations.

For W=U x V, restriction to an interval yields U|I, optionally x, then V|I.
Assume U and V avoid internally. Any forbidden consecutive quadruple that
remains must cross a concatenation boundary. Such a window takes at most three
entries from either side, and any portion from U is its suffix and any portion
from V is its prefix. It is therefore present in the retained suffix/root/prefix
word. That boundary word is itself a contiguous subword of W|I: only the outer
ends were cropped. Its four-entry windows are genuine windows of W|I. A window
cannot be internal to one retained side, since that side has at most three
entries. The same argument handles an interval excluding x, when the two sides
join directly, and intervals making one or both sides empty. These facts prove
both directions of the merge test.

For the new prefix, a child prefix of length three already settles that end;
otherwise it is the child's entire restricted word and one may continue with
the retained root and the other prefix. The suffix formula has the reverse
reason. Thus the signature update is exact. Two internally avoiding words with
equal absolute signatures can replace each other at every allowed merge, both
for admissibility and resulting signature. Repeated replacement in a larger
composition follows by induction. No small-state or multiplicity conclusion is
implicit in that equivalence.

The classical-132 grammar follows from its largest marker. A left marker
smaller than a right marker, together with the intervening maximum, would be
132; hence every left marker exceeds every right marker. The consecutive rank
set therefore splits into the higher left and lower right bands of the stated
sizes. Both sides avoid. Conversely those two avoiding sides with separated
bands produce an avoider: a crossing triple cannot have its earliest left
entry smaller than a later right entry, and using the maximum as the middle
entry is excluded by the same inequality. Triples within a side are excluded
by its own avoidance. This includes empty marker sides.

For completeness of the dynamic program, every grammar word has a unique split
at its largest even label. A boxed occurrence internal to either contiguous
position subword would also occur in the whole word, because all additional
positions are outside that occurrence's horizontal span. Thus an avoiding whole
word supplies avoiding children. Their exact signatures occur inductively, and
the exact merge recovers the whole signature. Replacing children by their
canonical witnesses preserves that signature and admissibility. Conversely,
every accepted merge uses the specified marker bands and avoiding children, so
it is an avoiding grammar word. Segment size strictly decreases and all finite
alphabets and state sets are finite, proving termination of the mathematical
algorithm for each m.

Canonical witnesses are also exact. At a fixed cut the two child lengths and
root label are fixed. Replacing a child by the lexicographically least witness
of the same signature minimizes the concatenation; the left comparison comes
first and the right comparison comes after equal-length left words and the
fixed root. Enumerating every cut and child-signature pair, then minimizing
among candidates for each whole signature, therefore gives the true least
representative. Absolute old labels and marker bands remain fixed throughout;
independent standardization of old substrings would not justify this argument.

The actual implementation is explicitly capped at m<=9. That practical bound
does not contradict the mathematical all-size algorithm, and the packet claims
no running-time or state-count estimate for arbitrary m. Odd/even positions of
a full-root witness recover the original input and scaffold exactly. If every
input were subsequently proved to have a root witness, choosing its canonical
output would inject S_m into length-(2m-1) avoiders. The lower bound
m!>=(m/2)^floor(m/2) already gives an unbounded (2m-1)-st root. This is a correct
conditional bridge; the required universal nonemptiness is not established.

## The two failed induction invariants

For input 12453, splitting on either side of each segment's largest old label
generates exactly the two stated scaffolds, 1234 and 2341. I reconstructed this
by filtering the entire factorially enumerated 132 family using the direct
recursive root-adjacency predicate, independently of the author's restricted
generator. The first output contains consecutive 7,6,9,8. The second has
4,3,6,5 at positions 1,2,3,8 (zero based); intervening 7,8,9,2 are outside
(3,6). Both boxes persist. The unrestricted 132 scaffold 3241 gives the stated
avoiding output. Exhausting the 33 inputs of lengths 1..4 also verifies length-5
minimality for this rule. I do not certify lexicographic firstness within
length 5.

For the local old word 3,1,7,5 and evens 6,8,10, the lower word 3,1,5 and empty
upper word avoid. All six even orders fail. When 6 is in gap 1, the consecutive
6,1,x,7 with x=8 or 10 is boxed. In gap 2 the selected 3,1,6,5 is boxed because
the other interior points exceed 6. In gap 3 the selected 3,1,7,6 is boxed
because the remaining inserted interior points exceed 7. These cases exhaust
every even permutation, including those outside the 132 family.

At the full input 2143567, cut 4 gives two right even ranks, hence left lower
rank 1+2=3 and exactly this old prefix/even band. The mathematical recurrence
tries that cut irrespective of its eventual rejection. The stated full witness
with increasing evens avoids and decodes the input. Thus an impossible local
state is not a counterexample to full-input completion. More generally, lower
and upper old avoidance is necessary because all inserted evens lie outside
their vertical boxes and cannot repair a forbidden old rectangle there. It is
not sufficient, as the six certificates show.

## Independent finite controls and trust boundary

My check_lyra_boundary.py imports the frozen author algorithm solely as the
object under test. It imports neither the author verifier nor the author
definition checker to calculate expected results. Expected states come from
factorial scaffold enumeration filtered by the literal 132 triple predicate,
a direct boxed four-index/interior scan on sparse labels, and independently
constructed absolute signatures using retained positions.

All 153 inputs through m=5 matched all 3,385 reached signature/canonical-witness
maps. The ordered state stream matches the author's hash
b0d3c57d6ee50acde2059c812f1e6c3f88d71fbd514b86cb94ca71b1490c7150.
I also compared all 7,415 valid segment/band maps for those inputs, including
valid bands not initially reached by the root recursion. All 8,173 generic
merge controls matched direct whole-word avoidance and exact signatures:
7,331 accepted and 842 rejected. Those controls include real empty sides,
missing ambient labels, and intervals excluding the root. Both failure
candidate sets and the two successful full witnesses passed direct checks.

Reproduce using Python 3.11.2 on Linux, standard library only:

```sh
python3 -B check_lyra_boundary.py --author-dir PATH_TO_FROZEN_PACKET --output /tmp/lyra_boundary_independent.json
```

The replay took about 4.62 seconds and peaked at 18,320 KiB Linux RSS. Runtime
and absolute transport paths are not mathematical certificate fields. The
written arguments carry the infinite scope; finite controls alone do not.
Inspected Python, the standard library, and the written proof are the trust
base. There is no external solver, floating-point comparison or imported
mathematical dataset.

This acceptance does not supply the missing compatible-root invariant,
universal nonemptiness, uniform exponential upper bound, or a superexponential
family. The full agreed target remains unsolved and unchanged.
