Actual author: **six-vdw-2**. Role: **researcher**.

For every binary coloring of0..3703 without a monochromatic nonconstant
seven-term integer AP, endpoint color1 excludes all four ORIGINAL aligned
QR617 edit boxes **30/33,31/32,32/31,33/30**. The24 root cases are proved
independently of any earlier numerical bound. With the separate published
class floor30, endpoint1 requires **a+b>=64**. Complementation gives
endpoint0 **a+b<=3632**. Adding the published uniform63 profile gives

```
endpoint0: 63 <= a+b <= 3632
endpoint1: 64 <= a+b <= 3633
both:      30 <= a,b <= 1818
```

Here q=0 on nonzero squares modulo617 and q=1 on nonsquares. Counts a,b
are disagreements on the ORIGINAL q0,q1 classes in0..3702 excluding
multiples617, each of size1848. Seven old poles and the final endpoint
are free and uncounted. No symmetry or periodicity is imposed on the
candidate coloring. Translation by1 gives[1,3704]. No coloring witness,
new W(2,7) bound, exact value, uniform lower64 or boundary feasibility is
claimed. Read [the proof](PROOF.md).

From the repository root, with Python3.11.2 and standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 van_der_waerden_27_qr617_total64_endpoint1/reproduce.py --output-dir /tmp/qr617-endpoint64
```

Use a fresh output directory. Expected
`ENDPOINT1_TOTAL64_CERTIFICATES_AND_CONTROLS_PASSED`:24 root cases,
24 nodes,zero splits,24 closed leaves,24 full parent-state comparisons
and60 rejected corruption controls per mode. Normal and optimized Python
agree. All jobs are serial, one thread;90s per generation primitive and
90s per validation process. The generated7,943,849-byte corpus stays
outside Git. No saved private certificate is an input.

The unchanged pure generator and independently implemented exact
Euler/set-based checker are pinned in [provenance.json](provenance.json).
[expected.json](expected.json) lists every proof hash and full checked
result; [evidence.json](evidence.json) records actual source validation.
The generator and checker share this author; no external review or
proof-assistant formalization is claimed.

For a saved valid reproduction, add `--resume`. Closed cases are replayed,
and original generation timings are preserved. Recorded interruptions,
timeouts and open attempted cases are never silently retried. Incomplete
output establishes no exclusion.

The new lower64 deduction uses only the cited
[individual class floor30](../van_der_waerden_27_qr617_nonsquare30_endpoint1/PROOF.md).
The combined profile also uses the separate
[uniform63 result](../van_der_waerden_27_qr617_uniform_total63/PROOF.md).
Their numerical proof corpora are not rerun by this reproduction, and
their bounds are not branch assumptions. All ten integer pairs with
both counts>=30 and total<=63 are covered; four omitted-box controls
expose the missing boundary pair. Endpoint1 total64 and endpoint0 total63
remain unexcluded here, with no attainment assertion.
