# J74 negative-gap obstruction strips

six-rupert-2, researcher; 2026-10-02. Author-checked, unformalized and
independently unreviewed intermediate result. Global J74 Rupertness remains
open. Read [the full proof](PROOF.md) for every quantifier and bridge.

Two complete closed two-dimensional receiving strips exclude every closed
fit at relative proper pose Q=R(q)Q0 with Euclidean Cayley norm at most
1/100, arbitrary actual physical translation, and every scale lambda>=1.
The physical support separation is strictly greater than67/75000 on A
and17/75000 on B. The source neighborhood is a hypothesis; it is not
derived for every fitted source. No global non-Rupert theorem or passage
construction is claimed.

The receiver raw normal is u=(m+t*d)/(1+t)+r*(m cross d), with m,d,Q0
specified in the proof. A uses t in[4+2sqrt5,11+5sqrt5], abs(r)<=1/100;
B uses t in[3+7sqrt5/5,11+5sqrt5], abs(r)<=1/200. These are receiving
coordinates, not angles. All boundaries and changing support horizons
are included.

Run from the repository root with Python3.11 or later and the standard
library only:

```sh
python3 -B round-two/six-rupert-2/negative_gap_strips/check.py
python3 -B -O round-two/six-rupert-2/negative_gap_strips/check.py --self-test
```

The first prints `exact J74 negative-gap strip hypotheses verified` after
comparing EVERY field against [expected.json](expected.json). The second
also rejects eight damaged controls. `--print-record` prints the full
compact canonical mathematical record. `--write-expected` is the explicit
author regeneration option; ordinary checking never rewrites expected
evidence.

The checker reconstructs both original-cupola gyrations, all60 original
points/norms, three antipodal spanning pairs,28+25 support/source triples,
all12720 original corner support evaluations and complete support tie
sets. It checks108 full six-component polynomial wrench coefficient
equalities,204 nonnegative bilinear weight controls, eighteen strictly
negative weighted-gap coefficients, eight mass sums, and both exact
quadratic absorption margins. Ordinary-power expansions additionally
verify the complete wrench and tensor-Bernstein gap identities.

The canonical21772-byte mathematical record has SHA256
`820d3b2674a5a22be94bfd60e16e6d1b7b2e6e8fee7be926975086cf9636537a`.
Ordinary and optimized complete-record runs match entry by entry,
including all actual original support records and semantic controls.
They used about5 seconds and under25 MiB peak RSS upper bounds,
each inside an unchanged one-CPU/two-GiB scope and a45-second
guard. See [VALIDATION.json](VALIDATION.json) for exact commands, source
and certificate fingerprints, interpreter version and damage reasons.

The [certificate](certificate.json) contains only exact field coefficients
and original indices. The LP discovery proposals were one-thread
SciPy1.14.1/HiGHS, repaired exactly. No numerical library or solver result
is part of the verification trust base. The source does not need a private
checkpoint, omitted large corpus, remote dataset, node, ledger or network.

The two published geometric/arithmetic inputs are pinned in
[DEPENDENCIES.json](DEPENDENCIES.json). The named original solid's
constructive identification is the explicit geometric premise; the
unrelated parent projection-area arrangement is not replayed or used.
The written convexity, Cayley, scale and physical support-distance bridges
remain unformalized. Matching author checks are not independent review.
