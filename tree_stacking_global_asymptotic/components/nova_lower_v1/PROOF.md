# An explicit eventual all-order lower component for Statement B

Author: Nova. Agent ID: studio-researcher-3. Role: researcher.
Date: 2026-10-05. Shared task: research-room17.
Status: author proof for an exact-version internal check by Rowan; no
assembled global theorem, historical-priority or publication verdict.

## Statement and conventions

A move removes two pebbles from a vertex and places one at an adjacent
vertex. A stack has nonempty support consisting of one vertex. For a finite
tree T with at least two vertices, stack(T) is the least integer k>=2 such
that every configuration of exactly k pebbles can reach a stack. Let N(T)
count individual nonstackable functions c:V(T)->Z_{>=0} of mass stack(T)-1,
without quotienting by automorphisms. Write M(n)=max_{|V(T)|=n} N(T).

For every integer n>=37, this component constructs a tree T_n of order n
and proves

    log_2 M(n) >= log_2 N(T_n) > (5/36)n^2-(5/4)n.       (L1)

Thus one permitted explicit lower choice in agreed Statement B242 is
C_minus=5/4 and n0=37. This is an explicit audit of an inherited restricted
construction. Neither its R-family nor its leading coefficient is claimed
as newly discovered here, and no optimal linear coefficient is asserted.

## Stable inputs and mathematical trust boundary

The construction and parameters are from the immutable predecessor:

https://github.com/helgithorskarp/math_results/tree/1c8b93869f785981f0f5b73a6a7253cd1a923a97/tree_stacking_branched_broom_all_orders

Its README SHA256 is
84d9fc9f2b5f80f544d0f4d5559a1ca259b9e77daba4524388e6567cf5071aa3.
The exact committed graph body is
bafkreignyano56e7pvwihgprbljwwnsv2z4lcwc7f3ryvqfjcvhsh5vy5y,
body SHA2561b3b87e4e407cc993e972dee2d3309abcb54b417e7294e0b3c32bf4a5698f825.
Its linear-error review is
bafkreih76pzukitjoutfawrvr5hpldol2uwl2bov6qfr5noiy2cnlpazem,
body SHA256ec10938ecce4b2777c343f1bdee998a06a5f5d27a507460a69d70cc3988cff80.
Those bodies are retained from the successful workday4 read at height10339.
No present commitment or fresh graph-queue assertion is inferred.

The primary input is J. Fairfax-Ball, *The stacking number of a tree*,
arXiv:2609.31811v1:

https://arxiv.org/html/2609.31811v1

We use its Section2 definitions and estimator identity(4), Theorem1.1
(the estimator formula), Theorem3.3 (the exact score criterion), and
Theorem4.1 (the canonical zero-score configuration). These are explicit
ordinary mathematical imports. This component does not independently
reprove the arbitrary-move transfer theorem, claim a new formalization,
or audit the paper's reported formal-verification environment.

The redistribution direction is also in the inherited sibling result:

https://github.com/helgithorskarp/math_results/tree/d4c0ebbc94ca2855f4fdc547549eed41d63d704c/tree_stacking_extremal_classification

README SHA256725400c0263838bb584fca6a2951ff8fd75a31619bb1394201e08940144fcbf8.
Its graph artifact is
bafkreigrlfot45gncrzuggfqitcuxbwmxdwto2kav4srp47b6zbmslfl5u.
We reconstruct the sufficient construction below. The lower bound only
needs these distinct constructed critical configurations. Exact equality
N(T_n)=the displayed binomial would additionally use the converse
classification; no such equality is required or claimed in this proof.
Iris's separately checked inherited-classification audit remains an
obligation for the global upper/assembly. The predecessor's554 finite
symmetric-broom comparisons and optimizer/onset results are also outside
the logical inputs of(L1).

## 1. Literal tree, full degrees and maximizing leaves

For positive integers d,e,t, form R(d,e,t) from the t-edge path

    p=v_0-v_1-...-v_t=q,

attach d new leaves at p, and attach e disjoint two-edge arms q-a_i-b_i
at q. All named/new vertices are distinct. The order is d+2e+t+1, the
graph leaves are the d leaves at p and the e vertices b_i, and their
number is L=d+e. The full-tree degrees of p,q,a_i and interior path
vertices are respectively d+1,e+1,2 and2. These formulas include t=1.

Let C be the nonleaf core and define, for any vertex v,

    Phi(v)=sum_{u nonleaf} deg_T(u) 2^dist_T(v,u).

Use full-tree degrees; a core degree is a different statistic. For a
core vertex x, write X_x=Phi(x). Primary identity(4) says

    E_T(v)-1=L+Phi(v),    stack(T)=max_v E_T(v).          (L2)

For completeness, this potential has no maximum at a nonleaf. At a
nonleaf v of degree D>=2, let S_w be the sum of terms of Phi(v) over
the component on the w-side of each incident edge vw. Then

    sum_{w~v} S_w=Phi(v)-D,
    Phi(w)=2Phi(v)-(3/2)S_w.

One w has S_w< Phi(v)/2. Indeed the average is
(Phi(v)-D)/D <=(Phi(v)-D)/2<Phi(v)/2. For that w,
Phi(w)>(5/4)Phi(v)>Phi(v). The positive weight at v ensures Phi(v)>0.
Thus any global maximizing vertex is a graph leaf. At a leaf z with
parent x, Phi(z)=2X_x. Consequently comparing the leaf-parent potentials
finds the global maximum of E, including any ties.

In R there are only two leaf-parent types: p and a_i. Summing the full
degrees along the literal paths gives

    X_p=(d+1)+2sum_{j=1}^{t-1}2^j+(e+1)2^t+2e 2^{t+1}
       =d-3+(5e+3)2^t,                                  (L3)

    X_a=(d+1)2^{t+1}+2sum_{j=1}^{t-1}2^{t-j+1}
          +2(e+1)+2+8(e-1)
       =(d+3)2^{t+1}+10e-12.                            (L4)

The middle sum is empty when t=1; the other-arm term is zero when e=1.
No leaves contribute to these sums. Their difference is

    X_p-X_a=(5e-2d-3)2^t+d-10e+9.                       (L5)

Distances between core vertices agree with distances in T. For this tree
the eccentricity of p in the core is t+1, since a_i are one edge beyond
q; its graph-leaf eccentricity is t+2. Neither height is the structural
deficit used in the next section.

## 2. Distinct critical configurations: sufficiency and count

Suppose X_p>X_a. Every leaf at p maximizes E, and(L2) gives

    stack(R)=L+2X_p+1.                                  (L6)

For every weak composition (x_z) over the d individual leaves at p with
sum_z x_z=X_p, put 1+2x_z pebbles at those leaves, one at each b_i, and
zero at all nonleaves. Its mass is L+2X_p=stack(R)-1.

Here is the sufficient nonstackability argument, with the exact primary
message convention. An occupied branch of effective input s sends

    F(s)=2s-3                       if s<=1,
         s/2                        if s>=2 is even,
         (s-3)/2                    if s>=3 is odd.

At a vertex v the score is its pile plus all incident branch messages,
where an empty branch contributes zero but remains distinct from a
nonempty branch with zero message. Theorem3.3 identifies stackability
at v with a strictly positive score.

Start with all X_p at one selected leaf z_0, so its pile is1+2X_p;
all other graph leaves have pile1. This is exactly the canonical
configuration of Theorem4.1 at z_0: in primary notation
sigma_T(z_0)-1=1+Phi(z_0)=1+2X_p. All its scores are zero.

After redistribution each sibling leaf has message

    F(1+2x_z)=x_z-1,

including x_z=0. Their aggregate into p is still X_p-d. All branches
outside those sibling leaves retain their original data; a recursion from
p shows that their messages and all scores outside that leaf set are
unchanged. In particular the score at p is zero. For an individual
redistributed leaf z, the complementary input at p is

    0-(x_z-1)=1-x_z.

The p-side is occupied, since it contains other graph leaves (e>=1).
It therefore sends F(1-x_z)=-1-2x_z. This cancels the pile1+2x_z,
so every leaf score is also zero. The exact score criterion proves that
each constructed configuration is nonstackable.

Different weak compositions give different vertex functions. Their number
is the ordinary stars-and-bars count

    binom(X_p+d-1,d-1).

No automorphism quotient or sum over nonmaximizing parents is taken.
Hence the sufficient result is

    N(R(d,e,t)) >= binom(X_p+d-1,d-1).                   (L7)

## 3. Every sufficiently large order and strict parent eligibility

Given an arbitrary integer n>=37, uniquely write

    m=floor((n-1)/18),    s=n-1-18m,
    n=18m+1+s,           m>=2, 0<=s<=17.

Choose the predecessor's parameters

    d=5m+3,   e=2m+2,   t=9m-7+s.                     (L8)

They are positive, t>=11, and their literal order is

    d+2e+t+1=18m+1+s=n.

All residues are covered: each fixed m gives exactly the consecutive
orders18m+1 through18m+18, and the next block begins at18m+19.
In(L5) the parameters give

    X_p-X_a=2^t-(15m+8)>0.                             (L9)

For the strict inequality, first2^11=2048>38 at m=2,s=0. If
2^{9m-7}>15m+8, the next exponential multiplies by512, and

    512(15m+8)-(15(m+1)+8)=7665m+4073>0.

Induction proves the claim for every m>=2, and s>=0 only increases the
exponential. Thus the maximizing-parent condition required in(L6)--(L7)
holds uniformly, without a finite extrapolation or a large-height cutoff.

Put r=d-1=5m+2 and Y=X_p+r. Direct substitution gives

    Y=(10m+13)2^t+10m+2,
    Y/r>2^{t+1},                                      (L10)

because10m+13>2(5m+2) and the additive term is positive. Both are
positive integers with Y>=r>=1.

## 4. Binomial and explicit linear remainder

For integers Y>=r>=1, the product formula yields

    binom(Y,r)=product_{i=0}^{r-1} (Y-i)/(r-i)
               >=(Y/r)^r.

For each i the displayed comparison is equivalent to i(Y-r)>=0.
Combining(L7), (L10) and this inequality gives

    log_2 N(T_n) > r(t+1)
                  =(5m+2)(9m-6+s)=:A(m,s).            (L11)

The exact polynomial identity is

    36[A(m,s)-(5/36)(18m+1+s)^2+(5/4)(18m+1+s)]
       =198m-392+s(107-5s).                           (L12)

For m>=2, the first part is at least4; for0<=s<=17 the second
part is nonnegative since107-5s>=22. Thus(L12) is strictly positive.
Equations(L11)--(L12) establish(L1) for every integer n>=37, with
explicit C_minus=5/4. No approximate logarithm, floating-point constant,
Stirling asymptotic, restricted optimizer, or earlier-order census is used.

## 5. Reproducibility and exact scope of finite controls

check_lower.py is a new bounded author-side control. It imports no
predecessor module/output. It constructs literal adjacency lists, computes
every Phi(v) by direct breadth-first search over ambient distances and
full degrees, compares directed structural-deficit recursions, verifies
leaf-max eligibility, and checks several literal redistributed families
using a separate iterative EMPTY-aware message computation. Exact integer
binomial comparisons and coefficient dictionaries check(L10)--(L12).
Its all-residue sampled orders and boundary/losing-parent controls are
documented by the generated RESULT.json. The output reports integer hashes
and bit lengths instead of printing enormous counts.

These bounded controls corroborate the proof and expose implementation
mistakes. They are not an infinite computation, raw legal-move reachability
oracle, independent researcher check, or proof of converse classification.
The universal conclusion follows from the written argument at its explicit
primary-input boundary. Rowan's separate exact-version internal check is
still required. All arithmetic in the control is integer/Fraction; timing
and platform metadata are separate. One standard-library process is used,
with no solver, external dataset, randomized sampling or native threads.

The combined global theorem additionally needs the separate uniform upper,
inherited equality/source audit and final assembly. This component gives
only the lower side and its precise source/constant/range interface.
