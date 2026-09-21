# Independent review of vertex-inflation Whitehead inheritance

This directory independently reviews the theorem in
[`../vertex_inflation_whitehead`](../vertex_inflation_whitehead): for a finite
two-dimensional simplicial complex, three local conditions characterize a
relative collapse of its vertex inflation, the sequence restricts to every
subcomplex, and this yields an operation-specific Whitehead inheritance
criterion.

Verdict: **accept with high confidence**.  See [REVIEW.md](REVIEW.md) for the
premise-by-premise proof audit, adversarial examples, caveats, literature
boundary, and strengthening opportunities.  See [SOURCES.md](SOURCES.md) for
the primary-source audit.

## Reproduce the independent evidence

Python 3.11+; standard library only.  From this directory:

```sh
python3 verify_independent.py
python3 -O verify_independent.py
sha256sum -c SHA256SUMS
```

The checker imports no target code or fixtures.  It uses a global free-pair
search rather than the target's copy-addition schedule, a separate mod-2
boundary elimination, exact signed integral sphere chains, and exhaustive
subcomplex replay on two boundary-sensitive fixtures.

It checks all 9,417 labelled complexes of dimension at most two on one through
four vertices with multiplicities in `{1,2,3}`.  The local criterion, the full
quantitative `H_2`-kernel formula, and the independent boundary computation
agree in every case.  All 697 and 2,099 subcomplexes of the two restriction
fixtures replay correctly.

Evidence payload SHA-256:

```text
553cbf2ea539b8ac3a78f49c73a5e7ea0c19c6600e4e147353adce75d344c19e
```

The universal theorem rests on the reviewed written proof.  The computation is
finite corroboration and does not decide arbitrary base asphericity.

