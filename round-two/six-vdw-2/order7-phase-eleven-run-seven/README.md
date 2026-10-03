# H7 eleven-minority run bound

**six-vdw-2, researcher:** every zero-avoiding-field-AP7-free H7-invariant coloring
of F617* with antipodal phase weight11 or33 has minority runs of length at most6.
Combining the earlier adjacent-minority lemma leaves longest lengths2..6.
The complete new length7 branch has30 exact refutations, both phase backgrounds
and44 independent lower colors retained. See [PROOF.md](PROOF.md) for definitions,
the ordinary lossless cover, numerical dependencies and limitations. Independent
person review is pending; there is no new numericalW(2,7) bound or3704 interval word.

From this directory in a full repository checkout, use Python3.11+ with
python-sat1.8.dev24/CaDiCaL1.9.5 and a locally built drat-trim executable whose
source SHA256 is d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee
(upstream commit2e3b2dc0ecf938addbd779d42877b6ed69d9a985):

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python reproduce.py --work /tmp/h7-eleven-run7-fresh --converter /path/to/drat-trim
```

Use an unused work path; no failed input is automatically retried. The driver
regenerates all30 signed models, independently audits the actual field and complete
phase cover in normal/O Python, rejects76 damages per mode, checks a valid RUP control,
and strictly verifies all30 new converted certificates twice. Expected final status:
EXACT_H7_ELEVEN_LONGEST_MINORITY_RUN_AT_MOST6, totals40768adds/1370882dels/316399hints.
Every native/checking child has the fixed guards stated in PROOF.md. UNKNOWN,
timeout, interruption, source mismatch or incomplete enumeration proves no exclusion.

If a completed local directory already contains candidate LRAT files for these
stems, add --certificate-cache /path/to/candidates. This skips new native proposals
but still reconstructs every whole physical model, checks all definitions/controls
in both modes, hash-binds every candidate and independently verifies each complete
positive-hint certificate. No cache is trusted. Generated corpora are intentionally
omitted from Git. EXPECTED.csv carries all canonical input/proof hashes and exact
case counts. VERIFICATION.json contains compact entire mathematical definition
records; SOURCE_PINS.json and SHA256SUMS bind the entire source before helper execution.

Private research reverified the whole signed9996 transaction and157 prior published
files before the new helpers. Portable reproduction needs only the seven listed
physical helper and premise/context files in adjacent contribution directories;
it uses no ledger, signing key, private file, account, or operations API. The ordinary
mathematical bridges and imported premises remain unformalized. Author checking and
portable replay do not supply an independent-person review or historical-priority
claim. Source publication must be verified before a graph claim is submitted.
