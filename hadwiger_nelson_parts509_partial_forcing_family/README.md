# The three remaining partial-forcing selectors are satisfiable

**Verified outcome.** For each q in {606,621,630}, the exact necessary
selector described below has a satisfying assignment. Each assignment
selects a **508-vertex, minimum-degree-four, four-colourable** unit-distance
graph. The assignments and complete colour rows are committed and checked
without invoking any solver. These three fixed support closures remain
open; no record graph or universal four-colourability claim is established.

This completes a bounded decision test of the remaining three supports
in the original eleven-point lifting cohort. The unchanged selector
formulas cannot yield an UNSAT closure certificate: explicit models prove
them satisfiable. The pilot stops here, without a colouring-cut loop,
runtime extension or second selector query.

## Exact hosts and necessary reduction

Let V={0,...,508} be the original Parts coordinates and P={509,...,584}
the 76 published first-level completion points with at least seven unit
neighbours in V. Define A7=UD(V union P) and, separately for each q,
H_q=UD(V union P union {q}).

| q | Exact coordinates (x,y) | Host order | Unit edges |
|---|---|---:|---:|
| 606 | (-(1+sqrt(33))/6, (sqrt(3)+sqrt(11))/6) | 586 | 3090 |
| 621 | ((-13+sqrt(33))/12, (-7sqrt(3)+sqrt(11))/12) | 586 | 3089 |
| 630 | (-1/3, (sqrt(11)-sqrt(3))/3) | 586 | 3091 |

The imported A7 closure excludes a non-four-colourable subgraph through 508
omitting q. Choose an inclusion-minimal vertex set W of size at most 508
whose induced graph is not four-colourable, if any such set exists.
Every proper four-colouring of H_q-f forces f into W. We use only the
fixed [published lifting library](../hadwiger_nelson_parts509_degree6_lift_family/README.md),
with no new colourings added. Unlike the preceding fully forced cases,
some original single-deletion witnesses do not lift.

| q | Original vertices without a lifted forcing witness M_q | Forced originals F_q | Free labels R_q | Free budget |
|---|---|---:|---:|---:|
| 606 | {122} | 450 | 135 | 57 |
| 621 | {223} | 450 | 135 | 57 |
| 630 | {72,87,338} | 448 | 137 | 59 |

Here F_q consists exactly of the original vertices with a lifted witness,
and R_q=(V union P) minus F_q. Thus W=F_q union {q} union X with
X subset R_q and |X|<=508-|F_q|-1. Failure to lift a particular library
witness says neither that f is dispensable in every obstruction nor that
H_q-f is non-four-colourable. Such vertices are left optional.

The earlier zero-through-three-completion closures force
|X intersect P|>=3. For each witnessed deletion set D subset R_q,
a proper four-colouring of H_q-D forces X to meet D. Among the original
337 inclusion-minimal killing sets, respectively 326,329,320 lift.
The source checks every one of the resulting 2323 four-colourings on
7127779 retained exact edges. It also checks proper five-colourings of
the three full supports. Input hashes, labels and missing row indices
are in [manifest.json](manifest.json) and [expected.json](expected.json).

Minimality of W implies minimum degree at least four: a vertex of degree
at most three could be coloured back into a four-colouring of its deletion.
The exact audit checks all 586 vertices of each support. All but optional
vertices184,185,186 already have at least four fixed neighbours in
F_q union {q}. Those three have two fixed neighbours each and the respective
free neighbour sets {13,14,125,126}, {14,15,126,127}, {13,15,125,127}.
Thus the complete degree condition is exactly

    x13+x14+x125+x126-2*x184 >= 0
    x14+x15+x126+x127-2*x185 >= 0
    x13+x15+x125+x127-2*x186 >= 0,

where subscripts in this display denote vertex labels.

The committed [OPB instances](instances) consist only of the lifted
killing rows, the pool quota>=3, the correct free budget, and these three
conditional degree inequalities. They have 135,135,137 Boolean variables
and 331,334,325 rows respectively. OPB variable x_i denotes the i-th entry
of sorted R_q, with one-based indexing. There is no symmetry restriction.

This is a one-way necessary-condition theorem: a smallest obstruction
would produce a selector model. A selector model need not be an obstruction.
The checked examples below make that distinction concrete in all three
remaining supports.

## Why the lost forcing matters at the family level

An exact row audit finds that every label in M_q occurs **only in the
budget row**, with coefficient -1. These labels occur in no killing row,
pool quota or degree inequality. Hence every satisfying X can be replaced
by X minus M_q without violating any constraint. Conversely a satisfying
selection on R_q minus M_q extends by assigning all M_q variables zero.

Consequently, existentially eliminating the newly optional variables gives
exactly a 134-variable formula on the original free set, with budgets 57,57,59
and the same other rows. This is an exact projection statement about the
selectors, not a claim that deleting M_q preserves graph chromatic number.
The audit explains why merely making the old forced literals optional
weakens the successful fully forced formulation. All three recorded models
in fact omit every vertex of M_q.

## Explicit models and colourings

[certificates.json](certificates.json) stores each sorted free selection X
and a 508-character proper four-colouring. Colour characters are 0,1,2,3
in increasing order of the derived retained vertex labels
F_q union {q} union X.

| q | Free selection size | Retained P points | Candidate order | Candidate unit edges | Minimum degree | Four-colourable |
|---|---:|---:|---:|---:|---:|---|
| 606 | 57 | 25 | 508 | 2475 | 4 | Yes |
| 621 | 57 | 12 | 508 | 2457 | 4 | Yes |
| 630 | 59 | 25 | 508 | 2477 | 4 | Yes |

Every model satisfies all its OPB rows, and every displayed graph colouring
is checked against the entire induced exact unit-edge set. These three
examples do not exhaust the selectors or colour the whole supports.

## Reproduction and validation

Use Python 3.11 or later and its standard library, from this directory
in a full repository checkout:

```sh
python3 -B verify.py
sha256sum -c SHA256SUMS
```

Expected status:
`THREE SAT SELECTORS AND FOUR-COLOURABLE ORDER-508 CANDIDATES VERIFIED`.
The expected detailed output is [verification.json](verification.json).
No native solver, missing proof trace or large external artifact is needed
to verify this result.

The verifier rebuilds the exact necessary instances, rechecks all lifted
witnesses, and decodes every committed OPB line against each primary model.
A separate coordinate parse and complete pair scan use the alternative
integer multiplication routine from the accepted
[point613 review](../hadwiger_nelson_parts509_point613_closure_review1/README.md).
All 514215 pairs across the three 586-vertex supports are checked; the
resulting full edge sets match the producer exactly. Each508-vertex induced
graph is then independently checked for its proper colouring and degree.
The executed candidate CNF identities are rebuilt too.

Controls decode all 990 input rows. For each nontrivial degree condition,
they exhaust its local Boolean star and check both absent and present
choices for all other optional vertices:576 exact local cases altogether.
Another 820 global assignments check the conjunction, including empty,
full, singleton and co-singleton optional selections, for 424894 direct
vertex-degree checks. The budget-only occurrence of the M_q variables is
checked explicitly. Invalid selector domains and genuinely monochromatic
edges are rejected in all six deliberately corrupted certificates.
These are author-run audits, not an external review of the new result.

Optional repetition of the bounded native pilot uses RoundingSat 2 at
d4edbf7908a9bb951fd181940919e0f3ac7ab1ee and Kissat 4.0.4. The interface also
accepts VeriPB 3.0.2 and drat-trim, which would check any UNSAT outcome;
neither negative-proof branch was used in this recorded all-SAT run.

```sh
python3 pilot.py --work /scratch/fresh-partial-forcing-pilot \
  --roundingsat /path/to/roundingsat --kissat /path/to/kissat \
  --veripb /path/to/veripb --drat-trim /path/to/drat-trim
```

Choose a new external work directory. The script refuses to restart an
existing pilot checkpoint. It permits only one 120-second selector call
per support and one 60-second candidate-graph call per SAT selector, serially,
with a 4 GiB Linux address-space limit. Each candidate CNF uses four Boolean
colour variables per vertex, at-least-one-colour rows and one exclusion
per edge and colour. A checked unit triangle is pinned to three distinct
colours; any proper four-colouring can be permuted to satisfy that pin.
There are no other symmetry assumptions. Native models are discovery
outputs; direct checking establishes the actual published claims.

The recorded pilot completed in 10.556 seconds, using three PB calls
totalling 4.584 seconds and three graph calls totalling 0.380 seconds.
[measurements.json](measurements.json) gives per-call times and cumulative
child-process peak RSS. No native call was repeated for publication.
Different native builds may choose other models; the committed models
are the stable reproduction inputs. Solver traces and logs remain local
and are unnecessary for checking these positive certificates.

## Scope, dependencies and stopping decision

The original Parts coordinates and old completion census are pinned data.
The old A7 closure and earlier small-augmentation theorems are explicit
imported premises of the necessary reduction, as recorded in the manifest.
Their large certificates were not rerun here. Positive selector and
colouring verification itself does not depend on solver soundness or on
these imported nonexistence theorems. Exact arithmetic uses
Q(sqrt(3),sqrt(5),sqrt(11)) at denominator288, with no approximate incidence
test. Ordinary unformalized reasoning, the source/data, Python integer
arithmetic, SHA256 and runtime/hardware remain in the trust base.

Prior passes closed eight supports in the original eleven-point cohort:
646,678,681 from the lifting library;
613 from the [point613 closure](../hadwiger_nelson_parts509_point613_closure/README.md);
and 637,643,675,689 from the
[four-support closure](../hadwiger_nelson_parts509_degree6_four_support_closure/README.md).
This pass leaves606,621,630 open and proves their present necessary formulas
satisfiable. It says nothing about other degree-six points or simultaneous
unions of extra points.

**Decision:** park this selector formulation. A future closure needs a
new family constraint or a different support mechanism, rather than more
time on a formula already certified SAT. Conditional restrictions linking
the missing originals to retained completion points are a possible next
mechanism to investigate; none has been derived or tested in this pass.
No next-phase solver, colouring-cut loop or background job was started.
