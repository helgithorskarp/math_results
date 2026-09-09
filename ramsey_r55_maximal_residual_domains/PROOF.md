# Maximal-packing residual contacts and a complete carrier bound

Let P be the exact un-oriented h4059 bare-carrier cardinality, and let U be
h4069's certified upper bound after its non-root three-block filter. Add the
requirement that no red K4 consists of one vertex of a blue four-block and
three vertices of the fixed core. The resulting globally covering family
has cardinality at most U_new, where the exact rational certificate gives

    U_new / U = 0.2448148363327823578875216003605909256029...
    1 - U_new / P = 0.9374560154400061321983332562584789590687...

Thus the upper certificate improves by more than a factor of four. The
second number is a lower bound on removal from the exact h4059 carrier.
The first is a ratio of two upper certificates; it is **not** a claimed
retained fraction of the unknown exact h4069 family. All 18 classes and all
2,189,178 original task IDs are accounted for. Exactly 1,641,765 task upper
bounds improve strictly. No task is decided and no good43 is produced.

## Declared family and coverage

The gate in `GATE.json` was declared before computation: U_new <= U/2, with
a complete independently checked core census and physical verification.
The input is the entire h4069 carrier, not a selected template or a solver
prefix. The gate passes. Only this one milestone is pursued.

In an h3887 task, the first r blocks are red K4s and the remaining q-r
blocks are blue K4s, followed by a fixed R(4,4) core C of order n=43-4q.
Here 7<=q<=10 and 5<=r<=q. The intended maximal-packing representative has
no red K4 outside the first r red blocks. The new restriction is a subset
of that already-required red-maximality condition. Every good43 has a
representative satisfying it, conditional on the inherited h3887/h4035/
h4045 coverage theorem. The h4059 and h4069 restrictions are retained.

A new forbidden four-set is a physical red K4 in the residual vertices.
It need not be a Ramsey defect in the original unnormalized graph. In
particular, it is not a red K5 certificate, and the interface does not
assert that an arbitrary good43 graph cannot admit a nonmaximal packing.

## Exact domain for one blue block and its core

Fix a blue four-block B with labelled vertices 0,1,2,3. Let X_i be the set
of core vertices red-adjacent to its vertex i. A red K4 contained in B union
C uses at most one vertex of B, since every pair within B is blue. The
core itself has no red K4. Therefore the new condition is equivalent to
each X_i inducing a triangle-free red graph.

The original blue-block star domain excludes a core vertex blue-adjacent
to all of B. Equivalently, the four red-neighbour subsets cover C:

    X_0 union X_1 union X_2 union X_3 = V(C).

Every ordered covering four-tuple gives one labelled physical block/core
matrix. Repetitions and overlaps of subsets are allowed. Conversely every
allowed matrix gives exactly this tuple. Define B(C) to be their count.
This is an exact domain count for these two requirements; further blue
K5 patterns are not implicitly included.

For S contained in V(C), let T_C(S) count the triangle-free subsets of S.
Inclusion-exclusion over uncovered vertices gives

    B(C) = sum_{S subset V(C)} (-1)^(n-|S|) T_C(S)^4.

The original blue-block domain has 15^n words, so 0<=B(C)<=15^n.
All 547,362 supplied cores have B(C)>0. This positivity does not prove
nonemptiness after the other global restrictions.

## Complete independent enumeration

The producer first computes the triangle-free indicator for every subset
X. Removing its least vertex reduces the test to the smaller subset and
the presence of a red edge between that vertex's neighbours. A subset-zeta
transform gives every T_C(S). Taking fourth powers and applying Mobius
inversion gives all union counts, including B(C).

The independent checker instead decodes a literal adjacency matrix and
lists every red triangle. It tests every subset directly against this
list. For every valid subset X it visits every superset S and increments
T_C(S), without using the producer's zeta transform or subset recurrence.
Every intermediate value is compared to the producer's binary profile.
Finally it uses the displayed signed inclusion-exclusion sum, without the
producer's Mobius algorithm. This agrees on all 1,139,954,976 intermediate
subset counts and all 547,362 final domain counts. The checker makes
71,535,730,612 direct subset/superset incidence updates.

| Core order | Cores | Minimum B(C) | Maximum B(C) |
| --- | ---: | ---: | ---: |
| 3 | 4 | 1,680 | 3,375 |
| 7 | 362 | 4,916,654 | 170,859,375 |
| 11 | 546,356 | 4,195,856,536 | 341,566,810,470 |
| 15 | 640 | 1,711,290,150,764 | 7,783,322,271,536 |

Each T_C(S)<=2^15, so its fourth power is at most 2^60. Every partial
Mobius difference counts tuples whose union contains the already-processed
coordinates; it is nonnegative and at most 2^60. The producer checks this
before subtraction. Each parity sum in the independent inclusion-exclusion
is at most 2^(5n)<=2^75. Two unsigned 64-bit limbs with explicit carry and
borrow suffice, and the final result is checked to fit the stated bound.
Profiles use explicit little-endian unsigned 16-bit entries.

Strict native builds have no compiler warnings. ASan/UBSan checks all order
3,7,15 cores and the first, middle, and last 128 order-11 records: 1,390
cores and 21,804,320 profiles, all equal to the complete release census.
This is representative sanitizer coverage, not a claim of a second full
sanitized order-11 census. The full independent release check is complete.

Two definition-level Python enumerations, one over ordered row subsets
and one over the 15 nonzero physical column masks, agree for all 75 labelled
graphs on one through four vertices. Native counts agree with both. Empty
and complete 15-vertex graphs test the large-value and zero-cover boundaries.
Six corrupt native certificates are rejected. No floating-point arithmetic
supports a count or inequality.

## Combine with the complete parent carrier

Put a=r-1 and b=q-r. The unchanged root and ordinary-pair domains contribute

    M(q,r) = binom(1998+a-1,a) binom(1931+b-1,b)
             * 37823^(binom(a,2)+binom(b,2)) * 35714^(a*b).

Let beta(q,r) be the exact upward rational multiplier from h4069. Its
ordinary non-root matrix events use no block/core edges. The root ordering
also uses no block/core edges. Thus beta applies for every choice of core
and allowed contacts, including the newly restricted contact choices.
Equal root keys and all labelled contact multiplicities remain present.

For q=7,8,10 the original blue contact count is 15^n. The red-block contact
count R_q is 15^15 for q7, 2433780807*15^3 for q8, and 15^3 for q10. The
q8 value includes exactly the unchanged h4035 selected augmentation filter.
Those filters concern red blocks, so their coordinates are disjoint from
the new blue-block restrictions. The new class upper bound is

    beta(q,r) * M(q,r) * R_q^r * sum_C B(C)^b.

The sum runs over every core of the appropriate order. In particular, it
does not replace the cores by a favourable subset or by edge-extreme R(4,5)
graphs. The catalogue multiplicities remain exactly 640, 546356, 362, and 4.

For q9, h4059 already restricts every blue-block contact domain to size
A(complement C), and every red-block domain to size J(C). The new domain
shares physical edges with this old blue domain. Its intersection has size
at most min(B(C), A(complement C)); no product of marginal fractions is
justified. The new q9 class upper bound is consequently

    beta(9,r) * M(9,r)
      * sum_C J(C)^r * min(B(C), A(complement C))^(9-r).

This minimum is only an upper bound on the joint blue domain. No exact
q9 intersection count or conditional independence claim is made.

Summing the 18 class expressions yields U_new. The independent Python
checker reconstructs the root multiset counts by an integer recurrence,
multiplies the individual pair-domain factors, and uses contact power sums
to reconstruct every old and new class weight. It checks all rational sums,
the declared gate, and every affected-task count. Six corrupt global
certificates are rejected. Normal and assertion-disabled checks agree.

The strictly improved task upper bounds split as follows:

| q | Task bounds improved |
| --- | ---: |
| 7 | 1,280 |
| 8 | 1,639,068 |
| 9 | 1,412 |
| 10 | 5 |
| Total | 1,641,765 |

These refer to the original bare registry, including tasks already settled
elsewhere. The registry itself is unchanged. Positive upper bounds do not
prove a surviving assignment exists, and no complete task is newly excluded.

## Physical meaning and controls

`physical.py` takes a complete 903-edge coloring and an original task name.
It returns either `RED_MAXIMALITY_WITNESS`, with one blue-block vertex and
three core vertices joined by all six red edges, or
`NO_DECLARED_RESIDUAL_WITNESS_NOT_TARGET`. The standalone verifier checks
the four vertex labels, the residual location, and all six edge colors.
Parent membership remains a caller precondition for the carrier measure.

Twelve complete physical controls use three pinned order-11 cores and all
four q8 red-block counts. Their ordinary matrices have two neighbours of
each color in every row and column, so the h4069 3+1+1 events are absent.
Root-column order and tied block keys are checked. Red-block core columns
have a single red neighbour, excluding the old selected augmentation.
Blue columns come from four triangle-free color classes of the core and
are nonzero, so the new predicate passes.

For every blue block, every one of its vertices, and every red core
triangle, its three contact columns are changed to that vertex's singleton
mask. Each of the resulting 1,416 indexed mutations stays in the old q8
star domains and preserves every root, ordinary-matrix, red-contact, and
core edge. Both the generated witness and the intentionally inserted red
K4 are checked literally. These are indexed tests, not a distinct-graph
count. There are 336 complete pair-palette checks (18,816 literal five-sets),
990 core four-set checks, and four rejected corrupt physical witnesses.

Every positive control and mutation separately has a red K5 on the first
vertices of five non-root blocks. None is a target candidate. The witness
interface checks a packing requirement; it does not establish SAT speedup,
new carrier codes, or a destination for repacking an arbitrary graph.

## Provenance, trust and boundary

The four input catalogues are byte-pinned to the previously imported
[McKay Ramsey data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
All four public downloads and decompression hashes are independently checked.
Catalogue completeness and global-cover premises remain imported; these
catalogues are not regenerated here. No R(4,5,23) catalogue is substituted:
the public data provide edge-extreme subfamilies at that order, not its full
set. This preliminary observation is not a new mathematical result.

H4079 independently accepts the h4069 parent conditional on the earlier
coverage and counts. That review is parent validation, not a review of this
new theorem. Its concern about dependent filters is addressed here by the
explicit ordinary-matrix/contact separation and the q9 minimum. No degree
or color-orientation bound is composed with this result.

Team-r55-1's q10 ledger remains 99 certified closures/161 UNKNOWN; its
separate orientation queue remains 67 active/94 redirects. This percentage
is not applied to that queue or any child prefix, and no child inputs are
read. H4001 separately remains 518 q7-r5 exclusions/122 UNKNOWN, leaving
2,188,660 whole task IDs undecided. The parked neighborhood route, earlier
packing bridge, and teammate's switching sources are not reopened.

The trust base comprises the unformalized finite argument, imported
catalogues and cover, published source, integer/bit execution, compiler,
interpreter, SHA-256, operating system, and hardware. No solver or heuristic
search supports this theorem. Inclusion-exclusion and subset transforms
are standard; no historical priority is claimed for the method.

This completes the single declared milestone. The q9 minimum is not
automatically followed by a joint-contact enumeration or another residual
constraint. Further work requires a separately selected consequential gate.
