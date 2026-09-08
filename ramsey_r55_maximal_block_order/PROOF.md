# Whole-block ordering in the complete maximal-packing cover

A good43 is a graph on 43 vertices with neither a clique nor an independent
set of order five. This result preserves all h3873 tasks while reducing their
labeled physical carriers. It gives no target, UNSAT result, or measured solve
speedup. Catalog completeness and the parent global coverage remain imported.

## Taskwise normalization

Fix any parent task `(q,r,c)`: q=7..10 four-clique blocks, with the first r
red, r=5..q, followed by its fixed catalog core of order 43-4q. Block 0 is the
red root. In each other four-block, its four vertices already have
nonincreasing root-column signatures. The root-to-block matrix is the
16-bit unsigned integer

    W_i = sum_{u=0}^3 sum_{v=0}^3 adjacency(u,4i+v)*2^(4u+v).

Permute the nonroot red blocks so `W_1>=...>=W_(r-1)`, and separately the blue
blocks so `W_r>=...>=W_(q-1)`. These are permutations of *whole* blocks;
there is no new permutation of the four positions within a block. Root
vertices and all catalog-core labels stay fixed. Equal keys are allowed.

The permutations preserve fixed internal edges, both block colors, every
within-block column order, and the entire union of blue blocks and the core.
All remaining physical edges are transported by the same 43-vertex
bijection, including transposition of a cross matrix if the order of its two
blocks reverses. No action on a core graph's automorphism group is assumed.

Consequently the no-red-K4 maximality condition and all monochromatic-five
conditions are preserved. Every good43 in a parent task has a labeling in
its ordered task, and every graph in the ordered task belongs to its parent
task. Thus the two formulas are satisfiable if and only if each other is,
for each individual task. The ordered physical model set is a subset, not a
projection-equivalent copy of every labeled parent model. Its global
covering interpretation inherits the catalog premise from h3873.

The normalizer returns an explicit new-label-to-old-label permutation and
checks every transported edge, carrier membership, and preservation of the
maximality condition in the finite controls. Normalization alone does not
certify that a graph is a good43.

Whole-block sorting is an established principle already used in h3859 and
in the restricted core action independently reviewed at h3875. No novelty is
claimed for that principle. The present result supplies the exact joint
carrier count with ties, an indexed physical subset of every h3873 task,
and checked direct and shared-triangle implementations.

## Counting the complete ordered carrier with ties

The reviewed h3835 domains reused in h3873 have 1998 possible root matrices
for a red child and 1931 for a blue child. Both lists are in increasing
unsigned matrix order. Let A=r-1 and B=q-r. Nonincreasing root tuples are
multisets, so their counts are

    binom(1998+A-1,A), binom(1931+B-1,B).

Do **not** replace these by 1998^A/A! or 1931^B/B!. Root keys can repeat,
and permutations among tied keys may still change edges elsewhere in the
graph. The ordered carrier can contain several isomorphic copies. We count
all of its labeled graphs; this is not a count of full-graph orbits.

All other coordinate domains have exactly the same cardinalities for every
allowed root tuple. They occupy disjoint physical edges and do not depend
on the chosen root matrices. For a fixed catalog core, their product is

    37823^(binom(A,2)+binom(B,2)) * 35714^(A*B) * 15^(q*(43-4q)).

The first factors concern nonroot four-block pairs; the last factor concerns
all core-vertex/four-block stars, including those incident with the root.
The fixed-core ordered count is therefore

    S(q,r) = binom(1998+A-1,A) * binom(1931+B-1,B)
             * 37823^(binom(A,2)+binom(B,2))
             * 35714^(A*B) * 15^(q*(43-4q)).

Sum `C(43-4q)*S(q,r)` over all 18 macro classes, with the parent's full core
counts C(15)=640, C(11)=546356, C(7)=362, C(3)=4. The resulting exact integer
P and parent N are in `COUNTS.json`. Two different calculations agree:
closed binomial products and a complete coefficient recurrence that inserts
one possible root value at a time and allows every repetition. The latter
then multiplies individual physical pair/star factors and checks all task
interval endpoints. They establish

    1939*P < N < 1940*P,
    P < 2^759,
    1024*P < N.

The last inequality is the predeclared gate. The count is recomputed jointly
in this one representation. No separate denominator is multiplied with
h3863 or any other reduction, and no claim about solver tractability follows.

Injectivity inside each task follows from the distinct matrix/star words
and the multiset unranking. Distinct tasks describe distinct labeled graphs:
core indices and red counts impose different fixed edges, while the first
extra four-block for a different q would lie wholly inside the smaller-q
Ramsey(4,4) core, an impossibility. This is the h3873 disjointness argument,
unchanged by ordering. P counts the full physical ordered carrier exactly,
including graphs that fail maximality or remaining five-set conditions.

The global task count stays 2,189,178. Every core index in every macro class
is retained, with complete disjoint code intervals in `TASKS.json`. The
smallest per-task carrier is q=7,r=7, with 640 tasks each below 2^695 codes.
This ranking by count does not rank empirical solver difficulty.

## Direct physical CNF

For each adjacent pair of same-color nonroot blocks, compare the words from
bit 15 down to bit 0. If p means all higher bits agree, forbid a first
increasing bit by `not p or left_bit or not right_bit`. Start with p=true,
using the parent's forced-true variable 1. Between successive bits introduce
z with the exact definition

    z <-> p AND (left_bit = right_bit).

The five clauses implementing this definition are

    (-z,p), (-z,-x,y), (-z,x,-y), (z,-p,x,y), (z,-p,-x,-y).

A sixteen-bit comparison uses 15 new variables and 91 clauses. There are
`(A-1)+max(B-1,0)` comparisons: between 4 and 8 across the 18 classes. The
new variables begin strictly after the parent variable range. Every old
physical clause is retained verbatim. All new clauses have width at most 4.

The five-clause definition has exactly one extension for each p,x,y, as
checked on all 16 local truth assignments. Induction over bit positions then
proves that the full comparator has exactly one extension precisely when
the unsigned left word is at least the right word. Exhaustion of every
four-bit word pair and every auxiliary assignment additionally checks the
assembled recurrence. The independent physical auditor derives adjacent
block pairs by scanning positions and omitting only the red/blue boundary,
rebuilds the bit-to-edge mapping separately, and compares every suffix
literal against the generator.

## Integration with h3881 shared triangles

The optional triangle form first builds the pinned h3881 formula for the
same physical task. Its triangle definitions are conjunctions of physical
color literals. Append the same block-order comparisons, numbering their
auxiliaries after all triangle variables. This leaves all of h3881's clauses
unchanged and preserves maximum width eight.

The restricted physical model set is identical to the direct ordered task;
the triangle and prefix variables have uniquely determined extensions.
Under a block permutation, triangle auxiliaries are recomputed from their
new physical edge inputs. They are not assumed to retain their old variable
indices: anchor selection depends on vertex labels. This distinction is
necessary for compatibility of the two encodings.

All 18 direct macro-class representatives and five complete triangle
instances are generated and independently audited literally. The five
include one from each q with r=5, and the first member of the smallest
carrier class q=7,r=7. The generic same-color action and prefix proof cover
every core index and both encodings; not all 2,189,178 formulas were generated.
The parent physical and triangle layers use their pinned independent
auditors, while the new suffix is independently reconstructed here.

## Scope and trust

Dependencies and source-manifest identities are in `DEPENDENCIES.json`.
The h3835 pair/root domains are independently accepted at h3845. The h3873
maximal-packing coverage and h3881 shared-triangle theorem are imported.
During this pass, an independent public review accepted h3873 at reviewer
source `a50b5e3a9937c4be77f98af91c6ca809e7c77459`; its source is
https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_global_maximal_packing_review1 .
The h3881 theorem was externally unreviewed at the initial graph cutoff. No hidden
or invalidated h3687 automorphism verification is used. The explicit
block-permutation proof above does not need an external automorphism tool.

The complete-family interpretation also imports McKay catalog completeness.
The code reuses the pinned inputs and defining-property checks from h3873,
rather than regenerating the catalog enumeration. Exactness further relies
on Python arbitrary-precision/file semantics, the stated transcriptions,
SHA-256 and ordinary hardware. This is ordinary mathematical proof with
checked finite implementations, not proof-assistant formalization or external
review of the new result. No target solver is invoked. All tasks remain
undecided and no good43 or Ramsey-bound improvement is established.
