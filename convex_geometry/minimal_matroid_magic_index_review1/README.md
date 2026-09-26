# Independent review of the minimal-matroid magic index

This directory records an independent correctness review of the theorem in
[`minimal_matroid_magic_index`](../minimal_matroid_magic_index/) at exact source
commit `497a9c81e65ed989cc927e012d83080de7600795`.

**Verdict:** accept for mathematical correctness, with high confidence.  The
proof establishes

$$
D_{k,n}(ax)\text{ is magic positive}
\quad\Longleftrightarrow\quad
a\geq\max(k,n-k)
$$

for every real $a>0$.  The integer magic index follows.  The full audit,
including the trust boundary and a nonfatal novelty qualification, is in
[`REVIEW.md`](REVIEW.md).

## Independent reproduction

Run from this directory with Python 3.11 or newer:

```sh
python3 independent_check.py | cmp - EXPECTED.json
python3 -O independent_check.py | cmp - EXPECTED.json
```

The checker imports none of the submitted code.  It reconstructs the Ehrhart
polynomial from exact lattice-slice values by Newton forward differences,
performs exact polynomial division by the known binomial factor, checks the
residual signs, and independently changes to the magic basis.  It checks 144
normalized parameter pairs through $n=24$, 650 residual signs, 432 magic-basis
vectors, 143 preceding integer dilations, and 40 direct coordinate
enumerations.  [`EXPECTED.json`](EXPECTED.json) is the compact output record.

These computations corroborate formulas and boundary cases.  The universal
theorem is established by the written proof, not by the finite range.

Check the evidence bytes with:

```sh
sha256sum -c SHA256SUMS
```
