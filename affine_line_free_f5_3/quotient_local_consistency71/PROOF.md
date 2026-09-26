# Local planar lifts with matching full-fiber laws do not constrain a quotient

**Constructive theorem and exact finite audit.** Let
\(w:\mathbb F_5^2\to\{0,1,2,3,4\}\) satisfy
\[
 \sum_p w_p=71,\qquad \sum_{p\in L}w_p\le16
 \quad\text{for every affine quotient line }L.
\]
For every one of the 30 planes \(H_L=L\times\mathbb F_5\), there is
a probability distribution on actual line-free planar subsets \(T_L\)
with exactly \(w_p\) selected points in each fiber \(\{p\}\times\mathbb F_5\).
If \(|T_L|\le10\), every line in \(T_L\) has at most three selected points.
For every fiber p the full five-point subset has the same marginal law
in each of its six containing planes: **uniform on all \(w_p\)-subsets**.

Thus checking individual planar realizability and requiring complete
shared-fiber marginal consistency rejects **no** quotient satisfying
the displayed weight conditions. This includes the small-plane line
cap forced by cardinality 71. The conclusion concerns a specified
relaxation, not the existence of a 71-point set.

The local laws can also make any pair of fibers in a common plane
independent whenever at least one of them has weight four. As a
consequence, prescribing the missing heights in any two weight-four
fibers never obstructs that individual planar lift. A three-hole gauge
at noncollinear quotient points therefore leaves every individual plane
realizable. The full marginal-consistency statement is **before** that
gauge; it is not asserted after conditioning on the three holes.

## 1. Two elementary planar filling lemmas

Use coordinates \((t,z)\) on \(\mathbb F_5^2\), with five fibers t fixed.
The following two assertions suffice:

1. Every integer profile \(0\le v_t\le4\), \(\sum v_t\le16\), is the
   fiber profile of a line-free planar set.
2. Every integer profile \(0\le v_t\le3\), \(\sum v_t\le10\), is the
   fiber profile of a planar set with no four collinear points.

For the first assertion, increase coordinates, without exceeding four,
until the sum is 16. The deficits from four now sum to four. There are
70 ordered profiles. Under the actual affine coordinate changes
\(t\mapsto at+b\), \(a\ne0\), they fall into the six types in the
first part of the table below. For the second assertion, pad to total
ten with coordinates at most three. The deficits from three sum to
five. The 101 ordered profiles give the seven types in the second part.

The table gives explicit realizations. A row mask r denotes selected
heights \(\{z: r\mathbin{\&}2^z\ne0\}\), so for example 15 denotes
\(\{0,1,2,3\}\). The five masks occur at \(t=0,1,2,3,4\).

| Line cap | Profile | Selected-height masks |
|---:|---|---|
| 4 | (0,4,4,4,4) | (0,15,15,15,15) |
| 4 | (1,3,4,4,4) | (1,14,15,15,15) |
| 4 | (2,2,4,4,4) | (12,3,15,15,15) |
| 4 | (2,3,3,4,4) | (5,7,14,27,15) |
| 4 | (2,3,4,4,3) | (6,11,15,29,7) |
| 4 | (3,3,3,3,4) | (14,13,11,7,15) |
| 3 | (0,1,3,3,3) | (0,4,11,7,7) |
| 3 | (0,2,2,3,3) | (0,12,3,7,7) |
| 3 | (0,2,3,3,2) | (0,20,7,7,3) |
| 3 | (1,1,2,3,3) | (8,1,10,7,7) |
| 3 | (1,1,3,2,3) | (4,4,11,3,7) |
| 3 | (1,2,2,2,3) | (1,20,6,3,7) |
| 3 | (2,2,2,2,2) | (12,6,5,3,3) |

Each row is checked on all 30 geometric lines in the plane. The
small orbit counts can also be read directly from the partitions of
four and five. The only splits requiring care are the unordered pair
of distinct nonzero labels modulo scaling: opposite and nonopposite
pairs are different. All 20 affine changes are checked explicitly by
the verifier; arbitrary permutations of the five labels are not used.

Apply the inverse affine label change to the appropriate template,
then delete points separately in each fiber to recover the original
profile. Deletion preserves the stated line cap. This proves both
filling assertions. The code checks the resulting set, entry by entry,
for all 3,069 profiles in the first domain and all 903 in the second.
The sufficiency proof uses only these thirteen explicit sets and affine
maps; it does not depend on a large catalogue or an optimizer.

For context, the first domain is also necessary: fibers have at most
four points and the planar maximum is 16. The optional classical
planar input is independently replayed here by checking every
17-subset for a full line. The second assertion is a sufficient filling
statement up to total ten; it does **not** assert that a planar set
with no four collinear points has size at most ten.

## 2. Every 71-weight quotient satisfies the filling hypotheses

Let \(m_L=\sum_{p\in L}w_p\). The other four parallel quotient
lines have total at most 64, so \(7\le m_L\le16\).
The six quotient lines through a point p have total weight
\[
 \sum_{L\ni p}m_L=71+5w_p.
\]
If one of these lines has \(m_L\le10\), then
\[
 71+5w_p\le m_L+5\cdot16\le90,
\]
so every fiber on that line has weight at most three. Its prescribed
profile therefore satisfies the second filling lemma. Every other
quotient line satisfies the first. Choose one planar realization
\(T_L\) for each line, using any affine parameter \(t\) on L.

These are exactly the local restrictions obtained from plane cap 16,
fiber cap four, and the stronger line cap in sections of size at most
ten. We do not assume the existence of an actual global S at this step.

## 3. Affine averaging matches entire fiber distributions

Act on a local plane by the 100 transformations
\[
 (t,z)\longmapsto(t,az+bt+c),\qquad
 a\in\mathbb F_5^*,\quad b,c\in\mathbb F_5.
\]
They are invertible affine transformations and preserve each fiber
setwise, its selected cardinality, and the line cap. Put mass 1/100
on each transformed copy of \(T_L\), allowing repeated copies.

For a fixed t, the induced height transformation is uniform on
\(\operatorname{AGL}(1,5)\). This group is transitive on the subsets
of each size k=0,1,2,3,4: sizes one and two follow from transitivity
and double transitivity, and sizes three and four follow by complements.
Consequently the whole selected subset in a fiber of size k is uniform
on its \(\binom5k\) possible values.

This law depends only on \(w_p\), not on L or its chosen realization.
Any two distinct projection planes are disjoint or intersect in one
whole fiber. Hence all their overlap laws agree exactly. This proves
the theorem for every quotient in its domain, rather than for a
sample of quotient matrices.

One may equivalently introduce a domain
\(D_p=\{A\subseteq\mathbb F_5:|A|=w_p\}\) for every fiber, and an
allowed relation on its five domains for every quotient line. The
theorem constructs a feasible point of the local marginal polytope:
each relation has a distribution on its actual valid assignments,
and every occurrence of a variable has the same full-domain marginal.
Thus adding any linear inequality valid inside a single such relation
cannot exclude the quotient.

## 4. Two full-fiber heights do not impose a local obstruction

Consider distinct fiber labels t and u in one plane, with weight four
at t. Let h be its unique missing height. For fixed a, the map
\[
 (b,c)\longmapsto(bt+c,bu+c)
\]
is a bijection of \(\mathbb F_5^2\). The two translations are therefore
independent and uniform. The transformed h is uniform on all five
heights, independently of a and of the transformed subset at u.
Averaging a then makes that second subset uniform on its entire domain.
Their joint law is the product of the two uniform marginal laws.

In particular every pair of prescribed missing heights in two
weight-four fibers occurs in at least one valid local lift. A single
prescribed missing height is also always attainable.

Now choose three noncollinear weight-four quotient positions and fix
their missing heights, for example all to zero. Any quotient line
contains at most two of them, so each individual planar relation
remains nonempty. This statement concerns individual relations. It
does not say that conditioning the separate distributions on the
three prescribed holes keeps their overlap laws equal. Our explicit
controls exhibit disagreements after this conditioning.

There is also a useful positive gluing statement. Choose any subfamily
of projection planes such that every shared fiber has weight four,
and each chosen plane contains at most two distinct shared fibers.
Prescribe an arbitrary missing height in each shared fiber. Every
chosen plane can be completed with these prescriptions by the preceding
argument. Other fibers belong to just one chosen plane, so the
completions agree and give one assignment satisfying the whole chosen
subfamily. This does not impose the unchosen planes' constraints.
In particular a triangle of three projection planes with three distinct
weight-four intersections cannot itself obstruct lifting. Cyclic
incidence alone is insufficient in this situation; a plane with three
shared fibers, or intersections of smaller fiber weight, is needed
to go beyond this gluing argument.

## 5. Why this does not produce a global lift

The 30 projection planes contain all 775 affine lines in three-space:
25 vertical lines occur six times, and the other 750 occur once. A
single assignment \(A_p\in D_p\) that lies in every planar relation
would consequently define a genuine line-free set of size 71.
Conversely any such set gives that assignment.

Likewise, a common probability distribution on all 25 fiber variables
supported on every relation exists if and only if some global lift
exists: choose an assignment from its nonempty support. Pairwise
agreement of the 30 local distributions supplies no such common
distribution. This is the precise loss of information in the relaxation.

For a concrete strict failure, the 72-weight quotient

    00233
    24334
    24433
    24442
    24334

has row and column profiles (8,16,16,16,16), all quotient line weights
at most 16, and no quotient line of weight eleven. The same construction
therefore gives local distributions satisfying even the pencil-derived
small-section cap at total 72. The verifier checks all overlap laws.
Nevertheless it has no global lift, by the committed
[complete upper bound 71](../upper_bound71/THEOREM.md). That prior
global theorem is used only for this strict counterexample; it is not
needed for the universal local-consistency theorem at total 71.

The 71-weight control in [quotient_controls.json](quotient_controls.json)
has two seven-lines and fourteen sixteen-lines. It also passes all
checks. We make no claim that it has a global lift.

## 6. Consequence for the remaining research problem

This closes the proposed route of excluding a 71-weight quotient by
independent planar completion or by full-fiber overlap consistency
alone. It also shows that merely testing individual planes after the
usual three-hole gauge cannot prune a quotient.

The theorem leaves open consistency tests **after** imposing that gauge,
fixing a whole planar section, joint restrictions involving several
projection planes, additional nonprojection-plane marginals, and integral global lifting. In
particular it does not close the stronger relaxation formed from all
155 planes with all their full shared-line laws. A concrete next
geometric object is an arrangement with at least three shared fibers
in one plane, or a cycle with smaller fiber weights at its intersections.
These are outside the positive gluing statement above.

The exact value of r_5(F_5^3) remains 70 or 71. This is a structural
obstruction to a method and gives no new extremal bound. The trust
boundary is the written construction, thirteen
explicit planar sets, ordinary exact Python checking, and the planar
cap replay. Independent peer review and formal verification are not
claimed. No active, uncommitted low-plane claim is a premise.
