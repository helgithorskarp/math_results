# Four-core compression of the XOR618 seed-growth cuts

**six-vdw-3, researcher; 2026-10-02.** Author-checked exact reduction,
with separate census/literal algorithms, constructive witnesses and strict
positive-RUP checks. No external-review verdict or formalization is claimed.

Let E be a three-point subset of F103 and let u:F103\E->{0,1}.
Write

    S={0,1,2,3,4},
    T={-2,-1,0,1,2,3,4,5,6,1/2,3/2,5/2,7/2}.

All arithmetic is in F103. For each nonzero r and p with p+r*S avoiding E,
define the regular core K=(p+r*T)\E. Let G(E) require every such K to be
mixed. Let F(E) require every nonconstant seven-term field AP avoiding E
to be mixed. F(E) concerns the orientation u itself.

**Exact reduction.** Normalize E affinely to {0,1,lambda}, with lambda
the least member of its six ordered-root transforms. The eighteen
representatives are

    2,3,4,5,6,7,8,9,10,11,12,15,16,19,20,21,25,47.

Under F(E), the whole G(E) family is equivalent to requiring only the
following listed cores to be mixed. There are no retained cores in the
other fifteen representative cases.

| lambda | Retained regular core |
|---:|---|
| 2 | 15,16,17,30,31,45,60,75,89,90 |
| 2 | 15,16,30,45,60,74,75,88,89,90 |
| 8 | 15,30,45,52,59,60,67,74,89,96 |
| 9 | 17,18,26,35,52,69,78,86,87,95 |

This retention is **irredundant under F(E)**, class by class. For each
listed core, [witnesses.json](witnesses.json) gives a coloring satisfying
F(E) and every other eligible G(E) cut in that same class, while that core
is all zero. The witnesses are certificates for this weaker field system.
Each has an explicitly checked bad outside-hole XOR618 cyclic progression.
They establish neither a cyclic coloring nor an interval coloring.

Across the eighteen representative instances there are 81,317 distinct
eligible regular cores: 81,313 contain a seven-term field AP and four do
not. This total adds separate normalized instances, rather than counting
raw hole triples or admissible colorings.

The [prior satellite lemma](../five-seed-satellites618/PROOF.md), source
13091ffdf1e909bccb36aa89ef4d2a702f936bb5, graph 9205
`bafkreibbwtzo6m3c2ahfo33ldjbtfz3qiz4lnugwa4ahjy5mr5cuhcgqoi`,
proves G(E) whenever the partial word

    c(t)=u(t mod103) XOR 1[t mod6>=3]

has no monochromatic nonzero-step cyclic seven-term AP avoiding E.
That cited input makes the four retained cuts valid in the XOR618 search.
The present equivalence, classification and weaker-system irredundancy
do not import its three native refutations. There is no new exclusion,
3704-point witness or W(2,7) bound.

## Why only four cores remain

If a regular core contains a seven-term field AP, F(E) already makes
that core mixed. It remains to classify the cores containing no such AP.
Normalize an eligible seed to S. The thirteen-point T has exactly these
six seven-term field AP supports, displayed in progression order:

    (0,1,2,3,4,5,6)
    (101,102,0,1,2,3,4)
    (102,0,1,2,3,4,5)
    (3,54,2,53,1,52,0)
    (4,55,3,54,2,53,1)
    (55,3,54,2,53,1,52).

Holes avoid S. To hit the first three supports, the holes must cover the
three edges of the path 101--102--5--6. Its minimum vertex covers have
size two and are {101,5}, {102,5}, {102,6}. To hit both of the next two
supports, the single remaining hole must be 53 or 54. Either also hits
the last support. Thus the complete three-hole transversals are

    {5,53,101}, {5,53,102}, {5,54,101},
    {5,54,102}, {6,53,102}, {6,54,102}.

No hole outside T can occur in a transversal using only three holes.
At most two holes cannot hit all six supports. The reflection x->4-x
pairs these six triples and preserves S and T. It transports arbitrary
orientations; it does not impose reflection symmetry on a coloring.

Use representatives E1={5,53,101}, E2={5,53,102}, E3={5,54,101}.
The maps 15x+30 and 88x+75 send E1 to {0,1,2} and give its two listed
cores. The map 59x+15 sends E3 to {0,1,8}; 86x+86 sends E2 to {0,1,9}.
The harmonic triple {0,1,2} has affine stabilizer of size two; the triples
with lambda 8 or 9 each have stabilizer of size one. The reflected
normalized triples duplicate the same transported seed/core pairs.
Hence there are precisely two, one and one retained cores.

Every distinct seed support is represented once by a half-slope/start
pair, or independently by its unordered first/last endpoints. To justify
uniqueness, a preserving affine map of S fixes its mean 2 and preserves
its centered second moment 10. Its multiplier therefore has square one;
the stabilizer is exactly the identity and x->4-x. The field has
characteristic 103, so 5 and 10 are invertible. The same mean/moment
argument for a seven-term AP uses 7 and 28. Reversal does not constrain u.

For three holes the usual six lambda transforms give the quotient.
The independent checker instead forms every affine image of each
representative and compares with all C(103,3)=176,851 raw triples. The
sixteen generic classes have 10,506 images each; the harmonic class has
5,253 and the equianharmonic class 47 has 3,502. All raw triples occur
exactly once in this quotient.

[generate.py](generate.py) classifies each transported core using the six
supports in T. [check.py](check.py) imports neither that implementation
nor the prior local-profile software. It reconstructs seeds and cores
from unordered endpoints, checks all 6,105,133 core endpoint pairs for
seven-term APs, compares entry-level transcript hashes and complete
exceptional rows, and exhausts all 152,096 seed-disjoint normalized hole
triples. Its second census applies all 63,036 affine maps to the six
transversals. Eight matches with normalized targets yield the same four
distinct seed/core pairs. Complete records and counts agree under -O.

The four constructive certificates have 100 regular bits each.
[check_witness.py](check_witness.py) reconstructs all 5,253 field endpoint
pairs and all eligible regular cores for each witness. Each satisfies
every outside-hole field seven, and its only constant eligible core is
the designated one. Thus omitting any retained cut would strictly weaken
F(E) together with G(E). No assertion of irredundancy under the stronger
full cyclic system is made: the cited satellite lemma already implies
every growth cut under that system.

## Explicit pair-model equivalence without native solving

The construction search uses variables p_xy=u(x) XOR u(y) for all 4,950
unordered pairs of the 100 regular points. Root at their least point R.
For every other pair x,y, four clauses enforce

    p_Rx XOR p_Ry XOR p_xy=0.

These 19,404 root-cycle clauses extend each anchored orientation word
uniquely and reconstruct u(R)=0, u(x)=p_Rx. Global color exchange accounts
for the other root color; there is no root unit.

For an outside-hole seven-field AP x_0,...,x_6, the full XOR618 cyclic
condition is that the four parities p_(x_j,x_(j+3)), j=0,...,3, are not
constant. Both signed four-pair ladder clauses enforce this condition.
The actual phase words and their complements give exactly the sixteen
seven-bit words with constant three-place parities. Constant field
orientations are two of these sixteen, so the cyclic system implies F(E).

A core with least point s is mixed exactly when its positive star

    OR_{x in K\{s}} p_sx

holds. Keep only the four listed stars in the eighteen cases. The full
and compressed models use the same variables. Their clause counts are
32,390--32,412 and 27,878--27,895 respectively. Neither has a no-five or
no-six hypothesis, fixed seed, weight bound, counter, extra unit or
imposed hole-stabilizer symmetry.

Here is a direct positive-RUP derivation of every removed star. Suppose
an AP witness lies inside K. For each of its four ladder edges xy, rooted
pair consistency implies the triangle clause

    D=p_sx OR p_sy OR NOT p_xy.

If s=R, D is already an input cycle clause. Otherwise put a=p_Rs.
Three original root-cycle hints verify D OR a by unit propagation:
under its negation, a=0 and p_sx=p_sy=0 force p_Rx=p_Ry=0, contradicting
p_xy=1. The other branch similarly verifies D OR NOT a using a=1.
Two hints from those additions verify D itself. Thus each needed
nonroot triangle takes three explicit positive-RUP additions.

Under the negation of the star, every p_sx is zero. The triangle clauses
force every AP ladder edge to zero, and its positive ladder input clause
conflicts. This verifies the star as another RUP addition. No empty
clause is proposed or checked. Since the compressed input is a subset
of the full target, and every target row is strictly derived with the
same variable domain, the two models have exactly the same assignments.

[compress.py](compress.py) generates these proofs directly; no solver or
converter is invoked. [check_extension.py](check_extension.py) visits
all 381,306 actual Z618 start/nonzero-step pairs in each case, checks
the entire literal sixteen-word relation before parity projection,
reconstructs all root truth rows and endpoint-derived cores, and compares
both full clause sets. It then strictly replays every positive hint and
requires every full-model target row to be present. Across all eighteen
cases, each Python mode checks 6,863,508 actual cyclic tuples,
321,019 additions and 960,153 propagation hints. The sums of the separate
full and compressed clause counts are 583,365 and 502,052.

The unit-propagation kernel is byte-pinned to six-vdw-1's credited strict
checker, source 223f0eaa45d24ff924e10edaa1e327fbf8a7259f, graph 7428
`bafkreic6ikxxfio6r5367szeoaz2mfhxt2vaakem7xr2mrmjgf5vy7cmou`;
[reader source](../../../van_der_waerden_618_binary_fibers/check_rup_lrat.py).
We call its positive-hint addition checker in an extension wrapper;
its refutation entry point, which requires an empty clause, is not used.
The wrapper forbids empty, tautological, malformed or noncanonical
additions and reports model equivalence rather than nonexistence.
Pair/ascent context is credited to [separable618](../separable618-exclusion/PROOF.md),
source f5985e678e95b4b122b9143cf4c8f411bc5e5232, graph 8985
`bafkreigpyvdzpke2nyx5dwabz6twmxpx4kpcrrfudup75wvpy7lmtycalm`.
Its intact-carrier refutations are not mathematical premises here.

## Scope and validation

The new information is an irredundant four-core basis under the weaker
field-seven condition, and an explicit checkable compression mechanism
for the pair search. It explains exactly where the full phase coupling
is needed for the prior growth lemma. It does not strengthen that lemma
to a full three-column exclusion.

A separate full harmonic native model with all 4,514 long cuts returned
UNKNOWN at 100,000 conflicts after 14.783 seconds. Its full-model SHA256
is the independently regenerated harmonic target hash in expected.json.
It was stopped without a retry or increased resources. The present proof
extensions perform no native search. The four weaker-system SAT proposals
only supplied explicit positive certificates; their independently checked
words, not their solver verdicts, establish irredundancy.

The frozen fixtures preceded the standalone compact-source restart.
That restart regenerated the census, both models and every proof stream,
repeated normal/-O literal and strict checks, checked all four witnesses,
and exercised repaired coverage, witness and proof damages. A fresh
selected-case restart additionally fetched the pinned helper and rejected
changed helper bytes before using them; it reported partial proof coverage.
Exact commands, pins and selective-coverage reporting are in
[README.md](README.md); completed provenance is in
[verification.json](verification.json). Large generated models and traces
remain outside Git. All jobs are serial, threads one, under the existing
1CPU/2GiB scope, with a 35-second guard per child stage.

[Monroe Tables 1 and 2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
were live rechecked 2026-10-02: two colors/seven terms >3703, with modulus
617. Monroe's length-first W(7,2) is this lane's color-first W(2,7).
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
provides the primary cyclic-construction context. The asymmetric three/
seven parameter is different. Bounded recent lane/graph/source comparison
found no duplicate of this four-core reduction; no exhaustive priority or
current-record assertion is made.

Trust remains in the cited conditional satellite input when applying
the cuts to XOR618, the written affine/cover/parity bridges, the byte-pinned
positive-RUP kernel and Python/runtime execution. Full outside-carrier
robustness and the interval-3704 construction remain unresolved.
