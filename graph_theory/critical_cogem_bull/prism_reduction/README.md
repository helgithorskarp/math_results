# A prism reduction for critical co-gem/bull-free graphs

Every connected **(gem,bull)-free graph containing a triangular prism is
perfect**. Consequently, every vertex-critical **(co-gem,bull)-free graph
is C6-free**, for all chromatic numbers and all orders.

The proof uses a reusable operation: replacing any triangle by a vertex
adjacent to its outside majority neighbors preserves (gem,bull)-freeness.
A 2,560-case certificate proves this local rule; 127 further local cases
give the prism facts. An ordinary odd-cycle parity argument then applies
at every order. See [the proof](proof.md) and [literature audit](literature.md).

The accepted critical-class equality with `(P3+P1)`-free graphs remains
unresolved. This result excludes the complete `C6`-containing part of the
remaining candidates; it is not a bounded graph census.

## Reproduction

Tested with CPython 3.11.2; Python 3.11+ and the standard library suffice.
From this directory:

```sh
python3 check.py
python3 generate.py > /tmp/prism-majority-certificate.json
cmp certificate.json /tmp/prism-majority-certificate.json
python3 check.py /tmp/prism-majority-certificate.json > /tmp/prism-majority-result.json
cmp expected.json /tmp/prism-majority-result.json
sha256sum -c SHA256SUMS
```

The checker reports `PASS`, verifies 2,666 individual forbidden witnesses
and all 21 allowed prism neighborhoods, and rejects a deliberately false
certificate. The certificate SHA-256 is
`781d4bbbfc3f947c2a2b69ef4dd07ac749f04710194982e5df047744150adf88`.
Generation plus checking takes less than a second in the recorded environment.

`generate.py` uses integer graph encodings and permutation recognition.
`check.py` imports no generator code and instead uses adjacency matrices and
definition-level recognition. This supplies implementation independence,
not independent authorship or external review. The unbounded reduction and
the application of the Strong Perfect Graph Theorem remain written proofs.
Private SAT experiments were discovery aids and are not proof dependencies.

No old proof or replay is replaced. This directory extends the
[earlier critical amplification result](../README.md).
