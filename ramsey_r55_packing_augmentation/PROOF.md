# A complete global cover with larger four-clique packings

Write good43 for a red/blue coloring of K43 without a monochromatic K5.
We use the complete ordered physical carrier of h3887, not an independent
root-sequence carrier and not the unknown set of actual good43 graphs.
The contribution is a finite normal-form reduction, with no new target,
individual-task UNSAT result, or measured solver acceleration.

## The new family and coverage

The h3873/h3887 cover partitions the vertices into q monochromatic K4
blocks, the first r red, and a fixed Ramsey(4,4) core C of order 43-4q.
Here 7<=q<=10 and 5<=r<=q. Red K4 packing is maximal: the union of all blue
blocks with C contains no red K4. The complete core catalogs and the prior
physical domain/order coverage are imported premises.

Retain q7 and q10 unchanged. For each fixed q8 or q9 core, greedily scan its
red edges in lexicographic order and accept edges with both endpoints still
unmatched. This is a maximal matching: two unmatched vertices cannot be
adjacent. The core has no independent four-set, so at most three vertices
remain unmatched. There are therefore at least four matching edges for
q8 (core order 11), or two for q9 (core order 7). Select the first m=4 or m=2
edges of this matching. Selection depends only on the fixed core.

For each red block B, each pair of selected core edges e,f, and each
two-subset S of B, forbid all eight red cross edges between S and e and
between B\S and f. The within-B and within-e/f edges are already red.
If these eight cross edges are present, S union e and (B\S) union f are two
disjoint red K4s. Replace B by these two blocks. Every other red block and
every blue block is retained, and exactly four vertices are removed from C.
Thus (q,r) becomes (q+1,r+1) on the SAME complete physical graph.

The new core is an induced subgraph of C, hence still Ramsey(4,4). The union
of blue blocks with the new core is a subset of the old such union, hence
still red-K4-free. Normalize its 7- or 3-vertex core to the appropriate
existing complete catalog representative, select a red root, sort each
child's root columns, and sort whole equal-color nonroot blocks as h3887
requires. For a good43, every reviewed local physical domain still holds
because all graph edges are transported by a bijection.

After this normalization the selected matching may change. Recheck the
new representation. Each further violation strictly increases q; starting
with q8 or q9 there are at most two exchanges before q10, which has no new
restriction. This proves that the new family still covers every good43.
It does not assert equivalence for each old fixed task. A good graph removed
from a q8 or q9 labeling would be represented in a larger-q task instead.
The argument uses elementary packing exchange, not a graph automorphism
quotient, any symmetry source, or a new lower bound on packing number.

## Exact retained fraction in each affected task

For a red block and a core vertex, the four red incidence bits range over
0..14: the all-red value 15 would extend the red K4 to a red K5. These
15-element star domains are independent physical coordinates in h3887,
including those meeting the root. Root-matrix sorting imposes no relation
on star coordinates, and its repeated-key multiplicities remain counted.

For a selected core edge with endpoint stars x,y, let z=x AND y. A pair
S of block positions can complete this edge exactly when S is contained in
z. Two different selected core edges yield an augmentation precisely when
their respective z values contain complementary pairs. Within one edge
there is no such issue: a z of value 15 is impossible.

For every proper four-bit mask z, the number of endpoint pairs is

    w(z) = 3^(4-|z|) - 2.

Without excluding endpoint value 15, each position outside z has three
possibilities 00,01,10. Exactly one of these endpoint pairs has x=15 and
exactly one has y=15; these cases are disjoint for proper z. This proves
the formula. The weights sum to 225.

The producer records the union of available pairs among already processed
edges. It rejects a new edge if one of its pairs complements a previous
pair. The resulting exact counts of accepted ordered endpoint-star tuples
are:

| m | Accepted a_m | All tuples |
|---|---:|---:|
| 1 | 225 | 225 |
| 2 | 50,151 | 50,625 |
| 3 | 11,087,517 | 11,390,625 |
| 4 | 2,433,780,807 | 2,562,890,625 |

Put p_m=a_m/15^(2m). Different red blocks use disjoint star coordinates;
unselected core vertices and all block-pair matrices are unrestricted by
this new condition. The EXACT retained fraction of every q8 task is p_4^r,
and of every q9 task is p_2^r. It is 1 for q7 and q10. There is no independence
assumption involving graph degrees, maximality, or Ramsey five-set clauses.
The count includes physical carrier assignments failing those conditions.

For A=r-1, B=q-r and n=43-4q, the old per-task count is

    T(q,r) = C(1998+A-1,A) C(1931+B-1,B)
             37823^(C(A,2)+C(B,2)) 35714^(AB) 15^(qn).

Multiply by the applicable p_m^r and sum over the existing core counts
640,546356,362,4. Every product is an integer. All 18 original T(q,r) values
and the global sum are pinned and independently regenerated. EXPECTED.json
contains the exact new per-task and total integers. The new carrier removes
5.4948242392645... percent of the full old carrier, exceeding the declared
5 percent gate. It removes 25.5438163... percent within q8 and 5.5135313...
percent within q9. The rule applies to 2,187,234 tasks, but decides none of
them. Their carriers remain nonempty, for example with all selected red
stars zero. This is not a fraction of unknown good43 isomorphism classes.

## Existing closures and degree accounting

The h4001 count of 518 closed q7-r5 tasks may be subtracted independently
because q7 is unchanged and no new transition enters q7. It leaves 122
UNKNOWN q7-r5 tasks and 2,188,660 whole tasks overall. The 99/161 q10 child
ledger is a different task level, so no child count is subtracted here.

Let d_r be h4029's certified retained-fraction upper bound in q8. A complete
new cover may also require every vertex degree in 18..24, since this is a
property of every good43 and is preserved under all graph relabelings.
Use min(d_r,p_4^r) for q8, p_2^r for q9, and 1 for q7/q10. In fact d_r is
smaller in all four q8 classes. This yields a 5.3580504705436... percent
decrease in the PREVIOUS CERTIFIED UPPER ENVELOPE after h4001 and h4029.
It is not a measured extra fraction of the actual degree-filtered set.
No two dependent probabilities are multiplied. The familiar global edge
window and h4015/h4021 restrictions remain compatible and are not assigned
additional numerical factors.

## Checkable physical interface and limits

Each restriction is an eight-negative-literal clause over the 903 physical
edge variables, positive meaning red, in lexicographic pair order. There
are 36r such clauses in q8 and 6r in q9. They define the NEW global family;
they are NOT individual consequences of the Ramsey formula. In particular
they must not be appended as learned Ramsey clauses to an old fixed task.

transport.py emits these clauses or an exchange certificate. The latter
includes a source hash, the two new physical blocks, a full new-to-old
vertex permutation, and the transported graph and packing. The separate
verifier checks every physical pair and both packing/maximality/core claims.
The packet deliberately says NEEDS_CATALOG_AND_ROOT_ORDER: it is a physical
packing transport, not an implemented catalog lookup or a target task ID.
The catalog/order normalization needed for global coverage is proved above
and inherited from h3887; automation of that existing step is left to a
receiver choosing to use the new cover. No owner input is read or changed.

The independent arithmetic checker imports no producer. It enumerates all
54,240 ordered mask tuples of lengths 1..4 with the proved intersection
weights, reconstructs every state-table entry, literally exhausts 50,625
four-star inputs, and regenerates root multiset counts by coefficient
recurrence instead of binomial products. The interface controls separately
exhaust 50,625 assignments against emitted physical clauses, check 18
complete43-vertex transports (16,254 physical pairs), and reject 90 altered
transport certificates. An actual eight-vertex good graph also survives
the exchange; the 43-vertex controls are explicitly non-target fixtures.
Normal and Python -O replays reject numerical corruption of the marginal,
global sum and composite bound. The public replay requires only Python 3.11+
standard library. No solver, bulk catalog input, or hidden graph is needed.

Completeness of the prior catalog cover, the reviewed domain counts,
h4001's closures and h4029's bound (for composite accounting only) remain
imported. The exchange proof is ordinary mathematics; integer/file semantics,
source transcription, SHA256 and hardware are not formalized. No external
review or historical novelty of packing exchange is claimed.
