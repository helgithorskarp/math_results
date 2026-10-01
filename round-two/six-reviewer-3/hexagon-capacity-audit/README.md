# Independent short-hexagon capacity audit

Actual author: **six-reviewer-3**, role **independent mathematical reviewer**.

This confirms committed lemma 8804's capacity-one restriction for every
short six-cycle's smaller closed region in any finite spherical code with
\(14/25\le c\le3/5\), and proves the same theorem with edge tolerance
\(1/60\) instead of \(1/100\). Concave cycles and overlapping forced caps
are included. The forty-cell certificate has minimum rational gap
\(9031/500000>1/100\). No global Tammes-15 optimality or numerical record
is claimed.

[REVIEW.md](REVIEW.md) gives the full independent proof, verdict, prior art,
dependency scope and strengthening opportunities. [NUMERICS.md](NUMERICS.md)
proves the quadrature error bound. [audit.py](audit.py) uses exact rational
composite Simpson integration, not either original inverse-trig series.
It imports no author code and requires no proof input.

From the repository root, standard-library Python 3.11 or later:
```bash
python3 -B round-two/six-reviewer-3/hexagon-capacity-audit/audit.py
python3 -B -O round-two/six-reviewer-3/hexagon-capacity-audit/audit.py
python3 -B round-two/six-reviewer-3/hexagon-capacity-audit/replay.py
```
EXPECTED.json contains all 45 cell records and controls. Complete
normal/optimized evidence agrees, canonical SHA256
`5ef5b0cb85139e53c95c038d6ca3ce1be0b2ab1486acc8b1357b4bd780deb5a2`.
VALIDATION.json records observed environment, fixed guards and resources.
INPUTS.json pins inspected original source for provenance only. SHA256SUMS
covers the compact package, excluding the manifest itself.

The geometry, quadrature kernel and derivatives are written and
unformalized; the code certifies the exact scalar obligations after that
reduction. Neither source publication nor normal/-O agreement replaces
the mathematical proof. Generated scratch, private operational evidence,
logs and caches are excluded from this contribution.
