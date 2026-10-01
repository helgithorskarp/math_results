# Independent 16/19-profile charge audit

**Actual agent: six-reviewer-5. Role: independent mathematical reviewer.**
Date: 2026-10-01. The shared signing identity does not establish distinct
authorship. The ordinary proof and independent programs here were written
by this reviewer; the credited star classifications were not.

**Verdict: conditional confirmation of lemma8820 with its published
premises.** Its final multiplicity-five argument is correct. I independently
derive its incidence budget, audit the charge transfer, reproduce every
entry of its finite readout, and check the relevant local pair obstruction
without using a group quotient or the author's collision certificate.
I also prove that the entire zero-internal-excess case can be discharged
before invoking the nineteen-star classification.

The target is six-code-1's **“A(18,6,5): no 71-word packing has replication
profile (16,19,20^16)”**, committed lemma8820,
`bafkreia4aqnqlxfe42okpty7hfi7agjtsmdrxbnywderpfa5l76ibavbpq`.
Its [proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-1/profile_16_19_exclusion/PROOF.md)
is pinned to source commit `a77603e74d3cba4ba9c2604b680d34a35a5b426d`.
The statement concerns 71 distinct five-subsets of 18 points, with
distinct members intersecting in at most two points and exactly the
specified replication multiset. It assumes no automorphism or minimum
pair multiplicity at other points.

The conditional qualification is material. I **import** the earlier
hub-multiplicity-five theorem8783 and its predecessor chain; I do not
supply an independent verdict on their complete global transfers.
I also import completeness of the generic twenty-star fixture coverage
in8720. The new pair search checks every relevant marking of every one
of its23 fixtures, but does not independently re-enumerate all twenty-stars.
The independently reviewed nineteen-star census8537/8623, universal
saturated-star theorem8323, and sharp67 result8794/review8855 are credited
inputs. These distinctions prevent the current review from establishing
more than its stated dependency boundary.

The unrestricted campaign interval remains69--71. This review does not
give upper70, a construction at70/71, or a verdict on another replication
profile. Historical priority is unassessed.

## Definitions and a direct budget derivation

Let the low-replication points be \(u,v\), with \(r_u=16,r_v=19\),
and let \(S\) be the sixteen points of replication20. Set
\(\delta_{ab}=5-\lambda_{ab}\). Pair tails are disjoint triples,
so \(0\le\lambda_{ab}\le5\). Import8783, which gives
\(\lambda_{uv}=5\).

The five common words have disjoint three-point tails whose union is
\(C\), of size15. Write \(x\) for the sole point of \(S\setminus C\).
The sole uncovered triple through both hubs is \(uvx\).
Partition \(S=A\sqcup B\sqcup T\sqcup Z\) by positive deficits to
only \(u\), only \(v\), both, or neither. Define
\[
W=B\cup T,\quad p=|W|,\quad z=|Z|,\quad c=|T\cap C|,
\quad X=\sum_{\{a,b\}\subset S}(\delta_{ab}-1)_+.
\]

The \(uS,vS,SS\) deficit weights are21,9,25. At a saturated center,
the weighted row is5. The universal theorem8323 excludes a leave pair
between two replication-five link points. If a saturated center has
\(h\) deficient neighbors, its high leave has \(h-1\) edges.
Here “homogeneous incidence” means a center of an uncovered triple
whose other two points are both deficient neighbors of that center.
Incidences at different centers are separate even for the same triple.

I derive the budget directly rather than assuming the cut identity
in8497. There are5 words containing both hubs,11 containing only \(u\),
14 containing only \(v\), and41 containing neither. Consequently the
number \(a_0\) of uncovered triples wholly in \(S\) is
\[
a_0=\binom{16}{3}-5\binom33-25\binom43-41\binom53=45.
\]
The cross deficit-support size is \(16+|T|-z\). The internal support
has \(25-X\) edges. Therefore the sum of saturated support degrees is
\(66+|T|-z-2X\), and the total number of homogeneous saturated
incidences is
\[
J_S=50+|T|-z-2X.
\]
An uncovered wholly saturated triple induces a path or triangle in the
positive-deficit support: at each center the universal no-low-low theorem
requires an incident support edge, so zero or one support edge is
impossible. Its homogeneous contribution is respectively1 or3.
Also \(Z\subset C\), since otherwise the uncovered \(uvx\) would
have two low neighbors at saturated \(x\).
The contribution of \(uvx\) is \(|T|-c\). Thus
\[
R:=J_S-a_0-(|T|-c)=5-z+c-2X
\]
is exactly the number of homogeneous saturated incidences in uncovered
one-hub triples, plus twice the number of wholly saturated uncovered
deficit triangles. All its terms are nonnegative.

Every center in \(T\cap C\) requires at least two one-hub incidences.
This agrees with8497. In my independent readout of all23 credited
twenty-star fixtures there are76 unordered choices of two deficient
marked hubs with their pair covered: their hub-to-other-high edge counts
are2 in64 choices,3 in8 choices, and4 in4 choices. Completeness of the
generic fixture coverage is the stated input. Hence
\[
R\ge2c,\qquad 2X+z+c\le5. \tag{1}
\]

## Independent local obstruction without symmetry assumptions

The key local assertion needed here is the following combined form.
Suppose saturated centers \(a,y\) have \(\lambda_{ay}=4\),
\(\lambda_{av}=5\), and a shared deficient point \(u\).
At \(a\), either the positive row is unit with isolated deficient
\(u\), or it is mixed2111 with its deficit-two \(u\) isolated.
At \(y\), \(v\) has deficit one and every other positive deficit
apart from possibly \(u\) is one. Suppose \(uay,uvy\) are covered
and \(vay\) is uncovered. Then the number \(e_u\) of high-leave
edges from \(u\) to deficient saturated neighbors at \(y\) is at
least2.

Conditional on generic twenty-star coverage, [local_pair.py](local_pair.py)
proves this for both \(e_u=0\) and \(e_u=1\). It does not read any
supplied group map. Literal degree, pair and leave tests retain all14
first markings and all32 second markings across the23 fixtures.
There are196 raw cases with \(e_u=0\) and252 with \(e_u=1\),
448 cases in total. This independently closes the specific zero-incidence
applications of8356/8397/8438 and the one-incidence application of8783
used in this transfer. It does not certify their other global conclusions.

For each raw pair, the four common words have disjoint triples.
The unique common tail containing \(u\) has2 point bijections fixing
\(u\). The other tails have \(3!\cdot(3!)^3\) bijections.
There are three residual points on each side, with all \(3!\)
bijections retained. The precise potential domain is therefore15552
full relative maps per raw case, or **6,967,296** in total.

My recursion assigns common tails in a fixed source order. It prunes
only when an actual three-subset of a private source quadruple maps
into an actual private first-center word. Such a triple is a literal
packing collision, and every extension of that partial map retains it.
For a pruned prefix with \(k\) remaining ordinary tails and \(r\)
residual points, \(k!6^k r!\) complete maps are accounted for; the
initial fixed-prefix case additionally retains the2 special-tail maps.
At every completed raw case the sum of those disjoint pruned cylinders
and accepted leaves is exactly15552. All accepted-leaf lists are empty.
No certificate omission, orbit order, clique bound or solver status is
used to exclude a map.

The full scan visits413196 states, maximum1611 in a raw case. A compatible
35-word union credited to the earlier author is a positive control:
the same algorithm uses its five common tails, accounts for62208 maps,
accepts144 actual maps, and recovers the known literal map. Each accepted
union is checked against every actual pair intersection. This control
does not concern the forbidden local hypotheses or assert a new size35
construction.

## Good friends and the exact charging argument

In the nineteen-word \(v\)-link, a point with replication5 has leave
degree1. Call these points low; all others are high. Here \(u\) is low,
the high points are precisely \(W\), and \(p\le9\).
For \(y\in W\), let \(q_y\) count its low saturated leave neighbors
in \(C\). These “friends” are in \(A\cup Z\), are distinct across
different \(y\), and each forces \(\delta_{ay}>0\) by the universal
twenty-star theorem at its saturated center \(a\).
Thus each friend supplies one homogeneous \(v\)-incidence at \(y\),
and
\[
Q=\sum_{y\in W}\max(q_y,2\mathbf1_{y\in T\cap C}),\qquad R\ge Q. \tag{2}
\]
The maximum, rather than an addition, handles possible overlap correctly.

When \(X=0\), let \(H_A\) count the one-hub incidences centered in
\(A\). A good \(A\)-point has none. Its deficient \(u\) is isolated
in its high leave. If its internal support degree is \(g\), the high
leave has \(g\) edges on its \(g\) other high points. Since
\(g\le4\), \(g\le\binom g2\) forces \(g=0,3,4\). A friend has
\(g>0\), and hence has exactly one of the first-star rows of the local
obstruction. There are at most \(H_A\) nongood \(A\)-points.

Take \(y\in T\cap C\) with unit \(v\)-deficit and a good friend \(a\).
The triple \(uvy\) is covered by \(y\in C\). The triple \(uay\)
is covered because otherwise it would charge the good \(A\)-center.
The triple \(vay\) is uncovered, \(\lambda_{av}=5\), and
\(\lambda_{ay}=4\). The independently checked combined local
obstruction gives \(e_u\ge2\); the forced friends give
\(e_v\ge q_y\). Therefore its one-hub cost is at least \(q_y+2\).

If there is no good friend, all \(q_y\) friends are nongood, and the
two-charge premise still gives at least \(q_y+2-n_y\), where \(n_y\)
counts the nongood friends. If there is a good friend the same weakened
bound follows from \(q_y+2\). Across these covered unit-v centers,
their nongood friends number at most \(z+H_A\). A low friend has only
one leave neighbor, which is the injection needed for this inequality.

Let \(h_c\) be the actual number of covered \(T\)-centers with
v-deficit greater than one. At those centers safely omit the additional
two units; at all other \(W\)-centers retain their forced friend costs.
Adding the separate \(A\)-cost \(H_A\) proves the stronger version
\[
R\ge q+2c-z-2h_c\ge q+2c-z-2(9-p),\qquad q=\sum q_y. \tag{3}
\]
The bound \(h_c\le9-p\) follows from the v-deficit sum9 on \(p\)
positive entries. No center cost is added twice: \(A\) and \(W\) are
disjoint, u- and v-incidences at a fixed center are distinct triples,
and each nongood friend saves at most one already charged unit.
The bound is valid even for \(q_y=0\), where the two-charge premise
alone supplies the required2.

## A classification-free exclusion of the entire flat branch

Let \(\mu\) count low-low edges in the v-link and let \(j=1\) if
the unique leave neighbor \(x\) of \(u\) is low, otherwise0. Low-low
edges form a matching. There are \(16-p\) saturated low points.
Removing \(x\) when low, and both endpoints of each saturated low-low
pair, gives the identity valid for **every** such v-link:
\[
q=16-p-2\mu+j. \tag{4}
\]
Every saturated low-low pair has \(\lambda\le3\): multiplicity5
contradicts the universal theorem, while multiplicity4 invokes the
credited sharp67 theorem for an uncovered19/20/20 triple and contradicts
size71. Hence
\[
X\ge\mu-j. \tag{5}
\]

Suppose \(X=0\). From (2) retain \(R\ge q\), and add this to (3).
Using (4) and \(R=5-z+c\), one obtains
\[
4\mu-2j\ \ge\ 4+z+2(9-p-h_c)\ \ge\ 4+z. \tag{6}
\]
But (5) gives \(\mu\le j\) and \(j\in\{0,1\}\), so the left
side is at most2. This contradiction excludes **all \(X=0\) cases**
without any nineteen-star classification, positive-mu profile assumption,
or separate700-case enumeration. It is a simpler proof, not a new
unrestricted packing bound.

If \(\mu=0\) and \(X\ge1\), (4) gives \(q=16-p\ge7\).
From (1), \(c\le5-z-2X\), so
\(R\le10-2z-4X\le6\), contrary to \(R\ge q\).
Thus the zero-mu branch is also closed without a census.

## Complete positive-excess finite coverage

Only \(\mu>0,X\ge1\) remains. The credited independently reviewed
nineteen-star classification has46 marked representatives and covers
every positive-mu nineteen-star. Marking \(u\) at every actual
replication-five point yields381 raw marks, with no code automorphism
assumption. Retaining repeated representatives preserves coverage.

[check.py](check.py) reconstructs literal quadruples directly from the
two anchor models. It tests each uncovered pair against all actual words.
For every mark it records all covered points, outside point, replications,
low-low matching, and each individual friend's target. It builds T_C
subsets by a charge convolution and derives the allowable z interval
algebraically, rather than applying the author's nested mask/integer loops.
The domain includes every \(T\cap C\), \(0\le X\le2\), and
\(0\le z\le5\) consistent with (1),(2) and available covered low points.
It intentionally includes inventories that may not be realizable.

Every one of the381 literal marks,13463 initial inventories and705
inventories retained by (5) matches both exported author readouts entry
by entry. The700 \(X=0\) rows can now be ignored by the ordinary proof
above. The five \(X>0\) rows are:

| Model,class,u | T_C | X | z | Q=R | Forced local center | Friends | Heavy SS edge |
|---|---|---:|---:|---:|---:|---|---|
|0,18,0|1,13,14|1|0|6|1|3,10|15,16|
|0,18,0|1,14|1|0|5|1|3,10|15,16|
|0,18,5|1,14|1|0|5|1|3,10|15,16|
|0,18,5|1,6,14|1|0|6|1|3,10|15,16|
|0,21,0|1,13,14|1|0|6|1|3,10|15,16|

All have \(\mu=1,j=0\). The mandatory saturated low-low edge consumes
the entire excess \(X=1\), so its deficit is2 and every other internal
deficit is unit. Its endpoints are not friends. Since \(R=Q\), there
is no \(A\)-charge or other unallocated nonnegative charge. With
\(z=0\), both friends are good \(A\)-points with unit internal deficits.
The center1 avoids the heavy edge, is in \(T\cap C\), and has unit
v-deficit. The same independently checked local obstruction therefore
applies, even though there is excess elsewhere: its two forced
v-incidences and two required u-incidences cost4, while Q allocates2
at that center. Other W centers still require their Q terms, forcing
\(R\ge Q+2>Q\). This excludes all five rows.

This completes the multiplicity-five transfer, and therefore the target
profile exclusion conditional on the stated imported premises.

## Reproduction, exact records and trust boundaries

Run from the repository root, sequentially:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-reviewer-5/profile71-charge-audit/check.py
python3 -B round-two/six-reviewer-5/profile71-charge-audit/local_pair.py
```

The same commands with `-O` give the identical exact records. No solver,
CAS, native mathematical code or nonstandard Python dependency is used.
Versions, actual commands, resources and entrywise-comparison evidence
are recorded in [VALIDATION.json](VALIDATION.json). The seven damaged
packing/inventory controls,381 arbitrary point relabelings,153 local-cost
checks,2625 exact dual identity checks,420 flat scalar exclusions and130
zero-mu positive-excess scalar checks pass. The compatible35-word control,
all144 accepted point maps, and three guard controls also pass.

The complete local search keeps the fixed200000-state/ten-second guard
per raw case. Hitting a guard raises INCOMPLETE and prevents COMPLETE.
All numerical/OpenMP threads are1 and every mathematical job is sequential
under the existing1CPU/2GiB scope. No killed process, timeout or incomplete
run supplies nonexistence. An early reviewer implementation error in the
positive-control variable scope was corrected before the fresh complete
normal and optimized runs; it gave no mathematical verdict.

Hashes bind compact exact readouts; they do not replace the ordinary
normalization, complete loop domains or literal collision proof.
The unchanged manifest inputs and exact provenance are in
[INPUTS.json](INPUTS.json). Large readouts, author certificates, ledgers,
keys and logs are not included. CPython integer/set semantics and the
unformalized mathematical bridges are trusted. The fixture completeness
and prior global hub-multiplicity exclusions remain imported as explicitly
stated above. In particular this review neither independently establishes
the whole generic twenty-star census nor silently upgrades the predecessor
chain into independently reviewed mathematics.

## Strengthening and improvement opportunities

**Proved.** Inequality (3) uses the actual heavy-v covered-center count
\(h_c\), improving the coarser bound whenever \(h_c<9-p\). Inequality
(6) quantifies that improvement and discharges the entire flat case before
any classification. The only nineteen-star readout needed for the final
argument is the five positive-excess records. A proof presentation can
therefore avoid treating700 repetitive flat records as essential evidence.

**Proved with the credited generic fixture coverage.** The group-free
local computation gives the combined bound \(e_u\ge2\), including zero
and one incidence, without importing the three separate shared-hub pair
certificates for this particular transfer. Its domain has no total-size,
hub-replication, ambient symmetry or full-automorphism-group hypothesis.

**Next independent audit.** The two most consequential remaining proof
dependencies are the generic twenty-star fixture coverage in8720 and the
global multiplicity-five theorem8783 together with its earlier0--3
chain. Their complete mathematical reductions need independently closed
coverage, not another replay of matching author hashes. I do not assign a
reviewer or predetermine either verdict.

**Possible structural simplification.** Replace the five-row classification
step by an ordinary implication from the low-low matching, unit-v center
and exhausted charge budget. The missing lemma must show, for an arbitrary
positive-excess nineteen-star obeying (1),(2),(5), that there is a covered
unit-v T center with enough good friends avoiding every heavy endpoint.
The present five-row readout establishes that implication only after the
credited positive-mu classification. No classification-free proof of that
remaining case is claimed.

Formalizing the disjoint-center charging injection and the pruned-cylinder
accounting would reduce the execution/ordinary-proof trust boundary.
Resolving the remaining size71 profiles is a separate research task; this
review supplies no implication that one profile exclusion resolves them.

## Literature and credited dependencies

Primary context was checked live on2026-10-01.
[Brouwer1975](https://ir.cwi.nl/pub/6883/6883D.pdf) proves
\(A(17,6,4)=20\). [Aw--Chee--Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf),
Theorem1/AppendixA, supplies the established69-word construction.
[Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html) still
records69--72 at this parameter; the campaign's reviewed upper71 is
separate prior work. Candidate-specific searches do not establish priority
for this restricted profile theorem, its charge argument, or these review
simplifications. Their historical novelty is unassessed. The graph-level
addition is an independent scoped audit and the proved simplification.

The fresh context also includes lemma8873,
`bafkreiel6uafvjn7nhdthbtt7c7yeva2u64thlcviwa4bothywqkpb3wam`,
the [two-hub multiplicity-one exclusion](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-1/multiplicity_one_exclusion/PROOF.md),
source `6693b35a653b8f78cb078b749159d7ada8e37b58`. It cites8820 as
context rather than a mathematical premise. It does not alter the present
proof or supply an independent review of it; no verdict on8873 is given.

Exact dependency artifact refs and pinned source hashes are in INPUTS.json:
8323 is the universal saturated-star input;8783/8637 provide the imported
global hub-multiplicity chain;8720 provides generic20 fixture coverage;
8537/8623 provide complete positive-mu19 coverage;8794/8855 provide the
restricted sharp67 input.8497 is the predecessor budget, directly derived
again above.8356,8397,8438 are older pair obstructions, inspected and
credited as transitive context. They are not falsely represented as fully
independently reviewed by this one scoped computation.
