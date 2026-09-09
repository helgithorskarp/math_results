# Failure of the declared constructive asymmetric local lemma certificate

This is a certificate-method obstruction, not an exclusion of a physical
Ramsey task. It applies to every original q8,r5..8 task, independently of
its eleven-vertex core. No resampling experiment is performed.

## Complete physical probability space and candidate implication

Fix any eleven-vertex graph H with neither monochromatic K4. Label eight
four-blocks 0,...,7 and H on vertices 32,...,42. Blocks 0,...,r-1 are red
K4s; the remaining blocks are blue K4s, for r in {5,6,7,8}.

For each pair of blocks, independently choose a uniform 4-by-4 binary cross
matrix from all matrices for which the union of those two fixed-color K4s
has no monochromatic K5. For each block and core vertex, independently
choose one of the fifteen four-bit columns that do not complete a K5 in
the block's color. Keep all block-internal and core edges fixed. There are
28 independent matrix variables and 88 independent star variables, covering
all 800 unfixed physical edges. This specifies a full graph on 43 vertices.

The bad events are every red or blue K5 on a physical five-set and every
red K4 in the whole tail {4r,...,42}. Identically impossible events can be
omitted. Join two events in the dependency graph if they depend on a common
matrix or star variable. This is the usual variable-overlap dependency graph.

If every event E had weights 0<x_E<1 satisfying

    Pr(E) <= x_E product_{F adjacent to E}(1-x_F),                   (1)

the Moser--Tardos theorem would give finite expected resampling time to an
assignment avoiding all events. Literal verification would then produce
a good43. Sorting vertices within the nonroot four-blocks by their root
columns would give an original task labeling, preserving H and every target
condition. Thus the proposed certificate has a direct physical candidate
implication, rather than merely optimizing dispatch or reducing a carrier.

No graph symmetry is imposed. The row/column invariance used below concerns
the sampling distribution and probability computation only. Root sorting
is postponed until a successful physical assignment; no successful assignment
is supplied here. The theorem is imported from Moser--Tardos, Theorem 1.2,
as identified in SOURCES.json. The obstruction to (1) below is self-contained.

## Exact distribution on an ordinary red block pair

For two red K4s, blue K5s are impossible, since a blue clique can take at
most one vertex from either block. A red K5 would use a rows and 5-a columns
for some 1<=a<=4, with the whole corresponding cross rectangle red.

Write D for the allowed matrix set, encoding entry (i,j) by bit 4i+j.
Complete enumeration of all 2^16 matrices gives |D|=37823. For any fixed
a-by-b rectangle with a+b<=4, let c_ab count matrices in D making it all
red. Independent row and column permutations, and transposition, preserve
D, so this count depends only on the dimensions. The exact counts are:

| a,b | c_ab |
|---|---:|
| 1,1 | 16447 |
| 1,2 or 2,1 | 6499 |
| 1,3 or 3,1 | 1976 |
| 2,2 | 784 |

The producer tests intersections of matrix rows. The separate checker
rebuilds the 56 forbidden patterns directly from the physical five-sets in
two red K4s. It compares the complete domain entry by entry and checks all 132 labeled
rectangles of the listed sizes. Every such rectangle has positive probability
strictly below one. No external matrix-domain file is imported.

## One unchanged clique of physical bad events

Use nonroot red blocks A={4,...,7}, B={8,...,11}, C={12,...,15},
and D'={16,...,19}. All exist and are red even when r=5. Consider every
five-set meeting all three of A,B,C, and every five-set meeting all three
of A,B,D'. Take only the event that all its edges are red.

Every event depends essentially on the same random variable X_AB. Indeed,
its required rectangle in X_AB is nonconstant on D, and the required
rectangles in the other two independent matrices have positive probability.
Fixing those other matrices to successful values makes changing X_AB turn
the event on or off. Thus these events form a clique in the specified
dependency graph, not merely a set with similar expectations.

For a fixed triple of blocks, a five-set has sizes (3,1,1) or (2,2,1),
including all three permutations of either type. For each permutation the
counts are 64 and 144, respectively. Its probability is the product of
the three rectangle probabilities, because the three matrices are independent.

Let L=37823^3=54108801960767. The event probabilities are

    p_311 = c_31^2 c_11/L = 64218561472/L,
    p_221 = c_22 c_21^2/L = 33113808784/L.

There are two triples of blocks, so the clique has
2*(3*64+3*144)=1248 distinct events: 384 of probability p_311 and
864 of probability p_221. The physical event lists and probabilities are
reconstructed independently and compared entry by entry.

## Verification of the stopping condition

The predeclared simple test was whether the probability sum exceeded one.
It did not:

    sum_E Pr(E) = 53270258394624/L < 1.

That initial test was inconclusive. The direct algebraic verification of
(1), on the same 1248 events, supplies the following stronger obstruction.
It was added after the exact probabilities were known; it was not the
predeclared numerical test. The original declaration and the explicit
verification addendum are retained without alteration. No distribution,
event set, physical family or dependency graph was changed.

For any clique of m>=2 events satisfying (1), let delta=min_E Pr(E).
Dropping factors corresponding to neighbors outside the clique and
multiplying the resulting m inequalities gives

    delta^m <= product_E [x_E (1-x_E)^(m-1)]
            <= [ (m-1)^(m-1) / m^m ]^m.

The last inequality follows by applying AM--GM to x_E and m-1 copies of
(1-x_E)/(m-1), whose sum is one. Also

    (1 + 1/(m-1))^(m-1) >= 2

by the binomial theorem. Therefore a necessary condition for (1) is

    delta <= 1/(2m).                                                (2)

Here delta=p_221 and m=1248, whereas the exact calculation gives

    2m delta = 82652066724864 / 54108801960767 > 1.

This contradicts (2). No assignment of asymmetric weights can satisfy
(1) for the declared full event family. The argument allows arbitrary
event-specific weights; no symmetry of those weights is assumed.

## Exact scope and physical outcome

This rules out the proposed asymmetric LLL certificate for each of the
2,185,424 original q8 tasks under the specified independent uniform block
distribution and the variable-overlap dependency graph. Its proof uses
no core data. It does not exclude any original task or any physical graph.

In particular, it does not prove that resampling cannot succeed, that the
avoidance probability is zero, or that every stronger or differently
formulated local lemma criterion fails. None of those alternatives was
tested. The initial sum below one is not an existence certificate either.

There are zero candidates, zero original-task closures and zero resampling
or target-solver steps. The registry and active q8 dispatch are unchanged.
The q10 queue is outside this pass. The certificate mechanism is parked at
this proof boundary, without altered probabilities, event regrouping,
alternative dependency graphs, another criterion or a target execution.

Trust comprises the ordinary proof above, exact Python integer/fraction
semantics and finite enumeration. The two implementations are author checks,
not reviewer-1's independent verdict or a proof-assistant formalization.
No novelty claim is made for the local lemma or the elementary clique bound.
