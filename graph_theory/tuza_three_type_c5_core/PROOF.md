# Five-cycle cores for three-neighborhood split graphs

## Claims and scope

Let `G` be a finite simple split graph with a specified partition `C ∪ I`,
where `C` is a clique of order `k` and `I` is independent. Suppose the
neighborhoods in `C` of vertices of `I` take at most three values
`S_1,S_2,S_3`, with nonnegative integer multiplicities `m_1,m_2,m_3`.
Absent or equal types, empty neighborhoods, and arbitrary multiplicities
are allowed. Write `tau(G)` for the minimum number of edges meeting every
triangle.

Independent-side vertices of degree at most one lie in no triangle and
may first be removed, then restored with all their spokes. Thus the
three-type hypothesis need only count triangle-active neighborhoods.

**Theorem 1 (computer-assisted normal form).** Some minimum triangle edge
cover of `G` has a surviving clique core admitting a graph homomorphism
to the cycle `C_5`.

Thus the surviving edges inside `C` can be placed between consecutive
classes of a cyclic five-part partition. Consecutive classes need not be
joined completely. The assertion concerns the clique core; it imposes no
homomorphism requirement on the entire surviving graph.

**Theorem 2 (exact formula).** The formula (4) below computes `tau(G)` and
a compact optimal-cover certificate using `O(k^7)` arithmetic operations,
uniformly in the three multiplicities. It uses 392 fixed templates on nine
vertices, and 18 fixed linear feasibility inequalities.

The reduction works for all orders, not just the orders in the regression
audit. The finite computer-assisted ingredient is Lemma 2: a complete
enumeration of the `2^20` optional-edge subsets of a fixed nine-vertex host.
The rest of the proof is given below. No floating-point calculation,
optimization solver, or imported dataset is used. The implementation and
the unformalized combinatorial argument remain trust boundaries.

These results do **not** establish `tau(G) <= 2 nu(G)` for all three-type
split graphs. They describe and compute the covering side of that problem.

## 1. Protected independent sets

For a fixed surviving triangle-free graph `F` on `C`, the spokes retained
at a center of type `i` must form an independent set of `F[S_i]`.
Conversely that condition suffices: a triangle contains either zero or
one independent-side vertex. All centers of one type may therefore retain
the same maximum independent set `A_i ⊆ S_i`. This is the standard exact
cover reduction, recorded in the prior sources.

For specified `A_1,A_2,A_3`, define the allowed clique-core host

    H(A) = K_C minus the union of E(K_{A_1}), E(K_{A_2}), E(K_{A_3}).

Let `a_B` count vertices whose membership pattern in these three protected
sets is `B ⊆ {1,2,3}`, and put `d=a_empty`. Two vertices of nonempty
patterns `B,D` are adjacent in the host exactly when `B ∩ D` is empty.
Vertices of pattern empty form a clique and are adjacent to every other
vertex.

## 2. Symmetrization to nine vertices

**Lemma 1.** A maximum triangle-free subgraph of `H(A)` can be chosen to
be a blow-up of a triangle-free nine-vertex template. Its seven protected
classes have weights `a_B` for nonempty `B`. Its two free classes have
weights `x,d-x` for an integer `0 <= x <= d`, with an edge between the two
free template vertices. Protected template vertices may be joined only
when their masks are disjoint.

**Proof.** Start from a maximum triangle-free subgraph. In each nonempty
pattern class, choose a vertex of largest full degree and replace the
neighborhood of every other vertex of that class by its neighborhood.
There are no allowed edges inside the class. The replacement respects
the host, preserves triangle-freeness, and does not decrease the number
of edges. Previously made classes of twins remain classes of twins:
adjacency to any such class is all or nothing. After seven such steps
all nonempty pattern classes are uniform independent classes.

It remains to treat the free set `D`. If it is empty, use two zero-weight
free classes. Otherwise choose a vertex `v` of maximum full degree among
`D`. Replace every vertex in `D \ (N_D(v) ∪ {v})` by a nonadjacent twin of
`v`. The neighborhood of `v` is independent. During these replacements
its degree is unchanged, while a vertex still to be replaced can only
lose neighbors among earlier replaced vertices. Each replacement is
therefore nondecreasing in edge count. It also preserves the already
uniform protected classes.

Now `D` consists of two independent classes: the copies of `v`, and
`N_D(v)`. They are completely joined, since the original `N_D(v)` is
independent and each copy of `v` has precisely those neighbors in `D`.
If the second class is nonempty, choose in it a vertex of largest full
degree and clone it throughout that class. These vertices have equal
internal degrees and no edges to one another, so this again cannot lose
edges. Both free classes are now uniform. When a class is empty its
template vertex can still be included, with the distinguished free edge.
All nonempty classes induce exactly a blow-up of the asserted template.
Maximality of the original edge count makes each nondecreasing operation
optimal. QED.

Number the protected template vertices by masks `1,...,7`, and label the
free vertices `u,v`. There are exactly six allowed edges among protected
vertices:

    (1,2), (1,4), (1,6), (2,4), (2,5), (3,4).

The template host also has all fourteen protected-to-free edges, and
`uv`. A triangle-free template containing `uv` gives each protected
vertex at most one free neighbor. It can be extended, by adding allowed
edges while possible, to an inclusion-maximal triangle-free template.
All class weights are nonnegative, so this extension cannot decrease its
weighted edge count. The argument also covers zero-weight classes.

**Lemma 2 (exact finite certificate).** There are 392 inclusion-maximal
triangle-free subgraphs of this labeled host that contain `uv`. Every one
admits a homomorphism to `C_5`.

The certificate [templates.json](templates.json) supplies the graph and a
nine-entry coloring in `0,...,4` for each template. Every edge has color
difference `1` or `4` modulo 5. The standalone verifier
[verify_templates.py](verify_templates.py) checks every one of the `2^20`
choices for the other edges. It finds 66,666 triangle-free choices and
exactly the 392 listed maximal choices, and checks their colorings without
searching for a homomorphism. The edge-count distribution is

| Edges | 8 | 9 | 10 | 11 | 12 | 13 |
| --- | --- | --- | --- | --- | --- | --- |
| Maximal templates | 4 | 12 | 96 | 172 | 96 | 12 |

The generator independently enumerates six protected-edge bits and seven
three-way attachment choices, and uses backtracking to find colorings.
No isomorphism quotient or symmetry reduction enters the finite proof.
The certificate's SHA-256 is

    820208149d71eedd53b73504a8d6707ec64526f236c798be536edae04ef7412a

Lemmas 1 and 2 show that a maximum triangle-free subgraph of every host
`H(A)` admits a homomorphism to `C_5`: use a template coloring on each
entire blow-up class. Applying this to an optimal selection of the
protected sets proves Theorem 1.

## 3. Exact weighted host formula

For a template `T`, let `E_T` be its protected edges and `L_T,R_T` its
protected neighbors of `u,v`. Set

    p_T(a) = sum_{B in L_T} a_B,
    r_T(a) = sum_{B in R_T} a_B,
    e_T(a) = sum_{BD in E_T} a_B a_D.

The corresponding blow-up has exactly

    e_T(a) + d r_T(a) + x(d+p_T(a)-r_T(a)) - x^2             (1)

edges. Over integral `0 <= x <= d` its maximum is attained at

    x_T = min(d, max(0, floor((d+p_T(a)-r_T(a))/2))).        (2)

When the unconstrained vertex is a half-integer the two adjacent integers
tie, so the floor is sufficient. Let `f(a)` be the maximum of (1), using
(2), over the 392 templates. Lemma 1 and maximal extension show that `f(a)`
is the exact maximum number of triangle-free edges in `H(A)`. Every
candidate is itself an allowed triangle-free blow-up, giving the reverse
inequality as well.

## 4. Which retained counts are feasible?

Let `c_M` be the eight original clique-cell counts, defined using the
neighborhoods `S_i`. A vertex in original cell `M` may receive a retained
pattern `B` exactly when `B ⊆ M`. Thus `a` is feasible precisely when
there is a nonnegative integer table `z_{M,B}`, supported on `B ⊆ M`,
with row sums `c_M` and column sums `a_B`.

**Lemma 3.** For nonnegative integer vectors with `sum a_B = sum c_M = k`,
such a table exists if and only if

    sum_{B in U} a_B <= sum_{M in U} c_M                    (3)

for every upper set `U` of the Boolean lattice of subsets of `{1,2,3}`.
There are 18 inequalities after removing the empty and full upper sets.

**Proof.** Necessity holds since any original pattern containing a member
of an upper set is itself in that upper set. For sufficiency make a
bipartite graph with `a_B` retained vertices of each pattern and `c_M`
original vertices of each pattern, joining comparable pairs `B ⊆ M`.
For any subset of retained vertices, let `U` be the upward closure of its
patterns. Its size is at most `sum_{B in U} a_B`, while its neighborhood
has size exactly `sum_{M in U} c_M`. Condition (3) gives Hall's condition.
A perfect matching supplies the integral table. QED.

The reference algorithm constructs the table by an integral augmenting
path algorithm on a constant-size capacitated bipartite network; it never
expands the independent-side multiplicities.

## 5. The cover formula and complexity

Put `q=binomial(k,2)`, `E=sum_i m_i |S_i|`, and
`mu_B=sum_{i in B} m_i`. The exact answer is

    tau(G) = q + E - max_{a feasible} [f(a) + sum_B mu_B a_B].  (4)

Indeed `sum_B mu_B a_B` counts all retained spokes when each center of
type `i` keeps `A_i`, and `f(a)` is the largest compatible triangle-free
clique core. Conversely every maximum triangle-free subgraph can first
make the retained set common within each center type, as in Section 1.
Its resulting count vector is feasible and its clique core has at most
`f(a)` edges. Both inequalities in (4) follow.

There are `binomial(k+7,7)` candidate vectors `a`. Testing 18 inequalities
and evaluating 392 constant-size quadratic expressions costs a constant
number of arithmetic operations per vector. The formula therefore takes
`O(k^7)` arithmetic operations. Integers have bit length bounded by the
input multiplicity bit lengths plus `O(log(k+1))`; this is also a
polynomial bit algorithm. A chosen table, template, and free split give a
compact description of an optimal cover. Printing every deleted spoke
individually would of course take its output size. This proves Theorem 2.

## 6. Why the five-cycle conclusion is substantive

The prior two-type normal-form result has a bipartite clique core. Its
three-type obstruction already shows that this stronger conclusion fails.
Here is that prior family, included to delimit the present theorem.

Take `C={v,c,d} ∪ P ∪ Q`, with `|P|=|Q|=t>=2`, and neighborhoods
`P∪{d}`, `P∪Q`, `Q∪{c}`, each of multiplicity greater than `q`.
An optimal cover cannot leave any edge within a neighborhood: such an
edge forces at least one deletion at each of its more than `q` centers,
whereas deleting all clique edges costs `q`. All spokes may be retained.
The allowed core consists of the star from `v`, the `t` edges `P-c`, the
edge `c-d`, and the `t` edges `d-Q`.

If neither `vc` nor `vd` is retained, all other edges give a five-cycle
blow-up with `4t+1` edges. If exactly one is retained, the corresponding
`t` vertex pairs contribute at most `t`, giving at most `3t+2` edges in
total. If both are retained, `cd` is excluded and the total is at most
`2t+2`. Hence the maximum is `4t+1`. A cut of the allowed host has at most
`4t`, `3t+2`, or `2t+2` edges, according as `c,d` lie with `v`, on opposite
sides, or both opposite `v`. Its maximum is `4t`. Every optimal clique
core is consequently nonbipartite.

The new theorem supplies a universal five-cycle normal form beyond this
known bipartite obstruction. The obstruction itself is prior work, and
neither generic tractability for a fixed number of vertex types nor the
standard cover reduction is claimed as new. See [SOURCES.md](SOURCES.md).

## 7. Verification boundaries

The exhaustive nine-vertex check establishes Lemma 2. The independent
literal-core audit checks 1,287 protected hosts through order five and
8,937 cover instances on 331 shapes, using all multiplicities in
`{0,1,2}^3`. It also reconstructs four complete cover witnesses, including
the order-seven nonbipartite example, and rejects four altered witnesses.
These small-graph checks test the reductions; they do not replace their
all-order proofs. All checks use exact Python integers and explicit
exceptions, so optimization mode does not disable verification. There
has not yet been an independent mathematical review of this contribution.
