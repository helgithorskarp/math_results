# Canonical residual selectors for the complete s=1 family

Write **good43** for a red/blue coloring of K43 with no monochromatic K5.
Let F be the union, up to vertex relabeling, of the nine reviewed greedy-closure
branches `gc1-rR-s1-tT`, where R=5,6,7 and T=0,1,2. These are whole physical
families. No residual graph or cross matrix is fixed in the definition of F.

**Theorem (conditional on catalog completeness).** The selector formula
generated here is satisfiable if and only if F contains a good43. In particular,
it retains every good43 in those nine branches up to relabeling. It does not
cover the other 30 branches of the reviewed 39-branch interface.

The imported completeness premise is that McKay's 12 listed Ramsey(3,5,12)
graphs cover every triangle-free 12-vertex graph with independence number at
most four, up to isomorphism. The premise is needed for the forward covering
direction. Soundness of a satisfying assignment is checked directly on all
43 vertices and does not require completeness of this catalog.

## Physical normal form and the relabeling proof

Use seven blocks `C_i={4i,...,4i+3}`, i=0,...,6, one red triangle
`A={28,29,30}`, and a residual `T={31,...,42}`. Blocks C_0,...,C_4 are red
four-cliques. The remaining two four-cliques have colors c5,c6 in {0,1}, with
red=1 and c6<=c5. Thus r=5+c5+c6. The induced graph on T is one of the 12
catalog representatives. When r<7 the induced graph on `{4r,...,42}` has no
red K4. Every physical five-subset is required to be nonmonochromatic.

Take a good43 in any of the nine source branches. Its residual T is exactly
the union of three blue triangles and the final triple. By reviewed greedy
closure, this entire 12-vertex union is red-triangle-free; by good43 it has no
blue K5. Apply an isomorphism on these 12 vertices alone to put it into one
catalog representative. This transports **all 372 edges** from T to the other
31 vertices. Those edges are unrestricted physical decisions in our formula.
The core cliques, red triangle, good43 property and large residual closure
are preserved. The previous subdivision of T and its root orderings are
discarded; they cannot in general be imposed simultaneously with this fixed
catalog labeling.

For the reverse direction, start with a satisfying assignment. It specifies
a physical good43 in the displayed normal form. Inside T, choose a blue
triangle at residual orders 12,9,6. Each exists by R(3,3)<=6 because there is
no red triangle. The last triple has t=0,1,2 red edges. These choices partition
T into the three blue triangles and the appropriate final triple required by
one of the nine source branches. Relabel the final triple into its standard
shape and sort its allowed root signatures, as well as those of the other
child blocks. This recovers a source-branch labeling. The large closure union
is unchanged. The proof establishes existential equivalence under relabeling,
not a bijection between assignments or a graph-isomorphism census.

The small normalizer supplies an explicit catalog isomorphism and full
43-vertex permutation when given an admissible core/tail graph. Its output is
only a structural normal form; it does not certify good43.

## Compatible core symmetry

Hold root C_0 fixed. Within every other core clique and within A, sort vertices
by their unsigned four-bit red-neighbor signature against C_0, in descending
order. Then sort whole nonroot red four-cliques by their concatenated signature
keys, and similarly sort whole blue four-cliques. These vertex permutations
preserve the fixed core types, the entire set T and the large residual closure
union. They commute with the chosen permutation on T.

The implementation enforces vertex comparisons in C_1,...,C_6,A; block
comparisons C_1>=C_2>=C_3>=C_4; C_4>=C_5 when c5=1; and C_5>=C_6 when
c5=c6. The last condition is split into the implications c5=0 and c6=1,
using c6<=c5. This is the identical-block action from h3859 restricted to the
core. Tied keys can leave several representatives; no factorial denominator
is asserted or multiplied into a carrier count.

For each bit comparison x>=y, let p record equality of all preceding bits.
Enforce `not p or x or not y`, with the appropriate activation guard.
The next prefix variable z is defined exactly by `z <-> p and (x=y)`.
Its five CNF clauses are checked by all 16 truth assignments to p,x,y,z.
Prefix definitions remain unconditional when a comparison is inactive.
The extension always exists, so these clauses add no restriction beyond the
specified order. There are 150 prefix variables and 900 symmetry clauses.

## Full target encoding and shared tail predicates

The variable map is deterministic:

| Variables | Meaning |
|---|---|
| 1 | true constant |
| 2--793 | 792 free physical edges, in lexicographic pair order |
| 794,795 | c5,c6 |
| 796--807 | exactly one of the 12 catalog representatives |
| 808--1034 | 227 shared tail predicates |
| 1035--1184 | 150 prefix equalities |

The free physical edges are 420 edges between distinct core blocks and
372 core-to-T edges. The former 54 variable edges inside the four residual
triples are now determined by the catalog selector. The 12 internal edges of
C_5,C_6 are represented by their two common color variables. There are 33
unconditionally red core edges and 66 selector-determined residual edges.

For a physical subset Q and a forbidden color, intersect the catalog truth
tables for all edges of Q contained in T. Let M be the set of catalog indices
where those edges have the forbidden color. If M is empty, the forbidden
clique is impossible and its clause is omitted. Otherwise require

    selected catalog is outside M OR some remaining edge of Q has the other color.

A fixed opposite-color core edge also makes a clause tautological. Repeated
common color variables are deduplicated. No five-subset is omitted for an
unproved structural reason. This construction treats all C(43,5)=962,598
physical five-subsets in both colors, producing 1,476,936 target clauses.

The direct reference encoding writes the first disjunct as a disjunction of
one-hot selectors. For the production formula, complement-pair every
nonconstant 12-bit membership table; use the smaller integer as its canonical
table. Introduce one variable for each of the resulting 227 tables. For each
table and catalog index, a two-literal implication from that selector fixes
the table's truth value. Exactly-one selection makes these 2,724 clauses an
exact definition, without assumptions about the physical graph. Replacing
each long membership disjunction by the corresponding signed predicate literal
therefore preserves the formula's models after projection.

Large residual closure is encoded by forbidding every red K4 on vertices
20..42 conditional on c5=0, and every red K4 on vertices 24..42 conditional
on c6=0. The second condition is redundant when r=5 and necessary when r=6.
For r=7 both are inactive. After tautology removal these yield 5,795 clauses.
The catalog itself supplies the red-triangle-free condition on T.

## Audited dimensions and scope

| Encoding | Variables | Clauses | Literals | Bytes |
|---|---:|---:|---:|---:|
| Direct selector disjunctions | 957 | 1,483,700 | 17,653,433 | 79,532,312 |
| Shared predicate version | 1,184 | 1,486,424 | 14,224,206 | 66,250,106 |

The shared predicates remove 3,429,227 literal occurrences and 13,282,206 file
bytes from the direct aggregate, at the cost of 227 auxiliary variables and
2,724 clauses. These are exact encoding measurements, not a measured solver
speedup. The complete aggregate can be larger than a single old branch formula.
The structural reduction is canonicalizing the whole residual while retaining
all catalog choices and all nine branches.

`audit.py` independently constructs physical edge truth tables, interprets the
catalog with a separate graph6 parser, and reconstructs every literal of both
complete formulas. It checks 4,096 selector assignments, 5,448 predicate
definition cases, 37,752 residual predicate cases, 36 normalization fixtures,
32,508 transported physical edges, 36 reverse repacking fixtures checking another
32,508 edge transports, and 24 closure-count transports. Six result-reader
controls check the solver status formats. Ten
negative controls cover malformed models and graphs and both monochromatic
43-vertex graphs. The structural fixtures deliberately contain a red K5.

The production solver is a separate, single capped experiment. Its result is
reported in RESULT.json and README.md; a partial DRAT stream cannot certify
UNSAT. No count of the global retained family is calculated here. No statement
about the other 30 refined branches, the older weaker branch formulas, or a
Ramsey bound follows from a timeout.

This is an ordinary mathematical proof plus checked finite code, not a
proof-assistant formalization. Trust includes the reviewed h3835/h3863
coverage, the explicitly imported catalog completeness, Python integer and
file semantics, the transcription and ordinary hardware. No historical
novelty for symmetry breaking or selector encodings is claimed.

Dependencies: [reviewed greedy closure](../ramsey_r55_global_greedy_closure/PROOF.md),
[independent acceptance](../ramsey_r55_global_greedy_closure_review1/README.md),
[identical-block normalization](../ramsey_r55_global_packing_block_symmetry/PROOF.md),
and [McKay's complete Ramsey(3,5) catalog](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
