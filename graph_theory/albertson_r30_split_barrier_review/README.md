# Independent split-barrier review of the Albertson `r=30` proof candidate

This directory independently reviews commit
`7bf1e64c31bed0b52213bd7dc1b0e2fcf09598c9`, which proposes that
Albertson's conjecture holds for chromatic number 30.

During the final repository refresh, commit `7e1f47396d20a431e9cd82bb121885bd7edf3ad9`
also independently accepted the conclusion through a stronger recursive seed
and a specialized Hall argument.  The route here remains distinct: it uses
neither recursion nor Hall.

**Verdict:** the reviewed proof candidate survives source reproduction, a
line-by-line audit of its structural lemma and recursive crossing calculation,
and a genuinely different end-to-end derivation.  The alternate derivation
uses only one-level induced sampling and two very small Tutte-barrier
enumerations; it does not use the reviewed recursive table, its Hall lemma, the
`r=29` theorem, or any old `r=29` configuration census.

The result should still be described as an independently reviewed **proof
candidate**, not as an established theorem: several named graph theorems are
imported, the new September 2026 degree-gain/join manuscript is a preprint, and
neither proof has been formalized end to end.

See [REVIEW.md](REVIEW.md) for the mathematical audit.

## Reproduce

CPython 3.11 or later, standard library only:

```sh
python3 -B verify.py | diff -u EXPECTED_OUTPUT.txt -
sha256sum -c SHA256SUMS
```

The checker uses exact integers and `Fraction`s.  Two independently coded
integer-partition algorithms agree at every barrier size.  It checks every
order in the finite bands, all sampling cutoffs, all endpoint split bounds,
and the regular-order Rabern arithmetic.  It does not formalize the cited
graph-theoretic implications.
