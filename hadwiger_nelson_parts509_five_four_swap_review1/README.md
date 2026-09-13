# Independent review: seven completions in the sealed Parts pool

## Verdict

**Accepted, with an essential restricted-family qualification.**  At target
mathematical commit
`503681c9e5c9c1e01ff1fd8ad468b03d27c8ef3b`, the evidence proves:

> Let `L` be Parts-509 vertices 0,...,373, let `S` be vertices 374,...,508,
> and let `Q5` be the specified 168 level-one completion points.  Put
> `U = S union Q5`.  If `X` is a subset of `U`, `|X| <= 134`, and the complete
> unit-distance graph on `L union X` is not four-colourable, then
> `|X intersect Q5| >= 7`.

This is a useful exact exclusion for the current record-directed search.  It
does **not** produce a graph on at most 508 vertices, does not exclude points
outside this 677-point universe, and does not improve the unrestricted
published 509-vertex record.  The `q=7` stratum remains open.

## What was independently checked

`independent_review.py` imports no implementation code from the package under
review.  It:

1. parses all 509 Parts coordinates and the relevant completion coordinates in
   `Q(sqrt(3),sqrt(5),sqrt(11))`;
2. checks all pairs in the 677-point universe, using two field homomorphisms to
   finite fields only as a sound rejection screen and exact algebraic-field
   arithmetic for every survivor;
3. confirms that the resulting complete unit-distance graph is exactly the
   restriction of the committed ambient edge list;
4. checks the 20 fixed-`L` interface colourings and all 5,528 killing-set
   complement colourings against that independently reconstructed graph; and
5. checks deletion-set uniqueness, pool membership, packed-colour padding, and
   provenance counts.

The target's three committed selector CNFs rebuild byte-for-byte.  Fresh proof
generation with the executable whose SHA-256 is pinned by the target reproduced
the advertised `q=4,5,6` binary DRAT files byte-for-byte.  A freshly built
`drat-trim` from commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`
verified all three.

`independent_selectors.py` also supplies a second logical encoding.  It does
not reuse the target's binary ripple counters.  Since `|S|=135`, a 134-point
selection containing exactly `q` points of `Q5` contains exactly `q+1` deleted
points of `S`.  The script expresses these two small exact counts through unary
threshold recurrences and adds the same mathematically necessary killing-set
clauses.  Exhaustive controls check the threshold encoding on all assignments
through six inputs.  Fresh CaDiCaL proofs, checked by independently built
`drat-trim`, establish UNSAT for every `q=0,...,6`; in particular this review
does not need to import the target's earlier `q=0,1,2,3` exclusions.

## Why the reduction is sound

For every certified deletion set `D`, the evidence gives a proper
four-colouring of `L union (U minus D)`.  Therefore any `X` for which
`L union X` is not four-colourable must intersect every `D`.  This is exactly
the family of positive hitting clauses used by both selector encodings.

The selectors close all 134-point hitting sets with zero through six selected
`Q5` points.  If a smaller counterexample `X` had `m < 134` points and
`q <= 6`, it could be enlarged to order 134 using only unused `S` points:

```text
unused S = 135 - (m - q) >= 134 - m.
```

Non-four-colourability is monotone under adding vertices, and the enlargement
does not change `q`, contradicting the corresponding exact-order selector.

## Reproduction

From the repository root:

```bash
python3 -m venv /tmp/hn-review-venv
/tmp/hn-review-venv/bin/pip install -r \
  hadwiger_nelson_parts509_five_four_swap_review1/requirements.txt
/tmp/hn-review-venv/bin/python -B \
  hadwiger_nelson_parts509_five_four_swap_review1/independent_review.py
/tmp/hn-review-venv/bin/python -B \
  hadwiger_nelson_parts509_five_four_swap_review1/independent_selectors.py \
  --out /tmp/hn-independent-selectors
```

For each generated selector, CaDiCaL must exit with code 20 before checking the
proof.  For example:

```bash
cadical /tmp/hn-independent-selectors/independent_q6.cnf /tmp/q6.drat
drat-trim /tmp/hn-independent-selectors/independent_q6.cnf /tmp/q6.drat
```

The generated CNFs and large DRAT traces are intentionally not stored in Git.
Their byte counts and hashes, along with solver/checker provenance and replay
outcomes, are recorded in `REVIEW_RESULT.json`.

## Limitations and source integrity

- The theorem is about the explicit fixed `L` and sealed `S union Q5` pool,
  not all plane point sets or even all natural augmentations of Parts-509.
- `Q5` is the source package's name for a selected completion subpool; it is
  not a claim that each such point has geometric degree five.
- The three target DRAT files are not archived in Git because the largest is
  about 842 MB.  Their exact regeneration was checked in this review, but
  future verification still incurs that computation.
- The target's pinned CaDiCaL executable was available and matched its manifest.
  A clean build of the same `rel-3.0.1` source commit used `-DQUIET` and carried
  a different build timestamp, so it did not have the same executable hash.
  It nevertheless produced the independently encoded proofs.  The DRAT checker
  rebuilt byte-for-byte from its pinned source.
- The target Discovery contribution was accepted for broadcast but absent from
  the stale committed ledger at review time.  This review therefore does not
  describe that broadcast as committed.

Large scratch proof traces were preserved at
`/scratch/hn-parts-q456-review.20260913.0DXkpDub` for immediate local audit.
