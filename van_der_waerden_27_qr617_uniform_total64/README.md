Author: **six-vdw-2**, role **researcher**. Exact computer-assisted lemma for
symmetric two-color, seven-term van der Waerden colorings.

Every seven-AP-free binary coloring of 3,704 points differs from the fixed
aligned QR617 reference at **at least 64 and at most 3,632 nonpole positions**.
The two original reference classes each have 1,848 positions; their edit counts
remain between 30 and 1,818, using the separately cited class-floor result.
The seven old poles and final point are free and uncounted. No symmetry or
periodicity is imposed on the actual coloring.

The new direct result excludes all four endpoint-zero original-class cap boxes
`30/33`, `31/32`, `32/31`, `33/30`. The 24 mandatory root cases contain 48 nodes,
four complete AP disjunctions and 44 terminal leaves. The class-30 floor gives
endpoint-zero total at least 64; complement gives endpoint-one total at most
3,632. The separately published endpoint-one lower-64 result completes the
uniform profile. Numerical dependencies are explicit in
[provenance.json](provenance.json); their old proof corpora are not rerun here.

From the repository root, using Python 3.11 or later and the standard library:

```bash
python3 van_der_waerden_27_qr617_uniform_total64/reproduce.py \
  --output-dir /tmp/qr617-uniform64
```

The output directory must lie outside this repository. The command regenerates
48 proposal primitives, checks every certificate hash, and runs 114 audit
partitions serially. Every subprocess has an unchanged 90-second limit and
one-thread environment. Generated proof data occupy 25,193,531 bytes. They,
logs, attempts, checkpoints and caches are omitted from Git. Source plus the
compact expected results suffice; no private certificate input is required.

Expected final status is `UNIFORM64_COMPLETE_FRESH_REPRODUCTION_PASSED`, with
24 roots, 48 nodes, four splits, 44 leaves, 24 full parent-state comparisons and
280 rejected corruption controls in **each** normal/optimized Python mode.
The finite arithmetic reduction covers all 10 integer pairs below total 64
and includes four meaningful omitted-box controls.

Explicit `--resume` reuses only completed jobs from identical source. A saved
interruption, failed subprocess, timeout or previously attempted open primitive
is never silently retried. Such a failure establishes no exclusion. Preserve
its output and inspect the exact next frontier under the same resource limits.

The proposal kernel enumerates squares and uses bitmasks. The unchanged
definition-level checker uses Euler's criterion, actual AP sets and exact
integers; it imports no generator. It derives every inherited state and full
child cover itself. This is implementation independence by the same researcher,
without external review or formalization. See [PROOF.md](PROOF.md),
[verify.py](verify.py), [generate.py](generate.py), [reproduce.py](reproduce.py),
[expected.json](expected.json), [provenance.json](provenance.json),
[VALIDATION.md](VALIDATION.md) and [evidence.json](evidence.json).

The total-64 boundary pairs `(30,34)`, `(31,33)`, `(32,32)`, `(33,31)`, `(34,30)`
remain unexcluded at either endpoint, as do their total-3,632 complements. No
attainment is asserted. This package supplies no 3,704-point coloring, improved
bound on W(2,7), exact W value or unrestricted nonexistence result.

Primary baseline checked live on 2026-10-01:
[Monroe Table 1/Table 2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
records length seven/two colors greater than 3,703 and prime 617. Monroe writes
W(length,colors), reversing this campaign's W(colors,length). This is distinct
from asymmetric w(3,k). Narrow primary searches are not an exhaustive audit of
current-best status or historical priority.
