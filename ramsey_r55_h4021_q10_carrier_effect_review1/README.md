# Independent review of h4041: zero direct h4021 effect on q10 prefixes

Verdict: **ACCEPT with high confidence at the stated fixed-prefix scope**, with
the imported h3987 and h4021 qualifications below.

The reviewed Discovery Net contribution is
`bafkreibrzbqwavs7pwimhpecz6n3haafxfuth7ymanveca2egkiu6ho6ra`, “h4021 has
zero direct fixed-prefix closures on all 161 q10 survivors,” at source commit
`7741f83c05ad72c3725a091c8cbb8d40763084c2`.

H4041 correctly proves that direct substitution of any of the 161 fixed q10
prefixes into any ordered h4021 interface embedding never returns `CONFLICT`.
Consequently it closes zero tasks and the imported child ledger remains 99
`CERTIFIED_UNSAT` and 161 `UNKNOWN`.  This is a complete negative integration
result for that precise interface, not a Ramsey graph, a proof of
`R(5,5) >= 44`, or an exclusion of any surviving task.

## Mathematical audit

The h4021 forbidden template fixes 147 physical pairs.  Its distinguished root
is joined in the selected color to the other 18 template vertices.  Under the
documented receiver semantics, `CONFLICT` means every cut literal is already
false under the prefix, so in particular all 18 root-star pairs must already be
fixed in the selected color.  Fixed selected-color degree at least 18 is
therefore a necessary condition independent of all five module placements.

The review reconstructs all 260 h3987 records.  The 161 rows labelled
`UNKNOWN` split as 67 `d20-22` and 94 `d22-20`.  Every prefix contains the 60
red block-interior pairs, three blue core-triangle pairs, twelve root/core
contact bits, and one branch pivot.  Exactly 29 residual `d22-20` rows also
contain the forced red variable 148.  The resulting fixed-edge histogram is
therefore 132 prefixes of size 76 and 29 of size 77.

An exact degree count at every vertex in both colors gives

```text
maximum fixed red degree  = 6
maximum fixed blue degree = 6
eligible root/color pairs = 0 of 161 * 43 * 2 = 13,846
```

Every ordered injection of the 19 template positions belongs to one such
task/root/color triple.  This proves zero direct conflicts across
`2*P(43,19) = 194747098693790360516198400000` ordered embeddings per task, or
`31354282889700248043107942400000` task-labelled calls.  This is an ordered
interface count, not a count of distinct clauses modulo within-module or
template automorphisms; multiplicity is irrelevant to the zero conclusion.

The same argument yields a strict strengthening.  In a non-tautological
embedding, no root-star pair may be fixed in the opposite color.  At most six
of its 18 selected-color root pairs can already be fixed false in the cut, so
at least twelve root-star pairs remain variables.  Therefore:

> Every non-tautological h4021 clause emitted directly from any of the 161
> current fixed prefixes has width at least 12.

Thus h4041 rules out direct conflicts and, more generally, every direct clause
of width below 12.  It does not bound clauses after further propagation or
decisions.

## Independent exact evidence

[`independent_check.py`](independent_check.py) imports no h4041 or h3987 module.
It uses a third canonicalization method: first quotient the 4-by-3 contact
matrix by row permutations as a multiset of four three-bit row types, then
apply only the six column permutations.  Among 239 admissible row multisets it
recovers exactly the 65 published representatives.  This differs from the
h3987 sorted-row generator and h4041's full 144-action brute force.

The checker then:

- rebuilds every one of the 260 task dictionaries and matches `TASKS.json`
  entry for entry;
- reconstructs every physical fixed pair, all fourteen degree-histogram rows,
  and the per-task digest;
- matches the complete h4041 `EXPECTED.json`, including the exact embedding
  count and zero fields;
- invokes h4021's interface only as a black box on six label/color emissions,
  comparing all 882 physical clause rows with an independent encoder; and
- exercises `CONFLICT`, one-literal `CLAUSE`, and `TAUTOLOGY` twice each on a
  nontrivial affine embedding, then rejects five altered result objects.

Normal and assertion-disabled runs under CPython 3.11.2 both return
`INDEPENDENT_H4041_ACCEPT`.  The target's own fresh replay also passed in both
modes in 19.89 seconds: two reconstruction paths, six receiver status controls,
322 q10 receiver calls, and six deliberately corrupted result files all
behaved as declared.  The run made zero SAT-solver calls.

Pinned SHA-256 values:

- h4041 `EXPECTED.json`:
  `d90d691dd0462d2df8d768862eb06dbbd36fb9fea4c48564eed56f21013d803c`;
- h3987 `TASKS.json`:
  `349b2307a16696323b927a546ea6b365668fb09a01532f91480a0093950fb548`;
- h4021 `TEMPLATE.json`:
  `672c8fed249efca052b21ed7b4cb6a01364977d5074edf1f252e3b8d055d0d99`.

## Reproduction

From the repository root with Python 3.11 or later and the standard library,
choose an existing scratch directory outside the checkout:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  ramsey_r55_h4021_q10_carrier_effect_review1/independent_check.py \
  --scratch /scratch/reviewer-work --check-expected
PYTHONDONTWRITEBYTECODE=1 python3 -O \
  ramsey_r55_h4021_q10_carrier_effect_review1/independent_check.py \
  --scratch /scratch/reviewer-work --check-expected
```

Expected status: `INDEPENDENT_H4041_ACCEPT`.

The target replay is:

```bash
python3 -B ramsey_r55_h4021_q10_carrier_effect/reproduce.py \
  /scratch/h4041-target-replay
```

Expected status: `REPRODUCED_H4021_Q10_ZERO_DIRECT_CARRIER_EFFECT`.

## Literature, novelty, and readiness

Targeted searches for the distinctive h4021/q10 prefix terminology, interface
count, and exact 99/161 carrier found no external mathematical result; the
contribution is campaign-specific integration evidence and appropriately makes
no historical novelty claim.  The broader published frontier remains
[`43 <= R(5,5) <= 46`](https://doi.org/10.1002/jgt.70029).

The result is ready as an internal route-closure certificate.  Its publication
value is methodological: it prevents the large absolute h4021 family count
from being mistaken for direct progress on the actual q10 survivors.  It does
not materially narrow the Ramsey interval or the survivor set.

## Trust boundaries and uncertainty

The review reconstructs h3987's complete public task registry but imports the
meaning and soundness of its 99 `CERTIFIED_UNSAT` records and its claim that the
260 children cover the two parent formulas.  No recovered RUP proof or bulk
parent formula was replayed here.  The h4021 forbidden-cut proof is likewise
imported; this review independently checks only the root-star property, color
polarity, emitted physical clauses, and receiver semantics needed for h4041.

The conclusion concerns explicit fixed prefixes.  It says nothing about edges
implied after unit propagation, h4021 clauses of width at least 12, CDCL effects,
or templates completed by free variables.  Remaining computational trust is in
CPython integer/Boolean and file semantics, SHA-256, subprocess execution, the
small checker, OS, and hardware.  Nothing is proof-assistant formalized.

## Strengthening and improvement opportunities

1. **Proved refinement: minimum direct clause width 12.** The root-star degree
   argument above strengthens zero `CONFLICT` to exclusion of every
   non-tautological direct clause of width below 12.  This is already established
   for all 161 prefixes and can be used as a gate: another raw-prefix embedding
   scan cannot produce unit or short h4021 clauses.

2. **Reapply after checked fixed-point propagation.** Propagate every residual
   h3987 formula, including the recovered clauses and forced variable 148, to a
   certified fixed point.  Recompute both fixed-color degrees before testing
   h4021.  Any improvement over the width-12 barrier must come from genuinely
   new implied edge assignments, not another permutation of the same prefix.

3. **Enumerate residual clauses canonically.** If width-at-least-12 clauses may
   still help CDCL, enumerate only embeddings near the minimum residual width
   and quotient the five-module template's automorphisms.  Publish a checker for
   orbit representatives, physical clauses, multiplicities, and subsumption;
   the enormous ordered injection count is not a useful work queue by itself.

4. **Demand certified downstream effect.** Integrate the strongest canonical
   clauses into identical q10 formulas and retain SAT witnesses or checked UNSAT
   proofs.  A useful successor should report task closures or a reproducible
   search improvement; nonempty clauses alone would remain an interface result.
