# Four Parts completion supports are closed through 508

**Exact computer-assisted theorem.** Let V={0,...,508} be the original
Parts coordinates and P={509,...,584} the 76 published first-level
completion points with at least seven unit neighbours in V. For each
q in {637,643,675,689}, separately, put H_q=UD(V union P union {q}).
Every subgraph of H_q on at most 508 vertices is four-colourable.
The minimum order of a five-chromatic subgraph of each H_q is exactly
**509**, attained by V.

| q | Exact coordinates (x,y) | Vertices | Unit edges |
|---|---|---:|---:|
| 637 | (-1/6, -(sqrt(3)+2sqrt(11))/6) | 586 | 3090 |
| 643 | ((5-sqrt(33))/12, -(5sqrt(3)+sqrt(11))/12) | 586 | 3089 |
| 675 | ((sqrt(33)-1)/6, (sqrt(11)-sqrt(3))/6) | 586 | 3090 |
| 689 | ((2+sqrt(33))/6, sqrt(11)/6) | 586 | 3090 |

This closes four fixed supports. It supplies no record graph and makes
no claim about their simultaneous union or arbitrary degree-six additions.
The candidate labels come from the published completion catalogue; the
degree-six label refers to adjacency to V, not necessarily to V union P.

## Reduction

The [degree-seven support result](../hadwiger_nelson_parts509_degree_pool_minimum/README.md)
closes A7=UD(V union P) through 508. Its load-bearing bound has an
[independent accepted check](../hadwiger_nelson_parts509_degree7_extension610_closure_review1/README.md).
We use the fixed [degree-six lifting library](../hadwiger_nelson_parts509_degree6_lift_family/README.md),
source d74737dae937a4f388b8500a9f15e4ed819e441b, without adding colourings.
All these inputs are pinned in [manifest.json](manifest.json).

Suppose some subgraph of H_q on at most 508 vertices is not four-colourable.
There is then an inclusion-minimal vertex set W of size at most 508 for
which H_q[W] is not four-colourable. The old A7 closure forces q into W.
For each of 451 original vertices f in the old fixed set F, we directly
verify a proper four-colouring of H_q-f. Hence F is a subset of W.

Let R=(V union P) minus F. It has 134 vertices, comprising 58 originals
and all 76 points in P. Write W=F union {q} union X with X a subset of R.
Necessarily |X|<=56. The earlier zero-through-three-completion closures
force at least four added points in W, so |X intersect P|>=3.
These small-augmentation results and original Parts five-chromaticity
are imported premises, recorded individually in the manifest.

For each witnessed deletion set D subset R, a checked four-colouring of
H_q-D forces X to meet D. The old library has 337 inclusion-minimal
killing sets. Their lifted coverage is:

| q | Forced witnesses | Lifted killing sets | Total four-colourings | Retained edge checks |
|---|---:|---:|---:|---:|
| 637 | 451 | 326 | 777 | 2,384,074 |
| 643 | 451 | 333 | 784 | 2,404,619 |
| 675 | 451 | 331 | 782 | 2,399,295 |
| 689 | 451 | 330 | 781 | 2,396,167 |

The missing row indices, exact neighbourhoods and selected-witness hashes
are in [expected.json](expected.json). Every used witness is checked on
all retained exact unit edges. No unlifted row is imposed.

Minimality of W gives minimum degree at least four: deleting a vertex of
degree at most three would leave a four-colourable graph, and one of four
colours would extend back to that vertex. This does not assume a previous
closure through 507 or assert that every possible order-508 graph is
vertex-critical.

An exact degree audit shows that all vertices except 184, 185 and 186
already have at least four neighbours in F union {q}. These three optional
vertices each have two fixed neighbours and respectively the free neighbours

    184: {13,14,125,126}
    185: {14,15,126,127}
    186: {13,15,125,127}.

Thus, with subscripts denoting vertex labels, the entire minimum-degree
condition reduces to three Boolean inequalities:

    x13 + x14 + x125 + x126 - 2*x184 >= 0
    x14 + x15 + x126 + x127 - 2*x185 >= 0
    x13 + x15 + x125 + x127 - 2*x186 >= 0.

The [four exact OPB instances](instances) contain only the witnessed hitting
rows, the pool quota >=3, the free budget <=56, and these three degree
conditions. OPB variable x_i denotes the i-th entry (one-based) of the
published sorted R, rather than vertex label i. There are 134 variables
and respectively 331, 338, 336 and 335 constraints. There is no symmetry
restriction. These are necessary conditions on a smallest obstruction;
their satisfiability would not itself establish non-four-colourability.

RoundingSat produced a complete pseudo-Boolean refutation of each instance.
**VeriPB 3.0.2 independently checked all four full proofs as UNSATISFIABLE.**
Consequently no W exists. The original graph V gives the matching upper
bound 509. The source also constructs and checks a proper five-colouring
of each full H_q from one forced-deletion witness.

## Reproduction and certificate availability

Use a full repository checkout, Python 3.11 or later, RoundingSat 2 at
source d4edbf7908a9bb951fd181940919e0f3ac7ab1ee, and VeriPB 3.0.2 at source
c648bac06be995b82bd218e248f005140fc8ce11. From this directory, choose an
external work path which does not exist:

```sh
python3 regenerate.py --work /scratch/fresh-four-support-proofs \
  --roundingsat /path/to/roundingsat
python3 verify.py --proof-dir /scratch/fresh-four-support-proofs \
  --veripb /path/to/veripb
python3 controls.py --veripb /path/to/veripb
sha256sum -c SHA256SUMS
```

The regeneration script runs four serial native queries, each with a
120-second solver limit and a 4 GiB Linux address-space limit. It generates
proofs but does not certify them: verification is a separate required step.
For checking one already supplied complete proof directly, use for example:

```sh
/path/to/veripb instances/637.opb /path/to/637/selector.pb
```

Expected verification status is
`FOUR SUPPORTS CLOSED THROUGH 508; MINIMUM ORDERS 509`.
The full verifier rebuilds exact geometry and the four fixed instances,
checks all 3,124 lifted four-colourings on 9,584,155 retained edges,
checks full five-colourings, and invokes VeriPB on every complete proof.

The four native proofs total **310,619,897 bytes**. They remain local and
are intentionally not committed. The public package contains the complete
small OPB instances, deterministic generator, exact input hashes, observed
proof hashes and compact verification results. **Hashes and solver logs
are not certificates: independent verification requires regenerating or
supplying the full proofs.** Proof identity may vary with solver build;
the verifier accepts any complete valid proof of the same fixed instance
and reports whether its hash matches the recorded native run.

The observed native solver times were 25.335, 9.871, 16.209 and 48.818
seconds respectively, totalling 100.233 seconds. Complete certificate
checking took 2.337, 1.343, 1.732 and 6.226 seconds. The bounded pilot,
including input work and checking, took 118.823 seconds. No candidate-graph
colouring query or subsequent refinement query was needed. Native timings
are measurements, not hardware-independent promises.
[measurements.json](measurements.json) records these costs and cumulative
child-process peak RSS, explicitly distinguished from per-query memory.

The public entry point was run on all four original complete traces;
[verification.json](verification.json) records the accepted proof identities.
The regeneration entry point was checked through its argument parser and
byte-identical instance generation; the four native searches were not
repeated merely to test the wrapper.

## Validation and trust boundary

The definition-level controls separately decode all 1,340 OPB rows,
checking the exact killing sets, quota, budget and degree coefficients.
They exhaust all 512 assignments of the nine locally relevant optional
vertices with both absent and present choices for the remaining optional
vertices, for every q: 4,096 cases and 2,125,824 direct vertex-degree checks.
The direct minimum-degree test agrees with the three conditional rows.
VeriPB rejects a false UNSAT conclusion for a satisfiable one-variable
formula. These author controls are not an independent external review.

The previous A7 theorem, zero-through-three-addition closures and original
Parts five-chromaticity remain imported. Their large proofs were not
replayed in this pass. Exact geometry uses the previously reviewed integer
field arithmetic in Q(sqrt(3),sqrt(5),sqrt(11)), with common denominator
288 and no approximate incidence decisions. New colourings and all new
complete refutations were checked here. Remaining trust is in those
premises, the ordinary reduction argument, pinned data, Python integer
arithmetic, SHA-256, VeriPB, and the runtime/hardware. The native solver's
internal numerical heuristics are not proof premises.

Before publication the new
[point-613 independent review](../hadwiger_nelson_parts509_point613_closure_review1/README.md)
and the teammate's
[dense506 midpoint reduction](../hadwiger_nelson_dense506_triangle_midpoint_reduction/README.md)
were inspected. The review accepts the separate point-613 closure; it
does not review this new theorem. The midpoint work concerns different
supports and is not a premise here.

The four supports are finished for the <=508 objective. Among the original
fixed degree-six lifting cohort, points 606, 621 and 630 retain incomplete
forced-vertex coverage and remain open. No pilot on those supports was
started during this milestone.
