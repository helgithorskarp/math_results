# Internal check of the exact inherited classification audit

Checker: Atlas, agent ID `studio-researcher-1`, researcher.
Author: Iris, agent ID `studio-researcher-2`, researcher; author task19.
Date: 2026-10-05, checker workday6. Author transfer284, following the
explicit EMPTY/equality feedback283 and my prior independent preparation.

**Verdict: ACCEPT Sections1--7 of this exact version at its two declared
primary-theorem inputs.** The ordinary argument establishes the inherited
classification of every critical nonstackable configuration, its exact
individual-function count, the full-tree degree normalization, all tied
maximizing parents, stars/d=1, and the separate K2 convention. It also
proves that every critical configuration has score zero at every target.
No mathematical defect was found within this scope.

This is an internal team check, not external peer review, a new
classification discovery, a proof-assistant check, or acceptance of the
global asymptotic, structural/analytic/lower modules or historical priority.
No mathematical computation or unchanged census was run for this check.

## Frozen inputs and primary boundary

All three source files were copied without edits and hash/size verified.
`INPUT_RECEIPT.json` maps the author paths to the copied inputs.

| File | Bytes | SHA256 |
|---|---:|---|
| PROOF.md | 17680 | e49e654abe3ae31e360033541aae4a58d93119a91f6ab400095f17d92e00427f |
| README.md | 1420 | e564ba540dfe8b9cf7dc422a10d738daeb91516ae1a35b05054f3046ca4ed5cf |
| SOURCES.json | 3693 | 6d5d793c6d0b25b65f5613cfee67f752d9acb2307100fce044480a862319dabc |

The unchanged author handoff has SHA256
0bcefa6a36e0802fa922d31fcad3134b377ce4800d26565519cbcd2e3ad60d9f.
I read the complete proof, README and source inventory, not just transfer284.

The external mathematical inputs are Fairfax-Ball,
[arXiv:2609.31811v1](https://arxiv.org/html/2609.31811v1), Theorem3.3
(exact rooted score criterion, with arbitrary legal move order) and
Theorem1.1 (the least-k>=2 exact-mass estimator). Its definitions and
Sections2--4/6 were independently read in the primary text in preparation
for this version. These ordinary published theorems are imports; this
check does not reprove arbitrary-move necessity or audit the paper's
reported Lean/mechanical-verification environment.

Corollary6.2 in that paper compares maximal masses. It does not classify
every extremizer or assert that every extremizer is zero-score. Iris's
Sections3--6 establish those stronger conclusions here, rather than
incorrectly treating the corollary as an additional imported theorem.

## 1. Independent normalization and maximum-leaf check

For an oriented branch rooted at v with external neighbor p, a
nonterminal root has k children and full-tree degree k+1. Substitution in
the deficit recurrence gives constant3+2k = 1+2deg_T(v), with four
times the child-rooted descendant sums. Therefore

    a(v->p)=1+2 sum_{u in B(v|p), u nonleaf}deg_T(u)2^dist(v,u).

The terminal branch has deficit1 and empty nonleaf sum. Summing at an
internal vertex gives D(v)=W(v); at a leaf it gives D(v)=1+W(v).
Thus E(v)=1+lambda+W(v) uniformly. For a leaf z at nonleaf p,
W(z)=2W(p), so its score is1+lambda+2X_p. This independently verifies
that the deficit score is exactly the primary distance/degree estimator,
including its leaf correction, rather than a changed normalization.

For an internal vertex of degree k>=2, the side contributions Q_i sum
to W(v)-k. Some Q_i is less than W(v)/2. Moving across that edge doubles
the complement and halves the side, giving
W(neighbor)=2W(v)-(3/2)Q_i>W(v). Hence a global maximum is at a graph
leaf, and every internal root has E(v)<s. This uses full-tree degrees;
replacing them with core degrees would break both identities.

P* retains all parents of maximum-score leaves. Every such parent is a
nonleaf at n>=3, d_p>=1, and X_p=W(p)>=deg_T(p)>=2. No uniqueness,
core-endpoint theorem, or assumption d_p>=2 is used.

## 2. Inverse transfer, majorant and EMPTY slack

I checked the actual preimages of the nonmonotone transfer function.
For an occupied branch and m<=-1, the effective input is
t=(m+3)/2<=1. For m>=0, its largest preimage is2m+3; the even preimage
2m exists only for m>0. In particular g(2)=1 and g(3)=0, so a
monotonicity argument would be invalid. The input proof uses these
preimages, not such an argument.

With A=sum child deficits, a=3+2A, x=m+a, and local budget
y=c(root)+sum child excesses=t+A, the two regimes give exactly
y<=b_a(x). At a terminal branch the maximal pile at excess x is the
odd pile1+2x; an even pile is smaller by three. The functions are
majorants on all real x>=0; no unattested attainability at every x is
needed for the proof.

The EMPTY branch remains a separate recursive state. Its numerical
contribution is zero, hence its budget excess is a, not zero. Its mass
is0<F_B(a), since F_B(a)>=ell_B>=1. Every cut component contains a
graph leaf, so the last inequality is valid. This explicit strict slack
repairs the ambiguity in a bare m+a notation. An occupied numerical
zero message instead uses the ordinary inverse rule, as required by
the primary theorem.

For a nonterminal occupied branch, the child bounds and root pile give
mass<=ell_B+c(root)+sum G_i(x_i). The convex allocation inequality
bounds this by ell_B+K_B(y), and strict monotonicity bounds it by
ell_B+K_B(b_a(x))=F_B(x). Every G is convex, strictly increasing and
zero at zero: these properties survive the finite maximum with the
identity and composition with the increasing convex b_a. Thus both
the mass bound and the strictness conclusions used later are justified.

At zero excess, y<=b_a(0)=0 forces the root pile and all child excesses
to vanish. Induction gives the unique side-branch equality configuration:
one pebble at every graph leaf, zero at every internal vertex. It cannot
be EMPTY. This uniqueness is needed for exhaustion, not merely the
numerical bound on mass.

## 3. Exact global boundary and the kink/chord step

I reconstructed the boundary evaluation independently before reading the
frozen proof, then matched every hypothesis against this version. For
nonleaf boundary p and nonterminal child v, let a=3+2O and
D(p)=a+P, P>=1. Direct substitution gives

    b_a(D(p))=3+O+2P=D(v).

For a terminal child v, G_B(D(p))=2D(p)=E(v)-1-lambda. Recursion then
gives the precise identity

    G_B(D(p))=max_{u in B}(E(u)-1-lambda).

The root-pile term is D(r)=E(r)-1-lambda, so K_r(D(r)) is exactly
Q=s-1-lambda. For a critical nonstackable configuration the score
criterion gives Y=c(r)+sum x_B<=D(r). In the full mass chain

    |c|<=lambda+c(r)+sum G_B(x_B)
       <=lambda+K_r(Y)<=lambda+K_r(D(r))=s-1,

both endpoints are s-1. Each child bound is sharp, EMPTY is excluded,
and Y=D(r) follows from strict increase. In particular S_r=0. This
argument uses only the exact threshold theorem and score criterion,
not configuration-wise monotonicity or a finite table.

At the nonterminal kink x0=a-1, the input y0=(a-1)/2 is positive.
For convex K with K(0)=0 and K(y)>=y, its left derivative at y0 is
at least the secant K(y0)/y0>=1. The one-sided slopes after composition
are(1/2)K'_-(y0) and2K'_+(y0), strictly different. The outer maximum
cannot erase this kink. Also D(p)>=a+1, so it lies inside the boundary
interval [0,D(p)].

For completeness, equality at an interior point of a convex endpoint
chord forces affinity on its whole interval. Subtract the chord to get
a convex function nonpositive on the interval, zero at both endpoints
and the alleged interior contact. Expressing that contact as a convex
combination of any point to its left with the right endpoint, or the
left endpoint with any point to its right, forces the function to be
zero at every point. Thus the genuine kink makes the allocation chord
strict at every interior positive allocation.

The root-pile identity has endpoint D(r)<Q, because internal vertices
never maximize E. It cannot receive positive mass at critical equality.
A nonterminal branch cannot receive a positive allocation smaller than
the full budget. Hence either the positive excess splits only among
terminal siblings, or one nonterminal branch receives it all.

## 4. Exhaustion and the non-backtracking equality walk

If the whole budget goes to one nonterminal branch, sharpness and strict
increase force its transformed budget to equal D(v), with all child
bounds sharp. The same endpoint/chord analysis applies again at v.
The parent-side deficit is part of D(v), so each child's complement
has P>=1; the kink remains strictly inside the next budget interval.

The branches followed from the initial internal root are strictly nested.
The proof never reroots into the preceding side or follows a cycle.
Every unused side branch has zero excess and the unique unit-leaf
configuration. Every internal vertex visited by the walk has pile zero.
The complementary parent-side component therefore also has zero excess;
no unaccounted heavy pile is lost at a later step.

Finiteness forces a final internal p with positive terminal allocations.
If p is the initial root, all its neighbors are considered children.
Otherwise its preceding neighbor is internal, so every graph-leaf
neighbor is still a forward child. Thus these terminal coordinates are
exactly L_p, including those assigned zero. Their sum is D(p)=X_p and
their common endpoint value is2D(p)=Q. Consequently E(z)=s for every
z in L_p, so this p is genuinely in P*. This verifies the subtle full
sibling-set issue in the final split, including a single positive
terminal coordinate. All tree vertices have been accounted for.

It follows that every critical obstruction has positive odd sibling
piles1+2x_z, sum x_z=X_p, unit pebbles on the other graph leaves, and
zero internally. This proves exhaustion; it is not inferred from a
majorant's attainability, an optimizer assertion, or a census.

## 5. Converse, all-target zero scores and labeled count

For such a sibling configuration every graph leaf is occupied, and both
sides of each edge contain a graph leaf. Thus every branch involved in
the converse is occupied. A sibling sends x_z-1. Their aggregate is
X_p-d_p, cancelling the other branch deficits at p because D(p)=X_p.
The score at p is zero. The complementary effective input for sibling
z is1-x_z<=1, giving reverse message-1-2x_z and score zero at z.

Outward along every other branch the unit-leaf configuration sends
-a_B. At an internal child with forward deficit sum A, the zero parent
score supplies reverse effective input3+2A and reverse message A,
cancelling the forward messages. At a leaf, its unit pile cancels
message-1. Induction reaches every vertex, proving all-target zero
scores without an EMPTY substitution. The score criterion therefore
proves nonstackability, and the mass islambda+2X_p=s-1.

The weak compositions index individual leaf coordinates, so the class
has binom(X_p+d_p-1,d_p-1) configurations. Different parents' leaf sets
are disjoint and X_p>0, so two such families cannot overlap. Hence the
exact sum over all tied P* is valid with no automorphism quotient.
The converse plus exhaustion proves the stronger all-critical-zero-score
assertion at the declared two-theorem boundary.

For a star d=n-1>=2 the sole parent has X=d, giving
binom(2d-1,d-1). For d_p=1 a class contributes one. K2 has empty core
and is separate: estimator/threshold3 and unique nonstackable mass-two
configuration(1,1). Applying the n>=3 parent sum to K2 would duplicate
the zero-excess family, which this source correctly avoids. Singleton
trees are outside the objective; the least-k>=2 convention is retained.

## 6. Provenance and excluded scopes

I fetched all eight immutable files in SOURCES.json afresh. Every response
was200 and matched its declared size, SHA256 and local repository bytes;
SOURCE_RECEIPT.json records each URL, commit and comparison. The sibling
README is725400c0... at d4c0ebbc94ca2855f4fdc547549eed41d63d704c;
the core README is02c41193... at the verified corrected commit
80b058418b869fcee4762ae8d4ec930acc33e7a2. The older malformed graph URL
and editorial `,qquad` do not enter the proof. File integrity alone is
not a correctness verdict on the excluded old code/censuses.

The inherited classification and potential remain prior art. I did not
run the predecessor census, transfer/classification code, a solver,
formalizer, raw move oracle, or new finite control. The independent
ordinary reconstruction above checks the universal new audit at its
explicit inputs. Its accepted scope does not include the separate
structural budget, binomial upper, all-order lower, final assembled theorem,
optimal trees/linear terms, formal verification, external review or priority.
The exact source bytes are unchanged; any future substantive repair needs
a preserved new version and corresponding new-version check.
