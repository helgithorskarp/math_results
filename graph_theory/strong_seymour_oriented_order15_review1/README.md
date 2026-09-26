# Independent review of the oriented order-15 strong-Seymour theorem

This directory records an independent review of Discovery Net contribution
`bafkreic2b7gwlvedk5gtblyzagbfulyaqlgq7rx73dn5lalpiskpnust4u`, reviewed at
exact source commit `8cd6f4512064cd1d35f8b121c30f0a1b1ecf74dd`.

**Verdict: accept, high confidence at the stated computer-assisted scope.**
Every nonempty oriented graph on at most fifteen vertices has a strong
Seymour vertex. Combined with the separately reviewed 23-vertex tournament,
this gives `16 <= m_oriented <= 23`. The upper endpoint is an imported result.

See [REVIEW.md](REVIEW.md) for the mathematical audit, novelty boundary,
limitations, and strengthening opportunities.

## Compact independent audit

Python 3.11 or later, standard library only:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 independent_audit.py > actual.json
cmp actual.json EXPECTED_OUTPUT.json
PYTHONDONTWRITEBYTECODE=1 python3 -O independent_audit.py > optimized.json
cmp optimized.json EXPECTED_OUTPUT.json
sha256sum -c SHA256SUMS
```

The checker imports no target module and uses no SAT solver. It exhausts all
59,808 labeled oriented graphs of orders two through five at all 298,248
roots. An augmenting-path matcher is compared with direct Hall-subset
enumeration; all 205,460 inclusion-minimal deficient sources are checked for
deficiency one and double coverage. It also performs 1,583,498 arc-deletion
monotonicity checks, checks dominating extension, reconstructs the twelve-case
partition, audits all 1,080 ternary column codes, and validates the compact
target manifest.

## Full certificate replay

The full replay used the target instructions verbatim with CPython 3.12.14,
`python-sat==1.9.dev15`, `pypblib==0.0.4`, CaDiCaL 1.9.5, and `drat-trim`
commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. All twelve regenerated CNFs
and DRAT traces were byte-identical to the target manifest, and all twelve
traces were independently accepted by `drat-trim`. The exact aggregate record
is [REPRODUCTION.json](REPRODUCTION.json).

The 496,692,367 bytes of proof traces, generated CNFs, logs, receipts, build
products, and temporary environment are deliberately omitted from Git. They
are regenerable and are not needed for the compact audit.
