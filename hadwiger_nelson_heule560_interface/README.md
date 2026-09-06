# A complete fixed-colouring interface for the 560-point seed

For the published 560-vertex unit-distance graph G, let M be its 492 mandatory
vertices and U its 68 optional vertices. Fix the proper four-colouring c of M
obtained by restricting the previous free50 covering colouring. We certify,
simultaneously for **every T subset U**, that

\[
c\text{ extends to }G[M\cup T]
\quad\Longleftrightarrow\quad
\{362,604\}\not\subseteq T,\quad
\{406,613\}\not\subseteq T,\quad
\{409,613\}\not\subseteq T.
\]

The three conditions on the right are conjunctive. These are host labels in
the fixed 632-point coordinate file, not fresh-centre identifiers. This is a
complete classification for **one fixed colouring of M**, not a classification
of graph four-colourability when M may be recoloured.

It closes **1,259,701,602,040,917** of the **1,469,568,786,235,308** labelled
508-vertex supports in the accepted M492/U68 reduction, about **85.7191%**.
Exactly **209,867,184,194,391** labelled supports remain outside this certificate.
They are not asserted to be non-four-colourable. No graph with at most 508
vertices and chromatic number five has been established.

## Definitions and inputs

The [parent certificate](../hadwiger_nelson_heule632_minimize/README.md) proves
that G has 560 vertices, 2,758 unit edges and chromatic number five. Its
[boundary.json](../hadwiger_nelson_heule632_minimize/boundary.json) fixes the
partition M, U. Every non-four-colourable subgraph of G contains M, because
proper colourings of G-v were checked for every v in M. Both claims received
[independent acceptance](../hadwiger_nelson_heule560_family_review1/README.md).

The fixed c is the restriction to M of `cover_colouring` in
[the free50 certificate](../hadwiger_nelson_heule560_degree_family/certificate.json).
This contribution checks c directly on all 2,390 edges inside M. It does not
assume that the newer free50 result has external review merely because its
parent does.

Exact coordinates come from the same two public input files as the parent:
[H510 coordinates](../hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json)
and [122 fresh points](../hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json).
The first 510 labels follow the increasing union labels whose provenance
contains `510`; fresh points follow in increasing `centre_index` order.
Coordinates lie in Q(sqrt(3),sqrt(5),sqrt(11)). Their coefficients in the basis

\[
(1,\sqrt3,\sqrt5,\sqrt{15},\sqrt{11},\sqrt{33},\sqrt{55},\sqrt{165})
\]

have common denominator 96. Both exact geometry paths check distinctness and
all 199,396 unordered pairs of the 632-point host, obtaining 3,112 unit edges.
Squared distance one means scaled coefficient vector `(9216,0,0,0,0,0,0,0)`.
The pinned parent plan checks the raw input identities; this directory's
[plan.json](plan.json) pins the boundary, source colouring and parent plan.

## Proof of the complete interface

For v in U define its available list

\[
L(v)=\{0,1,2,3\}\setminus\{c(w):w\in M,\;vw\in E(G)\}.
\]

A colouring extending c is precisely a proper list colouring of G[T] from
these lists. The checker reconstructs all lists from the exact edges and c.
There are 49 lists of size one, 17 of size two, and two of size three; the
optional induced graph has 61 edges.

For necessity, all three displayed pairs are edges, and

\[
L(362)=L(604)=\{0\},\qquad
L(406)=L(409)=L(613)=\{3\}.
\]

Thus selecting both endpoints of any one of the three pairs prevents extension
of c. Each pair is inclusion-minimal for that property, since its proper
subsets have nonempty lists.

For sufficiency the certificate supplies four full proper colourings, all
agreeing with c on M:

| Vertices omitted from G | Retained vertices | Retained unit edges |
| --- | ---: | ---: |
| 362, 613 | 558 | 2,741 |
| 604, 613 | 558 | 2,747 |
| 362, 406, 409 | 557 | 2,732 |
| 406, 409, 604 | 557 | 2,738 |

Every T avoiding the three pairs lies in one of these four optional supports.
Indeed, its omitted vertices meet {362,604}; and they either contain 613 or
contain both 406 and 409. These are exactly the four minimal hitting sets of
the three pairs. Restricting the corresponding checked colouring proves
sufficiency for arbitrary T, with no cardinality bound. The checker also
exhausts all 32 selection patterns on the five affected endpoints to verify
this covering argument; all 15 good patterns are covered. The other 63
optional vertices may all be present in each cover.

This proves that the three pairs are the **complete** minimal obstructions to
extension of c. It does not prove that any of the corresponding graphs
G[M union pair] is non-four-colourable: their mandatory vertices may admit
different colourings.

## Exact family counts and residual condition

The graph of forbidden pairs is a disjoint edge and a three-vertex path.
Consequently the generating polynomial for extending subsets is

\[
(1+x)^{63}(1+2x)(1+3x+x^2)
=(1+x)^{63}(1+5x+7x^2+2x^3).
\]

For optional cardinality k its coefficient is

\[
E_k=\binom{63}{k}+5\binom{63}{k-1}
       +7\binom{63}{k-2}+2\binom{63}{k-3},
\]

where out-of-range binomial coefficients are zero. All 69 coefficients are
published and checked by two methods: inclusion-exclusion on the projected
forbidden sets, and the independent 32-pattern enumeration followed by a
binomial convolution.

The number of extending subsets of arbitrary cardinality is
15 times 2^63 = **138,350,580,552,821,637,120**. At optional size at most 16,
there are **1,793,849,422,050,660** extending labelled supports and
**283,129,375,173,160** supports outside this certificate.

By the accepted mandatory-set lemma, every non-four-colourable subgraph of G
must contain M. By the present result it must also contain at least one of
the three pairs. In particular it must contain **604 or 613**. This strengthens
the previous necessary condition of hitting an 18-vertex set. The free50
family is contained in the present closure, because neither 604 nor 613 is
in free50.

The at-most-508 target within G is therefore still exactly equivalent to the
existence of a non-four-colourable induced graph G[M union T] with |T|=16, now
restricted to T containing at least one displayed pair. Enlarging a smaller
non-four-colourable support preserves that property. Every candidate inherits
the parent's five-colouring as an upper bound, but a fresh lower-bound
certificate would be needed for any claimed candidate. Counts concern labelled
supports, with no isomorphism quotient.

## Discovery computation and independent verification

The bounded protocol froze one c and permitted no further mandatory colourings
or graph-deletion solver calls. [build.py](build.py) starts with 68 selector
variables and 89 available-colour variables. It encodes at least one colour
for a selected vertex and excludes equal colours along optional edges.
At-most-one and reverse-activation clauses are unnecessary: from any satisfying
assignment choose one true allowed colour for each selected vertex; conversely,
a proper colouring sets exactly its chosen variables true and all absent
vertices' colour variables false.

The producer existentially eliminates each colour variable by replacing its
positive and negative clauses by all resolvents and deleting tautologies and
subsumed clauses. This preserves the projected selector relation. The initial
and maximum live clause counts are both 90. The final clauses are precisely
the three forbidden pairs. It finds the four cover colourings by deterministic
finite list-colour backtracking. No native SAT call was made.

The proof checker [verify.py](verify.py) **does not import this producer, perform
Boolean elimination, or trust its search status**. It uses the parent's
independent sparse-radicand geometry rather than the producer's ordered XOR
convolution. It checks the fixed M colouring, all lists, the three forced
conflicts, exact support and every edge of each of the four positive witnesses
(10,958 edge inequalities), and all 32 endpoint patterns. This is a complete
proof even if the producer's elimination implementation were wrong.

Seven deliberately damaged certificates are rejected: missing cover, wrong
support, changed mandatory colour, monochromatic optional edge, missing
obstruction, false list, and false cardinality count. Normal and optimized
Python checks agree except for timing. These checks are author-run independent
algorithmic paths, not external review or proof-assistant formalization.

The remaining trust boundary is exact integer/Fraction arithmetic, the
squarefree-radical coordinate interpretation, pinned public inputs, the Python
runtime, and the elementary written covering proof. The global mandatory-set
corollary additionally uses the accepted parent lemma. No solver UNSAT text,
omitted proof trace, numerical tolerance or uncompleted search is a premise.

## Reproduction

Use Python 3.11 or later, standard library only, from this directory in a clone
of the repository. Both commands require new output directories:

```sh
sha256sum -c SHA256SUMS
python3 -B build.py --out /tmp/hn560-interface-build
cmp certificate.json /tmp/hn560-interface-build/certificate.json
python3 -B verify.py --out /tmp/hn560-interface-check
python3 -B -O verify.py --out /tmp/hn560-interface-check-optimized
```

The checker also accepts `--certificate PATH`, so a fresh generated certificate
can be verified directly. The public certificate alone suffices for the
solver-free check; producer execution is optional.

[certificate.json](certificate.json) is **5,526 bytes**, SHA-256
`3df21aa84154341f7db3e10c1082e3948842b213c7211be7b2d763f1ddcd0bb7`.
[expected.json](expected.json) records exact counts and
[validation.json](validation.json) records provenance and timings. Production
took about 1.33 seconds and standalone verification about 1.90 seconds on
CPython 3.11.2. A fresh producer run reproduced the certificate byte for byte.
Generated run directories and the elimination transcript remain local;
neither is needed as a proof artifact. No background computation remains.

## Campaign checkpoint

This is a family-level advance within the existing support, not another
individual deletion cut. The current fixed-c interface is completely solved;
rerunning it or extending its runtime cannot change its classification.
The remaining 209,867,184,194,391 size-16 supports require a changed mechanism
that allows recolouring M. A next bounded phase could test a simultaneous
recolouring certificate for the three pair branches, followed by a go/no-go
decision. It should not resume a singleton-deletion ladder or treat one
failed fixed-c extension as a graph obstruction. No such next phase was begun.

At startup the new external H560 review was read and accepted as durable
context. The teammate's distinct
[connected dominating triple theorem](../hadwiger_nelson_dominating_unit_path/README.md)
was also inspected; it is coordination context, not a mathematical premise
of this result. That geometric family and the parked two-overlap census were
not re-enumerated. No priority or record claim is made.
