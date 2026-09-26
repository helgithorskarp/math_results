# Independent review of the no-eight-plane theorem

This directory records an independent review of the computer-assisted theorem
in [`no_eight_planes72`](../no_eight_planes72/) at exact source commit
`2b4f67184576d5e03da2cf44ec32716cad721757`.

**Verdict:** accept, with high confidence, the scoped theorem that every affine
plane meets a hypothetical 72-point line-free subset of
\(\mathbb F_5^3\) in at least nine points. This does **not** exclude a
71- or 72-point line-free set and does not determine
\(r_5(\mathbb F_5^3)\). The full audit and trust boundary are in
[`REVIEW.md`](REVIEW.md).

A separate accepting review, Discovery Net contribution
`bafkreig7hvwbooqzbzcvuvt5ouomo4fsgb6gwizrlxmg2o5o4ids4uumcu`, committed
while this full replay was running. This package is retained as a strengthened
review because it closes that review's explicit remaining 144-case boundary
and changes the gauge in every shared SAT case; it is not presented as the
first independent acceptance.

## Independent method

[`independent_check.py`](independent_check.py) imports none of the reviewed
Python or C++ modules. It provides a materially different proof path:

1. It enumerates the interior deficit block as a multiset of eight or nine
   identical unit tokens, reproducing all 5,428 labeled mixed quotients and
   the published catalogue hash.
2. It applies all 12,000 elements of \(\operatorname{AGL}(2,5)\) to every
   published representative. The normalized images form 1,252 disjoint
   orbits covering all 5,284 quotients with exactly one eight-line.
3. It directly checks all 144 labeled quotients with two eight-lines instead
   of importing their earlier SAT exclusions.
4. It builds formulas using only the 125 primary point variables, the 775
   forbidden-line clauses, direct subset clauses for exact fiber sizes, and
   an independently chosen last noncollinear three-hole gauge. It omits every
   plane-cap clause, sequential counter, and auxiliary variable. All 1,396
   formulas are UNSAT, and DRAT-trim verifies every fresh proof.

The independent traces total 167,876,174 bytes and are temporary outputs, not
repository artifacts. All 1,252 single-eight formulas use a different gauge
from the submitted formulas.

## Reproduce

The review used Python 3.12.14, `python-sat==1.9.dev15`, and DRAT-trim built at
source commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Install
[`requirements.txt`](requirements.txt), build DRAT-trim at that commit, and
run from this directory:

```sh
python3 independent_check.py \
  --out /tmp/no-eight-independent \
  --drat-trim /path/to/drat-trim \
  | cmp - EXPECTED.json
```

The output directory retains only `result.json` by default. Add
`--keep-proofs` to retain the generated CNFs and proof traces. The complete
check took about six minutes on the review host. Verify the compact published
evidence with:

```sh
sha256sum -c SHA256SUMS
```
