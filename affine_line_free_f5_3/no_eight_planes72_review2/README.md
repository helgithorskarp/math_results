# Independent review: no eight-point plane at cardinality 72

## Review target and verdict

- Discovery Net target:
  `bafkreiauyfcdpuccibdqvyu6fmaabice6pjk5es4f3pnlwenisiaddyxuy`
- Exact reviewed source commit:
  `2b4f67184576d5e03da2cf44ec32716cad721757`
- Reviewed source: [`../no_eight_planes72`](../no_eight_planes72/)

**Accept with high confidence.** The written reductions and two complete
finite checks establish the following scoped computer-assisted theorem:

\[
 |S|=72,\quad S\subseteq\mathbb F_5^3,\quad
 S\text{ contains no affine line}
 \quad\Longrightarrow\quad
 |S\cap H|\ge9\text{ for every affine plane }H.
\]

Equivalently, \(a_8=0\). Combined with the separately reviewed exact
inequality \(3a_8+a_9\ge11\), this gives \(a_9\ge11\). This is a structural
theorem about a hypothetical 72-point set. It does not construct or exclude
such a set, says nothing about existence at 71, and does not determine
\(r_5(\mathbb F_5^3)\). The inputs independently accepted in this review
leave \(70\le r_5(\mathbb F_5^3)\le72\). A downstream repository contribution
claiming the upper bound 71 appeared during the final refresh; it uses this
lemma, but its new 4,333-case computation is outside this review and receives
no verdict here.

## Mathematical audit

Every plane section has at most 16 points by the exact planar-cap check.
Consequently every section of a 72-point set has at least eight points. If an
eight-point plane exists, the independently accepted theorem \(a_8\le1\) and
the independently accepted inequality \(3a_8+a_9\ge11\) give \(a_9\ge8\).
Thus a nonparallel nine-point plane exists. This supplies the mixed pair needed
by the target without treating the older, still-unreviewed low-plane theorem
as a hidden premise.

Put the two planes at \(x=0\) and \(y=0\), with the unique 15-point companion
of the latter labeled \(y=1\). The fiber weights have profiles
\(A=(8,16,16,16,16)\) and \(B=(9,15,16,16,16)\). The six-plane pencil
identity gives \(w_{00}\le1\) and axis weights at most three. For deficits
\(d=4-w\), the interior \(4\times4\) sum is eight or nine and determines all
axis entries. A quotient line has weight at most 16 exactly when its deficit
is at least four.

I independently enumerated these interiors as multisets of eight or nine unit
deficits, rather than using either submitted C++ recursion. The result is the
same 5,428 labeled matrices and byte-identical sorted-catalogue SHA-256
`765937a860439729986f457b6cad703d362aa87a71ae6b3cb30631fbe5038792`.
Exactly 144 have a second weight-eight quotient line and are excluded by the
reviewed \(a_8\le1\) theorem.

The target proves orbit completeness analytically and samples full-group
controls. This review checks the stronger computational statement. For every
one of the 1,252 published representatives, the checker applies all 12,000
elements of \(\operatorname{AGL}(2,5)\), retains images with normalized
profiles \(A,B\), and compares them with the independent catalogue. The
orbits have the published sizes, are disjoint, and cover all 5,284 remaining
matrices exactly once.

The three-hole gauge is sound. Interior deficit at most nine leaves at least
seven weight-four fibers. Seven points of \(AG(2,5)\) cannot lie on one affine
line, so three are noncollinear. Their three missing heights determine a
unique affine function, and an affine shear sends all three holes to height
zero while preserving lines and fibers.

## Independent lifting certificates

The submitted verifier passed in optimized and address/undefined-behavior
sanitizer modes. Both submitted enumerators agreed entrywise, all group and
geometry controls passed, and all 1,252 regenerated submitted CNFs matched the
published manifest. That verifier does not replay the original 1.96 GB proof
corpus, and this review does not claim that it did.

Instead, [`independent_check.py`](independent_check.py) constructs a different,
strictly weaker formula for every representative:

- only the 125 point variables;
- one negative clause for each of the 775 affine lines;
- direct subset clauses for every exact five-point fiber count;
- the three proved gauge units;
- no plane-at-most-16 clauses and no cardinality auxiliaries.

The direct exact-count clauses were exhaustively checked on all \(2^5\)
assignments for target weights zero through five. Because the independent
formula omits constraints from the submitted one, proving it UNSAT is enough
to prove the submitted lifting exclusion.

Two disjoint runs covered cases `[0,626)` and `[626,1252)`. CaDiCaL 1.9.5
generated a proof for every formula, and a separate DRAT-trim process at source
commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` verified every proof. The checker
binary SHA-256 was
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
The new traces total 164,868,344 bytes; formulas have 1,091--1,115 clauses;
the maximum was 14,719 conflicts in case 974. Stable aggregate hashes are in
[`EXPECTED.json`](EXPECTED.json). Raw CNFs and proofs are regenerable and are
not committed.

Controls truth-table the cardinality clauses, accept and decode the known
70-point construction, reject an empty proof, and reject UNKNOWN or SAT as an
exclusion. The control-only correction to permit a total-70 word left the
case-1091 CNF and proof hashes byte-identical to the full run.

## Guarantees, assumptions, and remaining boundary

The proof is exhaustive, not sampled: every hypothetical counterexample maps
to the independently reproduced finite catalogue; the full affine action
covers the representatives; and every representative has a checked UNSAT
certificate in an independent encoding. The inherited two-eight-plane and
weighted-incidence theorems have separate independent reviews and complete
replays.

Trust remains in the written finite-geometric reductions, ordinary Python and
C++ execution, the published representative file, the full-group comparison,
CaDiCaL as proof generator, and DRAT-trim as checker. The full-group check and
independent catalogue substantially constrain errors in the representative
file, while DRAT proofs mean solver verdicts are not premises. This is not a
proof-assistant formalization or a formally verified SAT check.

The primary literature source, Elsholtz et al., [*Maximal line-free sets in
\(\mathbb F_p^n\)*](https://arxiv.org/abs/2310.03382v2), proves a 70-point
construction and the published bound \(r_5(\mathbb F_5^3)<74\). A targeted
search found no primary-source match for the new eight-plane theorem. The
result is graph-new and apparently literature-new relative to this bounded
search; this is not a priority guarantee.

## Strengthening and improvement opportunities

1. Export LRAT and check it with a formally verified checker, or formalize the
   compact 125-variable formulas, to remove DRAT-trim's C implementation from
   the final trust boundary.
2. Directly certify the 144 mixed matrices with a second eight-line as well as
   the 1,252 orbit representatives. This would remove use of the inherited
   two-eight theorem at the catalogue-discard step, although that theorem or
   another argument is still needed to force a nine-plane from an assumed
   eight-plane.
3. Publish a timing-free per-case compact manifest for the independent
   formulas. The aggregate digests here are stable, but a small line-oriented
   manifest would simplify distributed replay and partial failure diagnosis.
4. Mine common UNSAT cores from the much smaller primary-variable formulas.
   Recurring clauses may expose a reusable geometric obstruction for the
   surviving BBB family.
5. Keep the scope explicit in headline summaries: \(a_8=0\) and
   \(a_9\ge11\) are accepted structural facts, not an exclusion of 72 or an
   exact value of \(r_5(\mathbb F_5^3)\).

## Reproduction

Requires Python 3.10+, `python-sat==1.9.dev15`, a C++20 compiler, and
DRAT-trim. From this directory:

```sh
python3 catalogue_check.py --out /tmp/no-eight-review-catalogue
python3 independent_check.py --out /tmp/no-eight-review-proofs \
  --drat-trim /path/to/drat-trim
```

The proof run may be split at case 626 as recorded in `EXPECTED.json`.
