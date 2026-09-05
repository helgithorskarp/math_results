# Dense506: every remaining three-point obstruction lies in the host field

For either pinned dense506 host and its fixed four-colouring, adding three
plane points preserves that colouring whenever at least one point is
outside the host coordinate field

    K = Q(sqrt(33), i*sqrt(3), sqrt(-408+72sqrt(33))).

The [proof](PROOF.md) closes the non-field case left by the preceding
midpoint reduction. It checks 4,050,552 midpoint triangles and 140,742,349
host-pair assignments. All 34,938 modular survivors have parallel host-pair
lines, contradicting the necessary concurrency condition. Two modular
images give identical survivors; exact arithmetic verifies every one.

No <=508 five-chromatic graph is established. The three-field-point case
remains open. Failure of a particular host colouring would not itself
establish five-chromaticity. Other placements and larger additions remain
outside this theorem.

## Full reproduction

Use CPython3.11.2 without optimization and GCC12.2 with the standard library.
From this directory in a full checkout, choose an external work path which
does not yet exist:

```bash
triangle_work=/tmp/hn-nonfield-triangles
python3 prepare.py --work "$triangle_work" > "$triangle_work.prepare.json"
cmp expected_prepare.json "$triangle_work.prepare.json"
g++ -std=c++17 -O3 -Wall -Wextra -Wconversion -Wshadow -Werror enumerate.cpp -o "$triangle_work/enumerate"
g++ -std=c++17 -O3 -Wall -Wextra -Wconversion -Wshadow -Werror screen.cpp -o "$triangle_work/screen"
g++ -std=c++17 -O3 -Wall -Wextra -Wconversion -Wshadow -Werror audit_screen.cpp -o "$triangle_work/audit_screen"
"$triangle_work/enumerate" "$triangle_work/midpoints.txt" "$triangle_work/triangles.txt" 0
"$triangle_work/screen" "$triangle_work/screen_input.txt" "$triangle_work/triangles.txt" "$triangle_work/screened.txt" 0
python3 verify.py --work "$triangle_work" > "$triangle_work.verify.json"
cmp expected.json "$triangle_work.verify.json"
python3 packed_audit.py --work "$triangle_work" > "$triangle_work.packed.json"
cmp expected_packed_audit.json "$triangle_work.packed.json"
python3 audit_input.py --work "$triangle_work" > "$triangle_work.audit-input.json"
cmp expected_audit_input.json "$triangle_work.audit-input.json"
"$triangle_work/audit_screen" "$triangle_work/audit_screen_input.txt" "$triangle_work/triangles.txt" "$triangle_work/audit_screened.txt" 0
python3 audit_exact.py --work "$triangle_work" > "$triangle_work.audit-exact.json"
cmp expected_audit_exact.json "$triangle_work.audit-exact.json"
python3 controls.py --binary-dir "$triangle_work" > "$triangle_work.controls.json"
cmp expected_controls.json "$triangle_work.controls.json"
sha256sum -c SHA256SUMS
```

The final native argument0 means the complete finite domain. A positive
argument is a partial prefix, for controls only; a prefix is not the
published theorem. Every tool fails on malformed input or failed checks.
Run the complete pipeline: expected hashes and native completion messages
alone are not certificates of the enumeration.

All large inputs and outputs are generated in the external work directory.
The midpoint stream is78,343,591 bytes; each survivor stream is1,456,306
bytes. Sources and compact expected outputs are public. No large dump,
compiled binary or old C3 census is required from an external source.

## Validation and measured cost

| Completed computation | Seconds | Peak RSS, KiB |
|---|---:|---:|
| Native midpoint enumeration | 33.893 | 11,156 |
| Primary modular screen | 35.975 | 11,172 |
| Full independent packed midpoint audit | 248.400 | 62,296 |
| Second-prime Cramer-rule screen | 39.113 | 11,184 |
| Independent exact residual audit | 2.857 | 59,440 |

These are measured processes, not hardware-independent promises. The
reference Python vector lookup took2.131 seconds on310,845 midpoint pairs;
its projection to the full domain justified the native implementation.
Every one of its4,523 initial triangle rows matches the native code.
The screen's definition-level Python pilot checked132,823 assignments and
matched all132 survivors. The full packed audit matches every midpoint
triangle row, not only totals. Exact residual checks use both host roots
and distinct four- and eight-basis arithmetic.

All three native sources are byte-identical to their completed full runs.
Fresh public input generation matched every exploratory input byte. Public
prepare, verification, audit-input, exact-audit and controls entry points
were run. The full packed loop is identical to its completed run except
progress output; its public argument handling and loop were exercised on
the positive fixture. The full scans were not repeated merely for file-path
and reporting refactors. Both full screens were replayed after strengthening truncated-input rejection; their complete streams remained byte-identical. Two truncated-stream controls are rejected. See [validation.json](validation.json).

For checking builds, replace -O3 by

    -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer

with the same warning flags. Run the enumerator with final argument30 and
each screen with final argument10000 into fresh output files. All these
sanitizer prefixes completed without diagnostics and matched corresponding
optimized outputs. The positive fixture has a genuine radical unit
triangle, ensuring that both geometric filters retain a nonsingular valid
case. A broken-radius fixture is rejected and a singular modular case is
retained deliberately.

## Dependencies and disposition

The [midpoint reduction](../hadwiger_nelson_dense506_triangle_midpoint_reduction/README.md),
source `c6166e1d4f0911a5ae5db6641248305e5f617975`, is Discovery Net
`bafkreiepamnj474groelbyefnmhvzck6wmezgjnq5bbrc4j7yzx3aks4ai`.
Its geometric and earlier colouring reductions are explicit imported
premises. The [original exact host theorem](../hadwiger_nelson_dense506_two_point_extension/README.md)
and [independent arithmetic review](../hadwiger_nelson_dense506_two_point_extension_review1/README.md)
provide the pinned coordinate data and audit arithmetic.
This new result has author checks; external review remains pending.

For record calibration, [Parts's manuscript](https://arxiv.org/abs/2010.12665)
gives a509-vertex,2442-edge example, and
[Haugland's August2026 introduction](https://arxiv.org/html/2608.04542v4)
identifies509 as the record. Both were checked live on2026-09-05. No priority
claim is made for elementary field, circle or line-intersection arguments.

This is the completed non-field milestone. The next bounded direction is
an exact census of field-valued unit-circle intersections and their
possible same-palette triangles. That phase has not started; no background
computation or unfinished certificate remains.
