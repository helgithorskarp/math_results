# Independent review of the two-eight-plane exclusion

This directory records an independent review of the computer-assisted theorem
in [`two_eight_planes72`](../two_eight_planes72/) at exact source commit
`d2e5c9c1b51bf5d80823515ea38502526424c3df`.

**Verdict:** accept, with high confidence, the scoped theorem that a 72-point
line-free subset of \(\mathbb F_5^3\) has at most one eight-point affine-plane
section. This does **not** determine \(r_5(\mathbb F_5^3)\), whose interval
remains \(70\le r_5(\mathbb F_5^3)\le72\) in the reviewed campaign.

During this audit, a later `no_eight_planes72` result was published that uses
this theorem to exclude 144 two-eight-line quotient cases. This review closes
that inherited dependency only; it does not review or accept the later
1,252-class computation or its stronger no-eight-plane conclusion.

The full mathematical audit and trust boundary are in
[`REVIEW.md`](REVIEW.md).

## Independent method

[`independent_check.py`](independent_check.py) imports none of the submitted
Python or C++ implementation. It closes three important trust boundaries by a
different route:

1. It represents the interior deficit block as a multiset of seven or eight
   unit tokens. This independently obtains all 4,442 labeled quotients and the
   published catalogue hash.
2. It applies every one of the 12,000 affine transformations in
   \(\operatorname{AGL}(2,5)\) to every published representative. The normalized
   images form 164 disjoint orbits covering the full independently generated
   catalogue. This replaces the submitted selected-low-line canonicalizer.
3. It constructs a new SAT formula using only the 125 primary point variables,
   the 775 forbidden-line clauses, direct subset clauses for exact fiber
   cardinalities, and the proved three-hole gauge. It deliberately omits every
   plane-cap constraint and every sequential-counter auxiliary variable. All
   164 formulas are UNSAT and all 164 fresh binary proofs are independently
   accepted by DRAT-trim.

The independent proof traces total 22,656,471 bytes and are temporary outputs,
not repository artifacts.

## Reproduce

Python 3.12.14, `python-sat==1.9.dev15`, GCC 12.2.0, and DRAT-trim source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` were used. Build DRAT-trim at that
commit, install [`requirements.txt`](requirements.txt), and run from this
directory:

```sh
python3 independent_check.py \
  --out /tmp/two-eight-independent \
  --drat-trim /path/to/drat-trim \
  | cmp - EXPECTED.json
```

The output directory retains only `result.json` by default. Add
`--keep-proofs` to retain the generated CNFs and proof traces. The complete
check took 54 seconds on the review host. Check the published evidence bytes
with:

```sh
sha256sum -c SHA256SUMS
```
