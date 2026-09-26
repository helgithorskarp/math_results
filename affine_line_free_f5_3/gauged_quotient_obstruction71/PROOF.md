# Fixing the height gauge does not repair quotient marginal consistency

## Statement and geometric meaning

Let \(w:\mathbb F_5^2\to\{0,1,2,3,4\}\) be integral, with
\[
 \sum_p w_p=71,\qquad m_L:=\sum_{p\in L}w_p\le16
 \quad\text{for every affine line }L\subset\mathbb F_5^2.
\]
Write \(H_L=L\times\mathbb F_5\) for its 30 projection planes.

**Theorem.** Fix any affine function \(\ell:\mathbb F_5^2\to\mathbb F_5\).
There is a probability distribution \(\nu_L\) on actual line-free subsets
of each \(H_L\) such that:

1. Every set in its support has exactly \(w_p\) selected points in the
   fiber over \(p\in L\).
2. Every selected set avoids the entire transverse plane
   \(H=\{(p,\ell(p)):p\in\mathbb F_5^2\}\).
3. If \(m_L\le10\), each selected set has no four collinear points.
4. The full subset in a fiber over \(p\) is uniform on the
   \(\binom4{w_p}\) subsets of
   \(\mathbb F_5\setminus\{\ell(p)\}\). Thus its marginal agrees in
   all six containing projection planes.

In particular **every weight-four fiber has its hole fixed at \(\ell(p)\)**.
This includes the usual three-hole height gauge. Three arbitrary hole
values at noncollinear quotient positions determine a unique affine
\(\ell\), so the theorem applies to any such gauge.

These local laws cannot be marginals of any common global distribution
supported on their local relations. A global support point would be a
line-free 71-set avoiding H; its other four parallel plane sections each
have size at most sixteen, giving at most 64 points. The contradiction
does not use the team's SAT exclusion of 72 or any unsettled 71-point
claim.

This is a universal obstruction to **gauged, full-fiber local marginal
tests on the 30 projection planes**. It is not a 71-point construction
or exclusion. It does not address the larger relaxation containing
additional plane marginals or joint constraints on several planes.

The coordinate change \((p,z)\mapsto(p,z-\ell(p))\) is invertible affine,
preserves fibers and all line caps, and takes H to \(z=0\). It suffices
to construct the laws in this normalization.

## 1. Ordinary sections: a direct geometric construction

Consider any five-fiber profile \(0\le v_t\le4\), \(\sum_t v_t\le16\).
Work in the strip \(\mathbb F_5\times\mathbb F_5^*\), omitting height zero.
In fiber t choose \(4-v_t\) additional holes among its four nonzero
heights so that their union, over all fibers, contains all four heights.
This is always possible: list \(4-v_t\) consecutive colors of the cyclic
list \(1,2,3,4,1,2,3,4,\ldots\) for each successive fiber, continuing
where the previous fiber stopped. Each block has length at most four
and the total length \(20-\sum v_t\) is at least four.

The resulting set has no complete line. Vertical fibers contain at most
four points. Every line \(z=at+b\) with \(a\ne0\) hits the omitted
height-zero row. Every nonzero horizontal line has one of the additional
holes. The height-zero horizontal line is empty.

Permute the four nonzero height labels in all 24 ways and average. Each
image still has those blocking properties. These permutations are
**not** asserted to preserve arbitrary affine configurations; their
validity here follows from the empty row and horizontal holes just
proved. Each fiber is now uniform on all its \(v_t\)-subsets of
\(\mathbb F_5^*\), because the symmetric group is transitive on those
subsets. This proves the required ordinary planar filling statement.

## 2. Small sections: a uniform law with no four collinear

We need the following stronger filling lemma.

**Lemma.** For every profile \(0\le v_t\le3\) of total at most ten,
there is a distribution on sets of that profile in
\(\mathbb F_5\times\mathbb F_5^*\) with line cap three and with every
fiber uniform on its subsets of the given size.

First take total ten. The 101 ordered profiles have seven orbits under
the actual affine changes \(t\mapsto at+b\), \(a\ne0\). Their deficits
from three sum to five; the seven representatives are listed below.
The verifier independently lists all profiles and all 20 label changes
and checks this complete cover. No arbitrary permutation of fiber labels
is used.

A mask encodes selected heights by its binary digits, so 30 means
\(\{1,2,3,4\}\). Each row in the table is a five-mask planar set.
For every row, average the four affine maps \((t,z)\mapsto(t,az)\),
\(a\in\mathbb F_5^*\). In the two rows marked T, also average the five
translations of the t coordinate. Mix rows of each profile with their
displayed weights.

| Profile | Masks at t=0,1,2,3,4 | Mixture weight | Translate t? |
|---|---|---:|:---:|
| (0,1,3,3,3) | (0,2,14,22,28) | 1 | |
| (0,2,2,3,3) | (0,6,10,14,28) | 2/3 | |
| | (0,12,12,22,26) | 1/3 | |
| (0,2,3,3,2) | (0,6,14,22,24) | 2/3 | |
| | (0,12,14,14,18) | 1/3 | |
| (1,1,2,3,3) | (2,2,10,28,28) | 2/3 | |
| | (2,2,12,22,28) | 1/3 | |
| (1,1,3,2,3) | (2,2,14,20,28) | 2/3 | |
| | (2,2,28,18,28) | 1/3 | |
| (1,2,2,2,3) | (2,12,6,10,28) | 1/3 | |
| | (2,6,18,20,28) | 1/3 | |
| | (2,6,10,12,28) | 1/3 | |
| (2,2,2,2,2) | (6,10,24,6,12) | 1/3 | T |
| | (6,6,24,12,18) | 2/3 | T |

Every row avoids zero and has the claimed fiber sizes and line cap.
The finite checks concern just fourteen explicit sets and their actual
affine images, not an unprovided search catalogue. They are reproduced
against all 30 planar lines generated independently from point pairs.

Here is why the fiber laws are uniform. Multiplication by
\(\mathbb F_5^*\) is transitive on singletons and triples of nonzero
heights. For pairs it has two orbits: the two opposite pairs
\(\{1,4\},\{2,3\}\), and the four other pairs. Uniformity on all six
pairs is therefore equivalent to opposite-pair probability 1/3.

In the four two-row profiles the first template uses no opposite pairs
in its weight-two fibers and the second uses them in every such fiber.
Their weights give the required probability. In (1,2,2,2,3), exactly
one of the three weight-two fibers is opposite in each template, and
each fiber occurs once. In (2,2,2,2,2), row translation makes the
probabilities 1/5 and 2/5 in the respective templates. The displayed
mixture gives \((1/3)(1/5)+(2/3)(2/5)=1/3\). Empty fibers are trivial.

Apply the inverse affine fiber-label map for an arbitrary total-ten
profile. For a smaller profile, pad its coordinates to total ten without
exceeding three, use that law, and then independently choose a uniformly
random \(v_t\)-subset of the selected points in each fiber. Deletion
preserves the line cap and omission of zero. Thinning a uniform k-subset
of a four-element set to a uniform j-subset gives the uniform j-subset
law: a fixed j-subset has exactly \(\binom{4-j}{k-j}\) supersets, and
\[
 \frac{\binom{4-j}{k-j}}{\binom4k\binom kj}=\frac1{\binom4j}.
\]
This proves the lemma. The exact verifier constructs the complete laws
for all 903 profiles in its domain, including every deletion outcome,
and checks every marginal as a rational number.

## 3. Apply the filling laws to every admissible quotient

Four other parallel quotient lines have total weight at most 64, hence
\(7\le m_L\le16\). The six quotient lines through a point p satisfy
\[
 \sum_{L\ni p}m_L=71+5w_p.
\]
If one such line has \(m_L\le10\), then
\(71+5w_p\le10+5\cdot16=90\), so \(w_p\le3\) everywhere on that line.
The small filling lemma applies there. Apply the ordinary filling law
to every other line. This needs no assumption that the quotient is
globally liftable.

Both constructions give the identical fiber law
\[
 D_k(A)=\binom4k^{-1}\quad
 (A\subseteq\mathbb F_5^*,\ |A|=k).
\]
Distinct projection planes are disjoint or meet in a whole fiber, so
their complete overlap marginals agree. Weight-four fibers have the
deterministic subset \(\mathbb F_5^*\), fixing their holes at zero.

The small-section cap is a necessary restriction for an actual 71-set:
the six planes through any k-point line have total \(71+5k\). If one
has at most ten points, the other five contribute at most 80, implying
k at most three. Thus this additional global restriction has genuinely
been retained in the local model.

## 4. Exact correspondence and failure of global gluing

Introduce a variable \(A_p\subseteq\mathbb F_5\), \(|A_p|=w_p\), for
each of the 25 fibers. For every quotient line impose the relation
that its five subsets form a line-free planar set (with cap three for
size at most ten). Fix the three-hole gauge if desired. The theorem
provides a feasible point of this factor model's local marginal polytope.

The 30 projection planes contain every spatial affine line. The 25
vertical lines each occur six times, while the other 750 occur once.
Hence a single assignment satisfying all local relations gives a
genuine global line-free set, and every global 71-set satisfies these
relations and the small-plane restriction. Local **marginal** agreement
is the nonfaithful step, even after fixing the height gauge.

Our particular family forces \(A_p\subseteq\mathbb F_5^*\) at every p.
Any common global law with these local marginals would, with probability
one, avoid height zero and satisfy every relation. It would contain a
line-free 71-set in four parallel planes. The planar bound sixteen
therefore proves that no such global law exists. The bound 64 under an
empty plane is sharp, as the line-free Cartesian box
\((\mathbb F_5^*)^3\) shows. This last fact is directly rechecked on all
775 lines.

The omitted information is visible already in first moments for the
five transverse planes: their expected occupancies in our local laws
are \(0,71/4,71/4,71/4,71/4\). Each of the four positive values exceeds
sixteen. Adding those plane-cardinality inequalities rejects this
particular certificate. We do **not** claim that every other gauged
local family then becomes infeasible, or that this rejects the quotient.

Conversely, averaging our five globally translated constructions,
omitting each height in turn, gives the earlier ungauged uniform
full-fiber laws on \(\binom5k\) subsets. Each k-subset avoids exactly
\(5-k\) heights, so its probability is
\((5-k)/(5\binom4k)=1/\binom5k\). The present construction thus also
recovers that previous result while closing its stated gauge gap.

## Scope and trust

The theorem applies to every quotient meeting the displayed integer
conditions, including all types in the team's low-pair cover. It
neither enlarges that census nor solves a lifting case. There are no
solver verdicts, floating-point assumptions or unpublished external
catalogues in the proof. The source rechecks the plane cap on every
17-subset, all 3,069 ordinary laws, all 903 small laws, and the entire
spatial incidence model with exact arithmetic.

The exact value of r_5(F_5^3) remains 70 or 71. This projection-plane
marginal route is unproductive even after its height-gauge repair.
Further progress needs joint compatibility, additional nonprojection
plane information, or the separate complete integral lifting work.
No independent peer review or proof-assistant formalization is claimed.
