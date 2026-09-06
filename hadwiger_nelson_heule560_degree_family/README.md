# A four-colouring closes the free50 optional subfamily

In the [certified 560-point graph](../hadwiger_nelson_heule632_minimize/README.md),
delete the 18 fresh vertices listed below. The resulting **542-vertex,
2,672-edge graph is four-colourable**. One compact, directly verified
colouring therefore closes every subgraph of this support.

In terms of the preceding 492-mandatory/68-optional partition, the retained
optional block has 50 vertices. The result covers all `2^50` supports obtained
by retaining the mandatory set and any subset of this block, including all
**4,923,689,695,575** labelled 508-point supports choosing exactly 16 of them.
No enumeration of those subsets is needed: the single colouring restricts.

Every non-four-colourable subgraph of the full 560-point support must now
contain at least one of these 18 fresh host labels:

```text
515 526 541 550 551 555 567 569 574
590 592 595 597 604 607 609 613 624
```

This is a partial family closure, not a five-chromatic graph on at most
508 vertices, a record improvement, or a closure of the whole 560-point
family. The covered 508-point supports are only about 0.335% of the preceding
`binomial(68,16)` family. Labels count subsets of this fixed support, not
isomorphism classes.

## Why the degree test led to this block

Let M be the 492 vertices whose singleton-deletion four-colourings were
previously verified, and let U be the 68 remaining vertices. Every
non-four-colourable subgraph of the 560-point graph contains M. A possible
five-critical subgraph also has minimum degree at least four.

For a vertex v, let `b(v)` count its neighbours in M. All 492 vertices of M
already have `b(v) >= 4`. Among U, exactly 50 also have `b(v) >= 4`; call
this set F. The remaining set D has 18 vertices, all fresh, with deficiencies
`max(0,4-b(v))` distributed as follows:

| Optional-neighbour requirement when selected | Vertices |
| --- | ---: |
| 0 | 50 |
| 1 | 11 |
| 2 | 6 |
| 3 | 1 |

The proposed degree/cardinality feasibility formula therefore has the
explicit solution that selects no optional vertices. More strongly, every
subset of F of size at most 16 satisfies the degree requirements. Thus an
infeasibility proof from that screen alone cannot close the target family.
This observation is exact; no native feasibility solve was needed.

The follow-up within the frozen milestone tested the full covering graph
`A = G[M union F]`. A positive model settled all its target subsets at once.
The degree conditions still constrain some selections involving D; their
failure to close the entire family is not a claim that they are vacuous on U.
See [PROOF.md](PROOF.md) for the complete implication and scope arguments.

## Exact geometry and positive certificate

Use the same H632 host labels as the parent packages: the archived 510 old
Heule points occupy 0 through 509, and the 122 archived fresh centres in
increasing `centre_index` order occupy 510 through 631. The 560-point support
and M/U partition are pinned by hashes in [plan.json](plan.json).

Coordinates are rational coefficient vectors in
`(1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165))` on each axis.
Scaling by 96 makes every coefficient integral. The checker recomputes all
199,396 unordered pairs of the 632 distinct host points exactly and then
restricts to the specified support.

[`certificate.json`](certificate.json) contains a 632-character covering
colouring, with dots exactly outside A, and the full degree/neighbour row
for each of the 68 optional vertices. The independent checker validates all
2,672 edges of A. Restriction to M checks another 2,390 edges. It also checks
the frozen 508-point target restriction, with 2,500 edges.

This theorem uses a positive certificate. The SAT solver's search algorithm
is not a proof premise, and no UNSAT verdict or omitted negative proof is
needed for the actual result.

## Frozen protocol and actual execution

The plan allowed at most two colouring queries. The first was A, on 542
vertices. Only if A had a checked four-colour refutation would the second
query test one fixed 508-point subset of A. Its 16 optional points were
chosen greedily by the number of neighbours already retained, breaking ties
by the host label. Both exact CNFs were generated and independently matched
before querying.

The first query was SAT, so the protocol stopped. The second graph is
four-colourable by restriction and was not submitted to the solver.

| Quantity | Actual result |
| --- | --- |
| Native calls | 1 |
| Cover formula | 2,168 variables, 14,485 clauses |
| Cover graph | 542 vertices, 2,672 edges |
| Native verdict | SAT; every clause and edge checked |
| Solver time | 1.97 seconds |
| Whole producer run | 5.33 seconds |
| Conditional target query | Not run; covered by restriction |

The cover CNF SHA-256 is

```text
f8c9e2610e1a823083a83921391cb3eb78f01266c97c20c3882322ded7477681
```

The frozen 508-point formula, whose colouring is obtained by restriction,
has SHA-256

```text
a679e23efbd4fbc1113cca86ce10b18261285eaeb2a77a5f7ab0f5b18402ab87
```

The original query used Kissat 4.0.4, source revision
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, with seed zero, at most
2,000,000 conflicts and 120 seconds. Exact executable hashes and outer
resource limits are in the plan. DRAT checking was available for the
conditional negative branch but was not needed.

## Reproduction

The theorem verifier requires only Python 3.11 or compatible standard-library
Python. From the repository root, with a new output directory:

```sh
python3 -B hadwiger_nelson_heule560_degree_family/verify.py \
  --out /tmp/hn560-free50-verification
```

Expected output includes
`FREE50 OPTIONAL SUBFAMILY FOUR-COLOURABLE; DEGREE SCREEN FEASIBLE`,
542 covering vertices, 2,672 covering edges and 4,923,689,695,575 covered
508-point supports. No solver, external raw output, or proof download is
required for verification.

To replay the frozen native experiment using the pinned executables:

```sh
python3 -B hadwiger_nelson_heule560_degree_family/run.py \
  --out /tmp/hn560-free50-run --kissat /path/to/kissat \
  --drat-trim /path/to/drat-trim
python3 -B hadwiger_nelson_heule560_degree_family/verify.py \
  --out /tmp/hn560-free50-audit --archive /tmp/hn560-free50-run
```

The archive audit independently checks the 14,485 native-model clauses and
decodes the model back to the positive graph certificate. A rerun reaching
UNKNOWN is inconclusive; the public positive certificate remains directly
checkable.

## Validation, dependencies and handoff

The verifier imports no producing `run.py` code. It uses the parent's
independently written sparse-radical geometry and direct CNF builder, while
the producer uses ordered coefficient convolution. It reconstructs all
degree rows and both frozen formulas. Exhaustive controls cover 81,920
degree/selection assignments and 22,432 instances of the free-subcube
implication. Three malformed positive certificates are rejected.
[validation.json](validation.json) records the executed audit and standalone
checks.

The positive covering theorem relies only on the exact coordinate data,
faithful graph construction and direct colouring checks. The interpretation
as a refinement of the 492/68 target family additionally uses the preceding
verified mandatory-vertex certificate. Its parent 630-point seed now has a
separate independent acceptance, including DRAT and LRAT checks. That review
does not review the later 560-point result or this new closure.

Exact CPython arithmetic, independence of the radical basis, exhaustive
execution, JSON parsing and SHA-256 remain operational trust boundaries.
No proof-assistant formalization, independent-author review of this result,
or completeness of a historical colouring library is claimed. Raw CNFs and
solver logs stay local; the compact positive certificate is public.

This completes the planned degree-screen decision and covering-graph test.
The degree-only global-infeasibility route is a no-go because of its explicit
feasible subfamily. A subsequent phase must address actual colour extension
in the residual family that meets D, preserving the total optional budget
of 16. No new dependent-vertex block, repeated deletion sweep, or next
colouring-extension phase has started.
