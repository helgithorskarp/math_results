# Exactly two supporting oriented quotients on at most six vertices

An oriented graph has neither loops nor opposite arcs. A **strong Seymour
vertex** `v` has a matching from `N+(v)` into the vertices `N++(v)` at directed
distance **exactly two**, covering all of `N+(v)`. The empty matching makes a
sink strong.

For an oriented quotient `Q`, positive real weights `w`, and root `p`, put

    O_p = N_Q+(p),
    Γ_p(S) = (union of N_Q+(u) over u in S) \ (O_p ∪ {p}),
    Δ_p(w) = max over S ⊆ O_p of [w(S) − w(Γ_p(S))].

The empty source supplies zero. Call a weighting **all-deficient** if
`Δ_p(w)>0` for every root. Crucially, `Γ_p(S)` may contain vertices
**nonadjacent** to `p`; replacing it by in-neighbors would be wrong here.

## Classification theorem

For a nonempty oriented quotient on at most six vertices, an all-deficient
positive real weighting exists if and only if it has exactly six vertices
and is isomorphic to one of these two quotients:

| root | out-neighbors in T | out-neighbors in H |
|---|---|---|
| 0 | 1,2,3 | 2,3 |
| 1 | 2,3,4 | 4,5 |
| 2 | 3,5 | 1,3,4 |
| 3 | 4,5 | 1,5 |
| 4 | 0,2 | 0,3,5 |
| 5 | 0,1,4 | 0,2 |

`T` is the previously classified Dzitsoev tournament. `H` has exactly one
missing pair, `{0,1}`. Its occurrence and complete weight description are
the new oriented-quotient case.

Every all-deficient weighting belongs to at least one of **twenty** explicit
strict Hall systems: twelve for `T`, eight for `H`. Each has matrix `A`
with rows `1_S − 1_Γ`, determinant `−1`, and an entrywise nonnegative
integer inverse. Consequently its weights have the exact parametrization

    w = A^(-1) d,       d ∈ R_(>0)^6.                         (1)

For integer weights, `d` ranges over `Z_(>0)^6`. These systems cover the
weight set; no assertion that their interiors are disjoint is needed.

For positive integer weights the sharp total-weight and minimum external
out-degree bounds are:

| quotient class | minimum total weight | minimum external out-degree |
|---|---:|---:|
| T | 36 | 13 |
| H | 51 | 18 |

The minimum-total vectors, unique in the displayed labelings, are

    T: (7,3,9,3,3,11),
    H: (3,8,16,3,7,14).

Thus a missing quotient arc costs at least 51 vertices in this class,
regardless of how large or unbalanced the six part sizes may be.
This is not an unrestricted minimum-order or minimum-degree theorem.

## The eight systems for H

At roots 0,2,4 the following Hall source and target are forced in every
feasible closed-row system:

| root | S | Γ |
|---|---|---|
| 0 | {2} | {1,4} |
| 2 | {1,3,4} | {0,5} |
| 4 | {0,5} | {2} |

Independently choose one of the two rows at each remaining root:

| root | first S → Γ | second S → Γ |
|---|---|---|
| 1 | {4,5} → {0,2,3} | {4} → {0,3} |
| 3 | {1,5} → {0,2,4} | {1} → {4} |
| 5 | {0,2} → {1,3,4} | {0} → {3} |

These `2^3` choices are exactly its eight feasible systems. In the row order
obtained by choosing first before second, their smallest integer weights are:

| choices at 1,3,5 | componentwise minimum w* | total |
|---|---|---:|
| first,first,first | 3,15,25,3,9,23 | 78 |
| first,first,second | 4,19,31,3,11,28 | 96 |
| first,second,first | 3,10,20,3,9,18 | 63 |
| first,second,second | 4,12,24,3,11,21 | 75 |
| second,first,first | 3,13,21,3,7,19 | 66 |
| second,first,second | 4,16,25,3,8,22 | 78 |
| second,second,first | 3,8,16,3,7,14 | 51 |
| second,second,second | 4,9,18,3,8,15 | 57 |

The attached `certificate.json` also gives all twelve systems of `T`, with
sharp totals `36,39,42,42,45,48,48,54,56,64,72,88`. Those tournament systems
are prior work, reproduced here as part of the enlarged classification.

## Hall reduction and strict alternatives

For any source `S ⊆ O_p`, define its closure by

    cl(S) = {u ∈ O_p : Γ_p({u}) ⊆ Γ_p(S)}.

It contains `S` and has exactly the same target. Positive weights imply
`w(cl(S))≥w(S)`, so every positive Hall deficiency has a nonempty closed
witness. There are finitely many such witnesses, independent of the weights.
Choose one closed witness at every root, giving a matrix `A`.

If some nonzero vector `c≥0` satisfies `c A≤0` coordinatewise, no positive
weight vector can satisfy `A w>0`: the weighted sum of its strict Hall
inequalities would be both positive and nonpositive. We call `c` a
multicover certificate. The following finite computation supplies one for
every rejected system; no converse to this elementary observation is assumed.
Every surviving system has an explicit positive `w*` with `A w*=1`.

## Exact finite coverage

For the fifteen unordered pairs on six labeled vertices, use ternary digits
in lexicographic pair order, with the first pair the least significant digit:

* 0: no arc;
* 1: smaller label points to larger;
* 2: larger label points to smaller.

There are exactly `3^15 = 14,348,907` labeled oriented graphs. The native
verifier iterates all their codes in increasing order. For each first unseen
code it applies all `6! = 720` label permutations, marks its entire orbit,
and then evaluates that representative. It explicitly checks every marked
image is at least the representative, every orbit size divides 720, and
that all labeled codes have been covered. This is exhaustive orbit marking,
not reliance on a graph-isomorphism library or a supplied graph list.

The exact resulting counts are:

| item | count |
|---|---:|
| oriented isomorphism types | 21,480 |
| types with a root having no nonempty closed witness | 13,348 |
| choices of one closed Hall row at every root | 235,526 |
| multicover-rejected systems | 235,506 |
| feasible systems | 20 |

For 235,505 rejected systems a multiplier lies in `{0,1,2,3}^6 \ {0}`.
One more system uses a permutation of `(1,1,1,1,4,4)`. The verifier searches
these 4,110 candidate multipliers and checks every inequality with exact
bounded integers. The remaining twenty systems match the attached positive
certificates exactly, up to an explicitly checked relabeling. There is no
weight bound, numerical feasibility tolerance, or solver inference in this
classification over **all positive real weights**.

To exclude fewer than six quotient vertices, suppose such an all-deficient
quotient existed and adjoin dominating vertices until its order is six.
Old Hall witnesses are unchanged: old vertices cannot reach a new vertex.
Each new dominating vertex has a nonempty source and empty target, so is
also deficient. The resulting six-vertex quotient has a source vertex,
whereas both `T` and `H` have positive in-degree at every vertex. This
contradicts the complete six-vertex classification.

## Integral cones, minima, and degree obstruction

For each of the twenty matrices, the checker verifies exactly that
`det(A)=−1`, `A^(-1)≥0`, `w*=A^(-1)1>0`, and
`λ=A^(-T)1>0`. The inverse is integral by unimodularity. Formula (1) follows:
positive `d` gives positive `w` because every row of an invertible
nonnegative matrix has a positive entry, and conversely `d=A w` is exactly
the chosen Hall-defect vector.

For integer weights satisfying the strict Hall system, `d≥1`, hence

    w = A^(-1)d ≥ A^(-1)1 = w*.

Thus `w*` minimizes every nonnegative linear objective componentwise.
In particular it minimizes total weight and each root's external out-degree.
Alternatively the explicitly checked positive identity `λ^T A=1^T`
gives `sum(w)≥sum(λ)=sum(w*)`; equality forces `d=1`, proving uniqueness
of the total minimum in each system. Taking the minima across the twenty
systems proves the two bounds in the theorem.

As an additional audit, for each root's out-neighbor incidence vector `r`,
the checker computes `β=A^(-T)r` exactly and checks `β≥0`, `β^T A=r^T`,
and `β^T1=r^T w*`. Thus all 120 degree bounds also have exact dual proofs.

## Transfer to oriented graphs with uniform parts

Let `D=Q[F_0,...,F_(k-1)]`: replace quotient vertex `i` by a nonempty oriented
graph `F_i`, put all arcs from `F_i` to `F_j` when `i→j` in `Q`, and put no
arcs between the two parts when their quotient pair is missing. Set
`w_i=|F_i|`. Suppose each `F_i` has at least one strong Seymour vertex;
independent sets and transitive tournaments both satisfy this hypothesis.

For a vertex `v` in part `i`, its matching link is the disjoint union of:

1. its internal matching link inside `F_i`;
2. the expanded weighted quotient matching link at `i`.

Indeed, an external out-part of `i` has no edges into part `i`, and part `i`
has no outgoing edges into any external exact second-neighbor part.
Consequently no matching edge crosses between these two link components.
External sources within a single part are twins. Hall deficiency on that
component is maximized by taking complete parts, giving exactly `Δ_i(w)`.
Therefore `v` is strong in `D` precisely when it is strong inside `F_i`
and `Δ_i(w)=0`.

Since each part has an internal strong vertex, `D` has no strong vertex if
and only if its weighting is all-deficient. The classification applies to
all such substitutions with `k≤6`, including arbitrary positive part sizes.
In particular their order is at least 36 and minimum out-degree at least
13. If a quotient pair is missing, their order is at least 51 and minimum
out-degree at least 18. Each vertex's degree is its external weighted
degree plus a nonnegative internal degree. Transitive and independent
parts realize both sharp bounds, using the displayed minimizing vectors.

This assumption on the parts is essential: allowing a no-strong graph as
a single part would place unrestricted counterexamples into the class.
The theorem classifies quotient mechanisms, not every oriented graph.

## Why coefficient four is needed

There is precisely one rejected system, up to the orbit enumeration's
labeling, that the coefficient bound three does not eliminate. A convenient
labeling has out-masks

    (12,20,32,6,5,27),

with the entire out-neighborhood chosen at every root. Its signed matrix is

    [ 0 -1  1  1  0 -1 ]
    [-1  0  1  0  1 -1 ]
    [-1 -1  0 -1 -1  1 ]
    [ 0  1  1  0 -1 -1 ]
    [ 1  0  1 -1  0 -1 ]
    [ 1  1 -1  1  1  0 ].

For `z=(1,1,4,1,1,4)`, both `Az=0` and `z^T A=0`, and `rank(A)=5`.
The checker verifies the identities and a nonzero 5-by-5 minor exactly.
Since `z>0`, any nonnegative row multiplier `c` with `c^T A≤0` must in
fact have `c^T A=0`: dotting with `z` forces equality in every coordinate.
The left kernel is one-dimensional, so every nonzero such integer vector
is a positive integer multiple of the primitive vector `z`. Its largest
coefficient is at least four. Thus coefficient four is necessary, as well
as sufficient for the stated finite multicover classification.

## Verification and trust boundary

`orbit_audit.cpp` supplies exhaustive labeled-graph coverage and integer
multicover checks. `verify.py` compiles it in a temporary directory, matches
every surviving system to the certificate, and checks the exact inverse,
determinant, primal, total dual, and degree-dual identities with `Fraction`.
Four deliberately invalid certificates or incomplete survivor lists are
rejected. The full native computation also passes address and undefined
behavior sanitizers.

`independent_check.py` imports no primary checker code. It builds all
oriented graphs by vertex augmentation and pynauty isomorphism reduction,
obtaining counts `1,2,7,42,582,21480`. It checks **every** native orbit against
that independently generated set, with its automorphism-derived orbit size
and individual Hall-system count. It generates closed rows from subsets
of the right side, instead of the primary source-subset algorithm, and
checks every Hall system using separate bounded NumPy integer calculations.
Determinants and inverses are checked by permutation/cofactor expansion,
not the primary elimination routine. It also expands both minimum vectors
with independent and transitive parts and directly checks all 174 vertices
by exact-distance maximum matching.

In the native checks all ternary codes are below `3^15<2^24`, row entries
are in `{-1,0,1}`, and multicover dot products have absolute value at most
24. The secondary integer-array products use signed 16-bit entries, safely
within these bounds. No floating optimization, SAT/MILP status, random
search, or bounded weight enumeration enters the proof.

The finite classification trusts the written Hall and substitution
reductions, inspection of the executable source, compiler/interpreter
semantics, and hardware. It is not a proof-assistant formalization. The
second audit additionally trusts pynauty and NumPy; the primary proof path
needs neither. Both implementations were written by the author, and no
independent peer acceptance is claimed. The labeled orbit bitmap and
verbose audit stream are regenerated in memory or temporary storage and
are not required external artifacts.
