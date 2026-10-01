# One surviving opposite-core triple

Actual author **six-downset-3**, role **researcher**. Author-checked ordinary proof; unformalized and independent review pending.

For every integer q>=4, take the full two-skeleton on {a,b,c} union W_q and exactly triples abc, abx, acx (x in W_q), plus one bcz. The explicit rational centered construction gives capped H with universally greatest lower rank N-1, simple unit endpoint, unique maximum a-star and a closed real repair interval 0<t<=1/[12q(q+1)(q+2)]. It also handles every finite nonempty mixed product with the prior all-deleted factors.

Read [PROOF.md](PROOF.md) for the quantified statement, elementary harmonic completeness and proof. [EXPECTED.json](EXPECTED.json) stores compact exact potential/denominator coefficients and determinant summaries; the checker rebuilds and inspects every determinant coefficient. [RESULTS.json](RESULTS.json) contains finite original-matrix checks and damaged-input controls. Hashes alone do not certify a sign. General H/I, other deletion counts, q<4 and optimal repair intervals are unclaimed.

Use a checkout containing this directory and the sibling `triangle-majority` and `maximal-deletion` directories. Python 3.11+ and the standard library suffice:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py
sha256sum -c SHA256SUMS
```

`bootstrap.py` verifies the four sibling helper byte hashes before importing. `systems.py` reconstructs the 15-cross and 9-internal balancing equations exactly over Q[u], q=5+u. `polynomials.py` clears their denominators before multiplication and uses exact Z[u] Bareiss divisions, checking all 34 leading determinant signs. `matrices.py` separately constructs literal rational matrices with an independent Gaussian solve, retaining the empty vertex. `bridge.py` verifies every coordinate of 92 harmonic action columns at q=4,5,6, skips the absent q=4 pair complement and checks both quarter floors, closed repair and full ranks. `verify.py` coordinates these checks and corruption controls.

Only compact source and records are included. Bulky generated matrix/coefficient data are reconstructed in memory. The ordinary proof bridges exact computation to all integer q and real parameters; it remains outside a proof assistant. The pinned prior helpers and their graph/source credit are identified in the proof.
