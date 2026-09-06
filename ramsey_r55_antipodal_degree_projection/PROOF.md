# Exact antipodal degree projection for the fixed H92 subsystem

This is an existential projection lemma for the particular subsystem defined
below. It is not a Ramsey(5,5) existence or nonexistence result. The degree
criterion is classical; the application identifies exactly which physical
edges can be eliminated here and supplies a checked lifting algorithm.

## Fixed labeled instance

Use vertices 0,...,42 and red-edge variables. The complete induced coloring
on H={0,...,19} is the supplied H92.json (92 red edges, SHA-256
`926c18173764c02a45d6e6d46dc001eddff6a161570bdc3b1efcd8a24539f466`).
Set W={2,...,9}, D0={10,...,13}, D1={14,...,17}, D01={18,19},
X={20,...,28}, Y={29,...,37}, and Z={39,...,42}. The three fixed red stars are

- N_R(0)=D0 union D01 union Y union Z union {38};
- N_R(1)=D1 union D01 union X union Z union {38};
- N_R(38)=H.

The remaining incidences with these roots are blue. These stars agree with
H92. There are 276 fixed pairs and 627 free pairs. Desired red degrees are
20 at roots 0,1,38 and 21 elsewhere.

The **original subsystem** consists of the fixed coloring, these 43 degree
equations, the following six local Ramsey requirements, and two densities:

- each red neighborhood of 0,1,38 contains no red K4 or blue K5;
- each blue neighborhood of 0,1,38 contains no red K5 or blue K4;
- the blue neighborhoods of 0 and 1 each induce exactly 124 red edges.

This includes every monochromatic K5 through one of the three roots, but
does not include every other K5 of the 43-vertex graph. No automorphism,
sorted vertex labeling, family census, or extra hard-profile condition is
assumed. All 627 unprescribed graph edges were free decisions.

## The three eliminated blocks

For a non-root vertex v, take its three color bits to roots (0,1,38), with
red=1. An edge uv is in none of the six root neighborhoods if and only if
the two bit vectors are complementary. In this instance the nonempty
complementary pairs of classes are exactly:

| Left class | Right class | Opposite signatures | Free pairs |
| --- | --- | --- | ---: |
| Z | W | 110 and 001 | 32 |
| D0 | X | 101 and 010 | 36 |
| D1 | Y | 011 and 100 | 36 |

D01 has signature 111; signature 000 is empty. All 104 listed pairs are
free, and the three blocks have disjoint vertex sets. They are absent from
every local Ramsey constraint and from both 124-edge density equations.
Only the global degree equations use them in this subsystem.

Retain the other 523 free pairs as Boolean variables x_e. For each vertex v
define the integer residual

    r(v) = desired_degree(v) - fixed_red_degree(v)
           - sum{x_e : retained free e incident with v}.

Vertices 0,1,18,19,38 lie outside the three blocks and must have r(v)=0.
The root equations are identically zero; the equations at 18,19 are not.

## Projection theorem

For each block L x R, where |L|=4 and |R| is 8 or 9, impose

    0 <= r(i) <= |R|                  for i in L,
    0 <= r(j) <= 4                    for j in R,
    sum_{i in L} r(i) = sum_{j in R} r(j),
    sum_{i in S} r(i) <= sum_{j in R} min(r(j), |S|)
                                     for every nonempty S subset of L.

**Claim.** A retained 523-bit assignment has a completion to the original
subsystem if and only if it satisfies the unchanged neighborhood and
density constraints, the five outside residual equations, and these block
conditions. Thus 104 edge decisions can be existentially eliminated.
There are 45 labeled subset cuts, three balance equations, and 76 scalar
residual bounds. Some conditions are redundant: in particular the full-set
cut follows from the column bounds and balance. Redundancies are retained
to keep the schema transparent. The minimum expressions are part of a
mixed Boolean/integer model, not already a CNF or OPB encoding.

**Necessity.** In a completed graph the red edges of a block form a binary
4-by-|R| matrix with row and column sums r. Bounds and balance follow.
For S of rows, column j contributes at most both r(j) and |S| ones. Sum
these upper bounds to get each subset inequality.

**Sufficiency and constructive lifting.** Consider one block. Make a
directed network: source-to-row i has capacity r(i), every row-to-column
arc has capacity 1, and column j-to-sink has capacity r(j). A cut with
row set S and column set T on the source side has capacity

    D - sum_{i in S} r(i) + |S| (|R|-|T|) + sum_{j in T} r(j),

where D is the common margin total. For fixed S, minimizing over T gives

    D - sum_{i in S} r(i) + sum_{j in R} min(r(j), |S|).

For empty S this is D; for nonempty S the imposed inequality makes it at
least D. Therefore every source-sink cut has capacity at least D.

For completeness, an integer maximum flow can be constructed without an
external integrality assumption: start at zero and repeatedly augment
along a residual source-sink path by its smallest residual capacity. All
capacities and flows stay integral, each augmentation adds at least one,
and total flow is at most D<=36. If no augmenting path remains, the
residually reachable vertices define a cut whose capacity equals the flow
value (forward arcs saturated, backward flow zero). Since every cut has
capacity at least D, termination must occur at flow D. Source and sink
arcs are then all saturated; the row-column arc flows give the required
binary matrix. `flow.lift` implements this construction deterministically.

Complete each of the three disjoint blocks independently. Every degree
equation is now satisfied, and all other subsystem constraints are
unchanged because they contain none of these edges. This proves both
directions. Conversely any subsystem solution restricts to a projected
solution. The correspondence is generally many-to-one, not a bijection.

## Why weak margin checks are insufficient

Rows (4,4,0,0) and columns (3,3,1,1,0,0,0,0) obey all individual bounds,
balance, and every singleton row cut. The first two rows demand 8 ones,
but their subset bound is 2+2+1+1=6. They have no binary realization.
Appending a zero column gives the same example for the 4-by-9 block.

## Computational validation and its scope

The proof above is finite and self-contained, but not proof-assistant
formalized. The code is an internal validation, not independent peer review.

`audit.py` does not import the model, flow, or margin-test implementation.
It recovers the omitted pairs from complementary signatures, reconstructs
the physical clauses from all five-sets, and checks the complete
side-condition schema. It finds 70,848 distinct physical clauses on the
523 retained variables. Optional comparison with the previous local
200,127-clause formula confirms equality of its physical clause set; it
does not re-prove that formula's auxiliary-counter implementation.

`test_margins.py` independently enumerates binary matrices by successive
columns, retaining a sorted row-sum state and its labeled-matrix count.
For any row-permuted representative the multiset of successor sorted
states is identical, so counts may be aggregated without dividing by an
orbit size. All sorted column vectors are visited. For each, every sorted
row vector is compared entrywise with the inequality criterion. All
balanced pairs are also checked by flow, independently of the criterion.
These row/column permutations are symmetries of an abstract complete
bipartite degree problem, not assumed automorphisms of a Ramsey graph.
Small literal matrix censuses verify the DP, and column multinomial
weights recover all 2^32 and 2^36 labeled binary matrices. This does not
enumerate all 43-vertex graphs or establish a Ramsey census.

## Essential non-extension to the full Ramsey problem

The unchanged public G92 fixture has 653 monochromatic K5s. Its projected
values meet all degree and density conditions but violate 202 local
clauses, so it is not a witness to the projected subsystem. Flow lifting
changes 16 antipodal edge colors while preserving every entire root
neighborhood and all degrees. The lifted fixture has 637 monochromatic
K5s and still violates the same 202 local clauses. This is a reconstruction
test, not an optimization/descent experiment or a target improvement.

The five-set {2,3,15,26,34} is not monochromatic originally and becomes a
red K5 after lifting. Thus omitted full-graph K5 predicates need not be
preserved. The theorem does not authorize dropping these edges from a
full Ramsey encoding without retaining extra constraints on their lifts.
Neither fixture is a 43-vertex Ramsey(5,5) graph; no SAT/UNSAT verdict for
the six-neighborhood subsystem is supplied.

## Classical provenance

The binary-matrix margin criterion and network-flow method are classical;
no novelty is claimed for them. See D. Gale, *A theorem on flows in
networks*, Pacific Journal of Mathematics 7 (1957), 1073–1082, especially
the binary-matrix application in Section 3 ([official paper](https://msp.org/pjm/1957/7-2/pjm-v7-n2-p04-s.pdf));
and H. J. Ryser, *Combinatorial properties of matrices of zeros and ones*,
Canadian Journal of Mathematics 9 (1957), 371–377, Theorem 2.1
([official paper](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/S0008414X00044734)).
The contribution here is the scoped 104-edge elimination and reproducible
physical reconstruction for the fixed H92 six-neighborhood instance.
