# Exact vertex roles in dense family completion

This is a new author specialization of Keevash's generalized partite design
theorem, not a consequence of the earlier disconnected private-edge tags.
Those tags force global counts but do not force output roles at individual
vertices. The pendant tags below supply the missing constraint.

Fix r, beta, epsilon > 0 and a finite set of at most M patterns. A pattern
is a triangle or a single edge in an r-class mixed template; differently
labeled copies of the same edge pattern are allowed. Put s = sum s_h and
assume s_h >= beta s. Every pattern P has a positive integer count
m_P >= epsilon s^2. Write k_h(P) for its number of vertices in class h,
a_eP for its number of edges of type e, and l_hP for the incident edge-type
vector of one of its class-h roles. Repeated roles of a type in a triangle
or edge have the same l_hP.

**Role completion lemma.** There are delta > 0 and s_0, depending only on
these fixed parameters and the finite family, with the following property.
Let J = X - F, where X is the complete mixed-template host and
Delta(F) <= delta s. Suppose

    sum_P a_eP m_P = |E_e(J)|,
    sum_(v in X_h) r_vP = k_h(P) m_P,
    r_vP in {floor(k_h(P)m_P/s_h), ceil(k_h(P)m_P/s_h)},
    deg_J(v, e) = sum_P r_vP l_hP(e)     (v in X_h).       (R1)

Then, for s >= s_0, J has an edge decomposition into exactly m_P copies
of every pattern P in which vertex v has exactly r_vP roles of P.
Roles can be assigned to any vertices satisfying (R1); prefix extras are
only one choice. Zero patterns are omitted. If the family is empty, the
conclusion is the empty decomposition of the empty J.

## The host and the augmented family

For every P and h with k_h(P) > 0, introduce a private class A_Ph of size

    a_Ph = ceil(k_h(P)m_P/s_h).

Join X_h to A_Ph so that the degree of each original vertex v in this
private pair is exactly r_vP. To do this start with the complete pair and,
for each row with r_vP = a_Ph - 1, delete one edge. Distribute those deleted
edges cyclically over A_Ph. A row loses at most one edge, and an auxiliary
column loses at most ceil(s_h/a_Ph) <= ceil(1/epsilon) edges. The private
pair has exactly k_h(P)m_P edges.

Replace each original role of P by that role with one pendant edge to a
new auxiliary role in A_Ph. The k_h(P) auxiliary roles in the same A_Ph
are distinct. Call the augmented graph P^+. It has at most six nonisolated
vertices and six edges. For large s, every a_Ph >= epsilon s is large
enough for all these distinct roles. This includes repeated-type triangles
and repeated-type edges; there is one pendant per vertex role, not one
pendant per distinct class.

Let Gamma be J with all private pairs added. All other auxiliary pairs are
empty. Each m_P <= s^2/2, since P has an edge and the global equation in
(R1) holds. Thus a_Ph <= 3s/(2beta)+1, and, for large s, its augmented order
N satisfies s <= N <= C s, where C = 1 + 12M/beta is a sufficient bound.
Every original or private class has at least bN vertices, with

    b = min(beta, epsilon)/C.

Put every P^+ on one common partitioned role set, with at least three
roles in every part and the unused roles isolated. Pad further so that
Keevash's h(q) is at least 1/b. Let Phi be the complete complex of
type-respecting injections. It is exactly adapted to the group of
permutations preserving role parts. The numbers of parts and roles are
fixed, independent of s and of the actual counts.

## All indexed divisibility conditions

The global indexed vector of Gamma is sum_P m_P times the indexed vector
of P^+. At an original vertex v in X_h, its vector is exactly the sum of
r_vP copies of the class-h singleton vector of P^+: the original coordinates
are (R1), and its private coordinate Ph is r_vP by construction.
An auxiliary vertex in A_Ph has edges only towards X_h; its vector is an
integer multiple of the unit vector of a pendant endpoint. At a host edge
the two-vertex vector is the corresponding unit, supplied by an edge of a
family member. At a nonedge it is zero. These are all subset sizes 0,1,2
needed for a graph decomposition. In each case use roles of the same
part index as the host subset. This checks indexed divisibility, not merely
scalar degree divisibility. Labels are distinguished by their private parts.

## Positive approximate decomposition and extensions

The imported statement is Theorem 5.15, printed page 19 of Peter Keevash,
*Coloured and directed designs*, author manuscript dated 15 October 2018:
[primary manuscript](https://people.maths.ox.ac.uk/keevash/papers/lovasz70.pdf).
We use its Definitions 5.11, 5.12 and 5.14 and the bounded-rank extension
definitions in Section 4. This is the deep external existence premise.

Restore F and all missing private edges temporarily. If q_j roles lie in
part j, let

    L = product_j (|V_j|)_(q_j).

Give every full embedding of P^+ weight m_P/L. Its total weight is m_P.
For an original edge of type e, its load, summed over patterns, is
sum_P a_eP m_P/b_e = (b_e-f_e)/b_e. For a private edge in X_h A_Ph its load is

    k_h(P)m_P/(s_h a_Ph),                              (R2)

which is between 1 - 1/a_Ph and 1. These formulas count labeled embeddings
and padding completions explicitly; repeated roles introduce no omitted
automorphism factor. Original loads are at least 1-O(delta), and private
loads at least 1-O(1/s), uniformly in the allowed parameters.

Now retain only embeddings whose edges survive in Gamma, without changing
their weights. Condition on a particular role edge mapping to a surviving
host edge. Every other edge of P^+ has at most one endpoint already fixed.
Uniform injections leave at least bN-q choices for each free endpoint.
An original pair misses at most delta s neighbors at each endpoint, and
a private pair misses at most max(1,ceil(1/epsilon)). A union bound over
at most five other edges shows conditional loss O(delta+1/s). The bound
also applies when the two conditioned original roles have the same type.
Summing over possible role edges shows every surviving host-edge load lies
in [1-C_1(delta+1/s),1], for a fixed C_1. This argument applies to private
edges too, including those sharing an original endpoint with other edges.

For large N, (bN/2)^q <= L <= N^q and s <= N <= Cs. Therefore every valid
embedding has weight between

    (epsilon/C^2) N^(2-q)
    and (1/2)(2/b)^q N^(2-q).                         (R3)

For each bounded-rank extension, at most qh vertices and adjacency
requirements must be considered. Every supported pair is complete apart
from the deletions just bounded. Choose delta sufficiently small relative
to b/(qh); greedy extension then leaves at least bN/2 choices at each new
vertex for large s. This gives at least (b/2)^(qh) N^v extensions when v
vertices are new. Unsupported edge indices are omitted as specified just
before Theorem 5.15; no adjacency is demanded in an empty unsupported pair.

The constant order is essential. First choose q and a positive omega
smaller than the lower weight constant in (R3), the reciprocal of its upper
constant, the extension constant, and the theorem's omega_0. Then choose
delta small enough for the extension bound and
C_1 delta < omega^(h^20)/2. Finally make s_0 large enough that
C_1/s < omega^(h^20)/2, N^(-delta_source) < omega and all part/size bounds
hold. Here delta_source is the exponent in the imported theorem, not our
deletion tolerance. The hypotheses of Theorem 5.15 now hold. Finitely many
supports can be handled by minima/maxima of these constants.

## Decoding forces actual local roles

The resulting decomposition uses only P^+ to cover edges in its private
pair X_h A_Ph. Every such copy uses k_h(P) of those edges; there are
k_h(P)m_P in the host. Its global copy count is therefore m_P. At a fixed
original vertex v, every occurrence as a P role uses exactly one of its
r_vP private edges, and no other pattern uses any of them. Its actual
P-role count is exactly r_vP. Delete all pendant edges from the copies.
The remaining copies decompose J with all the claimed global and local
prescriptions. This last vertex-by-vertex conclusion is the strengthened
interface used in the bounded-type induction.

The finite audit checks tag degrees, full labeled-embedding load formulas,
restriction losses and an explicit augmented Fano decomposition. It does
not prove the universal design theorem or calculate delta and s_0.
