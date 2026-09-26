# Review of the complete 71-point certificate cover

**Decision:** accept the complete finite reduction, with high confidence.
The reviewed result is the equivalence between existence of a 71-point
line-free set and satisfiability of at least one of 109,676 fixed formulas.
Acceptance does not extend to a numerical bound of 70: this review
rechecks no global UNSAT proof and accepts no partial run as exhaustive.

Reviewed source: `decision71`, last changed at commit
`0bd139b2d32f58fcb080b6f90aa42387931d54b6`. The exact file manifest is in
[EXPECTED.json](EXPECTED.json). The original graph contribution is
`bafkreifrsrzf2igkvt5o3yfe6uvliewuha5glpyi5kfmi22kvumk2enitu`
(height 6046), originally published at
`6d2f193aecad54cc41dab4cdf67c16f9add58cc2`.

## 1. From an arbitrary set to two coordinate planes

Let $S\subseteq\mathbb F_5^3$ be line-free with $|S|=71$.
The production replay independently reruns the two author-supplied planar
censuses, agreeing on 91 admissible spectra. In particular they exclude
all 17-point line-free sections and establish the planar cap 16.
Every plane section is consequently between 7 and 16.

For any affine line $L$, the six containing planes count every point off
$L$ once and every point on $L$ six times. Thus

\[
\sum_{H\supset L}|S\cap H|=71+5|S\cap L|.
\]

If one containing section has size at most ten, then
$71+5|S\cap L|\le10+5\cdot16=90$, so $|S\cap L|\le3$.
The new checker verifies this pencil identity coefficient by coefficient,
for all 775 lines and all 125 points, using independently generated
planes. It also checks the corresponding quotient-star identity.

We use the [two-low-plane theorem](../low_pair71/THEOREM.md), due to Team A
researcher 3, with its [independent accepting review](../low_pair71_review1/README.md).
It supplies two nonparallel planes of section size at most nine. The
production replay rechecks all fourteen exact integer certificates and
containment of its fifteen types in the twenty-type decision domain.
The lower bound on the number of these sections is strictly greater
than one, and two such sections cannot be parallel because
$9+9+3\cdot16<71$.

This supplies a complete premise for the reduction without using the
alternative unique-low-plane certificates in the author proof. Those
certificates were also reproduced, including negative controls, but the
reviewed implication does not need them. The extra five pair types
are an allowed enlargement of a complete domain.

The normals $u,v$ of two nonparallel planes are linearly independent.
Complete them with a third linear form and subtract the two plane
constants to obtain coordinates $x,y,z$ in which the selected planes
are $x=0,y=0$. The new checker tests all 930 ordered pairs of normal
directions and 25 choices of constants: 23,250 affine plane pairs.
Each constructed coordinate map has an explicitly checked inverse and
preserves all spatial lines. Every translation is checked separately.

## 2. Legal profile normalization

If the section at coordinate zero has size $m\le10$, its four companions
have sizes $16-d_t$ with $d_t\ge0$ and
$\sum_{t\ne0}d_t=m-7$. Enumerating multisets of deficit locations gives
exactly 1, 4, 10, and 20 raw profiles for $m=7,8,9,10$.

Only the four field scalings of nonzero labels are permitted. Applying
them gives the ten profiles recorded in `profiles.json`, with five
profiles having low entry at most nine. Independent scalings of $x,y$
and coordinate exchange permit the fifteen pairs $0\le i\le j<5$.
The production domain also includes $(0,j)$ for $5\le j<10$.
The checker regenerates this list from deficit multisets and legal
scalars. No arbitrary permutation of parallel sections is used.

## 3. Quotient domain and the full-fiber guarantee

Project along the intersection direction and put
$w_{xy}=|S\cap\{(x,y,z):z\in\mathbb F_5\}|$. Then
$0\le w\le4$, $\sum w=71$, and every quotient line has weight at most
16 because its inverse image is an affine plane. Both zero axes have
weights at most three by the pencil argument. At their intersection,

\[
71+5w_{00}\le m+n+4\cdot16,
\qquad 5w_{00}\le m+n-7.
\]

If $T=\sum_{x,y\ne0}(4-w_{xy})$, then the interior contains
$71-m-n+w_{00}$ selected points, so the exact identity is

\[
\boxed{T+w_{00}=m+n-7.}
\]

Thus $T\le11$ in every retained pair type. At least $16-T\ge5$
interior fibers have weight four. They cannot all be collinear: five
such fibers on a quotient line would give weight 20, violating 16.
A noncollinear triple therefore always exists. The new checker verifies
all these facts for every generated quotient, as well as all thirty
line inequalities, profiles, and distinctness of words.

For completeness, we reviewed both enumerators' pruning rules.
The interior-deficit recursion ranges over every entry in $[0,4]$;
row and column upper bounds preserve the minimum deficit one on the
boundary. The total-deficit interval is precisely the allowed interval
for the inferred $d_{00}$. Both endpoints of every other boundary
entry are tested. The five vertical line sums are fixed by the profiles;
the code checks the other twenty-five quotient lines.

The second recursion visits all possible nonzero weight rows with the
correct row totals and first entry at most three, then infers row zero
from the column totals. It checks both endpoints of each inferred
entry and all remaining line constraints. Its intermediate column
upper-bound pruning discards no nonnegative completion. These are
complete, different parameterizations of the same necessary domain.

Their sorted outputs agree byte for byte on 309,611 typed words.
The fresh replay obtains catalogue SHA256
`a6d7af5e3cb1c4b6069892164453fed01da96e7ec1718d2333ace123a6909291`.
Our additional checker validates those words from definitions; it does
not independently enumerate every possible matrix. Domain completeness
rests on the reviewed recursions and their successful full replay.

## 4. Affine quotient representatives

Every affine image that remains in the typed domain has two preimages
of its zero coordinate lines. Their defining forms, constants, and
nonzero scales are exactly the choices visited by `quotients.py`.
Taking the least `(type,word)` therefore identifies all and only affine
equivalences in the normalized domain.

We replayed the separate author-supplied full-group checker. It constructs
all $25(25-1)(25-5)=12,000$ affine maps and applies every map to every
representative. It verifies canonical minima, claimed orbit sizes,
absence of overlap, and coverage of every typed matrix. It obtains
109,676 representatives with total restricted-orbit size 309,611.
The new checker additionally verifies that all representatives are
distinct typed catalogue entries and have that total multiplicity.

Any quotient affine map lifts to $(p,z)\mapsto(Ap+b,z)$ in three
space dimensions. Passing to a representative changes coordinates;
it does not impose an automorphism on the candidate set.

## 5. The three-hole shear loses no candidate

For any noncollinear full-fiber triple $p_1,p_2,p_3$, let $h_i$ be
the unique omitted height. The matrix with rows $(1,p_i)$ is invertible
over $\mathbb F_5$, so there is a unique affine function $\ell$ with
$\ell(p_i)=h_i$. The map $(p,z)\mapsto(p,z-\ell(p))$ is an invertible
affine shear. It preserves every fiber weight and every line and puts
the three missing heights at zero.

This applies to the lexicographically chosen triple after quotient
canonicalization, regardless of which triple was convenient earlier.
The new checker reconstructs field inverses by elimination and checks
all $\binom{25}{3}-30\binom53=2,000$ noncollinear triples and all
125 possible height assignments for each. It also verifies all 125
height shears on every spatial line. Collinear interpolation is rejected.

## 6. Exact meaning of the formulas

The variable numbered $1+25x+5y+z$ selects point $(x,y,z)$.
For each of the 775 independently reconstructed lines, one negative
clause forbids selecting all its points. In a five-point fiber of weight
$n$, all negative $(n+1)$-subset clauses enforce at most $n$ selections.
All positive $(6-n)$-subset clauses enforce at least $n$: fewer
selections would leave at least $6-n$ zeros. This remains correct at
$n=0$, when the positive family is empty and the negative clauses are
units. The three negative height-zero units impose the valid shear gauge.

The new checker exhausts all 160 fiber-weight/Boolean-assignment cases.
For the first representative of each of the twenty types it independently
constructs the complete expected clause multiset and compares it with
`point_model.generate`. It also checks three known 70-point controls
from raw point lists, normalizes their actual missing heights, and
verifies the resulting formulas directly from assignments. Removing a
selected point or completing an affine line is rejected in each control.
These positive cases guard against an encoding that accidentally forbids
every point set. They do not assert existence at cardinality 71.

Consequently every hypothetical 71-set yields a model of a formula in
the complete family, while every model selects a line-free set of
exactly 71 points. This is the asserted equivalence.

## 7. Evidence boundary and coordination

The complete author reduction was replayed, and all expected mathematical
summaries and hashes matched. The additional independent geometry code
passed normally and with Python optimization. This review did not rerun
the author's C++ sanitizer suite; the recorded sanitizer claim remains
attributed to the author. It did not execute any of the global lifting
proofs, nor independently inspect all 109,676 exported formulas.

The low-pair theorem and its existing independent review are the sole
nontrivial team theorem used in the preferred written route. Our earlier
universal gauged planar-marginal obstruction motivates supporting the
complete integral reduction instead of extending that insufficient
local method. Researcher 4's new two-six-plane classification and its
seven-plane corollary were inspected as context, but are neither assumed
nor reviewed here. Researcher 3's nonzero quadratic-moment theorem and
the symmetry exclusions are also not premises.

The bounded team refresh through ledger height 6059 found no completed
71-point decision or accepting review of the complete reduction. The
latest researcher-2 report still recorded 80,200 checked UNSAT cases out
of 109,676. A final exact-value claim requires a directly verified
71-point witness, or checked UNSAT proofs covering every formula,
followed by independent acceptance of that decisive evidence. This
review alone does not satisfy the campaign's exact-value handoff gate.
