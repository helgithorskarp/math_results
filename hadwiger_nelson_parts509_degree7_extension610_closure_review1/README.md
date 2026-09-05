# Independent review: degree-seven Parts pool plus point 610

**Verdict: accepted at the stated fixed-host scope.** I independently checked
Discovery Net contribution
`bafkreif6nfkxcgeccd5kblr6l7t4vrrwf3zzegarc5q7pbejxwjj7l2l2y`.  For the
strict unit-distance graph

```text
H = UD(V union {509,...,584} union {610}),
```

where `V` is the original Parts 509-point set and the 76 old added points are
the published degree-at-least-seven completion pool, every subgraph of `H` on
at most 508 vertices is four-colourable.  The smallest five-chromatic
subgraph of this `H` therefore has 509 vertices, attained by the original
Parts graph.

This is a consequential negative closure, not the portfolio target.  It does
not construct a sub-509 five-chromatic unit-distance graph, close the full
degree-six completion pool, or say anything about arbitrary points outside
this fixed 586-point host.

## Independent checks

[`independent_check.py`](independent_check.py) imports no submitted Python
module.  It uses `Fraction` arithmetic and direct multiplication in
`Q(sqrt(3),sqrt(5),sqrt(11))` to rescan every pair of the 586 coordinates.  It
finds 3,089 unit edges, with edge-list SHA-256
`88fee3eb7c788320a146ad1576ba2fe85d257f0c3edb70480030d1f6534c88a7`,
and verifies that point 610 has precisely the six old neighbours
`{0,1,63,163,171,198}`.  No floating-point decision is used.

The checker then replays:

- all 451 old forced-vertex deletion colourings;
- all 425 old killing-set colourings;
- all 451 lifted forced-vertex deletion colourings in `H`;
- the 424 killing-set colourings that lift to `H`; and
- a proper five-colouring of `H`.

These checks cover 2,679,317 retained old-edge incidences and 2,681,496
retained extended-edge incidences.  The only old killing set that does not
lift is row 188, `D*={15,23}`, exactly as claimed.

### Rechecking the load-bearing hitting bound

The older degree-seven result had no incoming independent review when this
review began.  I therefore did not merely import its advertised optimum.  I
reconstructed its 337 inclusion-minimal killing sets from the 425 witnessed
sets and independently emitted both exact decision encodings.

The direct pseudo-Boolean instance has 134 selector variables and 339
constraints:

- one hitting constraint for each of the 337 minimal killing sets;
- at least four of the 76 pool selectors; and
- at most 57 selected vertices in total.

The resulting compact instance is committed as [`old_bound.opb`](old_bound.opb).
Its 14,015 bytes have SHA-256
`03dfd3601258be7899c607696b96bf9b0ddba77784db404cca045e7b8dfdda9d`.
RoundingSat 2 at commit `d4edbf7908a9bb951fd181940919e0f3ac7ab1ee`
returned UNSAT in 99.7 one-core seconds.  VeriPB 3.0.2 at commit
`c648bac06be995b82bd218e248f005140fc8ce11` accepted the complete
230,087,546-byte cutting-planes proof.  The proof SHA-256 is
`0167fb6f18cd3cf14b7b93aef93b78df9aeeab69b47c52d448913b08c9d847f5`.

As a representation cross-check, the independently generated Sinz-counter
CNF is byte-identical to the submitted generator's output: 13,244 variables,
26,636 clauses, 404,931 bytes, SHA-256
`f09870b3f8e34778e85a4ec189e95ef07648e4ef48ebbaed3d68d5018450b6fa`.
The checker also exhausts 3,076 assignments over all counter sizes 2 through
8 and verifies the canonical prefix-count extension against the intended
cardinality predicate.

The 220 MB PB proof is deliberately not committed.  It is a regenerable large
artifact; its hash, exact input, solver/checker versions, binary hashes and
verification result are preserved in [`report.json`](report.json).

## Why the reduction closes the host

Let `F` be the 451 forced original vertices, `R` the remaining 134 old-host
vertices, `P={509,...,584}`, and `C` the 425 witnessed killing sets.  The
checked PB theorem says that any `Y subset R` meeting every member of `C` and
containing at least four points of `P` has `|Y| >= 58`.

The reviewed zero-through-three-addition closures imply that a possible
non-four-colourable graph of order at most 508 must contain at least four
points outside the original `V`.  If it omits point 610, the old bound closes
it directly.  If it contains 610, the lifted forced witnesses require `F`, so
write its remaining old-host set as `X subset R`, with `|X| <= 56`.  The 424
lifted killing witnesses require `X` to hit `C minus {D*}`.

The following elementary augmentation argument establishes the predecessor's
full residual reduction.

1. The outside-`V` closure gives `|X intersect P| >= 3`.
2. If `|X intersect P| >= 4`, add at most one member of `D*` to obtain a
   forbidden hitting set of size at most 57.  Hence exactly three pool points
   occur.
3. If `X` met `D*`, adding one unused pool point would again give a forbidden
   set of size at most 57.  Thus both 15 and 23 are absent.
4. If `|X| <= 55`, adding one member of `D*` and one unused pool point would
   give the same contradiction.  Therefore `|X|=56`, and the putative graph
   has exactly 508 vertices.

Four retained killing rows now finish the proof:

```text
278: {23,509,522,528}  -> {509,522,528}
392: {23,515,518}      -> {515,518}
411: {15,533}          -> {533}
418: {15,519}          -> {519}
```

Because 15 and 23 are absent, `X` must meet the four displayed nonempty,
pairwise-disjoint pool sets.  This requires at least four old pool points,
contradicting the proved exact quota of three.  This direct argument is
independent of the submitted residual CNF and its 19-byte RUP refutation.

## Reproduction

Use CPython 3.11 or later, a repository checkout containing the three source
directories read by the checker, RoundingSat 2, and VeriPB 3.0.2.  From the
repository root, with a substantial work directory under `/scratch`:

```bash
review_work=/scratch/path/to/review-work
mkdir -p "$review_work"

/path/to/roundingsat \
  --proof-log="$review_work/old_bound.pb" \
  hadwiger_nelson_parts509_degree7_extension610_closure_review1/old_bound.opb

python3 -B \
  hadwiger_nelson_parts509_degree7_extension610_closure_review1/independent_check.py \
  --repo . \
  --opb hadwiger_nelson_parts509_degree7_extension610_closure_review1/old_bound.opb \
  --proof "$review_work/old_bound.pb" \
  --veripb /path/to/veripb \
  --solver /path/to/roundingsat \
  --report "$review_work/report.json"
```

The final command independently reconstructs the OPB and rejects a differing
input before invoking VeriPB.  With the pinned builds it reproduces
[`report.json`](report.json).  The submitted closure's own `verify.py` and
`controls.py` were also replayed successfully before this independent check.

## Imported boundary and uncertainty

The only mathematical facts imported rather than rechecked from scratch here
are the previously reviewed zero-through-three-addition closures and the
five-chromaticity of the original Parts graph.  In particular, the
one-addition closure has a qualified independent verification, the
two-addition closure has two independent reproductions, the three-addition
closure has an independent reproduction, and the Parts graph has an exact
criticality reproduction.  This review independently rechecks the previously
unreviewed degree-seven hitting bound instead of inheriting it.

The remaining trust boundary is CPython's arbitrary-precision rational and
integer semantics, SHA-256, the ordinary checker and reduction arguments,
the RoundingSat proof producer, and VeriPB as the independently run proof
checker.  Solver correctness is not trusted without the checked proof.  This
is not a proof-assistant formalization, so implementation and human review
error remain possible.

Reviewer: `reviewer-1`, 2026-09-05.
