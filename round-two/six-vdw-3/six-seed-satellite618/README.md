# Matched six-seed satellite growth, XOR618/F103

six-vdw-3, researcher. [PROOF.md](PROOF.md) states and proves the conditional
lemma: with holes `{6,54,102}`, a monochromatic orientation seed `0..5`
forces at least three opposite regular satellites in `{7,52,53,55,56,101}`.
The mathematical input is published9311/sourceb18c33b5. One genuinely new
fixed twelve-point model, retaining88 free orientations, is strictly refuted.
No3704 coloring or improved symmetric two-color/seven-term W bound follows.

The standalone pipeline needs Python3.11.2, a C compiler, internet access to
the pinned public sources, and these dependencies. Run from this directory:

```sh
python3.11 -m venv build/venv
build/venv/bin/pip install python-sat==1.8.dev24 six==1.17.0
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 build/venv/bin/python reproduce.py --work build/reproduce
```

The author validation used Python3.11.2 and CaDiCaL195. `reproduce.py`
byte-pins the frozen [expected.json](expected.json), downloads credited
common-base audit/proposal/proof-control sources, the explicit written
mathematical input, positive-RUP checker and untrusted converter. It builds
all artifacts under `--work` and runs serially. Normal and optimized child
processes reconstruct the entire sparse-input cover and audit the production
model, complete small signed-word controls and damaged source records.
A fresh100000-conflict/35-second proposal is converted at25 seconds internal/
30 external and replayed strictly under a50-second guard per child stage.
An incomplete proposal aborts without an exclusion or automatic retry.

Expected final status `CONDITIONAL_THIRD_SATELLITE_LEMMA_AUTHOR_CHECKED`;
381306 actual cyclic pairs audited per mode; model4950 variables/27887
clauses;37908 checked additions/983868 hints per mode;34 necessary satellite
inputs and19 reflection classes. These are necessary input counts.

If an LRAT candidate already exists privately, use `--resume PATH.lrat`.
It remains untrusted: the source reconstructs coverage/models and replays
both strict proof modes. No bulky candidate is supplied in Git. Use `--tools
DIR` to reuse already downloaded helpers; every imported source is still
checked against its exact byte pin. Do not reuse prior UNKNOWN instances or
reinterpret a stopped proposal as mathematical nonexistence.

[VALIDATION.md](VALIDATION.md) and [verification.json](verification.json)
record the author's completed fresh standalone reconstruction. Exact
CNF/DRAT/LRAT hashes and source provenance are in expected.json. The cited
9311 theorem and ordinary mathematical bridges are not formalized or
reproved by this pipeline; external independent review is not claimed.
