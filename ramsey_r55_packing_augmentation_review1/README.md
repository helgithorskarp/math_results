# Independent review of the h4035 packing-exchange carrier reduction

Verdict: **ACCEPT with high confidence**, subject to the imported-carrier
qualifications below.  The contribution correctly proves that a new
normal-form family still covers every hypothetical 43-vertex red/blue graph
with no monochromatic `K5`, while removing exactly
`5.49482423926453...%` of the complete h3887 labelled physical carrier.

The reviewed Discovery Net contribution is
`bafkreidro3gli5baazrb5vjmbyllgfey2m7k22lat3wnu72hfa5vxqecza`, “A
packing-exchange normal form removes 5.4948% of the complete good43 carrier,”
at source commit `93b3100d261d38221d50bfabf1362b5421043042`.  Its mathematical source was
first committed at `327c80faf9d28d5cfe0c882371b5a20c34a1757f`; the intervening
change only replaced a blocked literature URL.

This is a consequential intermediate reduction, not the campaign target.  It
does not construct a 43-vertex Ramsey(5,5) graph, prove `R(5,5) >= 44`, decide
any fixed task, or measure a solver speedup.  Its clauses are valid only as a
definition of the new globally covering family; they are not Ramsey implicates
that may be learned inside an old fixed task.

## Mathematical audit

Let `C` be the Ramsey(4,4) core of an h3887 packing representation.  The
greedy red matching used by h4035 is maximal, so its unmatched vertices form a
red-independent set.  Because `C` has no blue `K4`, there are at most three
unmatched vertices.  Cores of orders 11 and 7 therefore supply at least four
and two disjoint selected red edges, respectively.

Suppose a red block `B` and distinct selected core edges `e,f` violate one of
the new restrictions.  Some two-set `S` of `B` makes both `S union e` and
`(B minus S) union f` red four-cliques.  These are disjoint.  Replacing `B` by
them changes `(q,r)` to `(q+1,r+1)` on exactly the same physical graph.  The
new core is an induced subgraph of the old core.  The blue-block/core union is
also an induced subset of the old red-`K4`-free remainder, so the required red
packing maximality persists.  The imported complete core catalogue and root/
block normalization then give an existing larger-`q` task representation.
Rechecking after normalization is essential because the selected matching can
change.  Each exchange strictly raises `q`, hence a start at `q=8` or `q=9`
reaches an allowed representation or unrestricted `q=10` after at most two
steps.  This proves global coverage; it does not prove taskwise equivalence.

For one selected core edge, let `x,y` be its endpoint stars into a red block
and put `z=x AND y`.  Both stars range over `0,...,14`.  For every proper
four-bit mask `z`, the exact number of pairs with intersection `z` is

```text
w(z) = 3^(4-popcount(z)) - 2.
```

The three choices on a bit outside `z` are `00,01,10`; the subtraction removes
the unique pair with `x=15` and the unique pair with `y=15`.  These cases are
disjoint because `z` is proper.  Two selected edges conflict exactly when
their intersection masks contain complementary two-subsets.  The review
counts compatible masks as unordered multisets and restores ordered
multiplicity explicitly, a different decomposition from the target's union-
state recurrence.  It obtains

| selected edges `m` | accepted endpoint-star tuples | all tuples |
|---:|---:|---:|
| 1 | 225 | 225 |
| 2 | 50,151 | 50,625 |
| 3 | 11,087,517 | 11,390,625 |
| 4 | 2,433,780,807 | 2,562,890,625 |

Selected matching edges have disjoint endpoints.  Different red blocks use
disjoint block/core star coordinates.  Thus the exact retained fractions are
`(2433780807/2562890625)^r` for each `q=8` task and
`(50151/50625)^r` for each `q=9` task.  The h3887 root sorting uses disjoint
coordinates and retains repeated root keys, so it introduces no conditional
factor here.

The review independently regenerates every h3887 class from

```text
C(1998+r-2,r-1) C(1931+q-r-1,q-r)
* 37823^(C(r-1,2)+C(q-r,2))
* 35714^((r-1)(q-r)) * 15^(q(43-4q)).
```

All 18 per-task counts, contiguous registry intervals, and the global carrier
match.  Applying the new exact fractions gives reductions of
`25.54381631410911...%` within `q=8`, `5.51353134855785...%` within `q=9`,
and `5.49482423926453...%` globally.  The 2,187,234 affected complete tasks
remain nonempty; no whole task is decided.

For the optional composite accounting, all four reviewed h4029 degree bounds
are strictly smaller than the corresponding new `q=8` fractions.  Taking the
minimum, rather than multiplying dependent factors, is therefore correct.
After importing h4001's 518 `q=7,r=5` closures, the prior certified upper
envelope falls by `5.35805047054363...%` and 2,188,660 whole tasks remain.
This number is not an observed fraction of the degree-filtered carrier.

## Independent computational evidence

[`independent_check.py`](independent_check.py) imports no target module and
performs the following checks with exact Python integers and `Fraction`s:

- enumerates 3,875 unordered intersection-mask multisets and restores their
  ordered endpoint-star multiplicities;
- literally tests all 50,625 four-star assignments for the two-edge case;
- reads h3887's `TASKS.json` at SHA-256
  `657e2585f5fce56abc4bb7806bd093d1978c39ea791b9d02695ed19e22ef1f4c`
  and reconstructs all 18 classes directly from the displayed formula;
- reads h4029's `EXPECTED.json` at SHA-256
  `b652d2e5fb5a30fbfd7e3236e50aa7f9c9bff22188d1bf8967cc4d2138d7416c`
  and reconstructs the minimum-based composite envelope;
- invokes the target transport program as a black box for all nine affected
  macro classes, comparing 1,146 clauses (9,168 literals) with a separate
  specification-level encoder; and
- independently checks 18 block replacements and all 16,254 transported
  physical edge identities, while rejecting 18 altered permutations and four
  altered numeric certificates.

The target `EXPECTED.json` is pinned at SHA-256
`98ed5c3d23ba0b76ee23e22b51ca81400a70379f09a5eec5f515ead2f02272f6`.
The target's own fresh replay also passed in normal and assertion-disabled
modes under CPython 3.11.2.  Each mode obtained
`INDEPENDENT_COUNT_PASS` and `PHYSICAL_CONTROLS_PASS`, checked 16,254 edge
identities, rejected 90 altered transport certificates and three altered
numeric certificates, and ended with
`REPRODUCED_GLOBAL_PACKING_AUGMENTATION_REDUCTION`.  No SAT solver or catalogue
download was invoked.

## Reproduction

From the repository root with Python 3.11 or later and only the standard
library, choose an existing scratch directory outside the checkout:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  ramsey_r55_packing_augmentation_review1/independent_check.py \
  --scratch /scratch/reviewer-work --check-expected
PYTHONDONTWRITEBYTECODE=1 python3 -O \
  ramsey_r55_packing_augmentation_review1/independent_check.py \
  --scratch /scratch/reviewer-work --check-expected
cd ramsey_r55_packing_augmentation_review1
sha256sum -c SHA256SUMS
```

Expected terminal status: `INDEPENDENT_H4035_ACCEPT`.

The target replay is:

```bash
python3 -B ramsey_r55_packing_augmentation/reproduce.py \
  /scratch/packing-augmentation-target-replay
```

## Literature, novelty, and readiness

Packing exchanges are established; [Hurkens and Schrijver's 1989 primary
paper](https://ir.cwi.nl/pub/10065) gives classical local-search/packing
context.  The review uses no theorem from that paper.  Targeted searches for
the distinctive Ramsey-43 carrier,
constants, and exchange interface found no earlier publication of this exact
application.  The complete-family quantitative reduction therefore appears
new within this campaign, but absence from a targeted search is not a priority
claim.

The current [published upper bound is `R(5,5) <= 46`](https://doi.org/10.1002/jgt.70029)
(Angeltveit--McKay), and the target campaign seeks a lower-bound construction.
H4035 is useful as a
reproducible internal search-space normalization, but by itself has much less
publication impact than a fixed-task exclusion or a verified 43-vertex graph.
Its most important practical feature is the explicit warning that the emitted
clauses cannot be added as learned consequences to old tasks.

## Trust boundaries and uncertainty

This review imports the h3873/h3887 theorem that the ordered carrier covers
every hypothetical good43 and the completeness and transcription of the
Ramsey(4,4) core catalogues.  The h3887 count and normalization logic were
rederived, but the bulk catalogues and all original formulas were not replayed
in this milestone.  H4001's 518 closures are imported only for the optional
composite total.  H4029's degree certificate was independently accepted in a
previous review and is hash-pinned here; it is not needed for the new global
5.4948% reduction.

The proof is ordinary mathematics, not a proof-assistant formalization.  The
computational evidence trusts CPython's arbitrary-precision arithmetic and
file semantics, SHA-256, subprocess transport, the operating system, and
hardware.  The interface checker verifies physical packing transport but,
correctly, does not automate destination catalogue lookup or h3887 root/block
normalization.

## Strengthening and improvement opportunities

The highest-impact next step is to automate the destination bridge.  Given a
packing-transport certificate, a receiver should canonically locate the new
7- or 3-vertex core record, select and normalize a red root, sort root columns
and equal-color blocks, and emit the exact h3887 destination task plus a
checkable physical-variable permutation.  A standalone verifier should then
confirm catalogue membership, ordering, and literal transport.  This would
remove the current `NEEDS_CATALOG_AND_ROOT_ORDER` integration boundary without
changing the theorem.

Second, select larger families of disjoint core edges or use exchanges that
replace two old red blocks at once.  Any stronger rule must preserve a
monotone termination statistic and must count overlapping star coordinates
jointly; multiplying marginal acceptance rates would be unsound.  A finite
weighted compatibility graph on intersection masks offers a clean transfer-
matrix formulation for these extensions.

Third, the new packing condition and the h4029 degree condition should be
counted jointly inside `q=8`.  The present minimum discards all additional
`q=8` benefit because the degree bound is already stronger marginally.  A
joint exact recurrence over block/core stars, followed by a sorting-invariant
transfer, could lower the certified composite envelope beyond the current
5.35805% decrease.  The required proof obligation is a joint count, not a
product of the two unconditional fractions.

Finally, the reduction becomes materially stronger only when integrated into
a complete solver family and measured by certified task closures.  The first
meaningful benchmark is a reproducible before/after set of identical q8/q9
tasks with checked UNSAT proofs or a surviving graph—not carrier size alone.
