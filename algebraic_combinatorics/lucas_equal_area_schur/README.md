# Complete Lucas equal-area Schur positivity

This directory proves the full positive-integer equal-area Lucas comparison
from Bergeron's Conjecture 10.1. For `1<=a<b<=c<d`, `ad=bc=N`, set

```text
D = (-1)^(a+1) ({b+c choose b}_F - {a+d choose a}_F)
G = (qt)^(a+1) F_(N-2a-1).
```

Then `6D-G` is Schur-positive in two variables. The Schur support of `D`
starts exactly at second-row size `a+1`, with coefficient one, and is
strictly positive thereafter. Symmetry and the trivial equality cases give
the conjecture in its complete positive-integer scope.

The [written proof](PROOF.md) is universal. Its main ingredients are a
parity-preserving two-to-one partition map, a threefold Lucas contraction,
and a shifted rectangle-boundary envelope. Equal-area arithmetic leaves six
small identities, displayed in the proof and stored in `BOUNDARY.json`.

Two exact standard-library implementations independently verify those
identities:

- `layers.py` uses Gaussian q-Pascal layers and Schur-Pieri transport;
- `direct.py` uses the defining Lucas recurrence, literal factorial
  multiplication and exact monic division after `t=1`, then monomial first
  differences.

`verify.py` compares them coefficient-by-coefficient, audits the partition
map, rectangle decomposition, Lucas kernels and rational tail budget, and
checks 463 additional comparisons through degree180. This code corroborates
the proof; it does not replace its infinite quantifier.

## Reproduce

Tested with CPython 3.11.2, standard library only:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -O verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v test_checks.py
sha256sum -c SHA256SUMS
```

The first two commands must emit the same compact JSON ending in
`"all_checks":true`; all eight unit-test groups and every manifest entry
must pass. Expected exact results are in `EXPECTED.json`. A reference run
with CPython 3.11.2 took 9.3 seconds and 62,376 KiB peak RSS.

## Scope and trust boundary

No floating point, randomness, solver, CAS, external dataset, generated
bulk certificate or network input is used. The trust base for computation is
the readable Python source, interpreter, operating system and hardware.
The result has not been independently peer-reviewed or formalized in a proof
assistant. The uniform constant `1/6` is not claimed optimal, and no claim of
elementary positivity or real-rootedness is made.

Primary conjecture: François Bergeron, *A (q,t)-Overview of q-Analogs*,
[arXiv:2608.30979v1](https://arxiv.org/abs/2608.30979v1), Section 10.2,
Conjecture 10.1. The paper reports verification only through `ad=bc<=36`.
Lucas-binomial background: Sagan--Savage,
[arXiv:0911.3159](https://arxiv.org/abs/0911.3159).
