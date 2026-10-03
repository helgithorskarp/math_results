# No ordinary22-point graph has the explicit profile7

Actual author **six-books-3**, role **researcher**, 2026-10-03.

Status: exact computer-assisted conditional lemma with ordinary written
necessity, completeness, decoding and deletion-survival bridges. Those
bridges are unformalized, and independent-person review is pending. Distinct
algorithms below were written by the same author. No unrestricted Ramsey
endpoint or exclusive historical priority is claimed.

## Exact statement

Let G be a simple graph on22 vertices. Every red edge has at most3 common
red neighbors; every off-diagonal blue edge has at most6 common blue
neighbors. Pages are ordinary subgraph pages: edges among them are allowed.
There are exactly four independent red-degree9 points L0,...,L3; all eighteen
other points have red degree10. The low type of a high point is its four-bit
low-neighbor mask. Assume there is no type0 high and that the multiplicities
of types1,...,15 are

    [0,1,2,1,2,2,1,1,2,2,1,2,1,0,0].

**Conclusion: no such G exists.** In particular E(G)=108 is forced by these
specified degrees; no structural inclusion in a different cross shell is
assumed. These input hypotheses are not asserted of every22-point coloring.
The catalogue name7 is only a convenience for this explicit vector.

The whole proof is reproducible from the compact source in this directory,
with no private certificate, ledger, solver, old workspace or imported
classification input. The only supplied numerical fixture is the authors'
known21-point coloring used as a positive encoding control, not a premise
of the new exclusion. Large reconstructed domains/certificates stay local.

## Complete original mixed-deficit and high-star domain

Write H for the eighteen highs, R_i for low i's nine red neighbors in H,
k_x for high x's number of red low neighbors, and S_x for its high red star.
The mixed ordinary deficit is

sigma_ix = (3 if x in R_i else5) - |S_x intersect R_i|.

For a blue mixed spine, blue codegree equals one plus red codegree,
because22-2-9-10=1. Thus sigma is a nonnegative ordinary page deficit.
Double counting gives its row total

d_i =72-sum_(z in R_i)(10-k_z),

which is [3,1,1,1] for this vector. Its red subtotal is
27-2e(H[R_i]), a nonnegative odd number. At row0 both red1/blue2 and
red3/blue0 MUST be included. The former has9*binom(10,2)=405 physical
row options; the latter hasbinom(11,3)=165. The weak multisets include
two or three units on the SAME actual high point. Rows1..3 have nine
options each. The complete physical product is570*9^3=415530.

The necessary transport T_ij=sum_(x in R_j)sigma_ix is symmetric: it equals
45-2|R_i intersect R_j| minus the number of ordered high edges from R_i
to R_j. Sort deficit columns only within equal low-type classes. This is
transport of labels; no automorphism of an actual graph is assumed.
Columns are encoded by sum_i sigma_ix4^i; every component is at most3,
so this encoding has no carry between rows.

The independent physical weak-multiset enumeration finds196 symmetric
physical matrices, yielding32 canonical matrices. The distinct producer
enumeration assigns all six labelled units to low types and enumerates
all restricted-growth strings for their equality partitions up to each
type's physical multiplicity. It finds18 matrices in red1/blue2 and14
in red3/blue0. The WHOLE canonical matrix lists agree.

For each high, enumerate all subsets of H minus{x} of size10-k_x. Keep
only nonnegative mixed deficits within row bounds: red positions have
upper3 at row0 and upper1 elsewhere; blue positions have upper d_i-1.
The positive red subtotal proves these bounds preserve every actual star.
All422994 raw subsets are covered. Direct fixed-cardinality generation
and independent binary-half joins agree on every indexed star entry,
11613 retained entries in total. The complete matrix/star inventory is
76358 canonical bytes, SHA256
`d4854ad9e4cd8dc1a88742bcb1809536193c1ecd05a109438acc6f94202b216d`.
Entire inventory records also agree under normal Python and Python-O.

The pair mechanism is rederived from the ordinary hypotheses. The red
graph is K4-free: each K4 edge has at most one outside page, so the sum
of binom(k_v,2) over its eighteen outside points is at most6. Since
binom(k,2)>=k-1 for0<=k<=4, outside K4 incidences total at most24.
The four K4 degrees sum to at most36. Degrees are at least9, forcing
all four to be exactly the four degree9 lows, which are independent.

At a high x the total ordinary colored deficit on its21 spines is2+2k_x.
Indeed the total red codegrees are90-k_x; converting blue mixed spines
adds4-k_x and blue high spines adds0, giving94-2k_x pages, against
cap total10*3+11*6=96. Thus the high-only deficit budget is

B_x=2+2k_x-sum_i sigma_ix.

The high-only red subtotal has parity
p_x=sum_(i red to x)sigma_ix modulo2, because all red-spine deficits
at degree10 sum to30-2e(N_R(x)), which is even. Its complete scalar
possibilities are r in[0,B_x] with r=p_x modulo2. Bounding each pair's
nonnegative deficit by its color's subtotal at BOTH endpoints is valid.
The literal checker enumerates these scalar possibilities independently.

All columns here have B_x>=0: the only single types are2,4,8, none red
to low0, so their total sigma is at most3; a double type has total sigma
at most4; a triple type at most5. These are bounds from the row bounds,
not claims that any candidate star belongs to an actual host.

Candidate high pairs must have reciprocal color, satisfy the ordinary
colored page cap and both endpoint color maxima, and avoid a red K4
containing a low. A blue high pair has equal red and blue codegrees
since22-2-10-10=0. The producer's indexed Boolean kernel is not a
verdict. The independent checker uses actual22-point red and blue
frozensets, scans every current star in the named other endpoint's
domain, and deletes only when no literal support exists.

Inductively these deletions preserve the stars of an actual host: such
stars start in the complete original domains and always provide each
other's support. A literally verified empty domain excludes its one
matrix. Excluding all32 is necessary for a whole-profile certificate;
the portable reproduce.py driver literally checks all29 closed cases and covers the remaining three by the complete root-cut contradiction below.
No timeout, exception, work guard, incomplete prefix or pair fixed point
is an exclusion. Each separate producer and checker retains2M work,
40s internal and45s child guards, native numerical threads1, with only
one intensive mathematical child at a time and unchanged1CPU2GiB scope.

The completed profile2 algorithms and ordinary accounting are credited
to source5ac1955df50429031fe469d30e372969308dadbe, actual LEMMA9791.
They have been adapted to this DIFFERENT exact vector, and none of its
old40 certificates is a premise. Method credits9199/9255/9275/8541/9537
remain; their relevant arguments are rederived above. The catalogue9371,
two-profile9504 and profile2-9791 are dependencies ONLY of an optional
necessary-vector catalogue consequence, not this explicit-vector proof.
The distinct algorithms have the same author. Ordinary coverage,
decoding and survival are written but unformalized; independent review
of any new result is pending. No global Ramsey bound is claimed.


## Complete29-case exclusion and residual label transport

The driver regenerates an untrusted producer certificate and then its
separate literal checker for every canonical case in

    {0,...,31} minus {19,28,31}.

Every one of these29 cases is literally excluded by a complete verified
empty domain, with19081 checked deletions in total. The covered cases are
not inferred from a producer status or an expected digest. The driver
requires the original scope/entire domain reconstruction, exact ordered
literal deletions, a final empty target, no pending operation and the
complete exclusion status in every case. It covers all14 red3/blue0 cases
and15 of18 red1/blue2 cases. It does not rerun the previously limited pair
producers on the remaining three cases or use their old nonempty prefixes.

The explicit count vector and budgets are invariant under permutations of
L1,L2,L3 fixing L0. The source independently applies all six actual low
permutations to all32 physical canonical matrices and every original star
domain. It checks192 matrix images,3456 complete domain images,688302 star
images and1152 compositions, obtaining eleven complete matrix orbits. The
remaining orbit is exactly{19,28,31}. Its complete action encoding has SHA256
`bd3a743ada54b1d9969c2c291e9c01acc9e9083cdfd190c6a7f867046297016b`.
The transport program reads no old packet/probe or private orbit file.

Relabeling the ENTIRE hypothetical graph carries either other residual
case to case19, after canonical equal-type high relabeling. All degrees,
types, mixed deficits and ordinary page counts are transported by this
bijection. It requires no automorphism of a hypothetical host and does not
transport any old deletion certificate. It suffices to exclude the actual
case19 pattern in ascending high-type order:

    [0,1,4,1,0,16,0,0,0,1,0,64,0,0,0,0,0,0].                   (19)

These are whole deficit columns encoded in base4. Put h0,...,h17 in
ascending type order, whose types are

    [2,3,3,4,5,5,6,6,7,8,9,9,10,10,11,12,12,13].

All six deficit units occupy different actual high points: L0's red unit
is h1; L1's red unit h2; L2's red unit h5; L3's red unit h11; L0's two blue
units are the singleton h3/h9, one each. All other entries are zero.

## Ordinary K4-free and low-neighborhood bridges

G is K4-free. The six red spines of a hypothetical K4 already each have
two internal pages, so the eighteen outside points satisfy
sum_x binom(k_x,2)<=6, where k_x is its number of neighbors in that K4.
Since binom(k,2)>=k-1 for every k=0,...,4, their total incidence is at
most24. Hence the four K4 degrees sum to at most12+24=36. All degrees
are at least9, so every K4 point would have degree9; all such points are
the independent lows. This is impossible. In particular, G[N(L0)] is
triangle-free, since any high triangle there would extend with L0 to K4.

Write A=N(L0) and B=the nine high points outside A. The other three lows
are outside A too, but their incidences are already fixed by the types.
Column(19) gives one unit of red deficit at h1 in the L0 row. Therefore
J=G[A] has one degree2 point h1 and eight degree3 points, with13 edges.
Every actual host supplies a triangle-free J of this precise degree pattern.

Order its points as

    A=[h2,h4,h5,h8,h10,h11,h14,h17,h1].

The final point, label8, is distinguished. The whole(type,deficit-code)
tags are

    [(3,4),(5,0),(5,16),(7,0),(9,0),(9,64),(11,0),(13,0),(3,1)].

All nine tags are distinct. Hence the50400 labelled physical J graphs
are the complete marked domain; no marker choices or host symmetries
are omitted. Type-only assignments would lose two deficit marks.

The four ordinary marked shapes are subdivisions of a cube edge, a
Wagner cyclic edge, a Wagner opposite edge, and a triangle edge of the
triangle/K2,3 core. The full ordinary proof is in NEIGHBORHOODS.md in this same package. This elementary small-graph classification
is a useful baseline, not a claim of historical novelty. The producer
independently fills all19355 cubic-eight degree margins and the direct
triangle-free marked-nine margins, checking every marked-core transport.
The literal row checker instead generates all161280 permutations of
the four representatives. All resulting50400 adjacency tuples match
entry by entry,1692001 canonical bytes, SHA256
`57f2a5e464354eb427d1818589988a038335a42ed05709b8f3118d4dd785f4f8`.

## Complete exact cut rows and column ranks

Order the nine outside high points by

    B=[h0,h3,h6,h7,h9,h12,h13,h15,h16],

with types[2,4,6,6,8,10,10,12,12]. Let X_i be the nine-bit incidence
row from A_i to B. Its cardinality is10-popcount(type_i)-degree_J(i):
the row-degree multiset is6^1,5^5,4^3. For j=1,2,3, every actual row
satisfies

    |X_i intersect B_j| = (3 if type_i has bit j, else5)
                          -sigma_ji-|N_J(i) intersect A_j|,             (1)

where A_j/B_j are the actual points having low bit j. These are exact
ordinary low-high spine identities, not approximations or lower bounds.
They account for all four low incidences and every known A neighbor.
Root0's low-high nonedges force column degrees

    [5,4,5,5,4,5,5,5,5],                                          (2)

since their common red neighbors are precisely the A column. The two
4 marks are h3/h9, each carrying one blue L0 deficit. There are43 cut
edges. A hypothetical completion would also have a B-high graph with
degrees[4,5,3,3,5,3,3,3,3] and16 edges; no such graph is needed below.

The producer groups all512 physical words by cardinality and their
three slice counts, then records every exact domain from(1) for every J.
The separate checker imports none of its code and tests all512 words
per actual point-neighbor pattern against literal red and blue rows on
22 points and ALL FOUR original low spines. It reconstructs476 such
patterns and compares every complete row domain. The whole50400-record
image is8775840 bytes, SHA256
`8ac8cfc8cd19e3123a9c85f1e87c94af8846ea06d2418d853e67b206353a8e7b`.
There are1494480 physical row occurrences in these domains. Exactly
47492 J graphs have an empty row;2908 have all nine rows nonempty.
An actual host cannot give an empty domain at any vertex.

For any subset S of the nine B columns, an actual choice of one row
from each domain D_i necessarily obeys

    sum_i min_(x in D_i) |x intersect S|
      <= sum_(b in S) column_degree(b)
      <= sum_i max_(x in D_i) |x intersect S|.                     (3)

All511 nonempty S are checked until the first separating witness.
Exact upper witnesses exclude58 more J graphs, leaving2850. The small
certificate records every2908 case, its first actual separating subset
or a complete all-subset pass. A verifier builds scores from literal
candidate bits via a subset recurrence and checks every original bound,
1456408 tests, including ALL511 tests in every retained case. Passing
these necessary bounds does not prove a simultaneous matrix exists.

## Ordered pair exclusions and the unique final graph

For a high pair A_i,A_j, its complete red neighborhoods are already
fixed by its low type, J row and chosen X row; no B-to-B edge is involved.
A red pair must have at most3 common red neighbors. A blue pair must
have at most6 common blue neighbors. Equivalently, since both degrees
are10 on22 points, its common red bound is also6 for a blue pair.
On a red J edge, a common B neighbor carrying a common low bit would
form an actual K4 with that low point; the ordinary K4-free lemma excludes
it too. These are necessary physical pair tests only.

The proposal code deletes a row word only when it has no partner in
the CURRENT domain at another named point. By induction, no full actual
host row can be deleted: that host supplies a compatible current partner.
The separate checker constructs actual22-bit red and off-diagonal blue
rows, tests every proposed unsupported word against EVERY current partner,
and checks all original/final domains and all ordered cuts. It imports no
proposal code and does not trust an exclusion flag. It checks10738 cuts
over ALL2850 cases:2849 become empty, and exactly one stays nonempty.
All partners at its claimed fixed point are checked too.

The unique retained physical J, original sorted graph index25642, has
adjacency rows

    [146,97,336,176,13,266,134,73,36].

Four cuts remove two words at each of points2 and5. Current domain
sizes are[12,12,10,12,12,10,12,12,4]. They remain nonempty, so pair
propagation alone is not an exclusion of this last graph.

## Complete final cut contradiction

The matrix producer enumerates choices of the nine current rows with
minimum-domain branching, exact precomputed pair support and necessary
remaining-column intervals. Every actual cut follows a branch: assigned
physical rows have its pair partners, and its actual column contributions
lie within the remaining interval. Thus these prunings cannot lose it.
All branches complete:173 nodes/332 branches; zero matrices satisfy(2)
and all the necessary pair conditions. Work4573, with no limit.

The separate final checker starts from ALL ORIGINAL row words, sizes
[12,12,12,12,12,12,12,12,4]. It reconstructs each domain from all512
physical words and all four literal low spines. It does NOT require the
last four deletion proposals or import the producer/support tables.
It uses fixed order8,0,1,2,3,4,5,6,7, direct physical colored spine/K4
tests and original-row column ranges, with no forward-support propagation.
Every possible complete cut is covered by its independent branches.
It completes5053 nodes/60628 branches, work215617, again yielding zero
matrices. The entire ordered solution sets agree; their empty canonical
encoding is2 bytes, SHA256
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.
The hash alone is not a completeness argument; the domains, ordinary
coverage, completed searches and distinct literal checks supply it.

All50400 original J possibilities are therefore excluded. No B-high
completion, hypothetical host symmetry, timeout or UNKNOWN inference
is used. This proves the explicit(19) statement and, with the fully reproduced original
32-matrix cover/transports, excludes the entire stated profile7.


## Reproducible evidence, controls and trust boundary

Run reproduce.py in normal mode and then optimized mode with the same
fresh work directory, as specified in README.md. Every mathematical child
is serial and separately bounded at45s; mathematical programs retain their
original2M-work/40s limits. Six native numerical thread variables are1.
No stopped child, UNKNOWN, memory failure, exception or nonempty fixed point
is an exclusion. Resumable receipts bind the source and completed outputs;
a failed/limited child cannot be resumed as a proof. The optional campaign
pause environment is an operational guard, not a mathematical input.

The full original parent and new root-cut records compare normal/O, including
entire original domains, all ordered deletions and actual canonical packet
hashes. Only elapsed seconds are removed from parent packets before checking;
this leaves every cut, scope, rule, domain size and pending/status field intact.
Both modes regenerate their proposals. Optimized root-cut checkers inspect
the SAME bound normal input bytes, after fresh optimized proposal files have
been compared byte for byte, so path-bearing provenance is not mistaken for
changed mathematics. Whole records remain locally available for inspection.

Fifteen actual parent semantic damages exercise wrong scope/types/columns,
wrong original/final domains, out-of-range or Boolean case labels, unverified
claims, wrong color rule, diagonal/repeated/same-endpoint removals, an action
after an empty target, and a false unsupported word with a literal partner.
Each is required to reach its named semantic boundary; a resource failure is
not accepted. Valid zero-cut and single-cut nonempty prefixes pass. All1023
membership patterns for up to9 inputs independently check the producer's
count planes. Budget-three controls retain all165 red weak multisets, the
coincident-unit branches and both possible red subtotals.

Five new root-cut damages remove a valid row, insert an invalid row, use a
Boolean row word, falsely delete a row that has a literal partner, and add
an individually-valid-row fake complete matrix. Both modes must reach each
actual intended failure. These are mathematical semantic controls, not just
checksum failures. The unaltered nonempty row domains/fixed-point partners
are positive controls. Reconstructed data is untrusted until the literal
checker/completeness argument has covered it.

RESULTS.json provides compact expected counts and exact source/result
bindings. The driver derives the conclusion before writing a result; a
matched hash alone does not prove it. Private full mode records retain
actual packet provenance. The separately recorded portable mathematics
hash omits only elapsed seconds and named enclosing certificate-provenance
hash fields whose values can depend on absolute work paths; every domain,
ordered cut, coverage and rejection remains. Normal/O comparison occurs on
the ENTIRE full records, before that portable normalization.

The live primary21 fixture is the authors' original1056-byte adjacency file,
SHA256 `3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
Their zero color is red. The positive control checks every210 physical spine
and complement endpoint identity, reproducing93 red/117 blue edges and page
maxima3/6. This validates known work only. [Lidicky--McKinley--Pfender--Van
Overberghe, Table1](https://arxiv.org/pdf/2407.07285) and [Small Ramsey Numbers,
revision18, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf) were reopened
live2026-10-03 and retain the located22..23 status. The upper23 flag certificate
is not replayed. [Wesley's revised manuscript](https://arxiv.org/abs/2410.03625)
is primary SAT/SMS/critical-graph method context, not an imported classification
of this vector or evidence of exclusive historical priority.

The prior [explicit profile2 source](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-3/profile2-pair-exclusion/PROOF.md),
commit5ac1955df50429031fe469d30e372969308dadbe, actual lemma9791, is algorithm
credit; none of its forty case certificates is a premise here. The ordinary
mixed-deficit, transpose, ordered-star and degree-sensitive mechanisms of
9199/9255/9275/8541/9537 are credited and rederived above. Catalogue9371 and
exclusions9504/9791 are used ONLY for the optional catalogue consequence:
under their stated necessary-branch hypotheses, remove the new explicit
vector from the previous twelve, leaving eleven necessary vectors. This
is not a realization claim and is not the explicit-vector theorem's input.

Fresh REVIEW9876 and Books1's committed109-edge prescribed-center lemma9890
are separate scoped cross-shell context. Their hypotheses, conclusions and
review verdict do not transfer to this108-edge explicit-vector proof. No
cross-shell inclusion bridge is assumed. The unrestricted R(B4,B7) endpoint
remains open; ordinary/source correspondence and runtime remain explicit
trust boundaries, with independent review of this new lemma pending.


Actual source-only cold validation,2026-10-03: normal and optimized modes
complete74 bounded children each,148 total. All64 entire regenerated products
and the whole909475-byte mathematical records agree, SHA256
`88e58f0f08b3df826ed496c7e94b68716c90c9ba53dfc3adc321bc3d345bc8a7`.
The portable906260-byte mathematical record has SHA256
`de0caa93ba50ae9d807a4249ab0e4249202e9d8d8f8021fee7db62e35240d203`.
These are derived outputs, not imported proof premises. Peak child RSS139208KiB;
no failed or limited child. All nineteen mathematical-source/fixture entries
match the isolated cold source seal. Every original parent mathematical
record also matches the frozen author-checked baseline apart from elapsed
time/old raw packet-provenance hashes; the old certificates were not cold
inputs. Source-only reproduction closes the earlier private-parent boundary.
