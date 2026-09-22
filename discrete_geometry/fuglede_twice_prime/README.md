# Twice-prime spectral profiles and paired-level extraction

For an odd prime `p` coprime to `n`, assume `Z_n` has no spectral set of
size `p` or `2p`. Then a `2p`-point subset of `Z_n x Z_p` is spectral exactly
when every prime level is a pair and all pair differences have one common
binary valuation below `v_2(n)`. An explicit spectrum and common tiling
complement are given in [PROOF.md](PROOF.md).

The main structural step extracts a `p`-point spectral pair downstairs from
the only remaining mixed level profiles. The proof also gives an unconditional
three-way profile alternative. Under the base hypotheses the number of
spectral subsets is

```text
sum_(0 <= t < v_2(n)) (n^2 / 2^(t+2))^p,
```

with zero when `n` is odd. For `Z_2310`, the 22-point spectral subsets are
exactly the complete residue systems modulo 22, numbering `105^22`.

**Literature correction:** this is not claimed as a new Fuglede solution.
Two retrieved August 2026 preprints by Jiahui Liang state broader square-free
closure and odd-prime-power descent. Their relation to the original graph
frontier is explained in [SOURCES.md](SOURCES.md). This package preserves an
elementary structural proof and exact corroboration independently of that
operator-theoretic route. It is not a peer-review certification of those
preprints.

## Reproduce

Python 3.11 or later, standard library only:

```bash
python3 verify.py --check
python3 -O verify.py --check
python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

Expected terminal line:

```text
PASS: all-subset classification, paired extraction, exact spectra, and tilings
```

[expected.json](expected.json) records the exact declared scope. The checker
enumerates every `2p`-subset containing zero for eight small coprime parameter
pairs, not only balanced subsets. Translation preserves the property, so this
covers all subsets up to a translation, with duplicates allowed. A Fourier-zero
clique search does not use the proposed criterion; found spectra are checked
again by integer Ramanujan traces. The count formula is compared separately.

The two extraction branches are exercised by explicit phase-vector families.
Those fixtures deliberately have `p|n` so the extracted base spectra exist;
they test the conditional vector algebra after the nonzero-row bound, not
the coprime reduction or an asserted realization of the mixed profile.
The prime-to-`n` pairing lemma is checked separately. Profile arithmetic,
negative Gram witnesses, empty-level projection, larger exact spectra and
tilings, and malformed inputs are also audited.

The universal proof is written mathematics. There is no solver, floating-point
zero test, omitted exhaustive run, external certificate, or formal proof
assistant. Code is corroboration, not the source of an unbounded theorem.
See [VALIDATION.md](VALIDATION.md) for the measured scope and runtime.
