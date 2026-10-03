# Independent repeated-profile cap audit

Actual **six-reviewer-5**, independent mathematical reviewer. The complete
LEMMA9838 repeated-triangle profile `(2,1)` is confirmed for every old
cube order `n>=3`. The same rational witness also has a strictly stronger
scaled upper gap `>7/4`, improving the source's `>3/4` guarantee.

[Review and exact scope](REVIEW.md), [complete independent proof](DERIVATION.md),
[compact exact certificate](PRIMARY.json), and [independence seal](PRIMARY-SEAL.json)
are substantive evidence. This is an ordinary unformalized proof with exact
computer-assisted polynomial identities. It does not settle general H or I,
the singular `n=2` chart, arbitrary repeated profiles, or an optimal gap.

From this directory, use Python 3.11 or newer and the pinned dependency:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python reproduce.py
.venv/bin/python -O reproduce.py
.venv/bin/python corroborate.py
.venv/bin/python -O corroborate.py
```

All six native thread settings are set to one. Run the commands serially.
The independent runs regenerate and compare the ENTIRE primary record,
then independently check both frozen 24-obligation certificates by rational
Gaussian elimination and reject 14 meaningful semantic damages. Expected
whole primary SHA256:
`887e359dd56a09a42f52a4b614bfb46d724fd29060f1ae9406b311ddbfc47297`.
Each uniform certificate has 594 positive coefficients; the maximal degree
is 80. Literal `n=3,4,5` checks include 4332 ordered positions per seed or
repaired matrix and 4332 whole lifted repair positions.

The separate corroboration commands require network access. They retrieve
ALL 17 exact pinned source files specified in [AUTHOR-SOURCE.json](AUTHOR-SOURCE.json),
check each full byte count and SHA256 before execution, run the unmodified
author code only in a separate child, and compare the ENTIRE independently
rebuilt [COMMON.json](COMMON.json). The native child has a fixed 45-second
timeout; timeout is incomplete verification. Its bulky mathematical record
is generated only in a temporary directory, never an external proof input.
The independently sealed primary proof and programs neither import nor
depend on author code. Written mathematics was visible before the seal;
this was not a blind review. [VALIDATION.json](VALIDATION.json) records actual
versions, costs, full-record comparison scopes, and trust boundaries.

[CONTROLS.json](CONTROLS.json) contains both complete frozen-checker results.
The primary generator uses integer Bareiss plus finite-degree interpolation;
the frozen checker instead uses rational Gaussian determinants. SymPy's
exact rational-function field, Python integer/Fraction arithmetic, the
handwritten complete-space and lift bridges, and the independently written
programs remain trusted. No proof assistant was used. Source hashes are
integrity checks, not proofs of correctness or distinct authorship.
