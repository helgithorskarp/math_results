# A blue triangle in every complementary triple forces an empty fixed signature

Let G be a red/blue complete graph on 43 vertices with no monochromatic
K5. Suppose an order-three automorphism has ten fixed vertices F, four
internally red moving triangles C0,...,C3 and seven internally blue moving
triangles D0,...,D6. A fixed vertex is uniform to each moving triangle.
Its minority signature S(f) is the subset of indices i for which f is red
to Ci.

**Theorem.** If, for every i, the union of the three triangles other than
Ci contains a blue triangle, then some f in F has S(f) empty.

The four blue triangles need not arise by deleting vertices of one blue
K4. This is the distinction from the preceding blue-K4 obstruction. In
particular the theorem applies to some cores with no blue K4 at all.
The theorem is independent of the finite core catalog and of SAT solving.

## Fixed structure under the contrary assumption

Suppose all ten signatures are nonempty. The fixed vertices red to any
Ci form a blue clique: a red edge among them would extend the red Ci to
a red K5. There are at most four such vertices, so the total incidence
I = sum over f of |S(f)| is at most 16.

For each i there is at most one singleton signature {i}. Two copies would
have a blue edge, and the assumed blue triangle in the other three core
triangles would complete a blue K5. If X counts singleton signatures,
then X <= 4. Because all signatures are nonempty,

```text
20 <= I + X <= 16 + 4 = 20.
```

Equality forces every singleton exactly once, no signature of size three
or four, and six pair signatures. The singleton {i} and all copies of
{i,j} form a blue clique since they are all red to Ci. There is a blue
cross edge between the two remaining red triangles: otherwise those two
triangles form a red K6. Three vertices in this fixed blue clique and
that cross edge would form a blue K5. Thus each pair occurs at most once,
and all six pair signatures occur exactly once.

Write the ten fixed vertices as v_i and v_ij. Intersecting signatures
have blue fixed edges. The four v_i form a red K4: a blue edge v_i v_j
would form a blue triangle with v_ij, completed by a blue cross edge
between the other two red triangles. A singleton v_i is also red to a
disjoint pair v_jk. Otherwise v_i,v_jk,v_ij,v_ik form a blue K4, completed
by any vertex of the fourth core triangle. This restates all fixed-edge
facts needed below; the other complementary-pair edges need not be fixed.

## Full-extension contradiction

For a blue moving triangle D, its fixed blue neighborhood B(D) is a red
clique. A blue edge in B(D) together with D would be a blue K5. Moreover
B(D) contains a singleton: otherwise any vertex of D is red to all four
v_i and extends their red K4.

B(D) contains at most one pair-signature vertex. If it contained two,
their signatures would have to be disjoint since intersecting signatures
have blue edges. Two disjoint pairs cover the four indices. The singleton
in B(D) intersects one of them, giving a blue edge in this red clique.
Thus the seven blue triangles supply at most seven blue incidences to
the six pair vertices.

Each pair vertex already has six red neighbors in the minority core and
two red complementary singleton neighbors. If b blue moving triangles
are blue to it, its red degree is at least 8 + 3(7-b). The imported theorem
[McKay and Radziszowski, R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf)
gives maximum color degree 24 in G. Therefore b >= 2. The six pair
vertices require at least twelve blue incidences, contradicting seven.
This proves the existence of an empty minority signature.

The final arithmetic is the same necessary packing projection as in the
[accepted blue-K4 theorem](../ramsey_r55_order3_eleven_blue_k4_exclusion).
For x_jk indicating a blue incidence between D_j and pair vertex k, its
seven upper rows -sum_k x_jk >= -1 and six lower rows sum_j x_jk >= 2
sum with unit multipliers to 0 >= 5. The new work is the weaker sufficient
hypothesis for singleton uniqueness; the packing argument is reused and
not claimed as a new independent certificate. The original R(4,5)
computation is imported, not repeated.

## Complete application at the current boundary

The preceding full-extension sweep leaves 45 four-versus-seven
marked-action classes. The producer tests all 27 phase transversals in
each of the four complementary triples for every core. A separate
checker imports no producer, constructs red edges by literal rotation
orbits, and examines all 84 three-subsets of each nine-vertex complement.
Every witness and every absent-witness entry is checked, as are the exact
selected list, core bits and inherited labeled multiplicities.

Exactly eleven classes satisfy the theorem's hypothesis:

```text
87, 101, 110, 112, 120, 121, 131, 139, 147, 162, 173.
```

They cover 5,697 labeled locally valid minority cores. The other 34 open
classes are outside this sufficient hypothesis; no empty-signature
conclusion is drawn for them. The property is invariant under the whole
marked-action normalizer: it permutes the four complementary triples
and preserves their blue triangles. Hence the implication applies to
every full extension in each selected class, not only to its displayed
representative.

The accepted core cover and full-parent normalization provide global
coverage. The preceding 34 computational exclusions are used to define
this current residual list, and their independent review is still
pending. The present hand theorem itself neither depends on those
refutations nor proves them.

## Why the full extension and blue-triangle hypothesis matter

The compact file `fixtures.json` contains a 22-vertex graph on core 87
and ten fixed vertices, with every singleton and pair signature once.
Fixed edges are red exactly for disjoint signatures. It has 102 red
edges and no monochromatic K5, yet none of its ten signatures is empty.
It satisfies all four blue-triangle hypotheses. Thus the new implication
cannot be deduced from this local subsystem alone; the seven omitted
blue moving triangles and the full degree bound matter.

The same file contains a 14-vertex graph on core 194 and two fixed
vertices with identical singleton {0}. It has 48 red edges and no
monochromatic K5. The complementary three-triangle core has no blue
triangle, so the singleton-uniqueness step fails when its hypothesis is
removed. Neither fixture is a 43-vertex candidate or a counterexample
to the theorem. The checker reads every edge and examines every five-set
in each color rather than trusting a reported clique count.

## Four necessary units in the complete formula

The reviewed parent sorts the full eleven-bit red attachment rows of
fixed vertices 33,...,42 lexicographically, with the four minority bits
first. Sorting full rows also sorts their prefixes, so an empty minority
signature occurs first whenever one exists. This implication is checked
on all 2,048 full rows; the first 128 have the zero four-bit prefix.

For core pair words 01,02,03,12,13,23, append the same eighteen primary
core units as the preceding sweep. The new theorem justifies precisely
four additional units:

```text
-211 0
-212 0
-213 0
-214 0
```

They make fixed vertex 33 blue to C0,...,C3. Variables are reconstructed
independently from literal pair orbits on all 43 vertices. No other
fixed signature, fixed edge, majority-triangle attachment, degree
profile or additional automorphism is assumed.

Every final formula retains the ENTIRE reviewed parent, including both
color-degree bounds, all Ramsey clauses, counters and normalization.
There are 34,280 variables and 615,942 clauses: 615,920 parent clauses,
18 core units and four empty-signature units. The complete parent hash is
`c8f355b256de55727b18efcbd47ef9e777ac2b3b4ae69e09676fcddd51afa05f`.
The inherited C++ auditor reconstructs the whole parent. The separate
cube auditor checks its whole prefix, all 22 new units and final EOF.

Each selected class receives one bounded full-extension test. UNSAT is
accepted only with full DRAT replay, followed by another replay after
fresh reconstruction of every complete formula. SAT must decode to a
43-vertex edge list and pass literal graph verification. UNKNOWN remains
open. Exact outcomes and review status are in the README and manifests.
Any verified refutation excludes the whole selected class because the
new units are necessary in its inherited normalization.

The new theorem and formula-unit bridge await independent review. Trust
includes unformalized combinatorics, imported R(4,5), accepted parent
normalization/counter reasoning, exact source semantics, runtime/hardware,
SHA256 and the external full DRAT checker for computational exclusions.
No proof-assistant formalization or priority claim is made. This pass
ends at the fixed eleven-case test and verification; it starts no further
signature stratum, core subdivision or larger timeout.
