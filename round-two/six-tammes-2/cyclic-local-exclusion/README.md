# Cyclic Tammes-15 certificate and 26-near-contact exclusion

Authoring agent: **six-tammes-2**, role: **researcher**. Date: 2026-10-01.

For the known cyclic packing, exact positive contact weights and a rational
inverse certificate give a local exclusion radius of **1/400000** in Euclidean
distance after fixing rotations. This closes the cyclic branch in the preceding
fourteen-point completion theorem. A fifteen-point code with maximum inner
product below the incumbent root cannot contain the specified **26 near-contacts
at tolerance 1/10^16**. At equality only the two known incumbents remain, up to
orthogonal transformations and the specified relabeling.

The theorem is conditional on that labeled graph occurring. Global Tammes-15
optimality and unconditional best bounds are unchanged. The packing and
rigidity are prior mathematics; the explicit certificate, quantitative local
inequality, and completed robust 26-contact exclusion are the contribution.
See [PROOF.md](PROOF.md) for the precise graph, hypotheses, proof, and primary
literature. Proof status: author checked; arithmetic audited by a second
implementation by the same researcher; independent team review pending.

From the repository root, Python 3.11 or later needs only the standard library:

```bash
python3 -B round-two/six-tammes-2/cyclic-local-exclusion/check.py --selftest
python3 -B round-two/six-tammes-2/cyclic-local-exclusion/audit.py
python3 -B round-two/six-tammes-2/cyclic-local-exclusion/controls.py
python3 -B round-two/six-tammes-2/cyclic-local-exclusion/replay.py
```

`replay.py` verifies pinned preceding source files, reruns the earlier complete
completion and stability calculations and the asymmetric local certificate,
and checks all 225 Gram entries of the cyclic relabeling. It expects the
preceding published directories in a full repository checkout. For a sparse
checkout with original prerequisite directories saved under `scratch`, pass
`--prerequisite-root scratch`; the two round-two directories still default to
their repository locations. The expected summaries are in the `*EXPECTED.json`
files. The proof has not been formalized in a proof assistant.

Regenerate a valid certificate without third-party packages:

```bash
python3 -B round-two/six-tammes-2/cyclic-local-exclusion/generate.py --output scratch/cyclic-rebuilt.json
python3 -B round-two/six-tammes-2/cyclic-local-exclusion/check.py --certificate scratch/cyclic-rebuilt.json
```

The generator solves the invariant equilibrium system exactly in
`Q[t]/(F)`. Ordinary floating-point row selection and matrix inversion only
propose a rational inverse. The exact checker must accept every regenerated
artifact. Equivalent row choices or inverse numerators can vary by platform.
All jobs run sequentially on one CPU; no solver, BLAS library, or resource
escalation is needed. Verification is under 2 GiB.

`check.py` adapts the previously published asymmetric checker; `audit.py`
imports neither it nor the generator, uses unreduced polynomial products, and
encloses `I-AR` directly with rational centered Taylor bounds. This separation
is a check on arithmetic and data, not a claim of independent peer review.
`INPUTS.json` pins the two dependencies by source commit, graph reference, and
file hashes. `SHA256SUMS` covers all compact source and certificate files.
