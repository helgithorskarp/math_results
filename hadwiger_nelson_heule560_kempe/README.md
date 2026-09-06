# Exact interface of the complete one-pair Kempe family

The fixed 560-vertex seed has a family of **118 distinct mandatory-set
colourings**, obtained by every choice of components for each of the six
colour pairs in the saved colouring. We certify exactly which of all **2^68
optional subsets** extend at least one of those colourings. Ten covering
colourings prove every positive case; nine sets of size three or four are the
complete minimal failures of this finite recolouring mechanism.

This closes **1,409,416,830,037,074** of the **1,469,568,786,235,308** labelled
508-vertex supports in the accepted M492/U68 family, or **95.9068%**. The
remaining **60,151,956,198,234** supports are outside this certificate. They
are not asserted to require five colours. No graph with at most 508 vertices
and chromatic number five has been established.

## The finite recolouring family

Let G be the 560-vertex, 2,758-edge graph from the
[accepted seed and mandatory-set reduction](../hadwiger_nelson_heule560_family_review1/README.md).
Its published [boundary](../hadwiger_nelson_heule632_minimize/boundary.json)
partitions V(G) into M of size 492 and U of size 68. Every non-four-colourable
subgraph of G contains M. Fix c on M by restricting `cover_colouring` in the
[free50 certificate](../hadwiger_nelson_heule560_degree_family/certificate.json).
The preceding [three-pair interface](../hadwiger_nelson_heule560_interface/README.md)
fully characterized extension of that one c and closed 85.7191% of the target
family.

For each unordered colour pair {a,b}, take the connected components of the
subgraph of G[M] induced by vertices with c-colour a or b. Exchange a and b on
any union of these components. The resulting colouring of M is proper:
edges within a switched component still have different colours; there is no
a/b edge between different such components; and an edge to a vertex of either
other colour cannot become monochromatic. These are Kempe component exchanges.

Define K to be the union of the resulting colourings for all six pairs,
identified under global palette permutations. **Each exchange uses components
of the original c and a single pair.** Arbitrary choices of components for
that pair are included. Sequences that change the pair, or recompute
components after another pair's exchange, are not part of K. This is not a
claim about the full Kempe-equivalence class or all proper colourings of M.

The exact component sizes, ordered by smallest host label, are:

| Pair | Component sizes | Choices modulo complementary exchange |
| --- | --- | ---: |
| 0,1 | 244,1,3,4,1,1,1 | 64 |
| 0,2 | 239,2,4,6,1,1 | 32 |
| 0,3 | 253,1,5,1 | 8 |
| 1,2 | 46,37,147,1,1 | 16 |
| 1,3 | 239 | 1 |
| 2,3 | 236,1 | 2 |

Exchanging a component subset and its complement differs by the global
permutation interchanging a and b. The producer therefore leaves the first
component unswitched and enumerates every subset of the others. There are
123 such slots. Normalize a colouring by naming its colour classes in order
of their first occurrence on increasing M labels, then deduplicate; this
gives **118** templates. Global permutation preserves extension existence,
since the same permutation can be applied to an optional colouring.

The independent checker constructs components by union-find and enumerates
**all 246** component-subset slots, without the complement quotient. It obtains
the same complete normalized template stream, SHA-256
`faad386a59949ff5b2c22cf2b8615cf1cccd777126e09342169299c0a801c3da`.
All 118 templates are directly checked on 2,390 mandatory edges each, for
282,020 proper-edge checks.

## Complete classification

For every T subset U, some colouring in K extends to G[M union T] **if and
only if T contains none of these nine sets**:

```text
{362,409,604}
{362,431,604}
{362,434,604}
{362,530,604}
{310,358,406,613}
{310,358,409,613}
{362,406,604,613}
{310,406,613,615}
{310,409,613,615}
```

All labels are host labels in the exact 632-point input, not sparse
fresh-centre identifiers. The union of the nine sets is

```text
E = {310,358,362,406,409,431,434,530,604,613,615}.
```

For necessity, for each of the 118 templates d define

\[
L_d(v)=\{0,1,2,3\}\setminus\{d(w):w\in M,\;vw\in E(G)\}.
\]

For every displayed set B, the checker exhausts all assignments from these
lists on G[B] and finds none proper, for every d. This is **1,062 complete
template/set problems**. There are 822 total assignments to check; many
problems have an empty list and therefore no assignment at all. Each problem
has at most four vertices. If B is contained in T, no d in K can extend to T.
This is an exhaustive negative statement about **K**, not about all colourings
of M or the chromatic number of G[M union B].

For sufficiency, the compact certificate supplies the following ten proper
colourings, with their mandatory restrictions belonging to K:

| Vertices omitted from G | Retained vertices | Unit edges | Template index |
| --- | ---: | ---: | ---: |
| 310,362 | 558 | 2,740 | 50 |
| 310,604 | 558 | 2,746 | 50 |
| 362,613 | 558 | 2,741 | 0 |
| 604,613 | 558 | 2,747 | 0 |
| 358,362,615 | 557 | 2,731 | 1 |
| 358,604,615 | 557 | 2,737 | 1 |
| 362,406,409 | 557 | 2,732 | 0 |
| 406,409,604 | 557 | 2,738 | 0 |
| 406,409,431,434,530 | 555 | 2,716 | 20 |
| 409,431,434,530,613 | 555 | 2,718 | 20 |

Template indices are zero-based in the sorted canonical stream. Only **four**
of K's 118 templates are needed for these witnesses. Thus these four templates
already have exactly the same optional extension coverage as the entire K.

The ten omission sets are precisely the minimal hitting sets of the nine
forbidden sets. The checker independently exhausts all 2^11 = 2,048 endpoint
selection patterns, finds all 1,344 patterns avoiding the forbidden sets,
and verifies the complete maximal positive boundary. Every good pattern lies
in a listed cover. Each of the other 57 optional vertices can be present in
every cover. Consequently restricting one of the ten proper colourings proves
sufficiency for any T, without a cardinality bound. All 27,346 retained-edge
inequalities and exact support masks are checked.

Every proper subset of each forbidden set lies in a positive cover, also
checked directly. Hence all nine failures are minimal, and completeness of
both sides follows from these finite boundary arguments. Neither Boolean
projection nor its search status is a premise of this proof.

## Cardinality counts and target consequence

The polynomial counting good endpoint patterns is

\[
P(x)=1+11x+55x^2+161x^3+299x^4+361x^5
        +281x^6+135x^7+36x^8+4x^9.
\]

The full extending-subset polynomial is **(1+x)^57 P(x)**. Its coefficient
at x^16 is 1,409,416,830,037,074. This adds **149,715,227,996,157** labelled
508-vertex supports to the preceding closure. All 69 coefficients are
published in the certificate and checked in two ways: inclusion-exclusion
over the nine forbidden sets and independent endpoint enumeration followed by
binomial convolution. There is no isomorphism quotient.

At optional size at most 16, **1,997,771,244,437,937** supports extend a template
and **79,207,552,785,883** are outside the certificate. Across all cardinalities,
exactly 1,344 times 2^57 = **193,690,812,773,950,291,968** subsets extend.

By the accepted M492 lemma, every non-four-colourable subgraph of G contains M.
By the present classification it must also contain one of the nine displayed
sets. As before, such a subgraph must contain 604 or 613. The <=508 target
inside G is exactly equivalent to a non-four-colourable induced graph
G[M union T] with |T|=16: any smaller obstruction may be enlarged. Restricting
to T containing one of the nine sets leaves the stated 60,151,956,198,234
labelled candidates. The condition is necessary, not sufficient.

The parent five-colouring supplies an upper bound for every candidate; an
independently checked lower-bound certificate is still required for any
claimed five-chromatic candidate. Neither the whole G560 family nor the
record problem has been closed.

## Computation, inputs and trust

The [frozen protocol](plan.json) selects this entire finite family and excludes
another Kempe depth, different pair compositions, or a graph-deletion sweep.
[build.py](build.py) uses the parent's ordered XOR-convolution geometry and the
preceding interface producer's exact existential Boolean projection. For each
template it projects all optional colour variables, obtains the minimal
nonextension sets, and intersects the failure families by taking inclusion-
minimal unions. This gives the nine-set boundary. It constructs the ten
positive witnesses by deterministic list-colour backtracking. No native SAT
solver was called.

[verify.py](verify.py) imports neither this producer nor the preceding
projection code. It uses the parent's independent sparse-radicand geometry,
union-find plus all 246 switches for template completeness, direct exhaustive
list assignments for the nine negative cases, and ten positive witnesses plus
all 2,048 endpoint patterns for sufficiency. These are different proof paths,
not a translation of the projection algorithm.

Both geometry implementations exhaust all 199,396 unordered pairs of the
632-point host, check distinctness and recover 3,112 unit edges. Coordinates
are the pinned public [H510 input](../hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json)
and [fresh122 input](../hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json).
The ordering and exact basis are those of the
[parent seed](../hadwiger_nelson_heule632_pair_pilot/README.md): coefficients in
(1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165)) have common
denominator 96. The scaled squared-distance vector for a unit edge is exactly
(9216,0,0,0,0,0,0,0). No floating-point comparison is used.

Eight damaged certificates are rejected: missing cover, false negative pair,
missing obstruction, invalid mandatory template, wrong support, monochromatic
optional edge, false family hash and false count. The false-pair control
{362,604} specifically catches confusion between the old fixed-colouring
failure and the new family. Normal and optimized Python checks agree except
for timing, and a second full producer run reproduces the compact certificate
byte for byte.

This is an author-run exact computer-assisted proof, not external review of
this new result or proof-assistant formalization. Trust remains in the exact
coordinate basis, pinned input identity, Python integer/Fraction arithmetic,
the complete finite reductions and the written extension proof. The general
non-four-colourable-subgraph corollary imports the independently accepted
mandatory-set lemma. No solver UNSAT text, omitted trace, numerical tolerance
or uncompleted search is a premise.

## Reproduce

Use Python 3.11 or later, standard library only, in this directory of a clone.
All output directories must be new:

```sh
sha256sum -c SHA256SUMS
python3 -B verify.py --out /tmp/hn560-kempe-check
python3 -B -O verify.py --out /tmp/hn560-kempe-check-optimized
python3 -B build.py --out /tmp/hn560-kempe-build
cmp certificate.json /tmp/hn560-kempe-build/compact_certificate.json
```

Verification of the public certificate needs no producer run. To check a
regenerated certificate use `--certificate PATH` with the verifier.

[certificate.json](certificate.json) is **8,288 bytes**, SHA-256
`289785ccccf47d967a3b1c3abd98f3a7fa9d188748f1aa525b292d176323cd4f`.
[expected.json](expected.json) contains exact outputs and
[validation.json](validation.json) records provenance and timing. Production
took about 4.04 seconds and standalone verification 2.37 seconds on
CPython 3.11.2. The full 105,911-byte template/projection archive and generated
run state remain local. The public semantic certificate contains the ten
positive witnesses and nine small negative sets; it needs none of that archive.
No background computation or unfinished proof remains.

## Decision and next boundary

The complete one-pair component-exchange family is now solved: its nine
residual sets admit no extension under any of its 118 templates. Extending
runtime or revisiting these templates cannot improve this certificate.
The full Kempe-equivalence class and arbitrary M recolourings are outside
scope; another radius ladder is not automatically justified.

A concrete next bounded test is the actual **503-vertex** induced support
G[M union E], where E is the eleven-endpoint set displayed above. It contains
every residual set and is outside every present positive cover. A fresh
decision there would either give a target-size graph certificate or expose
an M colouring beyond this finite family. This is a suggested next milestone,
not a completed SAT query; a SAT answer alone would not warrant another
isolated-cut ladder. No new search phase has started.

New durable context inspected at startup includes the teammate's
[dominating four-cycle theorem](../hadwiger_nelson_dominating_unit_cycle/README.md)
and the [independent acceptance of its connected-triple parent](../hadwiger_nelson_dominating_unit_path_review1/README.md).
Neither is a premise here. The distinct geometric lane, retired supports and
parked two-overlap census were not re-enumerated. No priority claim is made.
