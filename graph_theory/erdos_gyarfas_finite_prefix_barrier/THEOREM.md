# Eulerian triangle expansions form a finite-prefix barrier

## 1. Construction

Let `K` be a finite connected simple 4-regular graph.  Orient its edges so
that every vertex has indegree and outdegree two and the resulting digraph is
strongly connected.  Such an orientation is obtained by orienting the edges
along an Euler circuit.

Construct `X=X(K)` as follows.  Its vertex classes are

```text
B = V(K),                    A = {a_e : e in E(K)}.
```

For every edge `e=uv` of `K`, join `a_e` to `u` and `v`.  At each `v in B`,
let `e,f` be the two edges oriented into `v` and add the edge `a_e a_f`.
Call these last edges **transition edges**.

Equivalently, the vertices associated with `v` and its two incoming edges
form a triangle.  Every original edge of `K` becomes one cross-edge between
the triangle at its tail and the triangle at its head.

## 2. Exact equality structure

Write `n=|V(K)|`.  Since `K` is 4-regular, `|E(K)|=2n`.  Hence

```text
|A|=2n,       |B|=n,       |V(X)|=3n.
```

Every `a_e` has its two endpoint neighbors and one transition mate, so it
has degree three.  Every `v in B` has degree four.  The set `B` is
independent, while the transition edges form a perfect matching on `A`.

If `a_e a_f` is the transition at `v`, then `v` is their common neighbor.
It is their unique common neighbor: another common neighbor would be the
other endpoint of both `e` and `f`, giving parallel edges in `K`.  Thus

```text
|A| = 2|B|,
```

and `X` has exactly the local equality structure in the accepted
two-thirds theorem for minimal Erdős--Gyárfás counterexamples of girth three.

## 3. Degree-criticality

**Lemma 1.** Every proper subgraph of `X` has a vertex of degree at most two.

**Proof.** Suppose a nonempty subgraph `Y` has minimum degree at least three,
and put `S=B intersect V(Y)`.  The `A`-induced graph is a matching, so `S` is
nonempty.

Every `A`-vertex has degree exactly three in `X`.  If it belongs to `Y`, all
three of its incident edges and neighbors therefore belong to `Y`.

Fix `v in S`.  Its four incident `A`-vertices correspond to the two incoming
and two outgoing edges of the oriented `K`.  The two incoming `A`-vertices
are transition mates, so either both occur in `Y` or neither does.  Since
`v` has degree at least three in `Y`, both incoming vertices and at least one
outgoing vertex occur.  In particular, the tails of both arcs entering `v`
belong to `S`.

Thus `S` is closed under all in-neighbors.  Strong connectivity makes every
nonempty in-neighbor-closed set equal to `V(K)`, so `S=B`.  Applying the same
argument at every `v` shows that every incoming edge-vertex belongs to `Y`.
Every edge of `K` is incoming somewhere, hence `A subseteq V(Y)`.  Each
`A`-vertex then forces all of its incident edges, so `Y=X`.  Therefore no
proper subgraph has minimum degree three. `square`

This is the exact hereditary property used for a lexicographically minimal
counterexample: any proper subgraph that retained minimum degree three would
inherit all forbidden-cycle conditions.

## 4. Cycle projection

Let `h` be the girth of `K`.

**Lemma 2.** Every cycle of `X` other than its displayed triangles has length
at least `3h/2`.  Equivalently, `X` has no cycle of integer length `ell` with

```text
4 <= ell < 3h/2.                                      (1)
```

**Proof.** Contract each displayed triangle to its corresponding vertex of
`K`.  A simple cycle `C` of `X`, unless it is one displayed triangle,
projects through its cross-edges to a nonempty closed trail `W` in `K`.
No edge repeats, because each cross-edge of `X` represents one edge of `K`
and `C` is simple.  In particular, `W` contains a simple cycle, so if `r` is
the number of cross-edges used by `C`, then

```text
h <= r.                                                (2)
```

Traverse `W` cyclically and mark an edge `+` when it is followed in its
chosen orientation and `-` otherwise.  Between consecutive cross-edges,
`C` travels inside the corresponding triangle.  This internal segment has
length zero only at a `-` to `+` transition, when both cross-edges meet the
original `B`-vertex.  Every other transition requires at least one triangle
edge.

In a cyclic sign word of length `r`, the number of `-` to `+` transitions is
at most `r/2`.  Therefore the total number of internal triangle edges on `C`
is at least `r/2`.  Writing `ell=|C|` gives

```text
ell >= r+r/2 = 3r/2 >= 3h/2,
```

which proves (1). `square`

The argument permits repeated vertices in the projected trail and chords in
`C`; neither inducedness nor a simple projected cycle is assumed.

## 5. Finite-prefix theorem

**Theorem.** For every integer `R>=2`, there is a finite simple graph `X_R`
such that

1. `delta(X_R)=3` and every proper subgraph has minimum degree at most two;
2. two thirds of its vertices have degree three and one third have degree
   four;
3. the degree-four vertices are independent;
4. the degree-three vertices induce a perfect matching, every edge of which
   has a unique common degree-four neighbor; and
5. `X_R` has no cycle of any length from `4` through `2^R`.

**Proof.** Put

```text
H_R = floor(2^(R+1)/3)+1.
```

By the classical existence theorem for regular graphs of prescribed girth,
choose a finite connected simple 4-regular graph `K_R` of girth at least
`H_R`.  Give it the Eulerian orientation above and form `X_R`.
Sections 2--3 prove assertions 1--4.  If `4<=ell<=2^R`, then

```text
ell <= 2^R < 3H_R/2 <= 3 girth(K_R)/2.
```

Lemma 2 excludes an `ell`-cycle, proving assertion 5. `square`

## 6. Consequence and limitation

Every `X_R` has triangles, so its girth is three.  It saturates the known
two-thirds cubic-density inequality and all equality conditions listed
above, while avoiding any prescribed finite initial segment of the
power-of-two cycle lengths.

This does not disprove the Erdős--Gyárfás conjecture.  The construction may,
and generally will, contain a power-of-two cycle longer than `2^R`.
Instead it proves a method barrier: a strict improvement of the two-thirds
bound cannot follow from the known degree-critical equality structure plus
only finitely many of the forbidden cycle lengths.  It must use the
unbounded family of power-of-two exclusions or some additional global
property of an actual counterexample.
