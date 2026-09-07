# Complete planar transfer gate for generalized Mycielski constructions

**Theorem.** Let G be a finite simple graph and r >= 1 an integer. Its
generalized Mycielskian M_r(G), defined below, admits a map into the Euclidean
plane taking every edge to distance one **if and only if G is bipartite**.
The map may identify any nonadjacent vertices. No coordinate field, symmetry,
injectivity, or condition on nonedges is assumed.

Thus no ordinary Mycielskian of a four-chromatic graph can yield a
five-chromatic planar unit-distance graph, even by identifying vertices.
The obstruction applies to every number of layers and every order. This is a
complete construction-mechanism decision, not a record improvement.

## Construction and conventions

M_r(G) has vertices v^j for v in V(G), 0 <= j < r, and an apex a.
The edges are:

- u^0 v^0 for uv in E(G);
- u^j v^(j+1) and v^j u^(j+1), for uv in E(G) and 0 <= j < r-1;
- a v^(r-1) for every v in V(G).

There are no other required edges. In particular r=1 is the cone, and r=2
is the ordinary Mycielski construction. For n base vertices and m base edges,
the lift has rn+1 vertices and (2r-1)m+n edges. We include an apex also for
an empty base; the theorem is immediate in that case.

The ordinary construction raises chromatic number by one. This fact explains
its relevance to the Hadwiger–Nelson record problem; it is not needed to prove
the geometric theorem. No such chromatic-increment assertion for arbitrary
bases and arbitrary generalized heights is assumed here.

## A geometric square-chain obstruction

Use the free abelian group of oriented edges of a graph, with [vu]=-[uv].
For a closed walk W write [W] for the sum of its traversed oriented edges.

**Lemma.** Suppose a graph has an odd closed walk W and an integer identity

    q[W] = sum_t c_t[Q_t],     q != 0,

where every Q_t is a closed walk of length four and every c_t is an integer.
Then the graph has no planar unit-edge map, even a noninjective one.

Here is a proof that includes all possible vertex coincidences. Suppose such
a map exists. Among its finitely many edge directions choose one representative
of each pair {d,-d} of unit vectors. Send a directed edge with displacement
d to +e_d, and one with displacement -d to -e_d, in the **free abelian group**
on these representatives. Denote the resulting additive map on edge chains
by L. This is a group of formal symbols, not the additive group of coordinate
vectors: an equilateral triangle's three directions do not cancel formally.

For four consecutive mapped points A,B,C,D of a unit closed walk:

- If A=C, its first two and last two edge displacements cancel in pairs.
- If B=D, its second and third, then fourth and first, cancel in pairs.
- Otherwise B,D are the two distinct intersections of the unit circles about
  the distinct points A,C. Reflection across the midpoint of AC interchanges
  them. Consequently A+C=B+D, and opposite edge displacements cancel.

These cases exhaust the possibilities; adjacent points cannot coincide.
Therefore L([Q_t])=0, including every degenerate quadrilateral. The identity
gives qL([W])=0. The formal group is torsion-free, so L([W])=0. But the
homomorphism sending each formal basis element to 1 in Z/2 sends L([W]) to
the odd length of W, a contradiction. This proves the lemma.

An equivalent scalar proof chooses a linear functional nonzero on every mapped
edge displacement and assigns each oriented edge +1 or -1 according to its
sign. Opposite displacements cancel on each of the same three quadrilateral
cases. The signed sum on an odd walk is an odd integer, so no nonzero multiple
of it can equal a sum of zero square circulations.

The lemma is specific to the Euclidean plane. Four unit edges in three
dimensions need not have opposite displacements in pairs.

## The identity for every layer count

If G is not bipartite, choose a simple odd cycle v_0,...,v_(k-1), with indices
modulo k. Only its lifted vertices and the apex will be used. Let

    A = sum_i [v_i^0, v_(i+1)^0],
    T_j = sum_i ([v_i^j, v_(i+1)^(j+1)]
                 - [v_i^j, v_(i-1)^(j+1)]).

For r >= 2 the following oriented squares are all present:

    B_i = (v_i^0, v_(i+1)^0, v_(i+2)^0, v_(i+1)^1),
    D_(i,j) = (v_i^(j-1), v_(i+1)^j, v_i^(j+1), v_(i-1)^j),
                                                    1 <= j <= r-2,
    E_i = (a, v_i^(r-1), v_(i+1)^(r-2), v_(i+2)^(r-1)).

Expanding the four oriented edges in each square and reindexing the sums gives

    sum_i [B_i]     = 2A - T_0,
    sum_i [D_(i,j)] = T_(j-1) - T_j,
    sum_i [E_i]     = T_(r-2).

Adding these equations telescopes to **2A**, using exactly rk square terms.
The middle sum is empty when r=2. If r=1, use instead the k squares
(a,v_i^0,v_(i+1)^0,v_(i+2)^0); their sum is directly 2A.
All four labels in each specified square are distinct even when k=3.
The geometric lemma applied to the odd base cycle proves necessity.

For sufficiency, a bipartition gives a homomorphism G -> K2. Sending v^j to
(colour(v))^j and the apex to the apex gives M_r(G) -> M_r(K2). The latter
is the cycle C_(2r+1): every vertex has degree two, and following the alternating
layer paths from the apex, across the base edge, and back reaches all vertices.
Embed this cycle as the regular (2r+1)-gon of circumradius

    R = 1 / (2 sin(pi/(2r+1))).

The chord formula gives unit length on every edge. Composition is the required
plane map. Isolated base vertices cause no difficulty. This proves both
directions for every finite G and r, rather than only for enumerated examples.

## Consequence for a standard topological bound

For every finite plane unit-distance graph H with an edge,

    coind(B(H)) + 2 <= 3,

using the box-complex convention of Simons, Tardif and Wehlau.
Their [Corollary 3](https://arxiv.org/pdf/1601.04642) characterizes this bound
by homomorphisms from iterated generalized Mycielski graphs. Their class K3
consists of odd cycles, so every member of K4 is excluded by the theorem above.
Every higher class contains a K4-class member as a subgraph. Thus none can map
to H. This corollary uses that published characterization as an external
theorem; our elementary transfer proof does not depend on it.

The corollary limits this particular topological lower bound. It does not
bound the actual chromatic number of H by three. In particular it is entirely
consistent with the known four- and five-chromatic plane unit-distance graphs.
The bound is sharp, since an equilateral triangle belongs to their class K3.

## Reproducible certificates

Python 3.11 or later, standard library only:

```bash
python3 -B verify.py --check-expected
python3 -B controls.py
python3 -O -B controls.py
sha256sum -c SHA256SUMS
```

[generate.py](generate.py) accepts a finite base graph in JSON with fields
`vertices` and `edges`. It returns either an explicit map to the regular
polygon above, or an integer square-chain certificate derived from a BFS odd
cycle. For example, with an external input and a new output filename:

```bash
python3 -B generate.py --base /scratch/base.json --layers 3 --out /scratch/transfer.json
python3 -B verify.py --certificate /scratch/transfer.json
```

Omit `--base` to regenerate the six committed fixtures. Output files must not
already exist. Vertices of an n-vertex base lift are labelled j*n+v and the
apex r*n. The generator canonicalizes input edges. The checker requires exact,
canonical graph data and rejects malformed certificates.

[verify.py](verify.py) imports no producer code. It reconstructs the lift by
testing the definition on every unordered label pair; the producer inserts
edges layer by layer. For obstructions it accumulates signed integer edge
incidences of the supplied walks and checks the identity exactly. In fact its
`check_square_certificate` function works on **any graph**, with any nonzero
integer multiplier and signed square coefficients. It checks a sufficient
obstruction and does not search for all possible certificates. A missing
certificate is not evidence that a graph has a planar unit-edge map.

Positive certificates supply polygon indices, and the checker tests every
edge modulo the polygon order. The analytic chord formula supplies their
geometry. The six fixtures comprise four obstructions, a positive lift of
K_(3,3), and the empty-base boundary. [expected.json](expected.json) pins their
reports and the compact [certificate.json](certificate.json) hash.

[controls.py](controls.py) exhausts all 1,100 labelled simple base graphs on
zero through five vertices, each at heights one through four: 4,400 lift cases.
It independently decides bipartiteness by exhausting binary words. Four further
odd-cycle fixtures test lift orders 508,508,507,508. Exact rational controls
cover unit parallelograms and both collapsed-diagonal cases; a regular tetrahedron
checks the failure of formal cancellation in dimension three. Signed and
relabelled certificates and 17 malformed inputs are tested. Normal and optimized
runs agree. Counts and timings are in [controls_expected.json](controls_expected.json)
and [validation.json](validation.json).

The infinite theorem rests on the written geometric argument and telescoping
identity. The finite runs audit the implementation and its boundary cases.
No SAT result, floating-point computation, external graph dataset, or assumed
vertex distinctness is a proof premise. This is author-run independent checking,
not an independent-author review or proof-assistant formalization.

## Prior work and scope

The construction and signature methods are established prior art.
[Simons–Tardif–Wehlau (2016)](https://arxiv.org/abs/1601.04642) study generalized
Mycielski homomorphisms and abelian signatures modulo four-cycle relations.
Our integer edge-chain language is closely related; we do not claim to invent
four-cycle signatures. [Chung–Krebs (2026)](https://arxiv.org/html/2605.27778v1)
classify **injective** unit-distance embeddings of ordinary Mycielskians of
cycles: precisely C10 has a planar one. Their VecNeg obstruction tracks
individual opposite edges of nondegenerate rhombi. Here formal sums cancel
also through either collapsed diagonal, which is essential for unrestricted
vertex identifications. The theorem does not conflict with their even-cycle
classification: every even-cycle base here has a possibly noninjective map
to a pentagon when r=2. No priority claim is made for this transfer theorem.

The [Parts paper](https://arxiv.org/abs/2010.12665) and
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4) support the
509-vertex comparison, checked 2026-09-07. No <=508 five-chromatic planar graph
was constructed in this work.

The theorem excludes complete generalized Mycielski lifts of nonbipartite
bases, every graph containing one, and every possible unit-edge realization
after vertex identification. It does not classify deletions that remove the
certificate, gadget substitutions for selected edges, or arbitrary different
assemblies. No four-colourability assertion about their quotients is used.
The previously completed G372 repair, E477 spindle, EI17 assembly, and mixed
direction-support programs remain retired. New Heule-catalogue and E477-review
contributions were read for coordination; none is a mathematical premise here.

This complete transfer gate is preserved and retired. No height ladder,
larger Mycielski instance, or deletion-repair phase follows it.
