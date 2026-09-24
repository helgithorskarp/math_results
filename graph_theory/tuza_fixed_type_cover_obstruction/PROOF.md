# Exact split completion and a fixed-type obstruction

All graphs are finite, simple and undirected. Triangle packings are
edge-disjoint, and triangle covers are sets of **edges** meeting every
triangle. Write `tau` for the cover number and `nu*` for the fractional
packing optimum with unit capacity on each graph edge. In a specified
split partition `C disjoint-union I`, centered triangles contain a vertex
of `I`; their fractional optimum is `nu_c*`.

## 1. Balanced independent blow-ups

For an arbitrary graph `F` and a positive integer `p`, let `F[p]` replace
each vertex `v` by an independent group `V_v` of size `p`, and replace
each edge `uv` by all edges between `V_u` and `V_v`.

**Blow-up cover identity.** `tau(F[p])=p^2 tau(F)`.

For the upper bound, lift each edge of a minimum cover of `F` to all its
`p^2` copies. A triangle in `F[p]` uses three different groups and
projects to a triangle in `F`, so the lifted edges cover every triangle.

For the lower bound, let `A` cover `F[p]` and choose one vertex uniformly
and independently from each group. The induced graph is a copy of `F`,
and the restriction of `A` to this copy is a cover. Its size is therefore
at least `tau(F)`. Each edge of `A` is selected with probability `1/p^2`.
Taking expectations gives `|A|/p^2>=tau(F)`. Equivalently, one can sum the
cover inequalities over all `p^{|V(F)|}` transversals: each blow-up edge
appears in exactly `p^{|V(F)|-2}` copies. This is exact finite averaging.

The fractional packing identity is also exact:
`nu*(F[p])=p^2 nu*(F)`. For the upper bound, aggregate the weights of all
triangles having the same three parent vertices and divide by `p^2`.
An original edge has `p^2` copies, so the aggregate satisfies unit edge
capacities in `F`.

For an explicit lower lift, order each original triangle as `(a,b,c)`.
For every `x,y` in `Z/pZ`, use the triangle

```text
((a,x), (b,y), (c,x+y)).
```

These `p^2` triangles partition the edges of its complete tripartite
blow-up: any two coordinates determine the third. Give each lifted
triangle the weight of its original triangle. Thus each clone edge gets
exactly the original edge's load. This argument uses a Latin square over
the cyclic group, so primality of `p` is unnecessary. The same projection
and lift prove `nu_c*(F[p])=p^2 nu_c*(F)` whenever a split partition of
`F` is specified and only triangles containing a clone of its independent
set are considered. Here `F[p]` itself need not be a split graph.

## 2. Completion that preserves the split condition

Let `F` be a split graph with a specified clique `C` of size `s`. Starting
with `F[p]`, for every original clique vertex `v`:

1. Complete its group `V_v` to a clique.
2. Add `p-1` new independent vertices, each adjacent exactly to `V_v`.

All old and new independent vertices are mutually nonadjacent. Call the
result `J_p(F)` and put `L=s*binom(p,2)`, the number of added internal
clique edges. Its clique has order `sp`. For every `p>=2`,

```text
tau(J_p(F))   = p^2 tau(F)   + L,
nu_c*(J_p(F)) = p^2 nu_c*(F) + L,
nu*(J_p(F))   = p^2 nu*(F)   + L.                 (1)
```

**Cover identity.** The graph edges partition into the old blow-up edges
and `s` internal subgraphs. Each internal subgraph consists of a `K_p`
and `p-1` independent vertices adjacent to all its clique vertices.
Its centered fractional packing has value `binom(p,2)`: for each base
edge and each new center, give their triangle weight `1/(p-1)`. Every
base edge and every spoke then has load exactly one. Hence its integral
cover needs at least `binom(p,2)` edges; deleting its clique realizes
this number.

A cover of `J_p(F)` restricts to covers of these edge-disjoint subgraphs
and of `F[p]`. Section 1 gives the lower bound `p^2 tau(F)+L`. For the
matching upper bound, lift a minimum cover of `F` and delete every
internal clique edge. The old remaining graph is a triangle-free
blow-up, and every triangle involving a new center contains a deleted
internal edge. Triangles using two vertices of one core group also
contain a deleted internal edge. This proves the first identity in (1).

**Fractional identities.** In any fractional packing, partition the
triangles into those containing an internal clique edge and those
containing none. The former have total mass at most `L`, by summing
the capacities of internal clique edges. This remains an upper bound
when a triangle contains more than one internal edge. A triangle in
the second class contains no new center and projects to a triangle of
`F`. Aggregation as in Section 1 bounds its mass by `p^2 nu*(F)`, or
by `p^2 nu_c*(F)` in the centered problem.

For the matching lower bounds, lift an optimum fractional seed packing
using the Latin-square construction. Its support uses only old blow-up
edges. Independently add the internal centered packings just described;
their edges are disjoint from the old blow-up edges. This proves both
remaining identities in (1).

If `F` has `r` active neighborhood types of sizes at least two, then
`J_p(F)` has exactly `r+s` types: the old neighborhoods are unions of
at least two core groups, and the new ones are the distinct single
groups. An old multiplicity `m_i` becomes `p m_i`; each new type has
multiplicity `p-1`. Thus the caps `m_i<=|S_i|-1`, if present in `F`,
are preserved. Also

```text
D(J_p(F)) = p(D(F)+s),
|V(J_p(F))| = (2s+|I(F)|)p-s.
```

The elementary blow-up averaging, Latin squares, and complete-split
fractional packings are standard tools. Formula (1) is recorded here as
the transfer mechanism for the following fixed-type counterexample.

## 3. The seed and a full fractional certificate

Take a four-vertex clique `0123` and five independent vertices `a,b,c,d,e`
with neighborhoods `012,013,03,123,23`, respectively. This is the seed
from the earlier reviewed obstruction. Its short certificate is repeated
so that the present proof is self-contained.

There are eleven centered triangles. Giving every one weight `1/2`
is feasible because no edge is in more than two centered triangles.
Thus `nu_c*>=11/2`.

The following edge weights cover **all** seed triangles fractionally:

```text
Base edges:  01=1/2, 02=0, 03=1, 12=1/2, 13=1/2, 23=1.
Spokes:      a0=a2=b1=d1=1/2; every other spoke has weight zero.
```

Each centered triangle has total weight one. Clique triangle `012`
has weight one, and each other clique triangle has weight two. The sum
of edge weights is `7/2+2=11/2`. Weak duality gives

```text
nu_c*(F)=nu*(F)=11/2.
```

Every integral cover has at least `ceil(11/2)=6` edges, and all six
clique edges are a cover, so `tau(F)=6`. The triangles

```text
a02, b01, c03, d12, e23
```

are edge-disjoint. Consequently `nu(F)=nu_c(F)=5`, since the full
fractional upper bound is `11/2`. This exact full fractional value is
also verified by the new checker.

## 4. Nine types at every scale

Apply Section 2 to this seed, with `s=4`. For every integer `p>=2`,
let `G_p=J_p(F)`. Equivalently, partition its clique into four groups
`X_0,X_1,X_2,X_3`, each of size `p`. Add five types of multiplicity `p`
with neighborhoods

```text
X_0 union X_1 union X_2,
X_0 union X_1 union X_3,
X_0 union X_3,
X_1 union X_2 union X_3,
X_2 union X_3.
```

For each `j=0,1,2,3`, add a type of multiplicity `p-1` and neighborhood
`X_j`. All nine types are different, and every multiplicity is capped.
There are `13p-4` vertices, `17p^2-4p` spokes, and `25p^2-6p` total edges.
The clique order is `k=4p` and `D=17p`.

The completion identities give exact values

```text
tau(G_p) = 6p^2+4*binom(p,2) = 8p^2-2p = q,
nu_c*(G_p)=nu*(G_p) = (11/2)p^2+4*binom(p,2)
                         = (15/2)p^2-2p,
q = binom(k,2).
```

The full fractional equality also has an explicit dual: lift the seed
edge weights to every corresponding clone edge, give each internal
clique edge weight one, and give every new-center spoke weight zero.
A triangle with an internal edge is covered by that edge; any other
triangle projects to a seed triangle. The primal consists of the
Latin lifts of the eleven half-weight seed triangles and the four
internal centered packings from Section 2.

Lifting the five integral seed triangles gives an actual packing of
`5p^2` centered triangles. It follows directly that

```text
tau(G_p)=8p^2-2p < 10p^2 <= 2nu(G_p).
```

No exact integer packing optimum for `G_p` is asserted.

## 5. Failure of every subquadratic fixed-type repair

Define

```text
Phi_k(H)=k^2/4-k/2+H-H^2/k^2+1/4.
```

For `q=k(k-1)/2` and `delta=q-H`, expansion gives

```text
q-Phi_k(H)=delta/k+delta^2/k^2.
```

In `G_p`, `delta=p^2/2`, so

```text
tau-Phi_k(H)=p/8+p^2/64=k/32+k^2/1024.             (2)
```

The error divided by `k^2` tends to `1/1024` while `r=9` remains fixed.
Therefore there is no function `g_9(k)=o(k^2)` for which
`tau<=Phi_k(H)+g_9(k)` holds for all nine-type split graphs. In particular,
no error of the form `cD`, `crk`, or `C(r)k` suffices. For example,
`tau>Phi+cD` whenever `p>1088c-8`, since `D=17p`.

At `p=5`, `k=20`, `H=355/2`, and `tau=190`, but
`Phi=12095/64` and `ceil(Phi)=189`. Equation (2) is increasing in `p`,
so the rounded-up estimate fails at every scale `p>=5`.

The spoke count satisfies `E/2-H=p^2`, so the prior theorem assuming
spoke saturation `H=E/2` is unaffected. This is a refutation of the
specific proposed cover bound, not of Tuza or of the possibility of
an effective theorem for a fixed number of neighborhood types.

There is a further relevant limitation: this family has `H/k^2` tending
to `15/32`, rather than lying in the smaller range near `1/4`. The known
centered rounding estimate `nu_c>=H-3D/2`, together with `tau<=q`, already
proves Tuza when `H>=q/2+3D/2`. Thus an eventual positive proof does not
need the proposed cover bound throughout the range refuted here. A
restricted estimate in the remaining range is still a live possibility.

## 6. Proof and computation boundaries

The universal statements follow from Sections 1--5, not from finite
sampling. The proof uses exact counting, weak duality, and explicit
fractional packings. It requires no design-existence theorem, solver,
regularity lemma, or uncomputed threshold.

The standard-library checker exhausts all `2^19` edge subsets of the
seed and finds its cover optimum and 20 optimal covers. It verifies
the seed's full fractional dual, expands every transversal at scales
two and three, and directly checks the graphs at scales
`2,3,5,11,16,31`. In each graph it checks the centered primal, every
actual triangle against the full dual, the actual integer packing,
all nine types and caps, and the edge partition underlying the cover
identity. Five malformed witnesses must fail. The larger-instance
cover lower bound uses the proved averaging identity, not a claim that
the program has enumerated all covers at those scales.

The trust boundary is the unformalized proof, the visible finite checker,
and Python's exact integer and rational arithmetic. Independent review
of this new fixed-type result is pending. The earlier seed and its
growing-type amplification were independently accepted at h5741.
