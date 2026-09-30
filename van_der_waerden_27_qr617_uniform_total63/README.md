Actual author: **six-vdw-2**. Role: **researcher**.

Any binary seven-AP-free coloring on coordinates0..3703 has neither
ORIGINAL aligned-QR617 edit box30/32 nor32/30, at either actual endpoint
color. The new boxes are independently proved. With the two explicit
published numerical premises, the total edit count satisfies
**63<=a+b<=3633** at both endpoint colors.

Here q=0 on nonzero squares modulo617, q=1 on nonsquares. Counts a,b are
on the two original reference classes on0..3702 minus multiples617,
each of size1848. Seven old poles and the actual endpoint are free and
uncounted. No candidate symmetry or periodicity is assumed. Translation
by1 gives[1,3704]. This is a necessary distance constraint; no coloring
witness, exact W value or unrestricted exclusion is supplied.

Read [the written proof](PROOF.md). Reproduce from the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 van_der_waerden_27_qr617_uniform_total63/reproduce.py --output-dir /tmp/qr617-uniform63
```

Python3.11.2 and standard library only. Use a fresh output directory.
Expected `UNIFORM63_CERTIFICATES_AND_CONTROLS_PASSED`:24 root cases,
36 nodes,2 splits,34 closed leaves,24 parent-state regressions,
76 rejected corruption controls. Normal and optimized Python agree.
All computation is serial, one thread, with90s per generation primitive
and90s per validation process. Generated proofs total16,772,267 bytes
and stay outside Git. No saved private proof is an input.

`generate.py` reuses the unchanged pure mixed-clause generator and
reconstructs the two full checker-derived root1 disjunctions.
`verify.py` independently derives all covers and replays every child.
`checker_controls.py` compares full parent states between strict and
generic checking and rejects malformed coverage, metadata, states and
terminals. The implementations share this author; no external review
or formalization is claimed. [Expected manifests/results](expected.json),
[provenance](provenance.json) and [measured evidence](evidence.json) record
the precise dependencies and trust boundary.

For a saved valid reproduction, add `--resume`; closed cases are
replayed and original generation timings remain unchanged. A STARTED
attempt, timeout or open attempted child is preserved and never
silently retried. Incomplete output establishes no exclusion.

The separate numerical premises are [uniform class lower30](../van_der_waerden_27_qr617_nonsquare30_endpoint1/PROOF.md)
and [both-endpoint balanced31/31 exclusion](../van_der_waerden_27_qr617_max32_endpoint0/PROOF.md)
with its explicit [endpoint1 parent](../van_der_waerden_27_qr617_max32_endpoint1/PROOF.md).
Their proof computations are not rerun by this command and their bounds
are not branch assumptions. Both total63 and its complement boundary
remain unresolved; this artifact isolates the next finite frontier.
