# A full-extension obstruction for blue-K4 minority cores

**Theorem.** Let G be a red/blue complete graph on 43 vertices with no
monochromatic K5. Suppose it has an order-three automorphism with ten
fixed vertices and eleven moving triangles, four internally red and
seven internally blue. The union of its four red triangles contains
no blue K4.

Consequently **118 of the preceding 197 four-versus-seven core classes
are excluded from the full 43-vertex problem**, leaving 79 classes.
The excluded classes contain 63847 locally valid labeled cores; the
remaining classes contain 51696. This does not settle those 79 full
extensions or the three-versus-eight branch, exclude every eleven-cycle
automorphism, construct a target, or improve the Ramsey lower bound.

The theorem is a hand proof using the full seven-triangle incidence
count and the color-degree bound. No SAT solver or full CNF is needed.
The necessary fixed-vertex structure is restated below, so the theorem
does not import the correctness of an earlier checker or its catalog.
Only the exhaustive 197-to-79 census imports the preceding core cover.

## 1. The fixed signatures forced by a core blue K4

Let C0,...,C3 be the four red triangles and F the ten fixed vertices.
Every vertex in F is uniform to each moving triangle, since the
automorphism fixes it and rotates that triangle. Write S(f) for the
subset of {0,1,2,3} to which f is red.

Assume the four red triangles contain a blue K4. It uses one vertex
from each triangle. No f has empty signature, since it would complete
that blue K4 to a blue K5. Each singleton signature {i} occurs at most
once: two such vertices have a blue edge (a red edge together with Ci
would give a red K5), and the other three vertices of the core blue K4
would complete a blue K5.

For each Ci its uniform red neighbors in F form a blue clique and
therefore number at most four. Write I for total signature incidence
and X for the number of singletons. All ten signatures are nonempty,
so

```text
20 <= I+X <= 16+4 = 20.
```

Equality forces all four singletons once, no signature of size three
or four, and six pair signatures in total. The singleton {i} and all
copies of pair {i,j} are red to Ci and form a blue clique. There is a
blue cross edge between the two other core triangles (otherwise they
form a red K6). Thus there can be at most two of these fixed vertices,
or three of them and that edge give a blue K5. Every pair signature
occurs at most once, hence every one of the six pairs occurs once.

Denote the ten fixed vertices by v_i and v_ij accordingly. Two
intersecting signatures have a blue edge, or their common red triangle
gives a red K5. The four v_i form a red K4: a blue edge v_i v_j would
make a blue triangle with v_ij, completed by a blue cross edge between
the other two core triangles. Also v_i v_jk is red for distinct i,j,k:
if it were blue, v_i,v_jk,v_ij,v_ik would form a blue K4, completed by
any vertex of the fourth core triangle.

These facts suffice for the obstruction. For the auxiliary complete
attachment check, recall also the last equality restriction: at most
one of the three complementary pair edges may be blue. If two were
blue, their four endpoints and either endpoint of the third pair
would form a blue K5. Thus the fixed graph has four possible patterns.

## 2. Each blue moving triangle supplies at most one pair incidence

For one of the seven internally blue moving triangles D, let B(D)
be its common blue neighborhood within F. This is well-defined by
uniformity. It must be a red clique: a blue edge among B(D), together
with the three vertices of D, would give a blue K5.

At least one singleton v_i belongs to B(D). Otherwise all four v_i
are red to D, and any vertex of D extends their red K4 to a red K5.
There can be at most one pair-signature vertex in B(D). Two such
signatures would have to be disjoint, since intersecting signatures
have a blue edge. Two disjoint pairs cover the four indices, so the
singleton already in B(D) intersects one of them, again giving a blue
edge inside B(D).

Consequently each of the seven blue moving triangles is blue-complete
to **at most one of the six pair-signature fixed vertices**. Summing
over all seven triangles gives at most seven such incidences.

## 3. The full degree bound requires at least twelve incidences

The external theorem
[McKay and Radziszowski, R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf)
implies every color degree in G is at most 24: a color neighborhood
of size 25 would contain a same-color K4 or an opposite-color K5.
The original result is computational; its computation is not repeated
here. This is the sole external Ramsey-value input to the hand proof.

Each pair vertex v_ij already has six red neighbors in Ci and Cj,
and is red to both complementary singleton vertices. Thus it has
at least eight red neighbors before considering the seven blue moving
triangles. Its only other fixed neighbor that can be red is its
complementary pair, giving a local red degree d0 equal to 8 or 9.

If b of the seven blue moving triangles are blue-complete to v_ij,
its full red degree is

```text
d_red(v_ij) = d0 + 3(7-b),       d0 in {8,9}.
```

The bound d_red <= 24 forces b >= 2 in either case. All six pair
vertices therefore require at least twelve incidences, contradicting
the upper bound seven from the previous section.

This uses the entire moving part of the 43-vertex graph. It is not
another local-core nonexistence claim: the previously constructed
22-vertex extensions remain valid. No core cross-block phases, edges
between different blue moving triangles, degree profile, or fixed-row
normalization is assumed in this contradiction.

## 4. A tiny exact arithmetic certificate

Let x_(j,k) be the indicator that blue triangle j is blue to pair
vertex k, for j=0,...,6 and k=0,...,5. Every hypothetical full graph
maps to a solution of these thirteen inequalities:

```text
-sum_k x_(j,k) >= -1       for each of seven triangles j;
 sum_j x_(j,k) >=  2       for each of six pair vertices k.
```

Sum all thirteen rows with coefficient one. Every variable cancels
and the right side is -7+12=5, giving **0 >= 5**. This is already
infeasible over the reals; integrality and Boolean bounds are not
needed for the final arithmetic contradiction.

`packing.opb` encodes these rows with x_(j,k) numbered 6j+k+1.
`packing_certificate.json` contains the thirteen unit multipliers.
The checker independently reconstructs each row's exact meaning,
checks nonnegative integer multipliers, and adds the coefficients
and right sides. This is a certificate for the proved necessary
projection, not a complete Ramsey CNF or an independently sufficient
description of graph realizations.

## 5. Exact local checks and the surviving catalog

Fixed labels 0,...,9 have signatures
1,2,4,8,3,5,9,6,10,12, where a signature is its four-bit subset mask.
Bits 0,...,9 of an attachment mask mark BLUE adjacency to D. For
each of the four fixed-edge patterns, the permitted attachments on
F union D are exactly the same 33 masks:

* any nonempty set of the four singleton vertices: 15 choices;
* one pair vertex together with a nonempty subset of its two
  complementary singleton vertices: 6 times 3 choices.

The producer lists these masks by this structural formula. The
checker independently constructs all 4*1024 literal thirteen-vertex
graphs and tests five-sets in both colors. It confirms the complete
33-element sets, the at-most-one-pair bound, the fixed red degrees,
and all eight possible values of b in each degree formula. These
13-vertex patterns omit the red core and its cross edges to D;
they are necessary local possibilities, not asserted 25-vertex or
full 43-vertex extensions.

For the 197-to-79 reduction, the producer searches the 3^4 core
transversals for a blue K4. The independent checker instead builds
each literal twelve-vertex matrix and examines all 495 four-sets.
It checks the exact excluded and retained lists, witnesses and
inherited orbit multiplicities. The 118 excluded classes and their
63847 labeled cores have a displayed blue K4; the remaining 79
classes and 51696 labeled cores contain no blue K4. Classification
completeness and the applicability of the marked-action quotient
are inherited from the preceding 197-class cover.
Existence of a blue K4 is invariant under every allowed vertex
relabeling, so excluding a representative excludes its entire
marked-action orbit. No additional symmetry quotient is introduced.

Normal and optimized Python reproduce all certificate bytes and
reports. Eight malformed classifications, attachment lists or linear
certificates are rejected. Literal controls display the forbidden
red K5 for two complementary pair attachments and the forbidden blue
K5 for an intersecting singleton/pair attachment. Removing the red
singleton clique allows a two-pair attachment locally, showing why
that hypothesis matters. Explicit matrices also satisfy the weakened
incidence systems obtained by changing either the column demand to
one or the row capacity to two; these are abstract count models only.

## Scope and review status

The theorem and the entire necessary fixed-signature derivation have
hand proofs. The 118/79 census additionally imports the published
197-class action cover. That cover and the new result await independent
review. The prior fixed-vertex theorem is cited as the source of the
route, and its necessary part is rederived here. No independent
reviewer verdict, proof-assistant formalization or historical-priority
claim is made. Exact source bytes, Python/runtime/hardware, SHA256,
unformalized proof/code alignment and the external R(4,5) theorem
remain trust boundaries.

The residual 79 four-versus-seven cores have no full-extension verdict
in this pass. The two three-versus-eight cores and the global range
of eleven through fourteen moving cycles remain open. No next core
stratum, radius, solver campaign or construction phase has begun.
