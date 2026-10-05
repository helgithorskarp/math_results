# Exact classification and potential interface for tree multiplicity

Author: Iris, studio-researcher-2, researcher. Version 1, 2026-10-05.
Status: author derivation prepared for another researcher's internal check.

This component rederives the inherited sibling-leaf classification and the
full-degree potential identity. These are prior results, not a novelty claim.
The purpose is to expose the precise universal interface needed by a global
multiplicity bound. This component does not establish that asymptotic bound.

## 1. Definitions and external inputs

Let T be a finite simple tree on n>=2 vertices. A move takes two pebbles
from a vertex and adds one at a neighbor. A stack has nonempty support
consisting of one vertex. The number s=stack(T) is the least integer k>=2
such that every configuration of mass k can reach a stack. Configurations
are individual vertex functions with values in the nonnegative integers.

We import precisely two results from Fairfax--Ball, *The stacking number of
a tree*, [arXiv:2609.31811v1](https://arxiv.org/html/2609.31811v1):

1. Theorem 3.3: the branch-message score S_r is positive exactly when a
   positive stack at r is reachable, including arbitrary legal move order.
2. Theorem 1.1: s equals the maximum rooted estimator E defined below,
   with the stated least-k>=2 convention.

An empty branch is a separate state, with numerical contribution zero to
sums. On an occupied branch the transfer function is

    g(t)=2t-3                         if t<=1,
         t/2                         if t>=2 is even,
         (t-3)/2                     if t>=3 is odd.

For B=B(v|p), the v-component after deleting vp, its occupied message is
m_B=g(c(v)+sum_i m_i), where the children are B(u|v), u!=p, and empty
child contributions are zero. The rooted score is

    S_r=c(r)+sum_{u adjacent to r} m_{u->r}.

Numerical zero must not be treated as the empty state. An occupied terminal
branch with three pebbles has message zero; its clearing requirements
differ from an empty branch. Also g is not monotone on all integers:
g(2)=1 and g(3)=0. No argument below assumes that individual configurations
remain stackable when an arbitrary extra pebble is added. The imported
estimator theorem supplies the least exact-mass threshold.

Let L be the graph-leaf set, I=V(T)\L, and lambda=|L|. Define the odd
positive structural deficits by

    a_{v->p}=1                       if v is a graph leaf,
             3+2 sum_{u!=p} a_{u->v} otherwise,
    D(v)=sum_{u adjacent to v} a_{u->v},
    E(v)=D(v)+1+lambda-1_{v in L}.

Thus the second imported result is s=max_v E(v). The closed form in the
next section identifies this E with the distance-and-degree estimator of
the primary theorem; it is not a different threshold.

## 2. Full-tree degrees and maximizing leaves

Define W(v)=sum_{u in I} deg_T(u) 2^dist(v,u). All degrees here belong to
the full tree, including attached leaves.

For every oriented branch B(v|p), direct induction gives

    a_{v->p}=1+2 sum_{u in I intersect B} deg_T(u) 2^dist(v,u).       (2.1)

For a terminal branch the sum is empty. At an internal branch root with k
children, deg_T(v)=k+1; substitution in 3+2 sum_i a_i gives the constant
3+2k and the doubled descendant contributions on both sides of (2.1).
Summing over the branches incident with v therefore yields

    D(v)=W(v)                       if v is nonleaf,
    D(v)=1+W(v)                     if v is a leaf,
    E(v)=1+lambda+W(v)              for every v.                   (2.2)

For a leaf z with parent p, when n>=3 the parent is nonleaf and

    W(z)=2W(p),
    D(z)=1+2D(p),
    E(z)=1+lambda+2W(p).                                      (2.3)

No core degree can replace deg_T in these identities.

For n>=3, every nonleaf v has a neighbor of larger W, hence larger E.
Indeed, let Q_i be the contribution to W(v) from I on the i-th neighbor
side. Then sum_i Q_i=W(v)-deg_T(v). Since deg_T(v)>=2, one Q_i is
strictly below W(v)/2. Across that edge,

    W(neighbor_i)=2W(v)-(3/2)Q_i>W(v).

Consequently every global E-maximizer is a graph leaf, and every nonleaf
has E(v)<s. This statement retains tied maximizing leaves.

For a nonleaf p put L_p={z in L: z adjacent to p}, d_p=|L_p|, and

    P*={p: L_p contains an E-maximizing leaf},
    X_p=W(p)=D(p).

All leaves of one L_p have the same score by (2.3). For p in P*, d_p>=1
and X_p>=deg_T(p)>=2. The inherited leaf deficit is D(z)=1+2X_p; it is
not a core height. If needed by another component, the core eccentricity
is e_p=max_{u in I}dist(p,u), a separate quantity, equal to zero on stars.

## 3. Branch mass majorants, including empty branches

In this and subsequent sections assume n>=3. A branch contains at least
one graph leaf; let ell_B=|L intersect B|. Treat the numerical message of
an empty branch as m_B=0 only for sums, retaining its empty state.
For every configuration on B,

    m_B>=-a_B,  x_B=m_B+a_B>=0.                               (3.1)

An empty branch has x_B=a_B, not zero. Its mass is zero and its bound
F_B(a_B)>=ell_B>=1 is strictly slack; thus it cannot survive critical
equality. Zero excess means message -a_B and is a different state.

For a terminal occupied branch, its pile is at least one and its message
is at least -1. For an internal occupied branch write A=sum_i a_i.
Its effective input t is at least -A. If t<=1, g(t)>=-3-2A=-a_B;
if t>=2, g(t)>=0. Empty branches also satisfy (3.1). This proves the
lower bound without incorrectly assuming monotonicity of g.

Define real functions F_B=ell_B+G_B on x>=0. For a terminal branch,

    F_B(x)=1+2x,  G_B(x)=2x.                                  (3.2)

For an internal branch with a=3+2A, set

    b_a(x)=x/2                         for 0<=x<=a-1,
           2x-3(a-1)/2                 for x>=a-1,
    K_B(y)=max(y, max_i G_{B_i}(y)),
    G_B(x)=K_B(b_a(x)).                                      (3.3)

Every G_B is convex, strictly increasing, piecewise linear and vanishes
at zero. Inductively these properties hold for K_B, the maximum of its
child functions and the identity, and are preserved by composition with
the increasing convex piecewise-linear b_a. The maximum is strictly
increasing because each member of this finite family is strictly
increasing. In particular F_B(x)>=ell_B>=1.

For any finite collection of convex nondecreasing functions f_j with
f_j(0)=0, and allocations y_j>=0 of total Y, the chord inequality gives

    sum_j f_j(y_j)<=max_j f_j(Y).                             (3.4)

For Y>0, use f_j(y_j)<=(y_j/Y)f_j(Y) and sum the weights; Y=0 is
immediate. If equality holds, every positively used function must attain
the maximum endpoint value. If 0<y_j<Y, it must also be affine on [0,Y].
For a convex function, contact with its endpoint chord at one interior
point forces equality with that chord throughout the interval.

The universal branch mass bound is

    |c restricted to B|<=F_B(x_B).                           (3.5)

An empty branch has mass zero and strict slack, since F_B(x_B)>=1.
For a terminal occupied branch the inverse transfer rule gives pile
1+2x at equality; an even pile is smaller by three. For an internal
occupied branch put t=c(v)+sum_i m_i and y=c(v)+sum_i x_i=t+A.
If m_B<=-1, t=(m_B+3)/2 and y=x_B/2. If m_B>=0, the largest possible
t is 2m_B+3, so

    y<=2x_B-3(a-1)/2.

Together these give y<=b_a(x_B). The child bounds, (3.4) applied to the
root-pile identity and the G_{B_i}, and monotonicity of K_B prove (3.5).
No assertion that F_B is attainable at every real or integer x is needed.

At x_B=0, equality in (3.5) is attained uniquely by one pebble at every
graph leaf of B and zero at each internal vertex of B. The branch cannot
be empty. In the internal case y<=b_a(0)=0 forces c(v)=0 and every child
excess zero, so induction proves uniqueness. At a terminal branch, equality
at any excess x is uniquely the odd pile 1+2x.

## 4. The fixed-target bound is exact at the global budget

For a branch B(v|p) whose boundary p is nonleaf,

    G_B(D(p))=max_{u in B}(E(u)-1-lambda).                     (4.1)

This is a finite recursive identity, not a limiting or census assertion.
If v is terminal, write P=sum_{w!=v}a_{w->p}. Since p is nonleaf, P>=1,
D(p)=1+P and D(v)=a_{p->v}=3+2P. Consequently
G_B(D(p))=2D(p)=D(v)-1=E(v)-1-lambda.

If v is nonterminal, put O=sum_{u!=p}a_{u->v}, a=a_{v->p}=3+2O, and
P=sum_{w!=v}a_{w->p}>=1. Then D(p)=a+P>=a+1 and

    b_a(D(p))=3+O+2P=O+a_{p->v}=D(v).                        (4.2)

Thus G_B(D(p)) is the maximum of D(v) and its child values
G_{B_i}(D(v)). Since E(v)-1-lambda=D(v), induction proves (4.1).
The boundary in every recursive use is again nonleaf.

Choose any nonleaf root r, possible because n>=3. Let

    K_r(y)=max(y,max_{B incident with r}G_B(y)).

The root-pile term is D(r)=E(r)-1-lambda, so (4.1) gives

    K_r(D(r))=max_u(E(u)-1-lambda)=s-1-lambda=:Q.             (4.3)

For a nonstackable configuration all scores are nonpositive. Therefore

    Y=c(r)+sum_B x_B=S_r+D(r)<=D(r).

The branch bounds and allocation inequality now give the exact chain

    |c|<=lambda+c(r)+sum_B G_B(x_B)
       <=lambda+K_r(Y)
       <=lambda+K_r(D(r))=s-1.                               (4.4)

At the critical mass |c|=s-1, every inequality is an equality. Hence:

- every branch bound is sharp, so no incident branch is empty;
- Y=D(r), since K_r is strictly increasing;
- every positively used allocation has endpoint value Q at budget D(r).

In particular S_r=0. This reasoning uses the imported least-threshold
identity s=max E, rather than an unstated monotonicity property of an
individual configuration.

## 5. The nonterminal kink and complete equality rigidity

For a nonterminal branch, a>=5 and the breakpoint a-1 is positive.
Write G_B=K_B composed with b_a. At y0=(a-1)/2>0, convexity, K_B(0)=0
and K_B(y)>=y imply

    K'_{B,-}(y0)>=K_B(y0)/y0>=1,
    K'_{B,+}(y0)>=K'_{B,-}(y0).

One-sided derivatives exist because the functions are piecewise linear.
At x0=a-1 the left and right slopes of G_B are respectively

    (1/2)K'_{B,-}(y0),  2K'_{B,+}(y0).

They differ strictly. Thus the outer maximum cannot erase the kink. For
a nonleaf boundary p, D(p)>=a+1 by (4.2); the kink lies strictly inside
[0,D(p)]. Consequently G_B is not affine on that entire interval, and
its chord inequality is strict at every interior allocation.

Apply this to the equality in (4.4). The root-pile function cannot receive
a positive allocation: its endpoint D(r)=E(r)-1-lambda is strictly below
Q, since a nonleaf never maximizes E. If two or more branch allocations
are positive, each is interior to the full budget. A nonterminal branch
would then have strict chord slack. Therefore every positive branch in a
genuine split is terminal. All terminal functions are exactly 2x.

The other possibility is one positive nonterminal branch, receiving the
whole budget D(r). Follow that branch to its root v. Equality in its mass
bound forces all child bounds sharp and

    c(v)+sum_i x_i=b_a(D(r))=D(v),
    c(v)+sum_i G_{B_i}(x_i)=K_B(D(v))=Q.                      (5.1)

Strict increase of K_B is what forces the entire transformed budget to
be used. The same chord analysis restarts at v. The root-pile endpoint
D(v)=E(v)-1-lambda<Q again excludes c(v)>0. Every nonterminal child
again has its kink strictly inside [0,D(v)]; the complementary parent
deficit is included in D(v), ensuring the P>=1 hypothesis. Thus either
all positive excess is sent into one further nonterminal child, or it
splits only among terminal children.

The followed branches are strictly nested and the tree is finite, so
this process ends at a nonleaf p with terminal positive allocations.
All unused side branches have excess zero and hence, by Section 3,
one pebble at every leaf and none internally. Every visited internal
vertex has pile zero. At the final p, the terminal allocations obey

    sum_{z in L_p} x_z=D(p)=X_p,
    2D(p)=Q=s-1-lambda.                                     (5.2)

Equation (2.3) therefore says E(z)=s for every z in L_p: p belongs to P*.
Each terminal pile is 1+2x_z. All tree vertices have now been accounted
for: unused subtrees are the unique zero-excess configuration, the
followed path is empty internally, and the final children are the sibling
split. Hence every critical nonstackable configuration has the form

    c(z)=1+2x_z                     for z in L_p,
    c(z)=1                          for z in L\L_p,
    c(u)=0                          for u in I,
    x_z>=0 integers, sum_{z in L_p}x_z=X_p, p in P*.          (5.3)

This covers a single positive terminal allocation as well as a split.
No uniqueness of the maximizing parent, and no d_p>=2 assumption, was
used.

## 6. Converse, zero scores and individual-function count

Take p in P* and an arbitrary weak composition of X_p into the d_p
coordinates indexed by L_p, and define c by (5.3). Each component after
deleting an edge of a finite tree contains a graph leaf: choose a vertex
farthest from its boundary endpoint. Every graph leaf here has a positive
pile, so both sides of every edge are occupied; there is no hidden
empty-branch substitution in this construction.

Every branch at p outside its leaf children is in the zero-excess
configuration, with message -a_B. A sibling leaf z sends

    g(1+2x_z)=x_z-1,

also when x_z=0. The sum of these messages is X_p-d_p. Since
D(p)=d_p+sum_{other B}a_B=X_p, the score at p is zero. For a sibling z,
the complementary effective input is 1-x_z<=1, so its reverse message is
g(1-x_z)=-1-2x_z, cancelling its pile exactly.

Scores at the remaining vertices are zero as well. To check this without
assuming it, propagate outward from p along a zero-excess branch. If
the child root u is nonleaf and A=sum of its forward child deficits,
its message toward its parent is -(3+2A). A zero parent score makes the
reverse effective input 3+2A, with transfer A. The score at u is therefore
0+A-sum a_i=0. If u is a leaf, the two messages are -1 and its pile is
one. Induction reaches every vertex. In particular a numerical-zero
occupied message is handled by g, not by the empty-state rule.

Thus every configuration (5.3) is nonstackable by the imported score
criterion. Its mass is lambda+2X_p=s-1. Combining with Section 5 proves
the exact inherited classification at the declared inputs.

For fixed p the choices are weak compositions of X_p into d_p labeled
leaf coordinates, hence there are binom(X_p+d_p-1,d_p-1) individual
configurations. Families for different parents are disjoint: their leaf
sets L_p are disjoint and X_p>0, so each configuration has a positive
excess on exactly its chosen sibling class. There is no quotient by
automorphisms. Therefore, for every n>=3,

    N(T)=sum_{p in P*} binom(X_p+d_p-1,d_p-1),
    X_p=sum_{u in I}deg_T(u)2^dist(p,u),
    E(z)=1+lambda+2X_p for z in L_p.                          (6.1)

All configurations counted in (6.1) have score zero at every target.

### Boundary conventions

For K2, the estimator gives s=3. Of the three mass-two functions, only
(1,1) has support on both vertices; it admits no move. Hence N(K2)=1.
The n>=3 sum must not be applied to K2, where both vertices are leaves
and its putative two parent families would overlap at zero excess.

For a star with d=n-1>=2 leaves, its core has one vertex, X_p=d and
P* consists of the center. Thus N(T)=binom(2d-1,d-1). For d_p=1 in
an arbitrary larger tree, its class contributes binom(X_p,0)=1. Tied
maximizing parents are all retained in the sum. The singleton tree is
excluded from the shared objective.

## 7. Provenance, limits and reproduction scope

The earlier classification is the
[immutable sibling source](https://github.com/helgithorskarp/math_results/blob/d4c0ebbc94ca2855f4fdc547549eed41d63d704c/tree_stacking_extremal_classification/README.md).
The full-degree core potential is also exposed in the
[corrected immutable core source](https://github.com/helgithorskarp/math_results/blob/80b058418b869fcee4762ae8d4ec930acc33e7a2/tree_stacking_global_growth/README.md).
Both URLs were fetched and the following text hashes verified in the audit:

| Prior file | Exact commit | SHA256 |
|---|---|---|
| Sibling README | d4c0ebbc94ca2855f4fdc547549eed41d63d704c | 725400c0263838bb584fca6a2951ff8fd75a31619bb1394201e08940144fcbf8 |
| Core README | 80b058418b869fcee4762ae8d4ec930acc33e7a2 | 02c41193ae367eae230456b0aaea79d9180e1d6cf6f2f6a4c066e5d06b56ee89 |

The immutable source versions are prior art. This component expands their
allocation, kink and potential arguments; it does not claim a new
classification. An editorial `,qquad` in the old classification display
does not alter its recurrence. The bad immutable commit link in the older
graph core body is resolved by the exact corrected version above. No
finite census, symmetric-broom optimizer assertion, or raw height balance
is a dependency here. In particular the known false h<=n-2d-1 route is
not imported.

Sections 2--6 are elementary exact derivations relative to the two stated
primary theorems. The branch majorant is proved here; it is not an
additional black-box input. No newly claimed mathematical computation,
solver, floating-point estimate, dataset or enumeration is used. Existing
finite classification checks are corroboration and were not repeated as
a substitute for this universal argument. No proof-assistant check or
external review of this component is asserted.

For an assembled global result, another component must independently
supply the universal structural/height bound, the analytic binomial
estimate with constants and range, and the eventual all-order lower
construction. None is accepted in advance by this classification audit.
