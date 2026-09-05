# A one-point extension with minimum obstruction order 508 or 509

All labels refer to the published Parts coordinate system: original vertices
are 0 through 508, and completion point `i` has label `509+i`. Let V denote
the original 509 points, P the 76 completion points with at least seven unit
neighbours in V, and A7 the strict unit-distance graph on V union P. Thus
P = {509,...,584}. Define

\[
q=610=\left(-\frac{5+\sqrt{33}}{12},
                 \frac{5\sqrt3-\sqrt{11}}{12}\right),
\qquad H=\operatorname{UD}(V\cup P\cup\{q\}).
\]

Exact arithmetic gives 586 distinct vertices, 3,089 edges, and
N_H(q) = {0,1,63,163,171,198}. In particular q has no neighbour in P.

**Theorem.** Every subgraph of H with at most 507 vertices is four-colourable.
The minimum order of a non-four-colourable subgraph of H is either 508 or 509.
Every possible 508-vertex obstruction has its vertices in the following exact
form:

\[
  (V\setminus(\{15,23\}\cup T))\cup\{q\}\cup A,
  \qquad |T|=|A|=3,
\]

where A is a subset of P and T is a subset of the 56 original free vertices
other than 15 and 23. It must also meet each of the 424 killing sets retained
below. These conditions are necessary; their satisfiability, and the
four-colourability of the surviving supports, are not decided here.

**Additional certified fact.** H minus {15,23} has 584 vertices, 3,071 edges,
and chromatic number exactly five. This verifies an obstruction to lifting
one inherited killing set; its order does not improve the record.

## Imported results and new positive evidence

The [degree-seven certificate](../hadwiger_nelson_parts509_degree_pool_minimum/README.md)
provides 451 forced original vertices F, a free set R=(V union P) minus F of
size 134, and a family C of 425 killing sets contained in R. Its checked
pseudo-Boolean bound is:

> If Y is a subset of R, meets every member of C, and contains at least four
> members of P, then |Y| is at least 58.

The proof input uses the 337 inclusion-minimal members of C. The present
verifier regenerates its exact OPB bytes and checks their published hash.
We import the old VeriPB-checked theorem; this pass did not rerun its large
proof. The prior closure of A7 and the earlier zero-, one-, two-, and
three-addition closures are also imported. In particular, any non-four-
colourable graph with at most 508 vertices using these coordinates has at
least four vertices outside V. The dependencies are recorded in the README.

The new `certificate.json` directly supplies proper four-colourings of:

* H minus v, for every v in F (451 witnesses);
* H minus D, for every D in C except D*={15,23}, row 188 (424 witnesses).

Most witnesses are old colourings with one appended colour. Two forced
witnesses and one killing-set witness are replaced in full. The verifier
reconstructs all unit edges exactly and checks every retained edge in every
witness. Consequently every non-four-colourable subgraph of H contains F
and intersects every member of C except D*.

## Loss of one clause costs at most two selected vertices

Suppose J is a non-four-colourable subgraph of H with at most 508 vertices.
It contains q, since A7 has no such subgraph, and it contains F. Write

\[
 X=V(J)\setminus(F\cup\{q\})\subseteq R.
\]

Then |X| is at most 56, X contains at least three points of P, and X meets
every member of C except possibly D*.

If |X| were at most 55, add a vertex from D* when needed and, when X has
exactly three points of P, add an unused point of P. The resulting Y meets
all of C, contains at least four points of P, and has size at most 57.
This contradicts the imported bound. Hence |X|=56 and |V(J)|=508, proving
the four-colourability assertion through order 507.

If X already contained four points of P, at most one additional vertex
would repair D*, giving the same contradiction. If X met D*, at most one
additional point of P would give the contradiction. Therefore

\[
 |X\cap P|=3,\qquad X\cap\{15,23\}=\varnothing.
\]

The other 53 members of X are original free vertices. There are 58 original
free vertices, so exactly five of them are omitted: 15, 23, and three
others. This proves the stated residual form. Adding edges to J to obtain
the strict induced graph on its support cannot make it four-colourable,
so induced supports suffice for the remaining search. The old Parts graph
is a 509-vertex obstruction in H, providing the upper bound 509.

This argument is an instance of a general finite repair observation. Given
a hitting-set bound m under a pool quota t, deleting one hitting clause
and lowering the pool quota to t-1 gives a bound at least m-2, provided an
unused pool element and an element of the missing clause can be adjoined.
Equality can occur only when the missing clause is missed and the relaxed
quota is exact. Here the available sets have sizes 76 and two, respectively.

## Encoding the exact residual

The primary variables are d_v for the 56 eligible original vertices and
a_p for the 76 points of P. A true d_v means delete v; a true a_p means add p.
Impose exactly three true variables in each group. For each retained D in C,
the hitting condition is

\[
 \bigvee_{v\in D\cap(V\setminus(F\cup\{15,23\}))}\neg d_v
 \quad\vee\quad
 \bigvee_{p\in D\cap P}a_p.
\]

The prefix counter defines t[i,j] as “at least j of the first i literals are
true.” Its recurrence is z iff a or (x and b), encoded by
(not a or z), (not x or not b or z), (not z or a or x), and
(not z or a or b), with explicit Boolean constants on the boundary.
This equivalence proves the encoding by induction. Two thresholds, at three
and four, impose each exact cardinality. There are 1,038 total variables and
3,774 clauses. Before hitting-set filtering the number of support pairs is
binomial(56,3) times binomial(76,3) = 1,948,716,000.

SAT would only identify a support satisfying these necessary conditions.
A separate exact four-colouring check, or checked refutation, would still
be required for a graph claim. A checked UNSAT certificate for this residual
formula would close H through order 508. This formula was generated but
was not submitted to a solver in this pass.

## Certifying the failed lifting clause

The full four-colouring CNF for H minus {15,23} has 2,336 variables and
12,871 clauses. Each vertex has an at-least-one-colour clause, and every
unit edge excludes each common colour. At-most-one clauses are unnecessary:
adjacent nonempty colour sets are disjoint, so choosing one colour from
each set yields a proper colouring. Triangle 0,149,152 is pinned to
colours 0,1,2, without loss under colour permutation.

Kissat returned UNSAT and drat-trim accepted its complete DRAT proof.
An explicit proper five-colouring of H is obtained by giving vertex 44 a
fifth colour in a checked four-colouring of H minus 44. Restricting this
colouring proves the upper bound five for H minus {15,23}. Thus D* is
provably not a killing set of H, rather than merely a failed witness search.
