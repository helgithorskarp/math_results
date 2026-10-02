# Polyhex strips: no identity-U5 contact survives E2

Actual author: **six-heesch-2**, role **researcher**. Exact computer-assisted
local lemma, unformalized and independently unreviewed.

For literal T_k, every integer k>=6 and every integer b, the registered
relative pose (I;5,b) is outside E2. The proof reduces the complete raw
domain to two endpoints using an isolated-cell obstruction, then excludes
both endpoints. It uses full source-height inventories and a20-node
search-free rejection DAG. The complete all-k E2-subset-A2 statement and
the finite-five Heesch target remain open. This is not a corona construction
or a new Heesch-number value.

From a repository checkout, with Python3.11+ and only the standard library:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 round-two/six-heesch-2/strip-e2-side5-exclusion/verify.py
```

The verifier runs six serial jobs: the raw/sealed-cell/angled-contact and
upper-endpoint proofs, lower-endpoint producer, and search-free lower reader,
each normally and with `-O`. Their literal evidence hashes must match
[expected.json](expected.json). The core rejects five damaged controls;
the collar reader rejects six. The separate axial audit checks every exact
parameter representative6..11 and a supplementary far-tail case40.

The source tree includes thirteen byte-pinned published dependencies:
exact affine/column kernels, the separate interval sweep and unit-edge axial
module, the prior cap-tree producer/reader, and three earlier E1-cut inputs.
These are relative paths in the same repository, so this directory alone
is not a complete checkout. No solver, private search inventory, network
request, large proof corpus, or downloaded certificate is needed.

Each worker keeps single solver/BLAS/OpenMP thread settings,43s work,
45s signal,47s parent and100000-operation guards. A guard raises an error
and never proves nonexistence. `generated/` contains local evidence only
and is ignored. The guards also respect any operations-owned campaign
pause files when running in the original campaign environment.

[proof.md](proof.md) gives the literal family, complete finite reductions,
prior-premise citations and remaining global gap. Shared kernels and
same-author normal/optimized and damage checks are a disclosed trust
boundary; they do not constitute independent review.
