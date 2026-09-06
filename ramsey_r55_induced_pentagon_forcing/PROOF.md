# An induced pentagon is forced at order 42

**Theorem.** Every simple graph on at least 42 vertices contains a clique of
order 5, an independent set of order 5, or an induced cycle of length 5.
Consequently every hypothetical Ramsey(5,5;43) graph contains an induced C5.

This excludes the complete induced-C5-free43-vertex branch. There are no
degree-profile, fixed-core, symmetry, connectivity or catalog hypotheses.
It does not exclude any graph that already has an induced C5 and does not
improve the unrestricted Ramsey number. Neither the order 42 threshold nor
historical novelty is asserted to be optimal or new.

The proof has two components: an elementary ten-vertex lemma and the
classical mixed-triangle identity of Goodman. The finite checks accompanying
the proof verify the small contact lemma and arithmetic, but are not needed
in place of the reasoning below. No SAT verdict, external graph enumeration,
small-Ramsey value or asymptotic Erdős–Hajnal theorem is a premise.

Throughout, graphs are finite, undirected, and simple. A cycle mentioned as
an ordinary subgraph may have chords unless explicitly described as induced.
In a triangle-free graph every ordinary 5-cycle is induced: any chord joins
vertices at distance 2 around the cycle and completes a triangle.

## 1. Saturation of an independent neighborhood

Let H have neither a triangle nor an ordinary 5-cycle, and assume alpha(H)<=a.
Every neighborhood is independent, so every degree is at most a. Suppose v
has degree a, let A=N(v), and let B=V(H) minus ({v} union A).
Every member of B has a neighbor in A; otherwise that member together with
A is an independent set of size a+1.

In fact B is independent. If xy is an edge of B, choose p in A adjacent to x
and q in A adjacent to y. If p=q, then p,x,y is a triangle. Otherwise
v,p,x,y,q is a5-cycle. Both are forbidden. Hence |B|<=a, and |H|<=2a+1.

We have proved:

> If H has neither C3 nor C5, alpha(H)<=a, and |H|>=2a+2, then Delta(H)<=a-1.

We will also use the following part without the saturation hypothesis:
for any vertex v in a triangle/C5-free graph, the vertices at distance
exactly 2 from v form an independent set. The same p,x,y,q argument proves it.

## 2. The independence-three boundary

Every triangle/C5-free graph on 8 vertices has an independent4-set. If not,
Section1 with a=3 gives maximum degree 2. Its components are paths and cycles.
If every cycle is even, the graph is bipartite and a bipartition class has
at least4 vertices. The only possible odd cycle is C7, since lengths 3 and 5
are forbidden. The remaining vertex is isolated, and it joins an independent
triple of C7 to give an independent4-set. This is a contradiction in all cases.
The assertion extends to larger orders by taking an induced8-vertex subgraph.

Moreover, a triangle/C5-free graph J on 7 vertices with alpha(J)<=3 is exactly
C7. It cannot be bipartite, so it contains an odd cycle. A shortest odd cycle
has length 7, since lengths 3 and 5 are forbidden. It uses all the vertices.
Any additional edge is a chord whose shorter cyclic distance is2 or3, giving
a triangle or a5-cycle, respectively. Thus no additional edge exists.

## 3. A seven-cycle contact lemma

Label C7 cyclically by0,...,6. Let S,T be subsets such that each is empty,
a singleton, or a pair at cyclic distance 2, and suppose no cycle edge has
one endpoint in S and the other in T. Then C7 minus (S union T) has an
independent triple.

If neither subset is a pair, at most two vertices are removed. Removing two
vertices leaves paths on a total of five vertices; their independence numbers
sum to at least3. Removing fewer vertices cannot decrease that maximum.

Otherwise exchange S,T if necessary and use a rotation/reflection to put
S={0,2}. The no-cross-edge condition puts T inside {0,2,4,5}. Its permitted
two-element choices are exactly {0,2}, {0,5}, {2,4}. Consequently S union T
is contained in either {0,2,4} or {0,2,5}. In the first case {1,3,5} is a
missed independent triple, and in the second {1,3,6} is one. This proves
the lemma without enumeration.

For reproducible finite evidence, build.py records all 15 permissible contact
sets and all 141 compatible ordered pairs, with a missed independent triple
for each. check.py independently expands every one of the 16,384 possible
physical contact pairs on a rooted ten-vertex graph. It classifies triangles
and induced pentagons directly, then verifies the independent5 certificate
in every remaining case. No cyclic-distance classification is imported into
that check, and equality of the complete pair sets is checked entry by entry.

## 4. The ten-vertex lemma

**Lemma.** Every triangle/C5-free graph on 10 vertices has an independent5-set.
The order 10 is sharp: C9 is triangle/C5-free and has independence number 4.

Suppose H is a counterexample. Section1 with a=4 gives Delta(H)<=3.
For every vertex v, its nonneighbors induce a triangle/C5-free graph with
independence number at most 3, since an independent4 there would join v to
give an independent5. By Section2 this set has at most7 vertices. Therefore
d(v)>=10-1-7=2, and all degrees are 2 or 3.

First suppose H is3-regular. Fix v and let A=N(v), an independent triple.
Of the six other vertices, put U at distance 2 from v and put Z among those
with no neighbor in A. Section1 shows that U is independent, hence |U|<=4.
Any two vertices of Z must be adjacent, since otherwise they join A to an
independent5. Thus Z is a clique and |Z|<=2 by triangle-freeness. Since
|U|+|Z|=6, we have |U|=4 and |Z|=2, with the latter two vertices adjacent.

Each vertex of A has one edge to v, no edge inside A or to Z, and two edges
to U. There are therefore 6 edges from A to U. Each vertex of Z has one
edge to the other vertex of Z, no edge to v or A, and two edges to U.
There are therefore 4 edges from Z to U. But U has no edges to v or inside
itself, and its four vertices require total degree 12. The available edges
supply only6+4=10. This contradiction excludes the3-regular case.

Now let v have degree 2, with neighbors a,b. Triangle-freeness makes ab a
nonedge. The seven nonneighbors of v have independence number at most 3, so
Section2 identifies their induced graph as C7. Write S=N(a) intersect C7
and T=N(b) intersect C7. No two members of S (or T) can have cyclic distance 1,
which would make a triangle, or distance 3, which would make a5-cycle with a
(or b). Hence a contact set has at most two vertices, and if it has two they
are at distance 2. To see the size bound explicitly, a pair {0,2} has no third
vertex at distance 2 from both of its members.

There is no cycle edge xy with x in S and y in T: v,a,x,y,b would be a5-cycle.
Section3 now supplies an independent triple of C7 missed by both a and b.
Together with the nonadjacent vertices a,b, this is an independent5, the
final contradiction. Both possible degree cases are exhausted.

Equivalently, every ten-vertex graph has a triangle, an independent5, or an
induced C5: if it has no triangle, an ordinary 5-cycle is induced, and otherwise
the lemma applies. This formulation is the one used in the global extractor.

## 5. Global triangle counting

Color the edges of a complete graph red and blue. Let d_v denote red degree,
and let M count monochromatic triangles in both colors. A mixed triangle
has precisely two vertices incident with differently colored edges inside
that triangle. Counting these mixed wedges gives Goodman's identity

    M = binom(n,3) - (1/2) sum_v d_v (n-1-d_v).

Since d_v(n-1-d_v)<=(n-1)^2/4, it follows that

    3M >= n(n-1)(n-5)/8.                         (1)

For each pair e, let q_e be the number of common neighbors in the color of e.
Each monochromatic triangle contributes once to each of its three pairs,
so

    sum_e q_e = 3M.                              (2)

If all q_e<=9, then (2) gives 3M<=9*binom(n,2). Comparing with (1), for n>1
we obtain n-5<=36, hence n<=41. Thus every coloring on n>=42 has some pair
with at least 10 common neighbors of its own color. This conclusion requires
no Ramsey or induced-cycle hypothesis.

Choose ten such common neighbors. Apply Section4 in the color of the pair.
A triangle in that color joins the pair to give a monochromatic5-clique.
An independent5 is a monochromatic5-clique in the other color. The remaining
possibility is an induced C5. Its complement is also aC5, so this is an induced
pentagon in the original uncolored graph regardless of the chosen color.
The theorem follows.

At n=42 and43 the respective positive gaps after multiplying the comparison
by 8 are n(n-1)(n-41)=1,722 and 3,612. No rounded or floating-point value is used.

## Scope and trust

The entire induced-C5-free branch is excluded at order 43 (indeed42).
No excluded product core, induced-neighborhood catalog, global degree profile,
or graph automorphism is forced by this statement. It supplies no Ramsey43
construction, no unrestricted branch count change and no bound improvement
for R(5,5).

The former sufficient order 22 (4,5) SAT attempt remains UNKNOWN; this proof
neither reruns nor certifies that instance and does not establish that
stronger intermediate premise. It reaches the global family by an edge-common
neighborhood lemma and a global counting identity instead.

The proof is an ordinary finite mathematical argument, not a formalization
or an external peer review. Python exact checks support the cycle lemma,
the sharpC9 witness, the incidence and triangle identities, and the concrete
extractor. The five-vertex verifier needs only the input graph and the final
five labels, and does not trust the source of those labels or any classification.
