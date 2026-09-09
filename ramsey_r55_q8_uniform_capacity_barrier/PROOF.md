# Uniform fractional obstruction to the proposed q8 capacity test

Let H be any graph on eleven labeled vertices with neither a red nor a blue
K4. An external vertex has a signature S contained in V(H), its red neighbors
in H. Let x_S be a nonnegative real variable for every one of the 2048
signatures. A physical q8 extension would give nonnegative integer values
with sum_S x_S=32. No single signature is prohibited by the target's five-set
conditions: a single outside vertex would need a monochromatic K4 in H to
complete a forbidden five-set, and H has none.

We test the following explicitly limited linear system. It includes all
mixed common-neighborhood capacities from the standard Ramsey bound table
below and every individual signature
multiplicity capacity. It does not include an adjacency matrix for the 32
outside vertices, their prescribed K4 block memberships, stronger global
degree/edge-profile restrictions, or integrality. Those omitted constraints
remain necessary in a physical task.

Write C(s,t) for the imported upper-bound table: C(1,t)=1, C(2,t)=t,
C(3,3)=6, C(3,4)=9, C(3,5)=14, C(4,4)=18, C(4,5)=25, with
C(t,s)=C(s,t). Thus R(s,t)<=C(s,t) at every index used here. Defining the
system using C makes its exact interface independent of lower-bound proofs
for these small Ramsey numbers. There is no C(5,5) constraint.

Take disjoint A,B contained in V(H), where A is a red clique of size a and B
is a blue clique of size b, with 0<=a,b<=3 and a+b>0. Empty cliques are
allowed. Let

    U_H(A,B) = {v in V(H) minus (A union B):
                 v is red to every vertex of A and blue to every vertex of B},
    h_AB = |U_H(A,B)|.

The common neighborhood in a good43 has no red K_(5-a) and no blue K_(5-b),
because either would extend with A or B to a forbidden five-set. Hence

    sum_{S: A subset S, S disjoint B} x_S + h_AB <= C(5-a,5-b)-1.       (1)

The core part U_H(A,B), separately, has no red K_(4-a) and no blue K_(4-b).
Therefore

    h_AB <= C(4-a,4-b)-1.                                            (2)

All vertices in U_H exclude A and B, so there is no self-adjacency convention
hidden in these statements. If a=3 or b=3, (2) says h_AB=0. Intersecting A
and B imposes inconsistent adjacency requirements and adds no nontrivial
constraint, so disjoint pairs include every relevant mixed cylinder.

For each signature S, put p=omega(H[S]) and q=alpha(H[V(H) minus S]), taking
both quantities as zero on an empty set. Copies of S in an actual extension
induce a Ramsey(5-p,5-q) graph, so we also impose

    x_S <= C(5-p,5-q)-1.                                             (3)

Here p,q<=3 and p+q>0, so all entries used below are known and each right-hand
side in (3) is at least one.

## Explicit feasible point

Set x_S=1/64 for every S. Then sum_S x_S=2048/64=32. Exactly
2^(11-a-b) signatures satisfy A subset S and S disjoint B, so the external
mass in (1) is 32/2^(a+b). The following table gives the largest possible
core contribution from (2), the total capacity in (1), and the resulting
nonnegative slack. Transposed rows have the same values.

| a,b | core upper bound | total capacity | external mass | worst-case slack |
|---|---:|---:|---:|---:|
| 0,1 | 8 | 24 | 16 | 0 |
| 0,2 | 3 | 13 | 8 | 2 |
| 0,3 | 0 | 4 | 4 | 0 |
| 1,1 | 5 | 17 | 8 | 4 |
| 1,2 | 2 | 8 | 4 | 2 |
| 1,3 | 0 | 3 | 2 | 1 |
| 2,2 | 1 | 5 | 2 | 2 |
| 2,3 | 0 | 2 | 1 | 1 |
| 3,3 | 0 | 1 | 1/2 | 1/2 |

Thus every instance of (1) holds, even with its actual core occupants rather
than an empty-core simplification. Nonnegativity and (3) also hold, since
1/64<=1. This proves feasibility for every valid H; no catalog sweep or LP
solver is required. The point need not be integral or realized by any graph.

Consequently this exact fractional mechanism cannot prove an upper bound
below 32 for any q8 core. By weak duality, any nonnegative linear combination
of its capacity bounds that covers every signature has right-hand side at
least 32: simply evaluate that proposed bound at this feasible point.
This includes arbitrary weights chosen separately for the exact labeled
core. It is not a restriction to a symmetric target graph or symmetric dual.
The equality cases in the table are allowed; a capacity of exactly 32 is
insufficient to exclude an extension needing 32 outside vertices.

## Scope, assumptions and result of the gate

The imported Ramsey upper-bound table uses R(1,t)=1, R(2,t)=t,
R(3,3)<=6, R(3,4)<=9, R(3,5)<=14, R(4,4)<=18 and R(4,5)<=25, with color
symmetry. Only these upper bounds are used. The first two are elementary.
For the others, elementary proofs of 6,9,18 are included in the pinned parent
packing source; the cited Angeltveit--McKay paper explicitly uses 14 and 25.
SOURCES.json gives provenance. The usual exact values make the stated table
conventional, but independently re-proving those Ramsey results is outside
this pass. The feasible-point and weak-duality arguments above are elementary.

All 546,356 original q8 cores satisfy the theorem, and all four r values have
32 outside vertices. Hence the proposed test has zero possible task exclusions
across all 2,185,424 q8 original IDs. This is a universal failure of the test,
not a proof that any physical task is feasible, a registry reduction, a new
carrier percentage, or a good43. No stronger signature system is ruled out.
In particular, earlier exceptional-degree signature results include additional
weighted-degree and branch hypotheses; this argument does not contradict them.

The declared mechanism fails its task/candidate leverage gate. This pass ends
without adding degree constraints, cell interactions, unions with extra
structural hypotheses, integer variables, another backend, or a nearby phase.
No historical novelty or independent reviewer verdict is claimed.
