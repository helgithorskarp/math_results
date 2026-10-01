# Reproduce the Tammes-15 profile (0,6,0) exclusion

Author: **six-tammes-1**, role: **researcher**, 2026-10-01. The
[complete proof](PROOF.md) excludes this full count row under the complete,
connected degree3..5 contact-graph, simple strictly convex hemispherical
cellular T/Q, nine-Q and unique-three hypotheses, on open 1/2<c<3/5.
The finite cover produces two combinatorial maps; written angle inequalities
and exact rational certificates exclude both. Independent mathematical
review and formalization are pending. Global Tammes-15 numerical bounds
are unchanged.

Combined with the [preceding result](../tammes15_ordinary_five_four_one_exclusion/PROOF.md),
only single-three row (1,5,0) remains. The beta-restricted count cover has
24 profiles, 1/12/11 for r=1/2/3. These are necessary count profiles,
not realized packings or unrestricted optimizer coverage.

## Commands and dependencies

Use CPython 3.11.2 with its standard library. Keep the repository's sibling
directory layout. The only two imported dependencies are prior **public**
files from source b1a8438ea86ed00717e237dd001e1925700652ab, graph h8180:

| Imported public file | Required SHA256 |
|---|---|
| [original-face kernel](../tammes15_ordinary_five_four_one_exclusion/check.py) | 2d543e31857e3a64d31e9306617ac7fb3e20cd3f7605941f1d96c5306d579c86 |
| [separate audit primitives](../tammes15_ordinary_five_four_one_exclusion/audit.py) | f9d4ebbab1316f68e4dffdec8375ad158203c3cf2fd0627d90da68dee019eabb |

Both imports fail if the bytes differ. Neither dependency imports the
other, and this auditor never imports a production predicate, schema,
enumerator, face-forcing or canonicalization function. No private workspace,
external certificate, solver, floating-point sign decision or extra Python
package is required. The known N14 optimum is a credited mathematical
input to the written proof, rather than an imported finite certificate.

From this contribution directory:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -B check.py --export-partitions /tmp/tammes15-six-zero.json
python3 -B audit.py --production-partitions /tmp/tammes15-six-zero.json
python3 -B -O check.py --export-partitions /tmp/tammes15-six-zero.json
python3 -B -O audit.py --production-partitions /tmp/tammes15-six-zero.json
python3 -B audit.py
sha256sum -c SHA256SUMS
```

Each script checks its **whole compact expected summary** before printing.
The default audit regenerates the trace in a temporary directory by running
production sequentially. Export bulky traces outside the repository.

## Exact result and checks

Production: sixteen representative cases cover all sixty labelled roles
and U contact sets. The 328 covers visit 63,874 RGS nodes. Of 1,374 base
survivors, 1,278 reject by the proven early U-contact rule. Ninety-six
ordinary covers leave eighty closure roots. The 216 last-face covers
leave sixteen closed fifteen-point maps, eight occurrences of each of
two cell-isomorphism classes, with **zero open terminal patches**.
[MAPS.json](MAPS.json) contains their full small face/edge/rotation arrays.
Their F-U distances differ, two versus three; neither is a metric witness.

The separate audit checks 76,740 raw assignments and all 668 exhaustion
boundaries **entrywise**, every forced face and all sixty free-name
bijections. Explicit cell isomorphisms use 272 backtracking nodes altogether.
Both map complexes are positive controls; wrong F-three and sixteen-point
controls reject. A locally valid (2,1,2) strip prefix fails only the added
forced-strip condition. The auditor independently propagates the M1 Q
corner table. The producer evaluates a rational angle recurrence, while
the auditor uses projective matrix powers. Both recompute the M1 endpoint
branches and signs at c0=57/100, the M2 quarter-angle polynomial and the
N14 rational comparisons. Analytic necessity is supplied by the written
proof; these are same-author algorithmic checks, not independent peer review.

The deterministic 610,926-byte partition trace is regenerated,
not published:

    d2e3fce8710232895a11a5fd01490aa92e24ca73d5d45dbbc671833f3fe63d71

Its SHA256 and size are recorded in [EXPECTED.json](EXPECTED.json). The
separate [AUDIT_EXPECTED.json](AUDIT_EXPECTED.json) records complete audit
counts, controls, independent corner propagation and rational margins.
The auditor reconstructs the entire domain and does not treat a supplied
survivor list as an exhaustion certificate. Large partition traces,
isomorphism witnesses and exploratory outputs are deliberately omitted;
compact source regenerates the checks.

## Resources and trust boundary

All five public commands were run sequentially, with native threads one
and the existing one-CPU/two-GiB scope. Each completed under an unchanged
forty-five-second guard. Node/raw-assignment cap 200,000 per cover and
last-face forcing depth twelve are unchanged; reaching a cap raises
INCOMPLETE rather than an exclusion.

| Public command | Seconds |
|---|---:|
| Normal production | 7.879 |
| Optimized production | 7.969 |
| Normal supplied-trace audit | 10.826 |
| Optimized supplied-trace audit | 10.339 |
| Default audit, including sequential production | 18.694 |

Peak child RSS was 27,780 KiB. Normal and optimized
outputs agree with the complete fixtures. Geometric hypotheses, original
star forcing, role completeness, relabelling, necessity of pruning, angle
identities, analytic inequalities and the known N14 input remain written
and unformalized.

The initial unreduced sixty-case pilot timed out after 45.007 seconds and
32 cases; it supplied **no mathematical nonexistence verdict**. Exact
free-name relabelling, proven earlier strip/U constraints and the actual
fifteen-point bound reduced the mathematical cover. Resources were not
escalated. A floating-point fit or incomplete enumeration is not used as
an exclusion.

The next single-three frontier is the deficient-five row (1,5,0), with
three Ts and two Qs at F. Higher odd-degree branches, larger faces and
unrestricted numerical upper bounds remain open.
