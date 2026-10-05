# Theo's separate full partial review of Quinn's reverse/join packet

Reviewer: literature-researcher-4 (Theo), 2026-10-05.
Author: literature-researcher-3 (Quinn).
Verdict: **accept the entire stated uniform partial scope and the exact valid
counterexample to H**, with the exclusions below. This is an internal
different-researcher check, not external peer review or novelty verification.
The full agreed growth target410 remains unsolved.

Frozen proof `REVERSE_MERGE_AND_JOIN_BOUND.md`:
SHA2564a7469cd07b2c77ca79c9f1c03d50fb069d4640c0272d64a534a9f2fd39a96f7.
Manifest SHA256c9c19c86a3d33db6e725175f79069f56740751a5fa85e23fd67a7edb0da6baa8.
All19 author files and both dependency manifests were byte-matched;38 unique
source/dependency files are frozen in `received/quinn_reverse_join_v1/`.
Earlier review467 supplies the maximum-tree quotient as a stated dependency;
it does not preaccept any new reverse grammar, join theorem or certificate.

## All-size arguments reconstructed

For the two restrictions L,R of a parent at a fixed cut, only the right
spine of L and the left spine of R can participate in the Cartesian merge.
The parent root is one of these two roots. Removing it recurses with exactly
the opposite side and the boundary child. Off-spine subtrees remain attached.
Induction gives one parent per interleaving word and one word per parent.
Different first letters put the root on opposite sides of the distinguished
cut; equal first letters reduce to the same assertion on shorter spines.
This proves injectivity, completeness and the empty-side cases.

A blocker minimum to the left of the cut must be on L's right spine;
otherwise a greater right ancestor inside L ends its forbidden gap interval
before the cut. The first such spine node lacks a greater predecessor in L.
For each later node j, its immediate spine predecessor l is the nearest
greater position on its left: nodes between them are in j's left subtree
and smaller than j. The nearest greater position on the right, if present,
is the deepest R-left-spine node with priority greater than j. Its priority
exceeds l exactly when at least one R was processed before l and no R was
processed between l and j. This is exactly an adjacent LL after an earlier
R in the descending-priority word. A minimum to the right cannot block the
cut. Hence the proposed forbidden-word rule is necessary and sufficient.

For a child (L,R), deleting its maximum determines exactly one cut |L|.
Each legal incoming parent contributes all its avoiding labelings, and
different parent shapes or labelings cannot produce the same child
permutation. Conversely maximum deletion preserves avoidance and recovers
one of these incoming parents. The incoming weighted recurrence therefore
has no lost or duplicated multiplicities.

For a perfect tree, an avoiding permutation splits at the middle maximum
into two contiguous avoiding halves. Outside horizontal positions cannot
shade a box in a half; standardization preserves all comparisons and
emptiness. Its two standardized halves and the left value subset determine
the original uniquely. This proves the exact root-join identity, not a
heuristic product bound.

Under the proposed pointwise H, that identity gives
b_(h+1)>=2b_h+2^(h-1)-1. Its stated lower bound
b_h>=2^(h-2)(h-3)+1 follows by induction from b_1=0, including h1/2.
Since m_h=2^h-1, b_h/m_h diverges. Thus H really would imply the full negative
answer to410. No finite count supplies H, and the certificate below refutes
it rather than using it as an assumption.

The fixed-pair DP uses ascending global ranks. The source rank i+1 in alpha
has exactly G_alpha(i) smaller ranks before it; beta's next rank uses gap
i+G_beta(j). Higher source ranks have not appeared, so these are the correct
gaps in the concatenated retained halves, independently of the forgotten
rank partition. At a fixed total, j is determined by i. All histories with
the same (i,T) have identical future shape transitions and legality by the
accepted quotient. Summing their weights preserves their distinct global
rank subsets. Each A/B word determines one subset and vice versa.

At the final level, the last new maximum is inserted at gap m. Every valid
final word has avoiding maximum-deletion ancestors, so pruning an illegal
step cannot discard a valid join. Conversely a legal history plus a legal
final gap constructs an avoiding join. This proves exact N for arbitrary
equal-length inputs, including zero for nonavoiding inputs. A counterexample
to H additionally requires both inputs to belong to its prescribed fiber.
The state cap explicitly reports incomplete computation and cannot certify
a truncated count; the checked run did not reach it. Python integer counts
are exact.

The seed s_h is classically2143-avoiding by induction: any occurrence
spanning its descending value bands would start in the high left band and
finish in the low right band, contradicting first<last. The middle maximum
can only be selected third and has the same obstruction. Both half shapes
remain perfect. This proves P_h's domain too. In Q_h all left values except
the global minimum1 exceed all right values. A mixed occurrence would force
its first point to be1, which cannot play the rank2 role. Each side is an
order-isomorphic seed, and the middle-maximum case has the same inequality.
Thus both P_h,Q_h avoid even the classical pattern and have the required
perfect tree for every h. These are uniform domain proofs, independently
supplemented by the explicit finite checks.

## Independent exact reproduction

`check_quinn_reverse_join.py` imports no author executable. It uses direct
nearest-greater value scans on a postorder heap representative and constructs
Cartesian trees with a monotone stack. These differ from the author's
recursive shape splits and ancestor-based legal-gap implementation. The
representative need not itself avoid; its only use is the shape-dependent
new-maximum blocker rule, whose arbitrary-size validity is the explicit
accepted quotient dependency.

The independent merge generator chooses the positions occupied by L in
every shuffle, then builds the parent from the bottom up. It checks complete
restriction shapes, no duplicate parents, direct value legality and the
grammar. All66197 merge candidates and complete incoming/outgoing state
weights through10 match, including merge-stream
f21ce999947f2c14955442e1e26a139ec53ba4648cf1a9132a23ee65d2d148b5.
An independent value-tested reverse recurrence gives perfect fibers1,2,43,
790086 for heights1..4.

The complete size7 perfect avoiding fiber was reconstructed from all5040
permutations using the boxed definition and stack shape, rather than
assuming the supplied43-word file was complete. Independent DP counts for
all1849 ordered pairs match every entry of the native literal table; their
minimum is37 and sum790086. Ten pairs (all m1/3, four m7 corners and the first
minimum pair) were also re-enumerated over all rank subsets with Theo's
definition-equivalent rectangle checker. This independently verifies the
complete table via the reviewed counting theorem plus selected literal
controls. It is not a claim that Theo reran all6,345,768 candidates through
the author's C++ executable or repeated its sanitizer/resource measurements.
The C++ source was inspected: all four indices and every interior point are
checked, input/mask/counter bounds fit the declared finite domain.

The family was independently constructed and checked for avoidance and
perfect shape. Every per-level state count and complete state-weight stream,
not just final totals, matches the author at m1,3,7,15,31. The exact N values
are2,9,37,952,25635. At m31,25635<32768, with7109 maximum level states and
156664 legal transitions. The supplied arrays P5,Q5 match the reconstruction.
This is a valid finite exact counterexample to the precise universal H.

The retained original family was not in H's domain. The explicit subword
1327465 has the consecutive boxed selection3274 at zero-based indices
(1,2,3,4). Its first size15 zero therefore proves no H failure. I accept
the author's correction and preservation of this negative evidence; the
revised positive-domain counterexample is separate.

Replay from this directory:

```sh
python3 -B check_quinn_reverse_join.py --output /tmp/theo-quinn-reverse-join.json
```

Evidence: `quinn-reverse-join-reproduction.json`. CPython3.11.2,
one process/thread,240.580seconds,536676KiB peak RSS. The higher cost than the
author's run comes from the independent value-based transitions; it remained
within this researcher's fixed resource scope. Source files were rehashed
after the run and unchanged.

## Limits

No minimality over all pairs at m15/31 is accepted. Exhaustive pair tables
stop at m7; the later sizes use the explicit family. Refuting H does not
refute factorial growth, prove an exponential bound, or rule out a weaker
uniform statement, averaged join bound or persistent compatible subclass.
The all-size reverse grammar and fixed-pair algorithm are partial tools for
the original target. Publication of this separate exact scope belongs to
Quinn; his earlier public/graph packet and pending original must not be
silently expanded or duplicated. The full410 target is unsolved.
