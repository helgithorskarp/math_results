# Charney–Davis at eighteen vertices

24 September 2026. A computer-assisted proof, pending independent mathematical
review. The theorem concerns finite **flag generalized homology spheres over
a field**: every face link, including the empty-face link, has the homology
of the appropriate sphere. Global homology alone is insufficient.

**Theorem.** If such a sphere Delta has dimension five and eighteen vertices,
then gamma_3(Delta) >= 0, where

    h_Delta(t) = sum_{i=0}^3 gamma_i t^i (1+t)^(6-2i).

Equivalently, f_2 - 6 f_1 + 332 >= 0. Here f_i counts i-dimensional faces.
This proves the eighteen-vertex case, not the unrestricted conjecture or a
classification of all eighteen-vertex spheres.

## 1. Published inputs and coefficient fields

We use the following results, with their indicated hypotheses.

1. [Davis–Okun, Theorem 11.2.1](https://arxiv.org/abs/math/0102104):
   gamma_2 >= 0 for a flag rational homology 3-sphere.
2. [Labbé–Nevo](https://arxiv.org/abs/1612.01169), Lemmas 2.1, 2.4, 3.2,
   and 3.4: links are induced flag spheres; a flag (d-1)-sphere has at
   least 2d vertices; a vertex with one nonneighbor gives a suspension;
   the induced complex on a vertex's nonneighbors is connected; and a
   vertex with two nonneighbors x,y satisfies

       gamma_Delta(t) = gamma_lk(v)(t) + t gamma_lk(xy)(t).

3. Labbé–Nevo, Theorem 3.5(i): if the **minimum** complement degree is
   pi>1 and a vertex attaining that minimum has suspension link Sigma Gamma,
   then Delta = Gamma * C_(pi+3). We never apply this to a vertex that does
   not attain the minimum.

The connectedness assertion in item 2 also follows directly from Alexander
duality: deleting the induced equator lk(v) leaves v as one component and
the induced antipode complex as the other, and the latter is acyclic.

The rational hypothesis in item 1 causes no loss. For every finite face
link separately, universal coefficients imply that vanishing lower
homology over the given field forces the lower integral free ranks to
vanish. Euler characteristic then forces top rational Betti number one.
Thus every face link is also a rational homology sphere. This does not
assert absence of integral torsion.

For a homology 4-sphere Y, the vertex-link identity gives

    2 gamma_2(Y) = sum_v gamma_2(lk_Y(v)).

Consequently its gamma_2 is nonnegative by item 1. In the convention
kappa(X)=F_X(-1/2), this says gamma_2(Y)=8 sum_v kappa(lk_Y(v)).
It does not have the inverse factor 1/8 found in an older graph review.

## 2. Complement identities and the first reduction

Let H be the complement of the one-skeleton. Write q_v=deg_H(v), m=e(H),
T for its number of triangles, t_v=e(H[N_H(v)]), a=gamma_2(Delta),
b=gamma_3(Delta), and L_v=gamma_2(lk_Delta(v)). Then

    a = 39-m,
    b = 230 + (1/2) sum_v q_v(q_v-11) - T,
    L_v = a+8 + q_v(q_v-19)/2 + sum_{u in N_H(v)} q_u - t_v,
    S := sum_v L_v = 3b+4a
                  = 846 + (1/2) sum_v q_v(3q_v-37) - 3T.       (1)

These follow by counting independent triples in H:

    f_2 = choose(18,3) - 16m + sum_v choose(q_v,2) - T,

and using gamma_2=f_1-9f_0+48 and gamma_3=f_2-6f_1+22f_0-64.
The link of v is induced on B=V(H) minus ({v} union N_H(v)); its complement
has m-sum_{u in N_H(v)}q_u+t_v edges. Substituting into
gamma_2(lk(v))=f_1(lk(v))-7 f_0(lk(v))+30 gives the individual formula.
Summing, or double-counting vertex/face incidences, gives S.

Every L_v is nonnegative. Also 1<=q_v<=7: degree zero would make Delta
a cone, and the vertex links have at least ten vertices. If min q_v=1,
Delta is a suspension and b=0. If min q_v=2, item 2 above gives
b=gamma_2(lk(xy))>=0. If every q_v>=4, then for 4<=q<=7,
q(3q-37)/2<=-50, so (1) gives S<=846-900<0.

Hence a negative example has min q_v=3 and all degrees in {3,4,5,6,7}.
Let n_j be the degree multiplicities. Formula (1) becomes

    S = 90 - 8 n_4 - 13 n_5 - 15 n_6 - 14 n_7 - 3T >= 0.    (2)

There are at least eight cubic vertices. Indeed, twelve noncubic vertices
already cost 96 in (2). Eleven would cost at least 88, but eleven quartics
and seven cubics have odd total degree. Correcting parity requires at least
one quintic or septic, increasing that cost by at least five, beyond 90.

This elementary reduction replaces the later, unreviewed ten- and
eleven-cubic exclusions. Those exclusions are not assumptions of this proof.

## 3. Two restrictions at cubic vertices

Assume b<0 from now on.

**(i)** A cubic vertex v has t_v<=1. Its three nonneighbors induce a
connected complex in Delta. A connected graph on three vertices has at
least two edges, so its complement H[N_H(v)] has at most one.

**(ii)** Two nonadjacent cubic vertices u,v in H have at most one common
H-neighbor. Otherwise u has complement degree at most one in lk_Delta(v).
Degree zero gives a cone link, impossible; degree one makes that link a
suspension. Since v attains the minimum complement degree three,
Labbé–Nevo then gives Delta=Gamma*C_6, with Gamma a flag homology 3-sphere.
Thus b=2 gamma_2(Gamma)>=0, contrary to the assumption.

In particular, the graph induced by cubic vertices contains no K_4.
It has an independent triple. To see this, take any eight cubic vertices;
their induced graph J has at most twelve edges. If alpha(J)<=2, its
complement is triangle-free and has at least sixteen edges. Mantel's
theorem and its equality case force that complement to be K_(4,4), so
J is two copies of K_4, a contradiction.

## 4. A facet reduces the search to twenty-five incidence types

Every independent set of H extends to a six-vertex facet of Delta. Choose
a facet A={a_0,...,a_5} containing as many cubic vertices as possible, and
let their number be k. The preceding independent triple shows 3<=k<=6.
Label the cubic members first.

For each i, the ridge A minus {a_i} lies in exactly two facets. Let b_i be
the other completion. Flagness and the absence of a seven-vertex face give

    N_H(b_i) intersect A = {a_i}.

These six vertices are distinct. Put B={b_0,...,b_5} and
R=V(H) minus (A union B), so |R|=6. Every r in R has at least two
H-neighbors in A: zero would extend A, and one would give a third
completion of one of its ridges. If i>=k, then b_i is noncubic, since
otherwise replacing a_i by b_i increases the cubic count of the facet.

Each cubic a_i has its matching neighbor b_i and exactly two neighbors
in R. Regard that pair as an edge of an auxiliary graph M on the six
vertices R. Distinct cubic a_i give distinct pairs by restriction (ii).
Thus M is simple and has k edges. Moreover:

- If k=5, M has no isolated vertex: a vertex of R can obtain at most one
  additional A-neighbor from the sole noncubic member of A.
- If k=6, M is 2-regular: every R-vertex has degree at least two in M,
  and the degree sum is twelve.

There are exactly the following types up to permuting R:

| k | labelled auxiliary graphs | isomorphism types |
|---|---:|---:|
| 3 | 455 | 5 |
| 4 | 1365 | 9 |
| 5, no isolated vertex | 1581 | 9 |
| 6, 2-regular | 70 | 2 |
| total | 3471 | 25 |

`cases.py` enumerates all 2^15 edge masks, applies exactly these filters,
and removes complete orbits under all 720 permutations. It imports no graph
catalogue or isomorphism library. The representatives and orbit sizes
are in `EXPECTED.json`. The k=6 types are C_6 and C_3 disjoint union C_3.

For a representative, reorder the cubic a_i and their paired b_i to match
its edge ordering. The remaining a_i may independently be ordered by their
degrees, carrying their b_i along. Thus requiring the degrees of A to be
nondecreasing loses no graph. No degree sorting of B or R is assumed.

## 5. The exact finite exclusion

For each of the twenty-five representatives, `encoding.py` asks whether
there is a simple graph H on A union B union R with all of the following:

1. The fixed facet/matching/incidence data above; exactly the first k
   vertices of A are cubic; and b_i is noncubic for i>=k.
2. Degrees 3 through 7, at least eight cubics, and nondecreasing degrees
   on A; every vertex in R has at least two neighbors in A.
3. b<=-1, all L_v>=0, and S>=0, evaluated by the exact identities (1).
4. Restrictions (i) and (ii) above.
5. No independent seven-set in H. Every independent five-set has exactly
   two vertices outside it adjacent to none of its members.

Each is a necessary condition, not a sufficient test for spherehood. In
particular, omitted purity and higher homology constraints enlarge the
search domain and cannot invalidate an exclusion.

**Finite certificate lemma.** None of these twenty-five systems is feasible.

`ENCODING.md` gives the Boolean translation and its existential auxiliary
variables. `prove.py` regenerates each formula, obtains an UNSAT trace from
Glucose, checks it with DRAT-trim, translates it to LRAT, and checks that
with the standalone `strict_rup.py` program. All twenty-five checks pass in the
recorded run. No learned experimental cuts or adaptive exclusions enter
the formulas. `EXPECTED.json` records the input and certificate hashes.
The bulk formulas and traces are generated locally, not distributed here.

A hypothetical negative sphere yields a graph in one of the twenty-five
systems by Sections 1–4, contradicting the finite certificate lemma.
Therefore b>=0. QED.

## Scope, validation, and provenance

This is a computer-assisted proof with an unformalized mathematical
reduction. The trusted boundary comprises the named published topology
inputs, the reduction and CNF generator, exact cardinality/PB encoders,
and a proof checker. Solver correctness is not needed once the generated
proof is successfully checked; checker success does not itself verify the
reduction. The strict RUP checker and the CNF generator have not been verified
in a proof assistant here. Algorithmic checking within this package is
not external peer review.

The definition-level audit checks the counting identities, primitive
encoders, and every face link of an explicit boundary sphere over F_2.
That sphere is the join of two copies of an octahedron after three stated
edge subdivisions. It has f=(18,123,406,693,588,196) and gamma=(1,6,9,0).
It satisfies the same local restrictions, and the encoding with the
opposite gamma sign admits it. The original negative encoding rejects it.
The construction itself gives a sphere over every field; the F_2 check
is additional finite validation.

The graph source was the accepted seventeen-vertex result and the
eighteen-vertex frontier developed in the
[nine-cubic note](../../charney_davis_18_nine_high_degree/PROOF.md) and
[eleven-cubic note](../../charney_davis_18_eleven_high_degree/PROOF.md).
The former's identities are rederived here; the latter motivated looking
for a global bridge. Neither its profile exclusions nor a classification
of small vertex links is used. The new mechanism is the maximal-cubic
facet decomposition and the complete finite exclusion.

Targeted searches of the committed graph and primary literature did not
locate the eighteen-vertex theorem. This is search-relative novelty,
not a claim of historical priority. The unrestricted conjecture remains
open, and independent review of this proof is requested.

Combining the new eighteen-vertex theorem with the independently accepted
seventeen-vertex graph result
`bafkreieceq3ktydrabvxlu6fqn7zllvmi6lk4346k4y35ylczmychowcha`
(review `bafkreih354oq4heszi25fpl6wpqcfaancznjsss2nd4eqwf6gsmg2bhw5i`)
and Labbé–Nevo's Theorem C for at most sixteen vertices gives the cumulative
bound for at most eighteen vertices. The eighteen-vertex proof above does
not assume the seventeen-vertex proof.
