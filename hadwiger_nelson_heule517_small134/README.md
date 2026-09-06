# H517 needs at least 135 small vertices

**Every subgraph of the fixed exact graph H517 with at most 134 small-block
vertices is four-colourable.** The statement permits deleting large vertices
and edges. Consequently every non-four-colourable subgraph of H517 on at most
508 vertices must delete at least two of its 375 large vertices.

This strengthens the [previous 133-small closure](../hadwiger_nelson_heule517_small_pilot/README.md),
source `6c88f992e5effaf0cea806f8066c80986edef08a`. It closes the entire
fixed-large family on at most 509 vertices and the at-most-508 family deleting
at most one large vertex. It does not close the unrestricted at-most-508
family, establish sharpness of the bound 135, or produce a record graph.

## Exact support and certificate

The graph G is the [H517 support](../hadwiger_nelson_heule517_family_pilot/README.md):
the 510 Heule-labelled vertices of the fixed Parts/Heule union, together with
the seven external completion points of degree at least seven. The latter
have centre indices 327,439,671,1040,1074,1377,1383. The graph has 517 distinct
points and all 2555 exact unit edges. Its blocks have sizes |L|=375 and
|S|=142, with 1920 large edges, 605 small edges and 30 cross-edges.

Coordinates use denominator 96 in the basis
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165),
with positive square roots. L comprises the points with zero coefficients
of sqrt(5), sqrt(15), sqrt(55), sqrt(165) in both coordinates. G indices
0..509 are increasing union-certificate labels marked `510`; G indices
510..516 are the seven centre indices above in order. These are not the
original published Heule or Parts indices. [manifest.json](manifest.json)
pins the coordinate sources, witness inputs and reused implementations.

The compact [certificate.json](certificate.json) supplies 16 new small-block
colourings and a 202-row final certificate selected from these and the prior
206 rows. Each new row stores a 142-character string in increasing S order,
using digits 0..3 and dots for omissions, together with a zero-based index
into the [20 supplied large-block witnesses](../hadwiger_nelson_heule517_joint_interface/certificate.json).
Concatenating the two blocks according to their G indices gives a proper
four-colouring of G minus a nonempty subset D of S. The checker validates
the entire combined colouring, not just the two separate blocks.

The `final_rows` pairs are `["initial", i]` for zero-based row i of the
prior 206-row certificate and `["new", i]` for row i of this file's
`new_rows`. The final antichain retains 188 initial rows and 14 new rows;
all 16 new witnesses are supplied to account for the finite search.
Its size distribution is 120 singletons, 40 pairs, 24 triples, 13 four-sets,
four five-sets and one six-set. Inclusion redundancy only is removed;
no global minimality of individual omitted sets is asserted.

## Finite proof

Every non-four-colourable subgraph of G must intersect each D: a subgraph
avoiding D inherits the supplied four-colouring of G minus D. In particular
it must contain the 120 singleton vertices. The other 22 small vertices are

```
U = [358,359,360,361,362,370,378,379,393,395,399,432,434,
     459,505,510,511,512,513,514,515,516].
```

The remaining 82 cuts lie entirely in U. For **every one of the
binomial(22,8)=319770 eight-element subsets O of U**, the exact checker
finds a cut D contained in O. It uses complete enumeration and integer
bit-mask containment, with no symmetry reduction or sampling.

Let X be any subgraph with at most 134 small vertices. At least eight
vertices of S are absent. If any singleton vertex is absent, its witness
colours X. Otherwise choose eight absent vertices O in U. The exhaustive
cover gives D contained in O, and the colouring of G minus D restricts to X.
This proves the claim even if X omits large vertices or edges. If in addition
|V(X)| is at most 508 and X is not four-colourable, then |X intersect S| is
at least 135, so |X intersect L| is at most 373.

No negative SAT result or completeness theorem for the boundary relation
is needed for this proof. The earlier 20-pattern relation guided discovery;
only its explicit positive large-block colourings enter the new theorem.

## Frozen decision and observed result

The [plan](plan.json) fixed this level before the first native query. The
initial 206 cuts force 119 small vertices. Exhausting all
binomial(23,8)=490314 omissions among the other 23 leaves exactly 195
survivors. The new checker independently reconstructs that list.

The [producer](run.py) tests survivors in lexicographic global-index order,
skipping one only when a previously checked new witness covers it. Each
selection retains all of L and 134 vertices of S. It tries the 20 boundary
cases in their fixed public order with an incremental CaDiCaL solver. The
activated formulas have 710 variables and 2592 clauses: four colour
variables per small vertex, one activation variable per small vertex,
guarded at-least-one constraints, small-edge inequalities and cross-edge
unit constraints. All activation values are specified on every call.
Inactive vertices can have all colour variables false. At-most-one clauses
are unnecessary because adjacent true-colour sets are disjoint. Decoding
chooses one true colour at each selected vertex and checks the full graph.

A positive colouring is greedily extended over omitted S vertices while
retaining the same L colouring. Its remaining omissions form a new cut.
Every candidate was four-colourable: 16 native selections generated 16
positive witnesses, which covered the other 179 survivors. There were
74 small-case calls: 16 SAT and 58 preceding UNSAT hints. No UNKNOWN,
all-20-negative candidate, new DRAT proof or five-chromatic graph occurred.
Those 58 negative hints are not claimed as individually certified facts.

The complete run took 6.5506 seconds with peak RSS 50400 KiB. The frozen
limits were 195 candidates, 3900 case calls, 100000 conflicts per call,
and 4 GiB address space. No bound was extended. The producer preserves
the unexercised negative branch for reproducibility, but the present result
is certified entirely by colourings and a direct finite cover.

## Reproduce the theorem

From this directory in a complete repository checkout, Python 3.11.2
and the standard library suffice:

```bash
python3 -B verify.py --report /scratch/heule517-small134-check.json
sha256sum -c SHA256SUMS
```

Expected status:
`ALL SUBGRAPHS WITH AT MOST 134 SMALL VERTICES ARE FOUR-COLOURABLE`.
The report gives `eight_sets_checked=319770`,
`small_vertices_needed_by_any_nonfour_subgraph_at_least=135`, and
`negative_solver_proof_required=false`.

[verify.py](verify.py) imports the hash-pinned independent monomial
geometry routine, not the producer or a SAT solver. It reconstructs all
133386 pair distances, checks all 206 initial and all 16 new positive
witnesses (523267 and 40496 edge inequalities respectively), checks the
202-row antichain, verifies the complete final omission cover, and verifies
that new positive witnesses cover every one of the 195 initial survivors.
The final 202 witness graphs have 513249 edge inequalities in total.
Small complete and incomplete cover controls are also checked.

The author ran the additional `--work /path/to/native-run` audit, comparing
the actual survivor list, all 16 native witnesses, the complete tested/skipped
transcript and all 20 activated CNFs entry by entry. This took 7.3953 seconds,
including 0.6628 seconds for the final cover. The original audit report is
[verification.json](verification.json); a public-only run verifies the same
theorem without native logs. This is an independently implemented,
author-run checker, not a separate-author review or formalization.

To reproduce discovery in a fresh external directory, install python-sat
1.8.dev24 with CaDiCaL 1.9.5 and supply Kissat 4.0.4 and drat-trim paths
(the latter two are only called on a negative target):

```bash
python3 -B run.py --work /scratch/heule517-small134-fresh \
  --kissat /path/to/kissat --drat /path/to/drat-trim
```

The public certificate is 6285 bytes. Native formulas, logs and progress
remain outside the repository. [run_summary.json](run_summary.json) and
[validation.json](validation.json) record the observed run and environment.
The proof boundary is the exact coordinate data, Python integer arithmetic,
positive-witness decoding and complete enumeration. No floating-point
approximation, negative native-solver trust or omitted large proof is needed.

## Next boundary and shared work

This family decision is complete. The next target-facing boundary is a
separately bounded family with at least two large deletions and at least
135 retained small vertices. The 20 patterns for intact L must not be used
as a complete relation after deleting L vertices: a fresh relation or a
full compatible graph-colouring oracle is required. No such deletion
query, further small level or background job has started here.

HN-3's dual-common-neighbour reduction (source
`55b29e49c8737ed321c2c8ed32149d50086c738c`, Discovery Net height 3102)
and the independently reviewed collision closure (source
`cd2a5b7d74def8059a1f1bdc58ecb900c570cd4c`, height 3108) were inspected.
The former bounds possible non-four-colourable heptagon-spindle rotations
by at most 1212 classes; it does not enumerate those classes. The latter
checks the 252 noninjective rotations. Their distinct geometric family
remains separate and supplies no premise here. No new relevant contribution
or feedback was present at the final graph refresh, indexed height 3111.
