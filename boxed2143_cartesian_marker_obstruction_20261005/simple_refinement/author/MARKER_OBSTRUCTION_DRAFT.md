# Author draft: unbounded viable rank choices in one Cartesian-tree fiber

Author: Sage / literature-researcher-1. Date: 2026-10-05. Decision 410 remains the full boxed-2143 growth problem. This packet is a partial obstruction to a proposed bounded-branching proof route, awaiting Theo's independent full-scope check. It proves neither an exponential upper bound nor superexponential avoidance growth. The generic Cartesian/linear-extension encoding is known prior work, not a novelty claim.

Throughout, positions in the mathematics are one based; code uses zero-based positions. A boxed occurrence has positions p<q<r<s with values at q<p<s<r and no unselected point strictly inside its open bounding rectangle.

## 1. Marker construction and exact occurrence correspondence

Let m>=2 and sigma be any permutation of [m]. Put n=3m-2, and define

    X_i = m-1+sigma_i             (1<=i<=m),
    L_i = i                     (1<=i<=m-1),
    H_i = 2m-1+i                (1<=i<=m-1).

The three value bands are disjoint and cover [n]. Set

    Phi(sigma) = X_1,H_1,L_1,X_2,H_2,L_2,...,
                 X_(m-1),H_(m-1),L_(m-1),X_m.

Thus X_i is at position 3i-2, H_i at 3i-1, and L_i at 3i. Low markers and high markers each increase with their indices. The m=1 case is the identity permutation and will be used only as a boundary control.

**Claim 1.** The map (i_1,i_2,i_3,i_4) -> (3i_1-2,3i_2-2,3i_3-2,3i_4-2) is a bijection from boxed-2143 occurrences in sigma to those in Phi(sigma). In particular, Phi(sigma) avoids if and only if sigma avoids, and the map is injective and recoverable by reading the X positions and subtracting m-1.

**Proof.** First, a putative occurrence cannot select a low marker as its minimum.

Suppose its minimum is L_j. Any earlier low marker has value below L_j, so the first selected value cannot be low. The last selected value cannot be high: if the selected maximum is free, every high is above it; if the maximum is H_k, every later high is larger than H_k. The last selected value is therefore free (it cannot be low while exceeding a free/high first value). The first selected value must also be free, since every high exceeds every free. The selected maximum is free or high. Write the last point as X_t. Necessarily t>=j+2, because L_j and X_(j+1) are consecutive positions and a selected maximum must lie strictly between the minimum and last point. Hence L_(j+1) exists, lies strictly between the first and last positions, and has value strictly between L_j and the selected maximum. It is unselected, so it blocks the rectangle. This excludes the low-minimum case. Since every low is below every other band, any occurrence selecting a low would have a low minimum and is excluded.

Next, suppose an occurrence selects a high. Its maximum must be a high H_j. There are no selected lows by the preceding case. Its last point cannot be a high, since high values increase with position; thus its last point is free. Its first and minimum points are then free as well, by the required value order. Write the first and minimum points as X_i and X_k. Their positions give i<k<=j, so j>=2 and i<=j-1. The point H_(j-1) lies strictly between X_i and the last selected free point. Its value is above the selected minimum and below H_j. It is unselected and blocks the rectangle. This excludes the high-maximum case and hence every selected high.

Every occurrence therefore uses four free points. All intervening markers are outside their vertical value range. The relative values and positions of the free points are exactly those in sigma, so rectangle emptiness is equivalent before and after applying Phi. This proves both directions, the stated bijection and decoding. QED.

## 2. A common tree pair for all inputs of a fixed size

The minimum Cartesian tree has a low-marker right spine L_1,...,L_(m-1). Each L_i has left child X_i; each X_i for i<m has right child H_i; the last low marker has right child X_m. Equivalently:

    parent_min(L_1) = none,
    parent_min(L_i) = L_(i-1)       (2<=i<=m-1),
    parent_min(X_i) = L_i           (1<=i<m),
    parent_min(H_i) = X_i           (1<=i<m),
    parent_min(X_m) = L_(m-1).

The maximum Cartesian tree has a high-marker left spine H_(m-1),...,H_1. H_1 has left child X_1; H_i has right child X_(i+1), and X_(i+1) has left child L_i. Equivalently:

    parent_max(H_(m-1)) = none,
    parent_max(H_i) = H_(i+1)       (1<=i<m-1),
    parent_max(X_1) = H_1,
    parent_max(X_i) = H_(i-1)       (2<=i<=m),
    parent_max(L_i) = X_(i+1)       (1<=i<m).

**Claim 2.** These are the Cartesian trees of every Phi(sigma); their shapes are independent of sigma.

**Proof.** The specified left/right children have inorder sequence exactly Phi's positions. All minimum-tree parent values are smaller than their child values, by L_i<X_j<H_k and the increasing low spine. All maximum-tree parent values are larger, by the same band ordering and the increasing high values. For distinct labels, an ordered binary tree with fixed inorder positions and the minimum (respectively maximum) heap property is the Cartesian tree: its root is the interval minimum (maximum), and the assertion recurses on its left and right intervals. Thus both parent descriptions hold for every ordering of the free values. QED.

For completeness, the rank-assignment fiber of an arbitrary fixed tree pair is exactly the linear extensions of the union of its minimum-parent<child and maximum-child<parent constraints. Necessity is the heap property; sufficiency is the same recursive-extremum argument. This is an elementary instance of the known Cartesian/Baxter-congruence framework, not a new encoding claim.

## 3. Unbounded numbers of viable next rank positions

A rank prefix fixes the positions of successive values 1,...,r in a tree-pair fiber. A position is *viable* for the next rank if some complete boxed-2143-avoiding permutation with that same pair and prefix assigns the next rank there. Viability is stronger than availability in the heap poset; it includes the existence of a complete avoiding extension.

**Claim 3.** For every m>=2, the common pair in Claim 2 has a prefix of m-1 ranks with exactly m available positions, all m of which are viable. Hence no constant B bounds viable next-rank positions uniformly over all pairs and feasible prefixes.

**Proof.** Assign ranks 1,...,m-1 to L_1,...,L_(m-1). This is the prefix of every Phi(sigma). The incoming constraints on each X_i come only from low markers, so all X_i are available. Each H_i has incoming constraints from X_i and X_(i+1), so no high is available while all free positions are unassigned. The available set is exactly {X_1,...,X_m}.

For each t in [m], choose sigma^(t) with its value 1 at position t and all other entries 2,...,m increasing from left to right. Every inversion in sigma^(t) has the same lower endpoint, its 1. A classical 2143 needs two disjoint inversion pairs, so sigma^(t) has no classical 2143, and therefore no boxed 2143. By Claim 1, Phi(sigma^(t)) avoids. It has the fixed pair of Claim 2 and the common low prefix, and assigns the next rank m to X_t. Thus all m positions are viable. Given any proposed constant B, choose an integer m>B. QED.

This refutes the generalization of the failed binary-end-choice rule to *any constant number of viable next ranks*. It does not refute uniform exponential bounds on total avoiding fiber sizes: many choices at one prefix can be compensated by restricted continuation. It does not prove the agreed negative growth answer.

## 4. Exact scope and why this matters to the lane

The band-restricted slice of this one common fiber consists of the m! Phi images. Its avoiding subset has size exactly a_m, by Claim 1. Consequently the fiber problem retains the original boxed-avoidance entropy at a linear length change; the marker map repairs no forbidden input and cannot provide the arbitrary-input lower-bound completion sought by Lyra.

The construction eliminates a genuinely specified local proof strategy: bounding each viable rank-choice set by a fixed constant and multiplying those bounds. A successful fiber upper proof would require a different weighted, aggregate, or global encoding argument. No target pivot, narrower success criterion or completion request follows.

## 5. Evidence and prior work

The uniform proofs above are the mathematical arguments. Finite controls test occurrence sets, explicit tree formulas, decoding and viable-position witnesses through the documented ranges using both Lyra's literal checker and Theo's independently derived rectangle checker. They do not establish infinite quantifiers. Byte versions are frozen in received/CHECKER_SNAPSHOTS.json. There is no solver, floating point, heuristic search or imported certificate in the proof.

Relevant known framework: Giraudo, https://arxiv.org/pdf/1204.4776 , Proposition 4.10 and Theorem 6.3; Chakraborty et al., https://doi.org/10.4230/LIPIcs.ISAAC.2024.17 . Theo's increasing-block inflation packet is a different construction; no priority claim is made for this marker map without a targeted source refresh.
