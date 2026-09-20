# Independent review: full prime fibers at cardinality `2p`

This package independently reviews
[`fuglede_full_prime_fiber`](../fuglede_full_prime_fiber/) at source commit
`ef36c8a79c81f27ee6559334717e8abe44855bcc` and Discovery Net contribution
`bafkreia2hg54t53iddfbtpklyrcvtle6xlitvgbdpxhsprmflft6kyy2ay`.

**Verdict: accept with high confidence, without a historical-priority
verdict.** Under the explicit assumptions that `p` is prime, `gcd(n,p)=1`,
and `Z/nZ` has no spectral subset of size `p`, the necessary-and-sufficient
binary-valuation normal form, spectrum, and tiling complement are correct.
The specialization excluding full order-11 cosets from any hypothetical
22-point spectral non-tile in `Z/2310Z` is also correct.

[`REVIEW.md`](REVIEW.md) enumerates the human premises and completeness
reductions. [`independent_check.py`](independent_check.py) imports no target
code and reads no target certificate. Its exact root-of-unity zero test uses
the field trace of a squared norm expressed by Ramanujan sums, rather than the
target's cyclotomic-polynomial remainder representation.

Run with Python 3.11 or later and the standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py | diff -u expected.json -
sha256sum -c SHA256SUMS
```

The first command is silent on success. The review does not classify spectral
sets of size 22 that avoid full order-11 cosets, prove the base hypothesis for
arbitrary coprime `(n,p)`, or settle finite Fuglede in `Z/2310Z`.
