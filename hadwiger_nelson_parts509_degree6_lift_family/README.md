# Three degree-six extensions of the Parts degree-seven pool are closed

**Theorem.** Write V={0,...,508} for the original Parts vertices and
P={509,...,584} for all 76 first-level completion points with at least seven
unit neighbours in V. For each of the following three points q, every
subgraph on at most 508 vertices of the strict graph H_q=UD(V union P union
{q}) is four-colourable. Each H_q has 586 vertices and 3,089 unit edges, and
its minimum five-chromatic subgraph order is **exactly 509**, attained by V.

| Label q | Exact coordinates | Certificate |
|---|---|---|
| 646 | ((sqrt(33)-5)/12, -(5sqrt(3)+sqrt(11))/12) | Repair missing row 152 using pool point 515 |
| 678 | (5/6, sqrt(11)/6) | All required witnesses lift |
| 681 | ((5+sqrt(33))/12, (5sqrt(3)-sqrt(11))/12) | Repair missing row 287 using pool point 543 |

These are three separate single-point supports; no simultaneous union of
their extra points is claimed. No record improvement or pairwise
nonisomorphism claim is made. Original deletions are unrestricted within V,
including its previously fixed component L={0,...,373}.

## The pool-repair lemma

The [degree-seven certificate](../hadwiger_nelson_parts509_degree_pool_minimum/README.md)
gives 451 forced original vertices F and a free set R of size 134. Let C be
its 337 inclusion-minimal killing sets. They are equivalent, for hitting
purposes, to the full 425-row family. The imported, VeriPB-checked bound is:

> Every Y subset R meeting all C and containing at least four points of P
> has size at least 58.

Suppose the four-colourings proving all F forced lift to H_q, and proper
four-colourings lift for C minus M. If M is empty, or if every member of M
contains one common point p in P, then H_q is closed through 508.

Indeed, a possible non-four-colourable subgraph J with at most 508 vertices
contains q by the older A7 closure, and contains F by the lifted colourings.
Thus X=V(J) minus (F union {q}) is contained in R and has size at most 56.
The earlier zero-, one-, two-, and three-addition closures imply that J uses
at least four points outside V, so X contains at least three points of P.
It meets C minus M.

If M is empty, add one unused point of P when needed to reach quota four.
If M has a common pool point p and p is not in X, add p: this repairs every
missing clause and the quota simultaneously. If p is already in X, every
missing clause is already met; add any unused pool point only if the quota
is three. In each case the resulting Y meets C, has at least four points
of P, and has size at most 57, contradicting the bound 58.

For q=646 the sole unlifted minimal row is D_152={128,515}. For q=681 it is
D_287={219,543,545,550}. Their pool members provide the repair. A missing
row is conservatively omitted; this proof does not assert that its graph
is non-four-colourable. For q=678 every minimal row lifts. The original
Parts graph provides the matching upper bound 509 for all three supports.

## Fixed family pilot and its exact limitation

The bounded cohort was

    606, 613, 621, 630, 637, 643, 646, 675, 678, 681, 689.

These candidates were selected from the published degree-six compatibility
ranking by at most three failed old forced-vertex witnesses; the already
closed point 610 was excluded. Forty new SAT colourings and two previously
published point-610 colourings augment the old library. The committed
`catalogue.json` contains exactly these 42 extra four-colourings, each on
an appropriate deletion of A7. The fixed library has 830 rows in total:
451 old forced witnesses, 337 old minimal killing witnesses, and 42 extras.

The verifier checks every row and recomputes its extension availability
against every relevant exact neighbour of each candidate. Its final replay
uses the whole accumulated library, including colourings discovered later
than a candidate's original turn. The outcome is:

| Outcome under the fixed verified library | Candidates |
|---|---|
| Closed by complete lifting | 678 |
| Closed by a common pool repair | 646, 681 |
| Forced-vertex coverage incomplete | 606, 621, 630 |
| All forced vertices covered; missing killing rows have no common vertex | 613, 637, 643, 675, 689 |

**The eight unclassified supports remain open.** A failure to extend a
published colouring is not a proof of non-four-colourability. Likewise,
none of the 35 native UNSAT answers from repair queries is used as a graph
certificate. The full missing-row lists and exact neighbourhoods are in
`expected.json`.

The older sufficient four-disjoint-pool-set test was also evaluated on the
two candidates with a common repair vertex. Its conditional requirements
offered only two groups for q=646 and three for q=681. The sharper lemma above
closes them because their common repair vertex is itself a pool point.
It is unnecessary to start another SAT selector for these two supports.

## Reproduce without a solver

From this directory in a complete repository checkout, use Python 3.11 or
later and only the standard library:

```bash
python3 verify.py
python3 controls.py
sha256sum -c SHA256SUMS
```

The verifier checks pinned coordinate inputs, all 830 A7 colourings, all
cohort extension lists, and every retained edge in the chosen full-graph
witnesses for the three closed supports. It verifies the inclusion-minimal
family and regenerates the exact old OPB input hash. All distance decisions
use integer arithmetic in Q(sqrt(3),sqrt(5),sqrt(11)), denominator 288.
Native solver answers are not verification assumptions.

The lemma controls exhaust the repair construction over a seven-element
universe with five pool points. They include the case in which the repair
point is already selected, empty missing families, and a counterexample
showing why a common original vertex alone is insufficient for this rule.
Expected outputs are in `expected.json` and `controls_expected.json`.

To regenerate the bounded search, install `python-sat==1.8.dev24` and use a
fresh external work directory:

```bash
family_work=$(mktemp -d)
python3 search.py --work "$family_work"
python3 export_library.py --pilot "$family_work/pilot.json" \
  --out "$family_work/catalogue.json"
```

There is one query per missing witness per point, using CaDiCaL 1.9.5,
100,000 conflicts per query, one native worker, and a 4 GiB address-space
limit. A forced-witness failure stops that candidate's repair phase.
The pilot made 75 calls (40 SAT, 35 native UNSAT), using 88.58 native seconds.
Its negative answers remain uncertified observations. No selector proof,
candidate record graph, second augmentation or extra native repair cycle
was started. Raw checkpoints and verbose logs remain local; `measurement.json`
records the compact resource and validation results.

The older degree-seven pseudo-Boolean proof and small-augmentation closures
are imported theorems; their large proofs were not rechecked this pass.
During the prepublication refresh, an [independent review](../hadwiger_nelson_parts509_degree7_extension610_closure_review1/README.md)
accepted the point-610 closure and independently re-established the exact
degree-seven bound with a fresh VeriPB-checked proof. Its regenerated OPB
matches the hash used here. That review was inspected as durable support
for the imported bound; these three new extensions are not covered by its
point-610 review scope.
New positive witnesses and the finite coverage classification are checked
directly. The reduction and checker are ordinary mathematical/code proofs,
not proof-assistant formalizations or an external peer review.

Source dependencies are the degree-seven contribution
`bafkreieatmp2sjuzzsbbklwx25p63mfjc7blqipzzk6ofnolxo5oxynada` and point-610
witness contribution `bafkreig5j7ai5z3qqaemmh2qgqfukoekxhyhnoux7ki623hcrj6rodqsfe`.
The teammate's committed 1,926-point dense-host completion closure was
inspected and concerns a separate support. This cohort is a completed
certificate pilot. Further work should use a changed proof condition for
an unclassified support, rather than extend the same repair budget.
