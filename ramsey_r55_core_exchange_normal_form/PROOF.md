# A core-edge exchange normal form for every good43 graph

Call a red/blue coloring of the complete graph on 43 vertices **good43** if it
has no monochromatic five-clique. This note proves a new representative theorem
for the entire hypothetical good43 class, with no automorphism or regularity
assumption. Its complete-carrier consequence is a bound smaller than the
reviewed maximal-residual certificate by a factor greater than three. It
excludes no original carrier task and changes no Ramsey-number bound.

## 1. The representative theorem

**Theorem.** Every good43 graph has a partition into red four-cliques
`B_1,...,B_r`, blue four-cliques `B_(r+1),...,B_q`, and a core C, with:

1. `7 <= q <= 10`, `5 <= r <= q`, and `|C|=43-4q`.
2. No red four-clique lies outside the red blocks, and C has no blue
   four-clique. In particular C is a Ramsey(4,4) graph.
3. No red block and two disjoint red edges in C can be repartitioned into
   two red four-cliques by splitting that block into two pairs.
4. Whenever v in C has exactly three neighbors of a block's color in that
   block, and w is its unique opposite-color neighbor in the block,

   `|N_red(w) intersect (C minus {v})| <= d_red,C(v)`.

The graph's physical edges are never changed. Starting with any partition
satisfying (1)–(2), a deterministic sequence of at most 675 improvements gives
(3)–(4). Catalog and block-order normalization preserves both terminal rules.

**Proof.** First greedily pack red four-cliques until no further one is
available; then greedily pack blue four-cliques in the red-free residual.
The remaining core has neither color of four-clique. The residual after the
red packing is a (4,5)-Ramsey graph, so it has at most 24 vertices by the
imported classical result R(4,5)=25. Thus r>=5. The core has at most 17 vertices
by R(4,4)=18, giving q>=7; disjointness gives q<=10. These are the reviewed
maximal-packing carrier's bounds. They require maximal, not maximum, packings.

For every such partition order the potential

`Phi = (r, q, e_red(C))`

lexicographically. A violation of (3) replaces one red block and four core
vertices by two red blocks. It increases both r and q. The new core is induced
in the old core, and the red-free residual shrinks; (2) is preserved.

For a violation of (4), replace the block B by `(B minus {w}) union {v}`,
and replace v in the core by w. The replacement block has its required color.
If no repacking were required, the core's red-edge increase would be exactly

`|N_red(w) intersect (C minus {v})| - d_red,C(v) > 0`.

The following repairs restore (2).

* If a red four-clique is now available outside the red blocks, retain all
  current red blocks, discard the blue packing, and greedily add red blocks
  until the residual is red-free. Then greedily pack blue blocks there.
  The first new red block makes r strictly larger. A possible decrease of q
  is harmless because r is the first potential coordinate.
* Otherwise retain all current blocks and greedily add blue blocks from the
  new core. If one is added, q increases while r stays fixed.
* If neither repair adds a block, r and q stay fixed and the displayed
  strict increase of e_red(C) increases the potential.

For a blue-block exchange the vertex set outside the red blocks is unchanged,
so the first repair cannot be necessary. For a red-block exchange either repair
may occur. In every case the same graph remains partitioned into monochromatic
blocks and an induced Ramsey(4,4) core. Recheck both rules after each move.

For order 43 the number of possible potential triples is at most

`3*(binom(15,2)+1) + 4*(binom(11,2)+1)`
`+ 5*(binom(7,2)+1) + 6*(binom(3,2)+1) = 676`.

A strictly increasing sequence therefore has at most 675 moves. At termination
both (3) and (4) hold. This proves the theorem. The existence argument itself
is finite and does not use the catalogs. More generally, the same potential
argument works at every finite order, with order-dependent finite ranges. □

This is an existential normal form for every good43 graph, **not a claim about every
existing labeling of a graph**. The all-two-edge condition (3) is deliberately
stronger than the inherited selected-matching augmentation test. It makes the
new descent compatible with that test irrespective of catalog relabeling;
no intermediate catalog lookup is required. Its extra restrictions are not
assigned a numerical factor below.

## 2. Complete original-registry receiver

Choose the first red block as root, sort each other block's four vertices by
decreasing binary red-neighborhood signature to the root, and sort whole red
nonroot blocks and whole blue blocks by decreasing root-matrix word. Ties are
retained. Relabel the core to its representative in the appropriate complete
McKay catalog. These operations are bijections of vertices, not assumptions
that the graph has any symmetry. Conditions (3)–(4) quantify over every
applicable block/core incidence, so they survive these permutations.

The inherited ordered registry has the following complete scope:

| q | core order | cores | allowed r | original task IDs |
|---|---:|---:|---|---:|
| 7 | 15 | 640 | 5,6,7 | 1,920 |
| 8 | 11 | 546,356 | 5,6,7,8 | 2,185,424 |
| 9 | 7 | 362 | 5,6,7,8,9 | 1,810 |
| 10 | 3 | 4 | 5,6,7,8,9,10 | 24 |

`destination.py` implements this normalization for **all four core orders**.
`catalog.py` uses degree invariants only for pruning and a complete bijection
backtrack for isomorphism. Every accepted bijection is checked on all core
pairs. Imported catalog completeness ensures that a good43 core has a
successful destination; the algorithm does not assume canonicalizer correctness.
The output names the exact `bo1-qQ-rR-cCCCCCC` task and supplies all 903 physical
edge bits and a full new-to-old permutation. It checks the literal inherited
pair and star palettes, or returns a physical monochromatic five-set. Admission
only means admission to the ordered carrier with the proved normal packing;
it is not certification of every Ramsey clause.

The standalone `verify_destination.py` imports none of the producer. It checks
the final partition, both maximalities, both terminal rules, all physical edge
identities, catalog identity, root orders, and palette admission or the literal
five-set. It verifies the **endpoint**, not the submitted intermediate history.
The mathematical potential proof supplies termination.

The new rules have an exact auxiliary-free CNF interface. Number physical red
variables 1,...,903 by lexicographic pairs u<v. For each B,v,w, let g be the
four signed literals asserting three block-color contacts and the opposite
contact vw. For every S contained in C minus {v} of size d_red,C(v)+1, emit

`(OR_(literal in g) NOT literal) OR (OR_(u in S) NOT R(w,u))`.

An assignment violates these clauses exactly when it violates (4). This holds
for both block colors. The fixed core, including its degrees, is a receiver
precondition. `exchange.py clauses` emits all four rows, all blocks, and all
core vertices. A receiver using a different SAT vocabulary must translate
these physical variables explicitly.

These are **new-family clauses**, not Ramsey implicates of an original task.
An UNSAT proof after adding them does not retire that old task. To use the new
cover for nonexistence, the whole destination family must be covered, or each
removed old assignment needs a sound redirect/join. In particular r may increase
while q decreases during repair; one must not assume that redirects only enter
q9/q10 or any existing child queue. The old 518 q7 closures remain valid physical
task closures, but this note changes none of their accounting.

## 3. A complete counting relaxation

Fix a core with sorted red degrees d_1,...,d_n. A block-color star column is a
proper four-bit mask from 0,...,14. For a red block let D_w be row w's number
of red contacts. If column v is `15 XOR (1<<w)`, rule (4) says `D_w <= d_v`.
For a blue block use blue-contact bits instead. The opposite contact is red,
so the same rule becomes `n-1-D_w <= d_v`, or `D_w >= n-1-d_v`.

The theorem constrains all four rows. For an upper bound we count exactly the
words satisfying just rows 0 and 1. Call their numbers N_R(d), N_B(d).
For fixed final row degrees x,y, forbid the corresponding triple-column mask
at v when

* red: `f_0(v)=[d_v<x]`, `f_1(v)=[d_v<y]`;
* blue: `f_0(v)=[d_v<n-1-x]`, `f_1(v)=[d_v<n-1-y]`.

The per-column degree polynomial is

`4 + (4-f_1(v))*X + (4-f_0(v))*Y + 3*X*Y`.

For example X alone fixes row bits 10 and admits four possibilities on the
other two rows, except that the unique forbidden triple mask missing row 1
removes one. The XY coefficient is three because the all-one column is absent.
Take coefficient X^x Y^y in the product over v, then sum over x,y=0,...,n.
This is the exact two-row count. Nonnegative transfer coefficients and totals
are at most 15^15 < 2^59, so unsigned 64-bit arithmetic is sufficient.

### Separate inclusion–exclusion verification

Let A_0 and A_1 be the columns at which the first and second triple masks are
forbidden. They are threshold sets of the same degree list and hence nested.
Write a=|A_0|, b=|A_1|. Select i positions at which the first forbidden mask
is forced and j positions at which the second is forced. These selections
must be disjoint. Their number is

`binom(a,i)*binom(b-i,j)` if a<=b,

and `binom(b,j)*binom(a-j,i)` otherwise. Forced first-mask columns contribute
Y^i and forced second-mask columns contribute X^j. Thus the coefficient for
x,y is the sum over i,j of

`(-1)^(i+j) * selection_count`
`* [X^(x-j) Y^(y-i)] (4+4X+4Y+3XY)^(n-i-j)`.

`check_pair.py` evaluates this formula with arbitrary-precision signed integers.
It agrees with the C++ transfer calculation on all 1,648 counts for the 824
degree multisets occurring in the **entire** 547,362-core catalog union.
The degree multisets merely share an exact calculation; no core or profile is
excluded from the theorem or census. Direct proper-column enumeration also
checks all degree multisets, including nongraphical ones, through order three.

## 4. Safe composition with the reviewed carrier certificate

Use the complete **un-oriented maximal-residual family**, not an active solver
queue, a conditioned child, or an unknown set of Ramsey survivors. Its reviewed
bound will be denoted U_old. The old restrictions include selected augmentation,
q9 whole-block/core Ramsey contacts, nonroot 3+1+1 five-set exclusion, and the
one-blue-vertex/three-core red maximality condition. All remain compatible with
the new theorem: the first follows from (3), the next two are Ramsey conditions,
and the last follows from red maximality. Thus their intersection with the new
normal form still represents every good43.

For core C let P_R(C),P_B(C) be the old per-block contact upper bounds:

* q7: `P_R=15^15`, `P_B=B(C)`;
* q8: `P_R=2433780807*15^3`, `P_B=B(C)`;
* q9: `P_R=J(C)`, `P_B=min(B(C),A(complement C))`;
* q10: `P_R=15^3`, `P_B=B(C)`.

Here A,J are the reviewed exact q9 contact counts. B(C) counts ordered covers
of C by four red-triangle-free row subsets, as in the reviewed maximal-residual
proof. These values and their independent-review state are imported, not
claimed as new computations. The four residual count files were read without
modifying the historical workspace, copied to current scratch, and matched to
the reviewed SHA-256 receipts. Public replay can regenerate them in fresh scratch.

Put

`L_R(C)=min(P_R(C),N_R(d(C)))`,
`L_B(C)=min(P_B(C),N_B(d(C)))`.

These are safe intersection upper bounds. The new and old contact predicates
share edges; **their probabilities are never multiplied**. Different blocks'
contact coordinates are disjoint. Root ordering and ordinary block-pair
coordinates use no contact edges. Consequently, for a=r-1 and b=q-r, the
new class has size at most

`beta(q,r) * M(q,r) * sum_C L_R(C)^r L_B(C)^b`,

where

`M=binom(1998+a-1,a)*binom(1931+b-1,b)`
`  *37823^(binom(a,2)+binom(b,2))*35714^(a*b)`.

The upward rational beta is the reviewed nonroot three-block entropy bound.
It applies separately for every fixed contact choice. No degree-window,
orientation, separator or solver-child multiplier is composed here.

The complete exact rational census gives

`U_new / U_old = 0.30507766938747466... < 1/3`.

This compares **upper certificates**, not the unknown exact old family size.
It is not a measured 69.49% removal of its actual survivors or a SAT runtime
claim. Every class and every original task ID is included. Strict improvements
of the per-task upper certificates are:

| q | task upper bounds strictly improved | total task IDs |
|---|---:|---:|
| 7 | 1,920 | 1,920 |
| 8 | 2,185,424 | 2,185,424 |
| 9 | 1,120 | 1,810 |
| 10 | 18 | 24 |
| total | 2,188,482 | 2,189,178 |

The q8 class ratios are respectively 0.09583148, 0.07577122, 0.06478094,
0.05930703 for r=5,6,7,8. These decimals are displays; `EXPECTED.json`
contains every exact integer and rational. A separate corewise checker
reconstructs degrees by a different parser, all contact power sums, root
multiset counts, the entropy power inequality and the global sum. All 6,022,062
core-degree incidences are covered.

### Actual nonredundancy, beyond comparison of upper bounds

There is also an explicit old-family assignment violating (4) in every all-red
task whose core is not complete: **547,361 original all-red task IDs**. This
proves actual nonredundancy; it still excludes no complete task.

Use two-regular red cross-matrices between every pair of red blocks, sorting
root columns as required. Set all contacts to zero except those of the root.
Choose a core vertex v with degree d<n-1. Give it the three root contacts
missing row w=0. Give row 0 exactly d+1 other core contacts, each as a singleton
column. The displaced row gains one core red edge. Every intersection of two
distinct core columns has size at most one, so selected two-edge augmentation
is absent. Intersections of any three contact rows contain at most the single
vertex v, and intersections of two rows do too; hence the q9 whole-contact
conditions hold. Every ordinary cross-matrix row and column has two red bits,
so pair palettes and all nonroot 3+1+1 restrictions hold. There are no blue
blocks. The core itself is unchanged and red maximality holds.

All-red cores of orders 7,11,15 cannot be complete because they are K4-free;
three of the four order-3 cores are noncomplete. The count is therefore
640+546356+362+3=547361. `strict_witness.py` generates the full 903-bit assignment
for any such task. Its first vertices in five nonroot blocks form a declared
red K5, so none of these controls is a target graph. A literal instance from
each q stratum checks the implementation of this universal schema.

## 5. Evidence and remaining obligations

The exact computation has two different counting decompositions, a separate
complete corewise arithmetic check, release and address/undefined-sanitized
native agreement, 54,000 literal local exchange/CNF controls, 10,812 genuine
small Ramsey graph transports, and 38 complete 43-vertex physical transports.
The latter exercise r-growth, q-growth and pure core-edge growth, all 18 macro
strata, and both operation types. They are finite implementation controls;
the written potential argument supplies unrestricted coverage. Catalog
isomorphism controls cover every order-3/7 record and three records at each
larger order; this is not regeneration of the large catalogs.

`verify_destination.py` provides a separate physical endpoint check and rejects
altered edge words, permutations, task indices and partitions. This is
same-author validation, not an independent external review. The proof is not
formalized. Remaining trust includes classical R(4,5)=25 and R(4,4)=18,
imported catalog completeness and reviewed carrier/contact/entropy counts,
source transcription, integer execution, compiler/interpreter, hashes and
hardware. The defective historical order-five automorphism claim is unused.

No original task is newly decided. The complete-class theorem and quantified
all-q receiver restriction meet this lane's first-pass structural milestone.
The next phase must demonstrate useful original-task retirement or a whole
subclass closure, rather than merely count more rows or append another
necessary condition. Carrier execution and proof accounting remain with R2;
this package does not read or mutate its jobs. The new normal form is an
additional global cover, and must enter that accounting with its explicit
redirect semantics.
