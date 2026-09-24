# Linear triangle-packing loss for every fixed mixed template

Complete author proof; independent mathematical review is pending. Constants
are existential through Keevash's design theorem and a finite hierarchy.
Exact finite audits check the new interfaces, not that external theorem.

A mixed-template graph partitions its N vertices into at most t nonempty
clique/independent classes, with every cross pair complete or empty. Classes
need not be maximal twin classes. All graphs are finite and simple. Let nu
be the maximum number of edge-disjoint triangles and nu* the full fractional
triangle-packing optimum.

**Main theorem.** For every fixed t there is a finite K_t such that every
N-vertex mixed-template graph with at most t classes satisfies

    0 <= nu*(G)-nu(G) <= K_t N.                         (1)

More precisely, every feasible fractional triangle packing of weight W
rounds to an integral packing of size at least W-K_t N. There is no lower
bound on class proportions, no positive-profile-margin assumption, and no
restriction on the number of different class-size scales. Clique classes,
independent classes and all repeated-type triangles are included. Equivalently,
this holds for graphs of any fixed bound on neighborhood diversity.

The proof needs a stronger induction that retains labeled single edges and
bounded discrepancy of each individual pattern's vertex roles. Discarding
those invariants would leave a gap. The two new bridges are exact local-role
completion via private pendant edges and a proper-coloring repair that
preserves every edge-type/color count, even for very unequal classes.

This is not a proof of Tuza's exact inequality, an effective numerical
bound on K_t, a practical universal algorithm, or an independent review.
The statement is uniform in class sizes but t remains fixed.

## 1. The stronger invariant and fractional profiles

Fix a nonnegative integer L. In addition to every allowed triangle type,
allow L distinct labels of single-edge patterns on each supported edge
type. A full profile consists of nonnegative real y_P satisfying

    sum_P a_eP y_P = b_e,                              (2)

where a_eP is the edge multiplicity of type e in P,
b_ij=n_i n_j and b_ii=binom(n_i,2). If a combinatorial type has no actual
copies, its coordinate is required to be zero. Write k_i(P) for its number
of class-i vertices. We prove the following simultaneously for every L.

**Balanced profile theorem B(t,L).** There are finite C(t,L),D(t,L)>=1,
with D an integer, such that every full profile on every host with at most
t nonempty classes has edge-disjoint copies with integer counts m_P obeying

    0 <= m_P <= y_P,
    sum_P(y_P-m_P) <= C(t,L)N,
    |r_vP-k_i(P)m_P/n_i| <= D(t,L)   (v in class i).     (3)

Here r_vP is the ACTUAL number of P copies containing v. All patterns are
edges or triangles, so sum_P y_P<=|E(G)|<=N^2/2. Uncovered edges are allowed.
Labels distinguish otherwise identical edge patterns. Zero/unused labels
can be padded, so constants may be taken nondecreasing in their arguments.

Aggregate a fractional triangle packing by vertex classes and put its edge
slack in one single-edge label. This gives (2). Conversely, uniformly
distributing each supported triangle-type mass realizes its edge loads on
the complete template, including repeated-type multiplicities. Applying
B(t,1) and retaining only triangles proves (1), since every coordinate
loss in (3) is nonnegative. The empty host is immediate.

## 2. Comparable-class completion with exact local roles

Fix d,alpha>0, a label bound L and discrepancy A>=0. Let H have n vertices in
at most d classes, each >=alpha n. Let F have maximum degree <=eta n and
suppose its degree at every vertex in every incident edge type differs
from the class average by <=A. The input is ANY capacity profile against
b_e-|F_e|; it need not already be a fractional packing uniformly distributed
on surviving triangles.

**Comparable role lemma.** For fixed parameters there are eta>0,n_0 such
that for n>=n_0 the following counts are realizable in H-F, with every actual
r_vP a prescribed balanced floor/ceiling of k_i(P)m_P/n_i:

    M=binom(d+2,3)+L binom(d+1,2), lambda=8(M+A)/alpha,
    theta=1-lambda/n,
    m_P=floor(theta y_P) if that integer >=n; else 0.   (4)

The total COMPONENT loss is at most (lambda/2+M)n. The term lambda/2,
rather than lambda/6, includes labeled single-edge objectives. An edgeless
host is immediate.

Here is the full reduction. Assign each r_vP by balanced cyclic roles,
with prefix extras, and let d_v=sum_P r_vP l_iP be its requested incident
edge-type vector. Repeated roles in an edge or triangle have the same l_iP.
If p' is the average residual degree of an incident type, then

    theta p'-B_0 <= d_v <= theta p'+2M,
    B_0=M(6/alpha+2), U=ceil(lambda+B_0+A).

These follow from 0<=theta y_P-m_P<n, k_i<=3 and entries of l_iP<=2.
When eta<=alpha/4 and n is large, p'>=alpha n/2. The complementary integer
degree list deg_(H-F)(v)-d_v is in [1,U], since its lower bound is

    -A+lambda alpha/2-2M = 2M+3A > 0.                  (5)

Cross sums match and internal sums are even.

Use the new [role completion lemma](ROLE_COMPLETION.md), with dense lower
bound epsilon_j/2, to get delta_j. Start with epsilon_0=1 and, for j=0,...,M,
choose

    tau_j=min(alpha/128,alpha/[64(U+1)],delta_j/4),
    0<epsilon_(j+1)<min(epsilon_j/2,alpha tau_j/(16M)).

Finally fix eta<=min(alpha/4,min_j tau_j/2). An empty one of the M+1 bands
[epsilon_(j+1),epsilon_j) separates dense y_P>=epsilon_j n^2 from sparse
y_P<epsilon_(j+1)n^2, since at most M coordinates are positive and all are
<n^2. Every retained dense m_P is eventually >=epsilon_j n^2/2.

For each sparse P, assign its successive type-i roles in copy t to
(t k_i(P)+a) modulo n_i. This gives exactly the balanced roles, and distinct
vertices within a copy. Total multiplicity degree D_s is at most
6M epsilon_(j+1)n/alpha+2M<tau_j n/2 eventually. Every retained m_P>=n, so
its largest role count at a vertex is at most 4m_P/(alpha n).

The role-preserving switch from accepted h5857 removes repeats and edges
of F. From a bad copy at a type-i role u, with at most two other vertices A,
swap u with a type-i role w in another copy of the SAME P. Put
D=D_s+Delta(F). The condition

    (4D+5)r_P < k_i(P)m_P                             (6)

guarantees a valid position: w in {u} union A union N(A) excludes at most
(2D+3)r_P positions; a candidate whose other copy vertices meet {u} union
N(u) excludes at most 2(D+1)r_P more. Neighborhoods include F and the entire
component graph. New edges are mutually distinct and absent from that union.
Repeated-edge excess plus forbidden-edge occurrences strictly decreases.
Every vertex-pattern role stays fixed. The bounds on tau_j,D,r_P imply (6)
at large n. Labeled edges are handled just as triangles. Let S be the
resulting sparse packing.

Realize the complementary degree lists (5) by a graph R avoiding F union S,
pair by pair. The accepted elementary criterion from h5857 says that lists
bounded by U, with equal cross sums or even internal sum, requesting m edges
avoid a degree-D forbidden graph whenever m>3U(D+U+1). Here positivity gives
m>=alpha n/2 and D<=tau_j n, so the criterion follows at large n.
Moreover Delta(R)<=dU. The remaining H-F-S-R has the dense global counts
and actual local vector sum_dense r_vP l_iP. Its deleted maximum degree is
eventually below delta_j n. Pendant completion realizes the dense counts
with precisely those local roles. Together with S it proves (4).
Finally sum_P y_P<=n^2/2 gives the loss. Finitely many supports and hierarchy
levels give uniform constants.

This is the accepted sparse/complement argument with the stronger dense
interface proved in ROLE_COMPLETION.md. The old disconnected tags forced
only GLOBAL counts and cannot substitute for pendant tags here. The
elementary degree and switch lemmas are dependencies on
[h5857, Sections 1 and 4](../tuza_independent_extension_rounding/PROOF.md),
independently accepted in
[h5861](../tuza_independent_extension_rounding_review1/REVIEW.md).
That verdict does not cover the new interface or this induction.

## 3. Type/color repair without comparable part sizes

Let J be a simple graph on s vertices in r nonempty classes of arbitrary
sizes s_h. Every nonempty edge type e has m_e edges, and its degree at each
vertex of an incident class h is at most k_h(e)m_e/s_h+D, where D>=0. If

    min_h s_h >=64(r+1),    N>=64s,
    m_e >=16(D+1)s for every nonempty type,             (7)

then J has a proper N-edge-coloring with each edge type equitably distributed
over colors. Any initially type-equitable assignment can be repaired while
preserving EVERY individual type/color count.

Start with those counts but allow conflicts. For a color c let W_ch be
the class-h vertices incident to it. Counting incidences, even for an
improper coloring, gives

    |W_ch| <= sum_e k_h(e) ceil(m_e/N)
            <= s_h s/N + r+1.                         (8)

Use sum_e k_h(e)m_e<=s_h(s-1), at most r-1 cross types and one internal
type with two incidences. This per-class estimate avoids any lower bound
on s_h/s.

Take a conflicting edge uv of type e, color c. Seek an edge ab of the SAME
type, colored t, with t absent at u,v and c absent at a,b. At most 2s colors
appear at u,v, excluding at most 2s(m_e/N+1) candidate edges. Candidates
incident to c are at most

    sum_(h incident to e) (s_h s/N+r+1)(k_h(e)m_e/s_h+D).

With T=min_h s_h, total exclusions are at most

    [4s/N+2(r+1)/T]m_e +2s+D s^2/N+2D(r+1)
    <= (1/16+1/32+1/8)m_e =7m_e/32 <m_e.               (9)

Indeed the constant term is at most (2+3D/64)s<=m_e/8 under (7).
A candidate exists and its endpoints are disjoint from u,v, since those
vertices already see c. Swap c,t. No new conflict appears and at least
one disappears, so sum_(v,c) binom(deg_c(v),2) strictly decreases. All
type/color counts remain unchanged. Iteration proves the claim. Ordinary
equitable coloring is not assumed to supply this per-type control.

## 4. Small-block closure preserving the induction invariant

Suppose B(r,L+d) is available with constants C_-,D_-, D_- an integer >=1.
Let H be a d-class comparable core on n vertices, with n_i>=alpha n. Let X
have s vertices in r classes of arbitrary sizes, each >=64(r+1), with
arbitrary mixed-template adjacencies internally and to H. We prove (3) for
H union X when s<=eta n and n is sufficiently large. Constants may depend
on d,r,L,alpha,C_-,D_-, but not on individual s_h or the profile.

Separate triangle masses as XXX u_T, XXH v_ei (e an X-edge type), XHH w_hf
(f a core edge type), and HHH z_T. Retain all original single-edge labels
on XX, XH and HH pairs. Let b_hia be a labeled spoke mass, a=1,...,L.
On every adjacent pair the exact spoke capacity is

    sum_e k_h(e)v_ei+sum_f k_i(f)w_hf+sum_a b_hia=s_h n_i. (10)

On nonadjacent pairs all terms are zero. X-edge capacities contain XXX,
XXH and labeled XX edges; core capacities contain HHH, XHH and labeled HH.

### 4.1 Interior and XXH

Apply B(r,L+d) to X, treating each XXH core type i as an additional edge
label. The profile is full. Counts stay below their original masses, total
loss is <=C_-s, and every individual role discrepancy is <=D_-.
Discard each XXH type whose resulting edge count is below L_0 s, where
L_0=16(D_-+1). This costs at most d binom(r+1,2)L_0 s. Whole-pattern deletion
preserves the invariant for surviving types; discarded types have zero roles.

Let D_i be the retained graph labeled i. Its nonempty types satisfy (7)
at D=D_-. Choose eta<=alpha/64, so n_i>=64s. Use Section 3 with n_i colors,
identified with vertices of H_i. Each colored edge xy gives an XXH triangle
xyv. Properness prevents repeated spokes. Support follows from v_ei.

At x in X_h the used H_i-spoke degree differs by <=A=rD_- from the class
average t_hi=sum_e k_h(e)m_ei/s_h. At a core vertex, its used spoke degree
into X_h differs by <r+1 from s_h t_hi/n_i. Thus unused B_hi has row
discrepancy <=A and initial column discrepancy <=r+1. Every row is at least

    n_i-sum_e k_h(e)v_ei/s_h-A.                        (11)

For each individual XXH pattern, its X roles have discrepancy <=D_-, and
its H-center roles differ from their average by <1.

### 4.2 Labeled spokes must also be retained

Put B=2^(d+L)(r+3), Q=8B(A+rd+1). For b_hia choose exact row quota
floor(b_hia/s_h)-A if this is >=Q, else zero; its count is s_h times the
quota. For each XHH coordinate likewise put

    q_hf=floor(w_hf/s_h)-A if this is >=Q; else 0.       (12)

Every coordinate loses <(A+Q+1)s_h. At any adjacent pair h,i with a positive
request, total row requests are <=the original average demand minus A.
A loop-core type requests 2q_hf, subtracting at least as much. Equations
(10),(11) make every row feasible. If none survives there is no request.
Retaining these labeled edges is essential to the strong induction.

For an exact row demand a in an available bipartite graph, give each edge
fractional value a/d_x, where d_x is its row degree. Integral bipartite
flow realizes the exact rows and floor/ceiling column sums of
f_y=a sum_(x~y)1/d_x. If rows have mean D and discrepancy A, columns have
discrepancy delta, a<=min d_x, D>=Q>=2A, s_h/n_i<=1/(8A), delta<=B and
Q>=8AB, then, writing b_y for the available column degree,

    |f_y-a b_y/D| <= A b_y/(D-A)
                      <=2A s_h/n_i+2A delta/D<=1/2.   (13)

Selected-column discrepancy is <=delta+2; after removal row discrepancy
stays A and column discrepancy is <=2delta+2. Each positive demand is >=Q,
so its current mean is too. For fixed h,i there are at most L+d allocations.
Starting at r+1, delta_j<=2^j(r+3)-2 and every selected discrepancy is <B.
Reduce eta to alpha/(8A).

First perform all labeled spoke allocations, keeping their selected edges
with the corresponding labels. Then allocate XHH in the order below.
Previous requests subtract the same amount from all rows, so feasibility
persists. Labeled spokes have constant roles on X_h and discrepancy <B on H_i.

### 4.3 Globally ordered XHH pairing

Process all positive (h,f) in nondecreasing q_hf. For f=ij allocate q_hf
spokes at every x to each side; for f=ii allocate 2q_hf and split into two
disjoint q_hf-sets. Match each pair of sets avoiding previously used core
edges. At current quota q, even including the ENTIRE current type, all
processed types can use core degree at most

    2d s q/(alpha n)+rdB.                              (14)

All their quotas are <=q, endpoint counts are within B of their averages,
and sum_h s_h=s. Choose eta<=alpha/(16d). Since q>=Q>=8rdB, (14) is <=q/4.
Each q by q allowed graph has minimum degree >q/2, so Hall gives a perfect
matching. This includes earlier centers of the current type and loop-core
types. Pairing preserves all allocated endpoint counts.

Let F be the union of used core edges. A core vertex uses at most one spoke
to each exceptional vertex, so Delta(F)<=s. For each core edge type its
degree differs from the class average by <rB. Individual XHH patterns have
constant roles q_hf on X_h and role discrepancy <B on incident core classes.
All retained edges and triangles are pairwise edge-disjoint.

### 4.4 Core and constants

Use Section 2 at discrepancy rB and label bound L+1. Keep original HHH
and labeled HH masses unchanged; put sum_h(w_hf-s_h q_hf) in ONE new filler
edge label on core pair f. This is a nonnegative full capacity profile on
H-F. Choose eta below its deletion tolerance, and n above its threshold.
It realizes true core counts below their input with balanced roles and
loses <=C_core n components. Discard filler edges; they were never part of
the original objective. True-coordinate loss is bounded by total loss.

Overall loss is at most

    C_core n+[C_-+d binom(r+1,2)L_0
                  +(Ld+binom(d+1,2))(A+Q+1)]s,         (15)

and every individual original pattern's role discrepancy is at most

    max(D_-,B,1).                                     (16)

These checks cover XXX,XXH,XHH,HHH and labeled XX,XH,HH edges separately.
All true counts are <=input counts. For X empty use Section 2 directly.
This proves small-block closure with the full invariant.

## 5. Induction removes every class-size restriction

Induct on t, proving B(t,L) for ALL finite L simultaneously. For t=1 use
Section 2 at alpha=1,A=0,F empty. Below its threshold take the empty packing:
total mass is <=N^2/2 and all roles are zero. Enlarging C handles bounded
orders. Edgeless hosts are immediate.

Assume the assertion for at most t-1 classes and every L. Fix L and take
C_-,D_- for B(t-1,L+t+1), padding unused labels with zeros. They cover all
smaller-class subproblems below. Put T=64(t+1).

If a class has size <T, discard all patterns meeting it. Their total mass
is <=the number of incident edges, <=TN, since each such pattern consumes
at least one incident edge. Delete the class. Retain surviving coordinates
on the remaining host and add one filler edge label for capacity released
by discarded triangles on edges with both endpoints remaining. This is a
full profile. Apply B(t-1,L+1), then drop filler edges. Additional true loss
is <=C_-N. Remaining class sizes are unchanged, so role bounds transfer;
discarded patterns have zero counts and roles. This gives (3).

Otherwise every class has size >=T. We may assume there are exactly t
classes. Write p_i=n_i/N. At least one is >=1/t. Start epsilon_0=1/t.
For j=0,...,t-1 obtain Section 4's constants eta_j,n_0j,C_j,D_j uniformly
for at most t core classes, alpha=epsilon_j, at most t-1 exceptional
classes and the fixed L,C_-,D_-. Include the comparable-only case. Choose

    0<epsilon_(j+1)<min(epsilon_j/2,eta_j/(2t^2)).       (17)

All these constants are fixed before the class sizes or profile. At most
t-1 proportions lie below epsilon_0, so one of the t disjoint half-open
bands [epsilon_(j+1),epsilon_j) is empty. Let H consist of classes with
p_i>=epsilon_j and X of the remainder. H is nonempty, n>=N/t, and its
classes have size >=epsilon_j N>=epsilon_j n. Every small class has
p_i<epsilon_(j+1), so

    s<=t epsilon_(j+1)N<eta_j N/(2t)<=eta_j n.           (18)

X has at most t-1 classes and every one still has size >=T, meeting (7).
Apply Section 4. Its internal label bound is L+d<=L+t, within the available
smaller-class hypothesis. Increasing the label count creates no circularity:
the number of vertex classes has strictly decreased.

Take maxima over the finitely many hierarchy levels and supports, together
with the small-class constants. If n<n_0j, then N<=t max_j n_0j, so the
remaining total orders are bounded; use the empty packing and enlarge C.
Equations (15),(16),(18) prove B(t,L) uniformly in all class proportions and
profiles. This closes the induction and proves (1).

## 6. Scope, dependencies, and optimal error order

The error order cannot uniformly be o(N), even for t=1. In K_N with even
N>=4, giving every triangle weight 1/(N-2) yields nu*=|E|/3. Every integral
packing covers an even degree at each vertex, leaving at least one
uncovered incident edge per vertex. Thus at least N/2 edges remain and
nu*-nu>=N/6. This classical parity example is not claimed as new.

The new scope is arbitrary class proportions, beyond the preceding
comparable, independent-extension and one-clique theorems. Multiple joined
small clique or independent cells may grow at unrelated rates. Deep input
is Keevash's theorem via the new role specialization; additional dependencies
are the accepted elementary switch/degree lemmas and explicit flow, Hall
and color-swap arguments. No independent review of the new specialization
or induction is presumed. The audit does not compute K_t, design thresholds
or a universal decomposition, and no historical priority is claimed.

The classical tau<=2nu* inequality immediately gives tau<=2nu+2K_t N,
without resolving exact Tuza. Attribution, the bounded literature comparison
and finite evidence are in [SOURCES.md](SOURCES.md) and [README.md](README.md).
