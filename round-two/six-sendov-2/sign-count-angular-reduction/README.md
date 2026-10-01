# Sign-count angular reduction

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Ordinary complete author proof, unformalized; independent review pending.

[PROOF.md](PROOF.md) proves sharp moment barriers X>=13/84 when the
positive/negative counts do not split4+4, and X>=19/120 when at least
five original coordinates coincide. The spectral transfer gives C<112/5
on every at-most-four-level profile outside the4+4 sign sector, and C<20
on the entire heavy-block stratum. The angular upper constants are not
claimed sharp. Using the existing c3>49/2 benchmark, every competitive
four-level profile must have four positive and four negative coordinates.

For4+2+1+1 this restricts the chart to -2<b<0 and0<=V<(b+2)². It leaves
the true remaining optimum and the full first-power endpoint unresolved.
[Literature and priority scope](LITERATURE.md) credits classical moment
context and campaign sources. No priority for kurtosis inequalities is claimed.

Reproduce with Python3.11+ standard library (tested CPython3.11.2):

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 python3 -B verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 python3 -B -O verify.py
```

Expected29 records,4 damage controls, SHA256
`9e2789dabb9d77ccf0c005b1d20f76e4dfd4939da7585ef7f400af4ff08e5291`.
`--expected PATH` permits external missing/malformed/altered fixture checks.
`--write-expected` regenerates only the small regression fixture. Written
spectral/extremal arguments remain outside the exact arithmetic kernel.
