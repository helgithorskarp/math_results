# A pentagon bridge excludes a complete branch of the live M216 profile

**Theorem.** Every graph on 43 vertices with red degree multiset
`19^2 20^5 21^36` and an induced copy of `Q = P4[C5]` has a red or blue
five-clique. Here brackets mean the lexicographic product: four disjoint
pentagons, with all cross-bag pairs red exactly along a four-vertex path.

This decides the entire candidate branch with that configuration, including
every placement of its vertices among the degree classes. The induced core
fixes 190 physical pairs; all other 713 pairs vary subject to the full degree
profile. No count of graphs after imposing degrees is claimed. There is no
global automorphism, global module, neighborhood, catalog input, or selected
outside attachment in the family definition.

The degree profile is the live one in the
[M216 intrinsic partition](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m216_intrinsic_partition)
at Discovery Net height 3481, source commit
`54a9b2476eeeeb251d505291e14abd5d4f83dc86`. Its triangle caps and exceptional
edge theorem are unnecessary for this exclusion. Thus the configuration is
forbidden throughout all fifteen stated complete formulas. **None of those
fifteen general formulas is decided here:** a candidate may avoid Q. Neither
Q nor the earlier 24-vertex configuration is forced in the whole profile.
There is no decrease in the inherited 66-profile / 271-split census and no
new Ramsey-number bound or 43-vertex target.

## Connection to the deleted pentagon product

The previous
[deleted-product theorem](../ramsey_r55_deleted_pentagon_product)
excludes arbitrary 43-vertex completions of `H = C5[C5]` minus one vertex.
Deleting H's remaining four-vertex path leaves exactly Q, its four full
pentagon bags. This proof transports the same bag-activity classification
into a specified live degree-profile branch. It frees every pair incident
to those four path vertices and uses the global degree bound to control all
23 outside vertices. It does not start an unrelated fixed-core family.

The new theorem is not a claim that the old 24-vertex core is forced.
Its additional profile hypothesis and weaker 20-vertex induced configuration
have distinct scope from the old unrestricted-completion theorem. The prior
artifact is preserved unchanged. The argument below is self-contained;
reading or replaying the prior package is not required.

## Four-bag attachment classification

Label the four bags `B_i={5i,...,5i+4}`, for `i=0,1,2,3`. Inside a bag,
red adjacency means consecutive coordinates modulo five; between bags it
means `|i-j|=1`. Q has 95 red and 95 blue pairs. It contains no monochromatic
five-clique: a clique uses at most two bags and at most two vertices per bag.

Suppose an outside vertex x does not already create a monochromatic five-set
with four core vertices. Put i in R if its red neighbors in B_i contain a
red edge; put i in B if its blue neighbors in B_i contain a blue edge.
Red-adjacent outer bags cannot both lie in R, and blue-adjacent outer bags
cannot both lie in B. Hence R is independent in P4, B is a red clique in
P4, and both sets have size at most two.

Each full pentagon belongs to R union B. Otherwise it would partition into
an independent red-neighbor set and a red clique of blue neighbors, each of
size at most two. The four bags therefore partition disjointly between R
and B. The only compatible partition is `R={0,3}`, `B={1,2}`.

Consequently the blue neighbors of x in each end bag form a red clique:
the empty set, a singleton, or one of the five pentagon edges. In each
middle bag its red neighbors form an independent set, with the analogous
11 choices. These are also sufficient: every core monochromatic K4 is
formed from two edges in a same-color outer pair. There are exactly
`11^4 = 14,641` admissible 20-bit stars.

## The global degree contradiction

Use the end bag S=B_0. Each of its vertices has seven red neighbors inside Q:
two in S and five in B_1. All five global red degrees are at most 21. Thus
there are at most `5*21 - 5*7 = 70` red incidences between S and the 23 outside
vertices, and at least `5*23 - 70 = 45` blue incidences.

For an admissible outside vertex its blue set in S is a clique of size at
most two. Call a vertex ordinary if this set has size two. If there are m
ordinary vertices, the total blue incidences are at most `2m+(23-m)=23+m`.
Therefore m is at least 22.

For i modulo five let C_i contain the ordinary vertices whose blue set in S
is the edge `{i,i+1}`. These five classes partition the ordinary vertices.
Every vertex in `C_i union C_(i+1)` is blue to `i+1` and red to both `i+3`
and `i+4`; the latter two core vertices are red-adjacent.

If this union has at least nine vertices, the elementary bound R(3,4)<=9
gives either a red triangle or a blue four-clique inside it. A red triangle
extends through the red core edge `{i+3,i+4}` to a red K5; a blue four-clique
extends through `i+1` to a blue K5. Thus avoiding K5 requires

    |C_i| + |C_(i+1)| <= 8    for all five i.

Adding gives `2m <= 40`, contradicting `m >= 22`. This proves the entire
43-vertex branch exclusion. It uses all 23 outside vertices through the
degree sum and class counts; it does not assume they form any prescribed
graph or share a single attachment.

For completeness, R(3,3)<=6 follows by examining three same-color neighbors
of one vertex. In a triangle-free graph on nine vertices with no independent
four-set, each degree is at most three. A degree at most two leaves six
nonneighbors, which contain an independent triple by R(3,3)<=6, giving an
independent four-set with the original vertex. All nine degrees would then
be three, contradicting handshaking. This proves R(3,4)<=9 without a catalog.

## Exact certificate and independent finite checks

`derive.py` checks all 256 activity words and gives compact local pattern
factors, all five class-pair supports, and a six-row integer certificate.
With variables `c_i=|C_i|`, its rows are the five pair caps and
`-sum(c_i)<=-22`. Multipliers `(1,1,1,1,1,2)` cancel every coefficient and
yield the contradiction `0<=-4`. Each row is justified by the proof above.
The numerical cancellation alone is not credited with that graph meaning.

`check.py` imports no producer. It reconstructs the core by literal cycle
and path edge tables, checks its 15,504 five-subsets, and enumerates all
75 red and 75 blue core K4s. It then tests **all 1,048,576 possible stars**
against those literal four-cliques. The full satisfying set agrees entry
by entry with the factorization: 14,641 admissible, 1,033,935 rejected.
The sorted decimal-mask stream with one newline per mask has SHA-256:

    cd1ef77b6af2e3159a0597637f610188eb27893f7c60ba1e2dc4988aabaa929b.

The checker reconstructs every class support and the physical degree identity,
then checks the exact cancellation. Independently, it enumerates all 59,049
five-tuples in `{0,...,8}^5`: 8,105 satisfy the pair caps, their largest sum
is 20, and only `(4,4,4,4,4)` attains it. This finite occupancy check validates
the count inequality; the displayed proof supplies universal graph coverage.
No native SAT solver, floating-point bound, or external certificate is used.

## Full physical witnesses

`extract.py` accepts JSON fields `n:43`, `red_edges` (unique ordered physical
pairs), `core_embedding` (20 distinct physical labels in the stated core
order), and `core_color` (1 means the named red profile is physical red;
0 means its color reversal). It validates every degree and core pair.
Finding an embedding is not implemented: the caller supplies one.

The extractor returns an actual monochromatic five-set. It either detects
a forbidden one-vertex attachment or uses one of the five class unions and
the red-triangle / blue-four alternatives. `verify.py` imports neither
extractor nor producer. It independently validates the full profile, the
190 core pairs, the five labels, and all ten physical witness pairs.
Wrong-family inputs are rejected rather than given a Ramsey verdict.

The six compact fixtures are deliberately **non-Ramsey graphs**, covering
both color orientations and all three extraction mechanisms. The two global
mechanisms have all 23 individually admissible stars. They are degree-correct
43-vertex graphs, so neither one-vertex feasibility nor the degree equations
alone establishes a target. Their construction is deterministic: balanced
pentagon-edge class multiplicities, a Havel-Hakimi outside realization, and
one specified degree-preserving rectangle for the bad-star examples.

Controls include eight scrambled-label versions per mechanism/orientation,
plus degree-class transfers placing degree-19 and degree-20 vertices inside
the core. They reject four kernel-certificate mutations, four physical-witness
mutations, and six malformed graphs in both extractor and verifier. These
are author-written independent checks, not an external review or formalization.
No broad search or representative sampling is claimed for the fixtures.

## A usable constraint schema and its boundary

For any injective map f from the 20 core labels into a complete-profile graph,
the following 190-literal clause is valid under that profile and the Ramsey
constraints, with Boolean red-edge variables x:

    OR_(uv in E(Q)) NOT x_(f(u),f(v))
      OR_(uv not in E(Q), u<v) x_(f(u),f(v)).

It says that the embedded pairs cannot all equal Q. The schema covers every
embedding and every degree-class placement; no symmetry representative has
been selected. It is a profile-conditioned consequence, not an unconditional
clause for arbitrary graphs. This package does not enumerate embeddings,
append the clause to another encoding, or decide the fifteen M216 formulas.
A consumer must use its actual physical variable map and full hypotheses.

## Reproduction and scope

Python 3.11.2 standard library, no packages, external data, solver, build,
private input, or omitted large artifact. From this directory:

```sh
python3 -B reproduce.py
```

Expected final status: `VERIFIED_PENTAGON_M216_COMPLETE_CANDIDATE_BRANCH`.
It checks the file manifest and regenerates the certificate, exhaustive
kernel, fixtures and controls in normal and optimized Python, comparing the
outputs byte for byte. The displayed universal proof remains unformalized.
Trust also includes code/parsing, exact Python semantics and ordinary hardware;
hashes establish identity, not mathematical correctness.

For a supplied graph:

```sh
python3 -B extract.py graph.json > witness.json
python3 -B verify.py graph.json witness.json
```

The M216 source defines the live profile but contributes no imported code or
catalog completeness premise to this proof. Its fifteen-key cover remains an
upstream result; the literal profile theorem here does not require that cover.
For classical product context see
[Wigderson's PCMI 2025 Homework 8, optional problem 3](https://ywigderson.math.ethz.ch/math/static/pcmi2025/Homework8.pdf),
and for primary Ramsey-extension context see
[Angeltveit--McKay](https://arxiv.org/html/2409.15709v2).
A limited live search found no matching exact application; no historical
priority or new general-method claim is made for these classical mechanisms.

This is one completed bridge to a defined candidate branch. No general
forcing of Q, smaller-core ladder, new parent search, whole M-slice closure,
or further proof phase is claimed or begun. M215, the old neighborhood and
catalog routes, and the teammate's construction experiments stay parked.
