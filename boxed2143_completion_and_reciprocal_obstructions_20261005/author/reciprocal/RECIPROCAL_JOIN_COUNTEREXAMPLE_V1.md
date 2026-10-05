# Exact author counterexample to a reciprocal uniform entropy mechanism

Quinn, workday3,2026-10-05. This NEW scope awaits Theo's separate complete
check. It does not inherit498, enter the39045c3 public/graph packet, or solve
the full agreed target410. Every earlier proof/certificate is preserved.

Use F_h,m_h,N(alpha,beta) exactly as in the separately checked
REVERSE_MERGE_AND_JOIN_BOUND.md. The proposed reciprocal hypothesis R was

    forall h>=1, alpha,beta in F_h,
    N(alpha,beta)*N(beta,alpha) >= 2^(m_h-1).

This is not the previously refuted H. R could, in principle, compensate for
a small ordered join count by a large transposed count. It is a full-target
sufficient mechanism: AM-GM gives

    N(alpha,beta)+N(beta,alpha) >= 2*2^((m_h-1)/2).

Sum over ALL ordered pairs, including diagonal pairs. Reindexing by the
transposition of alpha,beta makes the two left sums identical. The exact
join identity would yield |F_(h+1)|>=2^((m_h-1)/2)|F_h|^2. The already checked
conditional recurrence then gives log2|F_h|>=2^(h-2)(h-3)+1, with unbounded
ratio to m_h. Thus R would solve the full negative growth answer. Favorable
finite products at m7/31 did not establish its universal quantifier.

## Valid finite failure

Take the SAME uniformly domain-proved family P_h,Q_h from the498 packet,
now at h6,m63. The family definition is s1=1,s2=132 and
s_h=(d+s_(h-1)),2d+1,s_(h-1) thereafter, d=2^(h-1)-1. With A=s_(h-1),

    P_h=(d+A),2d+1,A,
    Q_h=lift_{1,d+2,...,2d}(A),2d+1,(1+A).

Both classically2143 avoid and have perfect maximum shape for every h by
the accepted induction and mixed first/last value obstruction. The new
run independently checks the actual length63 arrays' avoiding domain and
perfect shapes before counting. The two full arrays are retained in the
count certificates, not inferred from the displayed totals.

The complete author counts are

    N(P6,Q6) = 751802,
    N(Q6,P6) = 46579123,
    product  = 35018277829646
              < 4611686018427387904 = 2^62.

`compact_join_dp_v2.json` retains all126 complete canonical state-weight
streams for EACH orientation, actual input arrays, counts, transition totals,
peak states and resource/cap data. The forward peak has112293 states; the
transpose has92811. Neither reaches the200000 per-level state cap or2000000
interned-node cap. Both finish below their600second per-orientation cap.
The one-process run takes208.77seconds total and peaks at395476KiB Linux RSS,
within the unchanged1CPU/2GiB scope. These measurements are not mathematical
constants. The numeric claim remains an author exact certificate pending
different-researcher reconstruction/reproduction.

No later all-pair minimality is claimed. The complete literal m7 table has
minimum reciprocal product4624>=64; the particular m31 pair has product
19051060410>=2^30. These are controls/context, not uniform evidence.

## Representation proof for the optimized exact recurrence

The mathematical fixed-pair recurrence is exactly the accepted498 algorithm.
The optimization stores each ordered binary shape by a canonical integer ID.
ID0 is empty. A nonempty ID is allocated once for its ordered pair of child
IDs. Induction on construction gives a bijection between allocated IDs and
their shapes: identical children give the same ID, different ordered child
shapes give different shapes/IDs. Child IDs are allocated before their parent,
so the representation DAG is acyclic. Size is1+the two child sizes.

The legal bitmask is computed by the accepted right-child/right-ancestor
criterion, visiting nodes with their inorder offsets. An eligible node at
position j with closest right ancestor R forbids exactly bits j+1 through R;
the program ORs ((1<<(R-j))-1)<<(j+1) over those nodes and complements within
the n+1 gap bits. Python bit arithmetic is exact. This does NOT assume the
unreviewed ABC summary or regular-language identity.

ID splitting follows the checked recursive inorder cut literally: if the
cut is in L, split L into A,D and keep suffix(D,R); otherwise split R into
D,B and keep prefix(L,D). The two resulting IDs become the new maximum's
children. The branch gaps are the same G_alpha(i),i+G_beta(j) as in498.
Every DP state (i,ID) therefore corresponds bijectively to its original
(i,shape) state, and every legal edge corresponds to the same original edge.
Summing each history weight implements exactly the old recurrence.

Periodic retention changes ONLY the cache representation. It collects every
subtree reachable from a current weighted state, rebuilds their IDs in
postorder, and translates current root IDs by the resulting shape-preserving
bijection. Every shape needed for a future split/insertion remains reachable
from a current shape or can be canonically allocated anew. Cached legal
masks depend on shape alone and remain valid after the reindexing. Removing
unreachable IDs removes no weighted current state or future shape. The code
checks that reindexing preserves the number of distinct current states.

For a level certificate, an iterative postorder rebuilds the original
parenthesis/dot shape word. Sorting by i and that word and hashing the exact
integer weights produces exactly the original canonical streams, independent
of numerical IDs or garbage-collection times. Before the new test, EVERY
level of all five accepted P/Q family cases through31 and all five previous
transpose cases matches the older implementation's streams, states, counts
and transition totals. The five tiny literal-definition pair baselines match
too. This is author validation of changed representation, not a substitute
for Theo's separate new review or an independent third implementation.

## Preserved incomplete runs and reproduction

The original nested-tuple m63 test reached its50000 state cap after130.8sec,
reporting NO count. The first interned-ID version passed the old controls but
retained obsolete caches/history and reached the conservative memory stop
below the fixed2GiB limit; it likewise reported NO count. Exact source and
outputs remain in reciprocal_family63_test_v2.py/.json and
compact_join_dp_v1.py/.json. Neither incomplete run is a counterexample.
The corrected version discards local serialization caches and periodically
reindexes only reachable shapes; it does not alter legality, transitions,
current weights, the target statement or the resource allocation.

The single-production script intentionally refuses to overwrite its original
JSON. To replay in a fresh temporary directory, copy the pinned proof/plan,
source and dependencies but omit the completed output. Run CPython3.11+:

    python3 -B compact_join_dp_v2.py

The manifest lists every local dependency and exact byte hash. Source paper
PDFs, credentials, compiled binaries and large raw state dumps are unnecessary.
Compact complete level hashes identify the reproducible exact computation;
the proof of the recurrence and ordinary Python/hardware correctness remain
the trust base.

## Scope of the obstruction

If independently reproduced, these two counts refute R and any claim that
its two orientations always supply the stated full-growth bonus. They do
NOT refute an average over the whole F_h population, a persistent compatible
subfamily, every weaker reciprocal bound, factorial growth or Conjecture7.4.
The full target410 remains unsolved. Next full-target work must address an
actual population/entropy invariant or a recoverable construction, rather
than silently lowering this hypothesis's coefficient and claiming success.
