# Linear full-LP rounding across the profile boundary

Complete author proof, awaiting independent mathematical review. The new
ingredients are a role-preserving sparse-component switching lemma and a
finite hierarchy separating sparse and dense profile coordinates. The dense
completion step applies Keevash's generalized partite family decomposition
theorem. The theorem is imported, and no absolute priority claim is made.

All graphs are finite and simple. A mixed template partitions the vertices
into clique or independent classes, with each cross pair completely joined
or empty. Classes need not be maximal twin classes. An edge type is an
unordered pair ij, allowing ii for a clique class. Its capacity is

    b_ij=n_i n_j (i<j),    b_ii=binom(n_i,2).

A triangle type is a multiset of three class indices with all three edge
types supported. A pattern P is an allowed triangle type or a supported
single-edge type. Write a_eP for the number of its edges of type e and k_i(P)
for its number of vertices of type i. Repeated indices denote different
actual vertices, never loops. A full profile is a real vector z>=0 with

    sum_P a_eP z_P=b_e  for every supported e.              (1)

Its single-edge coordinates represent unused capacities. When all classes
have at least three vertices, distributing each triangle mass uniformly
over its actual type realizes its fractional edge loads. Conversely, class
symmetrization aggregates any fractional packing to (1). Thus maximizing
the sum W of triangle coordinates gives the full fractional packing optimum
nu*(G), including all repeated-type and clique-only triangles. Write nu(G)
for the maximum number of edge-disjoint triangles.

## 1. Statement and scope

Fix d>=1 and 0<alpha<=1. Set

    M=binom(d+2,3)+binom(d+1,2),   lambda=8M/alpha,
    B=M(6/alpha+2),               U=ceil(lambda+B).         (2)

There are at most M patterns for any template with at most d classes.

**Theorem 1.** There is N_0=N_0(d,alpha) such that the following holds.
Suppose G has N>=N_0 vertices in at most d mixed classes, each of size
n_i>=alpha N. For EVERY full real profile z satisfying (1), define

    t_P=floor((1-lambda/N)z_P),
    m_P=t_P if t_P>=N, and m_P=0 otherwise.                 (3)

Then G has a triangle packing with exactly m_T triangles of each triangle
type T. Consequently

    nu*(G)-nu(G) <= M(1+4/(3alpha))N.                       (4)

The same packing has size at least W-M(1+4/(3alpha))N for any feasible
profile, whether optimal or not. There is no lower bound on its positive
coordinates. Zero coordinates and intermediate masses between N and N^2
are permitted. The constant and starting order are uniform over all such
templates, class proportions, supports and real profile values; no fixed
ray or denominator assumption occurs.

In particular, nu*(G)-nu(G)=O_{d,alpha}(N) over the whole indicated class,
including the finitely many orders below N_0 by enlarging the constant.
The explicit coefficient in (4) is asserted only for N>=N_0. The threshold
is existential and not made practical here. Nonempty classes of size o(N)
are still excluded: this is not a uniform O_d(N) result for all bounded-type
graphs, nor a solution of all-order three-neighborhood Tuza.

Linear order cannot be reduced to o(N) for this class. For even N>=4,
uniform triangle weight 1/(N-2) gives nu*(K_N)=binom(N,2)/3. A packing uses
an even number of incident edges at each vertex, so at least N/2 edges
remain. Hence nu*(K_N)-nu(K_N)>=N/6. This standard parity example concerns
the order of the error, not sharpness of our coefficient.

## 2. A role-preserving sparse packing lemma

For a type-i role in P, let l_iP be its incident edge-type degree vector.
All roles of a repeated type in one pattern have the same vector. It has
coordinate k_i(P)-1 internally and k_j(P) towards another type j, and sums
to two for a triangle or one for a single edge.

For a requested integer count m_P, the balanced role prescription gives
vertex v in class i either floor(m_P k_i(P)/n_i) or its ceiling roles, with
the first remainder vertices receiving the extra role. This prescription
can be made simultaneously for every pattern.

Construct an initial list of copies as follows. Number vertices within
class i by 0,...,n_i-1. In copy t of P assign its successive type-i roles

    (t k_i(P)+r) mod n_i,  0<=r<k_i(P).                   (5)

Provided n_i>=3, every component has distinct vertices and the balanced
role prescription holds exactly. Different components can initially repeat
edges. Let D bound the largest degree of their union counted WITH edge
multiplicity. For a fixed P let r_P bound its largest role count at any
actual vertex, across every class occurring in P.

**Lemma 2 (sparse switching).** If for every active P and every i in P,

    (4D+5)r_P < k_i(P)m_P,                                (6)

the initial components can be changed into edge-disjoint copies of the
same patterns, preserving every individual vertex's role count in every
pattern. In particular the final union has the same maximum degree bound D.

*Proof.* Maintain a list of simple components, allowing repeated edges
between components. Its conflict statistic is

    E=sum_e max(mu(e)-1,0),

where mu(e) is the edge multiplicity. When E>0, choose one component Q
containing a repeated edge uv, and choose its role occupied by u, of type i.
Write P for its pattern, and A for the other one or two vertices of Q.
Consider all k_i(P)m_P type-i role positions in copies Q' of this same P.
For a candidate position occupied by w, let A' be Q' minus that position.

Use neighborhoods in the current underlying simple graph. Reject w if

    w in {u} union A union (union_{a in A} N(a)),          (7)

or if some a' in A' lies in {u} union N(u). The forbidden vertex set in
(7) has size at most 2D+3, so it rejects at most (2D+3)r_P positions.
For the second rejection rule, each of at most D+1 forbidden vertices
occurs in at most r_P copies of P. Each such occurrence is another role
beside at most two candidate positions. It therefore rejects at most
2(D+1)r_P positions. Their sum is the left side of (6).

Some candidate survives. Swap the positions occupied by u and w. The
components are distinct, since every position of Q is excluded by (7).
Their vertices stay distinct. Each new edge w a, a in A, or u a', a' in A',
was absent in the current underlying graph. These new edges are mutually
distinct: within a component this follows from vertex distinctness, and
an equality across components would require w=u or u in A, both excluded.
All other component edges are unchanged. The repeated occurrence of uv
is removed, no new repeated edge is created, and E drops by at least one.
The swap exchanges same-type roles within the SAME pattern, so every
vertex-pattern role count and local degree vector is preserved exactly.
Iterating terminates because E is a nonnegative integer. This proves the
lemma without a random-packing or degree-sequence assumption.

**Corollary 3.** For fixed d,alpha, there is a sufficiently small eta>0
such that counts N<=m_P<=eta N^2 for any set of at most M patterns can be
realized as in Lemma 2, for sufficiently large N and n_i>=alpha N.
More quantitatively, their initial multiplicity degree is at most

    D<=6M eta N/alpha+2M.                                 (8)

For N>=alpha/eta this is at most 8M eta N/alpha. Each active pattern has

    r_P<=3m_P/(alpha N)+1<=4m_P/(alpha N),                  (9)

using m_P>=N and alpha<=1. Therefore (6) follows from

    16D+20<alpha N.                                      (10)

Equations (8)-(10) are the bounds used below. For example D<=alpha N/64
and sufficiently large N suffice. The finite checker also tests (6) directly
on its literal instances; they need not meet the looser sufficient bounds.

## 3. Small degree lists avoiding a forbidden graph

The next lemma lets us retain the sparse components while realizing the
constant-sized local deficits.

**Lemma 4.** Let U>=1 and let a forbidden simple graph have maximum degree
at most D. In the bipartite case let both sides have length at least L;
in the ordinary case let the vertex set have length at least L. Suppose

    L>8(U+1)(D+U+1).                                     (11)

Any prescribed degrees in [1,U] are realized by an allowed simple graph,
provided that the two sums agree in the bipartite case, or that the single
sum is even in the ordinary case.

*Proof.* Choose an allowed graph F of maximum edge count subject to the
prescribed upper degree bounds. In the bipartite case, if F is incomplete,
there are deficient vertices a on the left and b on the right. Every
deficient right vertex lies among the at most D+U forbidden or existing
neighbors of a. All others are saturated with degree at least one, so
|F|>=L-D-U. At most 2U(D+U+1) edges cd of F have their left endpoint among
the forbidden/existing neighbors of b or a itself, or their right endpoint
among those of a or b itself. Inequality (11) makes the former edge count
larger. Choose an edge outside those restrictions and replace cd by ad,cb.
This increases |F| while preserving the upper bounds, a contradiction.

In the ordinary case the deficient vertices form a clique in the union of
F and the forbidden graph, so there are at most D+U+1 of them. Thus
|F|>=(L-D-U-1)/2>2U(D+U+1). With distinct deficient a,b choose an edge cd
outside their forbidden/existing neighborhoods and {a,b}, and replace it
by ac,bd. If only a is deficient, parity makes its deficiency at least two;
an edge cd outside its forbidden/existing neighborhood and {a} can instead
be replaced by ac,ad. Both contradict maximality. All added edges are
allowed and new. This proves the lemma.

## 4. Uniform completion of dense patterns

We give the analytic interface needed for the finite hierarchy. The proof
is included so the new result does not silently assume the preceding
unreviewed robust-profile specialization.

**Lemma 5 (dense completion).** Fix d,alpha,epsilon>0. There are delta>0
and N_1 such that the following holds uniformly over all mixed templates
with at most d classes of sizes n_i>=alpha N. Let F be a subgraph of the
template host G with maximum degree at most delta N. Let P be a set of
triangle and single-edge patterns with integer counts m_P>=epsilon N^2.
Suppose their global edge vector is exactly that of G-F, and the incident
edge-type vector at every vertex of G-F belongs to the integer lattice
generated by the appropriate type-i vertex vectors of these patterns.
Then G-F decomposes into exactly m_P copies of each P whenever N>=N_1.
Zero patterns are omitted from this statement.

The imported theorem is Peter Keevash, *Coloured and directed designs*,
[author manuscript](https://people.maths.ox.ac.uk/keevash/papers/lovasz70.pdf)
dated 15 October 2018, Theorem 5.15 on printed page 19, with Definitions
4.3-4.5, 5.11, 5.12 and 5.14. It gives a generalized partite family
decomposition from full indexed divisibility, regularity with comparable
positive embedding weights, bounded-rank extendability, and sufficiently
large comparable parts. The family consists of ordinary simple graphs on
a common role set; disconnected graphs and isolated unused roles are
allowed. This universal existence theorem is the deep external premise.

For each P introduce private parts A_P,B_P of sizes
a_P=ceil(m_P/N) and N, respectively. Give their pair exactly m_P edges by
deleting (j mod a_P,j) for 0<=j<a_P N-m_P. The deletion has maximum degree
at most ceil(2/epsilon) for large N. Every m_P<=N^2/2 follows from the
global edge-vector identity, since each pattern has at least one edge.
Consequently epsilon N/2<=a_P<=N for large N.

Let Gamma be G-F disjoint from these auxiliary graphs. Its total order n
lies between N and C N, with C=1+2M. Every part has size at least beta n,
where beta=min(alpha,epsilon/2,1)/C. For each P take H_P to be its original
component together with one edge in its private auxiliary pair. Place all
H_P on a common partitioned role set, with at least three roles in every
part, unused roles isolated. Choose a fixed q, padding further if necessary,
so the source's h(q)>=1/beta. It depends only on d,alpha,epsilon and the
support. There are only finitely many supports; padding can give a common
q if desired. Let Phi be the complete type-respecting injection complex,
which is exactly adapted to the type-preserving permutation group.

The global indexed edge vector of Gamma is sum_P m_P h_P. Its original
singleton vectors are in the assumed vertex lattices. Auxiliary singleton
vectors are integer multiples of the unit vector supplied by a tag-edge
endpoint. At every host edge the two-vertex vector is the appropriate unit,
supplied by an H_P edge; at nonedges it is zero. These verify every indexed
divisibility condition, including the type restrictions. Scalar degree gcds
are not substituted for them.

Write q_j for the number of roles in part j and L=product_j (n_j)_(q_j),
the number of full role embeddings including all padding. Give every valid
H_P embedding weight

    y_P=a_P N/L.                                         (12)

Temporarily restore F, retaining the auxiliary graphs. Every private edge
has load one, because L/(a_P N) embeddings use it. The total weight for P
is m_P. Original class symmetry then gives an original edge of type e
load b'_e/b_e, where b' is the vector of G-F. This counts all automorphisms
and isolated-role completions, with no suppressed factor.

Now restrict original components to G-F. Since Delta(F)<=delta N, original
base loads are at least 1-2delta/alpha for large N. A surviving edge belongs
to at most 2delta N destroyed triangles across all types. Each type-T
triangle has effective weight m_T/C_T, where C_T is its actual type count
in the complete template. For large N, C_T>=alpha^3 N^3/48 and m_T<=N^2/2,
so this weight is at most 24/(alpha^3 N). Single-edge components incur no
additional loss. Thus surviving original loads lie in [1-c,1], with

    c<=50delta/alpha^3.                                  (13)

For a private edge, the lost proportion is at most the sum of the removed
fractions of the at most three original edges, at most 6delta/alpha. The
same bound (13) therefore controls all edge loads of Gamma.

For sufficiently large n, (beta n/2)^q<=L<=n^q and

    [epsilon/(2C^2)] n^(2-q) <= y_P
      <= (2/beta)^q n^(2-q).                             (14)

Every supported original pair misses at most delta N neighbors at each
vertex; auxiliary pairs miss boundedly many. In any rank-h extension there
are at most qh vertices. If delta<=beta/(4qh), greedy choices into prescribed
parts give at least beta n/2 choices per new vertex, for large N. Thus an
extension with v new vertices has at least (beta/2)^(qh)n^v completions.
Unsupported edge indices are omitted, exactly as prescribed before the
source's Theorem 5.15; no unsupported pair is required to be an edge.

Choose omega>0 smaller than the lower constant in (14), the reciprocal of
its upper constant, (beta/2)^(qh), and the theorem's omega_0. THEN choose
delta>0 small enough that delta<=beta/(4qh) and
50delta/alpha^3<=omega^(h^20). Increase N_1 so n^(-delta_source)<omega and
all the preceding bounds hold; delta_source is the imported theorem's
exponent, distinct from our deletion tolerance delta. The part-size
condition follows from h>=1/beta. Theorem 5.15 gives a family decomposition.
Exactly m_P members have type H_P, since only those use its private pair,
consuming one auxiliary edge each. Discarding private edges proves Lemma 5.
Taking minima and maxima over the finitely many supports gives uniform
delta(d,alpha,epsilon) and N_1(d,alpha,epsilon).

## 5. A finite threshold hierarchy

Fix d,alpha and the constants (2). Set epsilon_0=1. Recursively for
j=0,...,M, apply Lemma 5 with lower bound epsilon_j/2, and call its deletion
tolerance delta_j. Set

    tau_j=min(alpha/64, alpha/[32(U+1)], delta_j/2).

Choose a positive epsilon_(j+1) satisfying

    epsilon_(j+1)<min(epsilon_j/2, alpha tau_j/(16M)).      (15)

This is a finite recursion of length M+1; every constant is fixed before
the graph or its profile is supplied. No compactness assertion across a
vanishing profile coordinate is being used.

Each z_P/N^2 is at most 1/2 by (1), and there are at most M positive
coordinates. Of the M+1 disjoint intervals

    [epsilon_(j+1),epsilon_j),  0<=j<=M,

at least one contains no coordinate. Fix such a j. Call a pattern dense
when z_P>=epsilon_j N^2, and sparse when z_P<epsilon_(j+1)N^2. These two
classes exhaust all patterns, including zeros in the sparse class.

For large N, each dense pattern retains its positive count in (3) and

    m_P>=epsilon_j N^2/2.                                (16)

Each retained sparse pattern has N<=m_P<epsilon_(j+1)N^2. By (8), (15),
and sufficiently large N, the initial sparse union has multiplicity degree

    D<=8M epsilon_(j+1)N/alpha<=tau_j N.                  (17)

In particular (10) holds, so Lemma 2 realizes all sparse components with
their balanced role prescriptions. Call their simple edge union S.

Every original supported edge type is covered by some dense pattern.
Indeed b_e>=alpha^2 N^2/4 for large N, whereas if all contributing patterns
were sparse, (1) would imply b_e<3M epsilon_(j+1)N^2. Inequality (15) and
tau_j<=alpha/64 make the latter smaller than alpha^2 N^2/4. In particular
the dense family is nonempty unless G is edgeless, which is immediate.

## 6. Completing the exact local roles

Put theta=1-lambda/N and assume N>=4lambda. Allocate balanced roles for
ALL retained patterns in (3), including the sparse ones already realized
in S. Write

    d_v=sum_P r_vP l_iP,  v in class i.

Equation (1), with internal incidence counted twice, says

    sum_P [z_P k_i(P)/n_i]l_iP,e=p_i,e,                   (18)

where p_i,e is n_j across classes and n_i-1 internally. The truncation
rule satisfies 0<=theta z_P-m_P<N for every P. Each balanced role count
differs from its mean by less than one, each k_i<=3, and each coordinate
of l_iP is at most two. Therefore

    theta p_i,e-B <= d_v,e <= theta p_i,e+2M.              (19)

The lower error per pattern is at most 6/alpha+2; this is why B in (2)
differs from the previous robust-profile rounding bound.

Set r_v,e=p_i,e-d_v,e. For N>=2/alpha, equations (2) and (19) give

    1<=2M<=r_v,e<=U.                                     (20)

Across a supported pair the two lists have equal sums: both target the
edge count b_e-sum_P a_eP m_P. Internally their sum is twice that quantity
and is even. This explicitly uses internal role incidence twice.

Apply Lemma 4 to these lists, forbidding all edges of S. By (17),
D<=alpha N/[32(U+1)], and for sufficiently large N every part length
n_i>=alpha N satisfies (11). This constructs a simple R disjoint from S,
with maximum degree at most dU. The host G-S-R has exact global edge
counts sum_dense a_eP m_P. At every vertex its incident vector equals

    p_i - deg_S(v) - r_v = sum_dense r_vP l_iP.            (21)

The equality holds because Lemma 2 preserved EACH sparse vertex-pattern
role count, not only total sparse degrees or aggregate type counts.
Thus (21) is an explicit nonnegative integer singleton-lattice witness
for the dense family.

The deleted graph S union R has maximum degree at most D+dU. Since
tau_j<=delta_j/2, this is at most delta_j N for sufficiently large N.
Equations (16), (21) and the global count identity supply Lemma 5's
hypotheses with lower bound epsilon_j/2. It decomposes G-S-R into exactly
the dense m_P components. Combine them with the sparse components in S,
and retain all original triangle components. This gives precisely (3).

All lower bounds on N depend on the finite hierarchy, d and alpha only.
Take their maximum, together with the finitely many Lemma 5 thresholds,
to obtain N_0(d,alpha). This proves the uniform quantifiers in Theorem 1.

Finally W<=N^2/6, and the error theta z_T-m_T is less than N for each of
at most M triangle types. Consequently

    sum_T m_T >= theta W-MN
      >= W-(lambda/6+M)N
      = W-M(1+4/(3alpha))N.

Applying this to an optimal full profile proves (4).

## 7. Explicit optimum profiles approaching a face

The theorem genuinely includes profiles excluded by a fixed positive
epsilon assumption. Consider a complete split graph with core order k
and independent-side order l. Its triangle types are CCC and CCI.

Let k=t^2 and l=t^2-1-t, for integers t>=3. An optimum full decomposition
profile is

    x_CCC=t^3/6,   x_CCI=k l/2,

with no spare edges. Indeed CCI uses two spokes and one core edge,
while CCC uses three core edges, so both capacity equations hold. Its
optimality follows from the edge-count upper bound. With N=k+l,
x_CCC/N^2 tends to zero at order 1/t, while both classes have order N.

On the other side of the same face, let l=t^2-1+t. An optimum full
profile has x_CCC=0, x_CCI=binom(k,2), and spare spoke mass t^3.
Every triangle consumes at least one core edge, which proves optimality;
the spoke capacity equation is exact. This time a positive SPARE coordinate
has intermediate order N^(3/2). Both sequences satisfy n_i>=N/3 for t>=3.
The checker validates these formulas and the truncated local-role equations
at large exact integer scales. It does not materialize large triangle
packings or claim these familiar complete-split examples themselves are new.

## 8. What the executable evidence establishes

The finite source constructs cyclic role lists, removes repeated pairs by
the specified swaps, and realizes bounded degree lists while avoiding a
forbidden graph. A separately formulated checker replays each swap, checks
strict conflict decrease, verifies every final edge and vertex-pattern
role count, and checks exact degrees and forbidden-edge avoidance in the
second construction. It also checks compressed role equations at large
orders, explicit optimum profiles on both sides of the complete-split
face, the finite empty-interval argument, and negative controls.

These are exact finite audits of the new constructive bridges. They do not
prove Keevash's universal theorem, formalize the present argument, bound its
omega_0 or N_0, or turn a finite test into an arbitrary-order decomposition.
Sublinear vertex classes remain the next unresolved boundary in this work.
