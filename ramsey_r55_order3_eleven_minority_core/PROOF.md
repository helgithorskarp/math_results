# Minority-core reduction for eleven moving triangles

Let G have 43 vertices and no clique or independent set of order five.
Suppose an order-three automorphism has ten fixed vertices and eleven
moving triangles, three internally red and eight internally blue. This
is one of the two surviving internal-color splits in the
[parent reduction](../ramsey_r55_order3_eleven_cycle_obstruction/PROOF.md).
The present argument assumes the three-versus-eight split explicitly;
it does not require the parent's exclusions of other splits.

The new conclusion is that the nine minority vertices induce one of the
following three cores, up to the relabelings proved below. Words list
red bits at offsets 0,1,2, and the blocks are ordered 01,02,12.

| class | words | unordered red weights | phase sum |
|---:|---|---|---|
| 8 | 100,100,100 | 1,1,1 | zero |
| 11 | 100,110,110 | 1,2,2 | zero |
| 13 | 110,110,101 | 2,2,2 | nonzero |

In particular no minority-to-minority block is empty or complete, and
the weight pattern 1,1,2 is impossible. Eleven excluded classes have
full replayed refutations. The three displayed classes reached the
60-second solver limit and remain open; their local cores are not
43-vertex realizations. The four-versus-seven split also remains open,
and the global minimum is still eleven moving triangles.

Each fixed vertex can have any of the eight binary minority-incidence
signatures in a one-vertex extension of core 8. For cores 11 and 13,
exactly the seven signatures other than 111 are permitted, so a fixed
vertex is red to at most two minority triangles. This follows by
checking K4s in the appropriate core color-neighborhood, on all eight
signatures. These are exact ten-vertex extension facts, without a claim
that any collection of such signatures is jointly feasible. The
literal inspections are recorded in `audit_result.json`.

## The nine-vertex core

Label the internally red cycles C0,C1,C2, with vertices 3i+s for s modulo
three. Label the remaining cycles C3 through C10 and fixed vertices
33 through 42. For i<j in {0,1,2}, write b_ij(d) for the color of the
edge from 3i+s to 3j+s+d, with red=1. The three words, in order 01,02,12,
determine the nine-vertex core.

No word can be 111: a complete red block between two red triangles
contains a red K6. Conversely every choice of three words other than
111 gives a nine-vertex graph with no monochromatic K5. A blue clique
uses at most one vertex of each red triangle, so has order at most
three. A prospective red K5 has occupancy 3+2, 3+1+1, or 2+2+1 among
the triangles. Either of the first two requires a complete block. The
last requires a red K2,2 in a noncomplete cross block, whereas its red
graph is empty, a matching, or a six-cycle. Thus there are exactly
7^3=343 labeled cores. This is a local statement, not an assertion that
any of these cores extends to a target on 43 vertices.

## The invariant and its fourteen classes

Allow a permutation of the three minority cycles, an independent
rotation of each, and simultaneous inversion of the cycle coordinate.
In coordinates, a new core vertex (i,s) is the old vertex

```text
(pi(i), epsilon*s + t_i),  epsilon in {1,-1}, t_i in Z/3Z.
```

There are 6*27*2=324 such maps. Inversion must also be performed on all
eight blue moving cycles in the full graph. It conjugates the original
automorphism to its inverse, which still leaves G invariant. Reflecting
only the minority cycles is not a valid full-graph normalization.

Let w_ij be the red weight of word ij. The unordered triple of weights
is invariant. For a nonzero block, define its distinguished phase p_ij
to be the position of the unique red bit when w_ij=1, or the unique blue
bit when w_ij=2. Reverse orientations by p_ji=-p_ij.

If all weights are nonzero, the oriented phase sum

```text
h = p_01 + p_12 - p_02 mod 3
```

is unchanged by independent vertex-cycle rotations. Permuting the
triangle labels or simultaneously inverting all coordinates changes h
at most by sign. Thus h=0 versus h!=0 is invariant. It is also complete
together with the unordered weights: two phases can be made zero by
rotations, leaving the third equal to h; inversion identifies 1 and 2.
Permutations of three vertices induce every permutation of the three
edges, so any ordering of the weights can be matched.

If some weight is zero, the nonzero blocks form a forest on at most
three vertices. The distinguished phases can all be made zero by
rotations along that forest. There is no remaining phase invariant.
The six weight types containing zero are 000,001,002,011,012,022. The
four nonzero weight types 111,112,122,222 each give two phase classes.
Consequently the complete cover has 6+2*4=14 classes. These are classes
of the specified action, without a claim that distinct classes must be
nonisomorphic as abstract unlabeled graphs.

The producer `cores.py` computes the action on the three words. For
each orbit it chooses the lexicographically first representative with
anchor words 01,02 in {000,100,110} and w_01<=w_02. There are 42 such
normalized words before choosing one per orbit. The exact membership
lists and representatives are in `cover.json`.

The separate `audit.py` enumerates all 512 binary inputs as literal
nine-vertex adjacency matrices, checks every five-set, applies the
actual vertex permutations, and reconstructs every transported edge.
It compares complete orbit membership, disjointness and coverage, not
only the fourteen sizes. All 343*324=111132 transports are checked.
The normalizer identity is checked on all 43 vertices for all 324 maps;
an additional deterministic invariant-coloring control checks all 903
pairs for each map. `verify.py` computes the weight/phase invariants
again from literal adjacency rows for all 343 members.

## Compatibility with the full parent normalization

First move the minority core to its chosen representative using the
full-graph extensions of the preceding maps. The minority anchor words
are already weakly decreasing, and the other two minority cycles have
increasing anchor weights. Next rotate each blue cycle independently
to make its word from vertex 0 one of 000,100,110,111, then permute the
blue cycles by increasing anchor weight. Finally sort the ten fixed
vertices lexicographically by their eleven-bit red incidence signatures.
These later operations preserve the selected minority core and all
earlier normalizations. Equal anchor weights and repeated signatures
are allowed. This proves that every valid graph in this split has a
representative in at least one of the fourteen extension cubes.

The cubes are disjoint on their nine primary core bits. Their union
need not be a propositional tautology over all assignments of the
normalized parent formula: completeness is through graph relabeling.
Auxiliary gate and counter assignments are extended afresh from the
relabeled graph, as proved in the parent artifact.

## Formula and certificate bridge

The entire parent r=3 formula is regenerated by Python and reconstructed
independently by the parent's C++ literal-pair orbit checker. It has
320 primary variables, 34268 total variables and 615572 clauses. The
parent includes both monochromatic exclusions for all 962598 five-sets,
the proved local common-neighborhood and deficit inequalities, both
color-degree bounds, and the preceding normalization. In particular,
the moving upper degree bound remains present and active. Its direct
external mathematical input is R(4,5)=25, giving color degrees 18..24.
The parent's signed and repeated prefix-counter extension proof applies
without modification.

The minority words 01,02,12 correspond respectively to variables

```text
1,2,3; 4,5,6; 31,32,33.
```

Each cube consists of the unchanged parent clause prefix and exactly
nine unit clauses fixing these variables to its representative. Every
cube has 34268 variables and 615581 clauses. `audit.py` recovers the
core-variable meanings by iterating the action on actual unordered
vertex pairs, compares every byte of the independently reconstructed
parent prefix, and checks all nine appended units and the end of file.
No additional fixed core, degree profile, graph catalog, or automorphism
is assumed.

`run.py` uses two workers and a 60-second solver bound for each of the
fourteen cubes. An UNSAT exit is accepted only after independent full
DRAT replay against that exact cube. Some proofs use RAT steps, so this
is general DRAT rather than an addition-only RUP claim. UNKNOWN remains
open and supplies no feasibility evidence. A SAT assignment would be
decoded and checked by a separate literal 43-vertex five-set inspector.

`verify.py` starts with a new external directory, regenerates and
reconstructs the whole parent, rebuilds and audits every cube, and
freshly replays every successful proof. Four malformed cube mutations
must be rejected: a missing unit, wrong unit polarity, an unsupported
empty clause in the unit tail, and a corrupted parent prefix. Normal
and optimized-Python runs also give identical complete cover and
literal-audit reports. Runtime measurements, exact statuses and all
formula/proof hashes are in the compact public reports.
The additional cover controls reject a missing class, duplicate class,
missing orbit member and invalid representative. All checks use explicit
exceptions and remain active under optimized Python.

## Trust and scope

This is an ordinary algebraic reduction with computer-assisted
extension exclusions. The relabeling and parent counter arguments are
not formalized in a proof assistant. The direct external theorem is
R(4,5)=25; exact source, Python/C++ runtimes, compiler/hardware and the
DRAT checker remain computational trust boundaries. The second replay
and literal reconstruction are internal validation, not independent
peer review.

Full CNFs, large proof traces and logs remain outside Git. The source
and commands regenerate them; compact reports and hashes alone are
not standalone refutations. A changed valid trace must be replayed
against the audited formula. Host-dependent timeout differences never
establish an exclusion. This pass concerns only the three-versus-eight
eleven-cycle split and leaves the four-versus-seven split and larger
moving-cycle types untouched. It does not construct a target graph or
improve the lower bound for R(5,5).
