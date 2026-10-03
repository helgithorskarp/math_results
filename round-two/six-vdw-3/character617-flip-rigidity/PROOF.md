# At least 22 edited columns for a prime 617 character extension

Actual author: **six-vdw-3**, role **researcher**, 2026-10-03. This is an exact finite-certificate lemma with ordinary combinatorial bridges. The separate generator and verifier are implementations by the same author; external review and formalization are not claimed.

Let p=617 and let L(x)=0 for a nonzero square in F_p and L(x)=1 for a nonsquare. L(0) is undefined. A binary coloring c of [1,N] has an affine-character baseline

    b(n)=sigma XOR L(n-r), for n mod617 !=r,

where r is an arbitrary marked field root and sigma is a constant palette bit. Colors at every actual occurrence of r are entirely arbitrary and need not repeat. This includes every single affine input L(an+b) with a!=0: write r=-b/a and absorb L(a) into sigma. Extra columns may have arbitrary colors at individual integer positions, without any periodicity assumption.

Define the **actual flip columns** F as the nonroot residues q for which at least one actual point n in [1,N] with n mod617=q has c(n)!=b(n). Padding a template with free columns that remain unchanged does not enlarge F.

**Lemma.** If N>=3702 and c has no monochromatic nonconstant seven-term arithmetic progression, then either F is empty or **|F|>=22**. Consequently every AP7-free coloring of [1,3704] obtained from a single constant-phase affine character needs at least **22 additional nonroot edited columns**, or at least 23 free columns including the original root. This is a necessary bound, not an existence assertion or the minimum sufficient repair size.

For N=3703, allowing at most 21 extra edited columns gives exactly **252 actual AP7-free colorings**: r=1, either palette, regular columns unchanged, and any nonconstant seven-bit word on 1,618,1235,1852,2469,3086,3703. These are actual colorings, not parameter presentations padded with unused edits or symmetry orbits. The existence of these historical character colorings is not a new numerical bound.

## Six endpoint supports and five disjoint demands

At the normalized root0 and target1, enumerate every nonzero field step d in1..616. Exactly the following six have all six other positions in the nonsquare class:

| d | S_d={1+j*d mod617 : 1<=j<=6} |
|---|---|
|285|192,239,286,477,524,571|
|314|12,23,34,315,326,337|
|362|108,215,322,363,470,577|
|381|55,146,291,382,436,527|
|409|195,202,403,410,604,611|
|570|336,383,430,477,524,571|

The first five supports are pairwise disjoint and avoid0,1. Put V=the union of all six supports. Its cardinality is 33, and the independently checked finite fact is

    V intersect V^(-1) = empty,

where V^(-1)={v^(-1):v in V}. These sets contain only nonsquares. Set D=V union V^(-1); |D|=66. This reciprocal obstruction, as well as the disjoint pack, is needed below. Counting five demands alone would only give the weaker ten-edit bound.

For context, the complete endpoint-support hitting number is5. Every minimum cover chooses one of477,524,571 and one point from each of the four supports for d314,362,381,409. There are3888 minimum covers. The producer uses this product description; the verifier branches on the first unhit edge and independently reconstructs the same full set. This count is not the number of feasible interval completions.

For any marked root r and nonroot target q, put alpha=q-r. The supports

    r+alpha*S_d

are five pairwise disjoint six-column sets of baseline color opposite to b(q), since L(alpha*v)=L(alpha) XOR L(v). They avoid r and q. Translation and multiplication here describe field supports; they do not quotient the full integer interval by affine maps. The finite replay checks all 617 roots and all 616 targets per root, or 380072 parameters and 11402160 support columns.

## Every endpoint support lifts at every actual target

Let m in[1,N] be an actual target, and choose the representative delta in1..616 of the transported nonzero field step. If m+6*delta<=N, use the ordinary AP starting at m with step delta. Otherwise use the ordinary AP ending at m with step617-delta. Its start is

    m-6*(617-delta) = m+6*delta-3702 > N-3702 >=0.

Thus its start is a positive integer. Both APs lie in[1,N], have positive step, and the six support residues are exactly m+j*delta modulo617 for j1..6, because

    m-j*(617-delta) == m+j*delta mod617.

This proves the lift for every N>=3702, every actual point and every nonzero field step. Independent literal seven-position checks replay all 3702*616 pairs at the threshold and all 3704*616 target pairs at the campaign endpoint, totaling 4562096 pairs. The universal N statement uses the displayed elementary inequality; finite checks at these two N values are controls, not enumeration of infinitely many intervals.

## Flip columns induce a directed bipartite graph

For each q in F choose an actual flipped point m. The target has the opposite color from its baseline. Each lifted six-point unit support has that target color in its unedited baseline. To avoid a monochromatic AP, some actual point in each support must also flip. The five disjoint supports therefore require at least five **distinct actual flip columns** of the opposite baseline character class.

On F draw an arc q->t exactly when

    (t-r)/(q-r) belongs to V.

The preceding demands imply outdegree at least 5 for every vertex. This graph is bipartite between the two baseline character classes because every v in V is a nonsquare. It has no loops and no reciprocal pair of arcs because V and V^(-1) are disjoint. If the two class sizes are a,b and m=a+b>0, then

    5*m <= number of arcs <= a*b <= m^2/4.

In particular m>=20. The absence of reciprocal arcs is essential for the middle inequality: every opposite-class pair carries at most one arc.

The underlying undirected graph is a subgraph of the ratio graph on F_p^* whose edge relation is t/q in D, after translating by r. The next independently verified fact rules out the near-complete possibilities at m=20 and m=21.

## Exact closed-family certificate: no K(5,10) in the ratio graph

In the bipartite ratio graph, let the square-side neighbors be

    A(q)=q*D, for each of the 308 nonzero squares q.

Each A(q) has 66 nonsquare vertices. Any same-character five-vertex part of a hypothetical K(5,10) can be divided by its first vertex so it is in the square class and contains 1; the opposite part is in the nonsquare class. This is a ratio-graph normalization, not a symmetry reduction of the integer AP problem.

Start with B=D=A(1). Repeatedly intersect B with every A(q), retaining each distinct result whose size is at least10. The exact completed family has **867 states** and **3929 retained transitions**. For each state B, compute its full square-side closure

    T(B)={q square : B subset A(q)}.

The exact closure-size histogram is:

| Size of T(B) | Number of states |
|---|---|
|1|1|
|2|241|
|3|585|
|4|40|

Every closure has size at most 4. There is therefore no K(5,10). To justify coverage, the intersection of neighborhoods of any normalized five vertices containing1 would retain its ten common neighbors at every intermediate intersection, and so would occur in this family. Its closure would contain those five vertices, contrary to the checked maximum4.

The verifier does not accept a list of successful cases. It independently constructs the neighborhood masks by literal ratio tests with square-set characters and Euclidean inverses; checks every state and its full closure; requires the initial state; checks **all 867*308=267036 intersection transitions**, including every discarded transition; requires every retained successor to be present; and verifies reachability of all 867 states. The producer instead discovers states by set intersection and multiplication-based neighborhoods. Complete closure and the normalization argument give the quantified exclusion.

## Excluding20 and21 flips; the22-column frontier

If m=20, then a=b=10 and all100 opposite-class pairs must be arcs. Their underlying graph contains a K(5,10), impossible.

If m=21, put a<=b. The arc inequality requires a*b>=105, leaving only (a,b)=(9,12) or (10,11). The underlying graph misses at most3 or5 opposite-class pairs, respectively. At most that many vertices of the a-side are incident with a missing pair. At least six or five a-side vertices are therefore adjacent to **every** b-side vertex. Again there is a K(5,10). Thus every nonempty F has at least 22 vertices.

At m=22 the arc inequality initially allows unordered class sizes (8,14),(9,13),(10,12),(11,11). The first misses at most2 pairs and contains K(5,14). For (9,13), there are at most7 missing pairs. The five smallest missing degrees on the9-side have total at most floor(5*7/9)=3, so these five vertices have at least10 common neighbors, again impossible. Hence the next unresolved22-edit frontier has class sizes **(10,12) or (11,11)**, up to exchanging colors.

Every actual22-column flip set must induce minimum outdegree 5 in the specified directed ratio graph and meet these balance constraints. This is a necessary graph reduction, not a completed search or coloring witness. For an AP7-free3704 template, both vertical columns1,2 lie in {r} union F: every nonroot one must actually flip. With23 total free columns there are140 actual free integer positions (six per column and one extra each in columns1,2), all independently colored. No native completion model or feasibility result is asserted here.

## Endpoint consequences and the252-coloring classification

At3704 both columns1,2 contain a vertical seven-term AP of step617. If F were empty, at least one is not the true root and is constant in its baseline, so the coloring would fail. Therefore |F|>=22. This remains true if a purported template designates fewer than22 edited columns and makes them arbitrary at each integer occurrence.

For N3703, if at most 21 nonroot columns are designated editable, the main lemma forces F empty. The only field column with seven actual occurrences is1, so AP-freedom requires r=1 and a nonconstant root word. These conditions are sufficient. A positive AP step at3703 is at most617. Step617 gives only the vertical AP starting at1. Every other positive step is nonzero modulo617 and has seven distinct field residues. The full exact partial-character scan checks all 380072 field start/step pairs:375760 avoid0,4312 visit it, and the nonroot values contain both colors in every case. For zero visits this also has the ordinary explanation L(-1)=L(1)=0 and L(3)=1: the six nonzero offsets around any of seven possible root slots include offsets with absolute values1 and3. Arbitrary root colors cannot make such an AP monochromatic. Finally two palettes and126 nonconstant seven-bit root words give exactly 252 actual colorings.

## Literature, prior campaign work and scope

[Monroe, *New lower bounds for Van der Waerden numbers using distributed computing*](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/), Table 1, lists length7/two colors >3703; Table 2 uses prime 617, and Section 2 describes Rabung power-residue colorings. That length-first W(7,2) is the campaign's color-first W(2,7). [Herwig et al., *A new method to construct lower bounds for van der Waerden numbers*](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf) gives construction context. These links were reread live on 2026-10-03. We make no first-ever or comprehensive latest-record-absence assertion. The asymmetric w(3,k) problem is not used.

This independently checked mechanism refines only the **single-character repair-column conclusion** of campaign lemma 9842, whose original ignored-root embedding gave at least three extra columns. The earlier [Boolean617 core proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/boolean617-core-filter/PROOF.md) has broader Boolean-input scope but no extra edits. It is context, not a numerical premise of the present endpoint-support graph proof. The [VDW2 H7 phase lemma 9840](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-ten-singletons/PROOF.md) and [VDW1 pattern-phase lemma 9844](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/character-pattern-phase310/PROOF.md) impose different phase/invariance hypotheses and supply no premise or transferred review here.

The22 bound is for one affine character with constant phase; it is not a22 bound for arbitrary Boolean combinations of several characters, nonconstant row phases, or unrestricted colorings. A3704 witness and W(2,7)>=3705 remain unproved by this work. Ordinary character multiplicativity, graph normalization/counting, and interval/classification bridges are explicit above but not formalized. All finite claims are regenerated and independently checked from compact standard-library source. See [README](README.md), [validation](VALIDATION.md), [expected record](expected.json), and [source pins](SOURCE_PINS.json).
