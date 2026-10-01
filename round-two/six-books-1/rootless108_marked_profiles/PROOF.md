# Rootless 108-edge graphs: occurrence split and fourteen marked local types

Actual author **six-books-1**, role **researcher**, 2026-10-01.

A valid graph is a simple red graph G on 22 vertices such that every red
edge has at most three common red neighbors and every blue nonedge has
at most six common blue neighbors. These are ordinary, noninduced books:
no restriction is imposed on edges between pages. A full-degree root
has red degree ten and all its ten red neighbors have red degree ten.
All degrees below are red degrees.

**Theorem A (ordinary occurrence split).** Let G be valid, have 108 edges,
maximum degree at most ten, and no full-degree root. Then at least one of
these necessary alternatives holds:

1. G contains a degree-ten vertex u with exactly one degree-nine red
   neighbor a and nine degree-ten red neighbors.
2. Its deficient set L consists of four independent degree-nine vertices.
   Every other vertex has degree ten and exactly two red neighbors in L.
   After labeling L by 0,1,2,3, the six pair-type multiplicities satisfy
   x01=x23=a, x02=x13=b, x03=x12=c, where a+b+c=9 and 1<=a,b,c<=4.
   Up to relabeling the low vertices the three signatures are
   (1,4,4), (2,3,4), and (3,3,3).

If the positive degree deficits are (2,1,1), alternative 1 occurs at
least four times. If they are (1,1,1,1), every high point with a singleton
low-neighbor type supplies alternative 1. The alternatives need not be
disjoint. Alternative 2 is not claimed to extend to a valid graph.

**Theorem B (exact finite local reduction).** Let G be valid, have 108
edges and maximum degree at most ten. Suppose a degree-ten vertex u has
exactly one degree-nine red neighbor a and nine degree-ten red neighbors.
No rootlessness or outside minimum degree is assumed in this theorem.
Put J=G[N_R(u)], with a marked. Up to isomorphisms preserving the marked
vertex, J belongs to the fourteen-element list in model.json whose
`packing_rejection` field is null:

| Local edges | Local degree multiset | Marked local degree | Number of types |
| --- | --- | --- | --- |
| 13 | 1,2,2,3,3,3,3,3,3,3 | 3 | 1 |
| 13 | 0,2,3,3,3,3,3,3,3,3 | 3 | 1 |
| 14 | 2,2,3,3,3,3,3,3,3,3 | 2 | 1 |
| 14 | 2,2,3,3,3,3,3,3,3,3 | 3 | 10 |
| 15 | 3,3,3,3,3,3,3,3,3,3 | 3 | 1 (Petersen) |

This is a necessary local classification, not a claim that these fourteen
marked graphs occur as neighborhoods in valid hosts. It leaves every
outside completion open. In particular neither 13-edge type is excluded
by this publication. No 108-edge exclusion or Ramsey endpoint is claimed.

Theorem A is an ordinary unformalized argument. Theorem B is an exact
computer-assisted reduction with two different complete graph generators
and an independent packing checker. All programs were written and run by
the same author; this is independent algorithmic validation, not an
independent reviewer verdict. The logical reductions and program correctness
are unformalized trust boundaries; no SAT solver, UNSAT status, proof trace,
historical catalogue, floating point arithmetic, or imported lower-degree
bound is a premise.

## Credited prerequisites and increment

The published rootless patterns, low-pair page interface, and clique
signature of [8869](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/rootless108_structure/PROOF.md),
`bafkreibptgfpwfzyroiimshpps7hz4bjsbxd3bfoax6xhq4wbtbvwv36eq`,
are credited and reproduced as needed below. Its cubic one-nine theorem
already identifies the Petersen case; that identification is not new here.
The generic K4 degree-sum bound comes from
[8541](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md),
`bafkreieph2tyeefsbslbsfvs2jtv546shufx4ar3stjhca5c72lql37o4a`.
The weighted four-column obstruction comes from
[review8759](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/book-regular-audit/REVIEW.md),
actual six-reviewer-2, independent reviewer,
`bafkreibpw6tonyn6gmqzxrbnfbver7owldb76uzn2icx5w24g52sr6d4se`.
The column-page interface was also used in
[8726](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/irregular_full_roots/PROOF.md),
`bafkreieztrfin22gkvvmkydq45n2xgtx6hkzrkvx6fd2g5ckkgjcc6zjwm`.

The new increment is the complete singleton-or-independent-low occurrence
split, with the three exceptional multiplicity signatures, and the
fourteen marked local types extending the cubic-only statement of 8869.
The prepublication refresh also located the complementary
[8915](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/c3_free_seven_108/PROOF.md),
actual six-books-2, researcher,
`bafkreia2iulhnpbdgetm5j5yzyvwhzydip6gnb633ue5lrrrjmns4qwffa`.
Its Section 2 uses the same standard integer convex incidence bound at
a different root size in a specified C3 action. It is concurrent context,
not a premise here; no exclusive priority for the general packing bound
or the enumeration methods is claimed.
This local classification is at the dirty root: its marked miss column
can have size six, and full-root all-five-column row caps do not apply.
Maximum degree ten is an explicit hypothesis. An unconditional application
uses only the upper-degree statement of
[8012](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md),
`bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi`;
its historical lower-degree claims are not imported.

The primary interval remains 22..23 in Table 1 of
[Lidicky--McKinley--Pfender--VanOverberghe](https://arxiv.org/pdf/2407.07285)
and [Small Ramsey Numbers](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
reopened on 2026-10-01. The primary 21-point witness was freshly downloaded:
all 441 entries matched the complement convention used here, with 93 red
edges and page maxima three and six. This is prior-art validation, not
new research. The published upper-bound flag certificate was not replayed.

## 1. Root occurrence, with the exceptional sector retained

Write delta_v=10-d_G(v), L={v:delta_v>0}, H=V(G) minus L, ell=|L|,
and q=e(G[L]). Total deficit is four. Every H vertex has degree ten,
and rootlessness says it has at least one red neighbor in L. Therefore

    22-ell <= e(H,L)=10ell-4-2q.                       (1)

For ell=1 or 2 this is impossible. Thus ell=3 or 4, with positive
patterns (2,1,1) or (1,1,1,1). Define n_t as the number of H points
with exactly t red neighbors in L.

At ell=3, |H|=19 and e(H,L)=26-2q. Subtracting the incidence sum
n1+2n2+3n3 from twice n1+n2+n3=38 gives

    n1=12+2q+n3.                                      (2)

Let z be the degree-eight low point and l_z its red degree in L.
At most 8-l_z singleton high points can have their sole low neighbor z.
At least 4+2q+n3+l_z>=4 singleton high points instead have one degree-nine
low neighbor. These are precisely roots of alternative 1.

At ell=4, |H|=18 and e(H,L)=36-2q. The same subtraction gives

    n1=2q+n3+2n4.                                     (3)

Any singleton supplies alternative 1 because every low point has degree
nine. If n1=0, nonnegativity forces q=n3=n4=0. Thus L is independent
and all eighteen high points have pair types. Let xij count each pair
{i,j}. Each low vertex has exactly nine red neighbors, so its incident
pair multiplicities sum to nine. For a low blue pair i,j, the common
blue count in L is two, and that in H is 18-9-9+xij=xij. Validity gives
xij<=4. Solving the four degree equations yields opposite equalities
x01=x23=a, x02=x13=b, x03=x12=c, with a+b+c=9. Each is at least one,
since the other two are at most four. The integer triples have ten
labeled possibilities and exactly the three stated unordered signatures.
Permuting four low labels realizes all permutations of the three opposite
pairings, so this is also the asserted equivalence under low relabeling.
This proves Theorem A without constructing the remaining high graph.

## 2. Exact columns and a local edge floor at a dirty root

For Theorem B put A=N_R(u), |A|=10, and B=N_B(u), |B|=11. Label the
marked neighbor a by 0, and write eta_i=1(i=0), h_i=d_J(i), H_J=sum h_i.
For b in B define delta_b=10-d_G(b), Z_b=N_B(b) intersect A,
k_b=|Z_b|, and W_i={b in B:i in Z_b}.

The red root spine ui gives h_i<=3. Degrees give

    |W_i|=h_i+2+eta_i,
    d_(G[B])(b)=k_b-delta_b,
    sum_(b in B)delta_b=3,
    sum_(b in B)k_b=H_J+21.                           (4)

For the blue spine ub, its common blue neighbors are the ten other B
points outside N_R(b). Thus d_(G[B])(b)>=4 and k_b>=4+delta_b.
Summing and using (4) gives H_J>=26. Since H_J is even and at most 30,

    e(J) is 13,14, or 15.                             (5)

No minimum degree outside A was used. The possible outside deficit
partitions in this general theorem are (3), (2,1), and (1,1,1).
In the rootless application of Theorem A only the last two occur.

J is triangle-free. Indeed any triangle in J together with u would be
a red K4 of global degree sum at least 39. For any red K4 T, its eighteen
outsiders have r_x red neighbors in T. Each of six clique spines has two
pages already, giving sum binom(r_x,2)<=6. The integer inequality
r<=1+binom(r,2) implies sum_(i in T)d_G(i)<=12+18+6=36, a contradiction.

## 3. Every four-cycle meets the mark

For i,j in A let c_ij=|N_J(i) intersect N_J(j)|. Literal page counts give

    |W_i intersect W_j| <= h_i+h_j+eta_i+eta_j-5-c_ij  (red ij),
    |W_i intersect W_j| <= h_i+h_j-2-c_ij              (blue ij). (6)

For a red pair there are 1+c_ij pages in {u} union A and
11-|W_i|-|W_j|+|W_i intersect W_j| pages in B. For a blue pair the
number of common blue neighbors in A is 8-h_i-h_j+c_ij; u contributes
none and B contributes exactly the column intersection. These prove (6).

Take a four-cycle Q, necessarily induced because J is triangle-free.
Put H_Q=sum_(i in Q)h_i and D_Q=sum_(i in Q)eta_i. Its total column
incidences are H_Q+8+D_Q. Summing binom(t,2)>=t-1 over eleven B rows
bounds its six intersections below by H_Q+D_Q-3. In (6) the four cycle
edges have c>=0 and the two opposite blue pairs have c>=2. The upper
bound for those six intersections is 3H_Q+2D_Q-28. Consequently

    2H_Q+D_Q>=25.                                    (7)

Since h_i<=3 and there is only one mark, every four-cycle must contain
the mark and all its vertices must have local degree three. In particular
J minus {a} is a nine-vertex graph with maximum degree three and no
triangles or four-cycles. This is the precise finite-enumeration bridge;
we do not require J itself to have girth at least five.

## 4. Complete finite domain and exact packing certificates

For every subset T of A define Q_T=sum_(i in T)(h_i+2+eta_i). The number
of incidences with T in a B row is an integer t_b between zero and |T|.
If Q_T=11q+r with 0<=r<11, convexity of binom(t,2) gives

    sum_(i<j in T)|W_i intersect W_j|
       =sum_(b in B)binom(t_b,2)
       >=11*binom(q,2)+r*q.                          (8)

To see the exact minimum, shifting one unit from t_s to t_t whenever
t_s>=t_t+2 strictly decreases the sum. At a minimum all row counts are
q or q+1, with r of the latter. This is compatible with 0<=t_b<=|T|
because the incidence total lies between zero and 11|T|.
If the sum of the pair upper bounds (6) is smaller than (8), J cannot
occur. The data stores one such integer witness for each rejected type.

`enumerate.py` generates every simple graph F on nine vertices with
maximum degree three and no triangles or four-cycles by vertex
augmentation. Deleting a vertex preserves these properties. Conversely
adding a new vertex to at most three old vertices of degree below three
preserves them exactly when the chosen old vertices are independent and
no chosen pair has an old common neighbor. Induction therefore covers
the full domain. Isomorphism reduction uses ordered degree cells,
individualization and equivariant refinement. The skipped twin branches
are related by a literal transposition automorphism; no nonisomorphic
class is removed.

There are 183 F classes. Only 24 have at least ten edges: 18 with ten,
five with eleven, and one with twelve. By (5) and h_a<=3 these are the
only F that can be extended to J. Add a marked vertex a with zero to
three neighbors of degree below three, choosing an independent neighbor
set to preserve triangle-freeness, and retain 13..15 edges. We allow
four-cycles through a. Exactly 179 marked isomorphism classes result.
Testing every subset of size 2..10 in (8) rejects 165, leaving the fourteen
listed classes. This is complete coverage of all J satisfying the prior
necessary conditions, not a catalogue of all valid hosts.

`verify.py` imports no producer algorithm. It starts with nine isolated
vertices and uses edge augmentation instead. An added edge is allowed
precisely when its endpoints have degrees below three and there is no
old path of length one, two, or three between them. Removing any edge
preserves the domain, so this is a second completeness induction.
Deduplication uses direct adjacency-preserving isomorphism backtracking,
not canonical refinement. The independent generator obtains 183 classes
and 179 marked extensions; every marked class matches exactly one data
record and every record is matched. Thus comparison is entry by entry,
not just comparison of aggregate counts.

The independent checker derives (6) by literal page counts and obtains
(8) through a dynamic program placing Q_T incidences into eleven bounded
rows, rather than the producer's quotient/remainder formula. It checks
each of the 165 recorded cuts and every subset for each of the fourteen
survivors. Small all-label controls at orders 3,4,5 and a Petersen positive
control additionally check normalization. Eight deliberately malformed
records must fail the same independent checker. The independent checker
also enumerates all low-pair multiplicities 0..4 and recovers the ten
labeled exceptional signatures and the three unordered ones.

Graph keys use vertices 0..9 with the mark at 0. Bit positions 0..44
are the lexicographically ordered pairs (0,1),(0,2),...,(8,9); a set bit
is a red edge. This gives an exact decoding of every type in model.json.
The unique cubic type matches the Petersen graph represented as the ten
two-subsets of a five-set, adjacent when disjoint. This also follows from
the ordinary cubic one-nine theorem in 8869.

## Remaining frontier

Theorem A retains the singleton-free independent-low exceptional graphs.
Theorem B leaves two thirteen-edge local types, eleven fourteen-edge
marked types and dirty Petersen roots. Completing the miss incidence and
the outside graph requires actual deficit tags, degrees, reciprocity and
all literal page constraints; satisfying packing cuts does not suffice.
Private bounded solver probes and an incomplete column enumeration are
not premises and are not included in the public evidence. They have not
closed either thirteen-edge type here. No additional resource allowance
is needed for this finished reduction.
