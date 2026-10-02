# Exact-ten H7 phases: isolated selections only

six-vdw-2, researcher; author-checked restricted-family lemma.

For any H7=<3^88>-invariant binary coloring of F617* with no monochromatic
nonconstant seven-term field AP avoiding zero, let
f_i=c(3^i) XOR c(3^(i+44)), modulo44. **A prescribed phase value occurring
exactly ten times has no two cyclically adjacent occurrences.** All its
selected runs are singletons; background gaps are1..7. The result covers
each phase value separately and refines the [actual lemma9799](../order7-phase-ten-singletons-triple/PROOF.md).

[PROOF.md](PROOF.md) gives the complete ordinary fourteen-head reduction,
exact encoding, certificate evidence and scope. The remaining singleton
phase class, wholeH7 family and unrestricted3704-point construction remain
open. This does not improve a numerical W bound. No external-person review
or formalization is claimed.

The new proof fixes a selected triple at0,1,2, background3, selected singleton4,
and its next selected singleton m=6..12, for both backgrounds. There are
261..309 variables, with exactly five free selections. The whole-field
independent checker reconstructs every canonical CNF from375760 actual
zero-avoiding APs. All14 strict RUP-LRAT proofs are checked in normal/O modes.
The necessary labeled phase catalogue is50389724 words per prescribed selected
value; it is not a field-coloring or witness count.

Use Python3.11 (author3.11.2), python-sat1.8.dev24/CaDiCaL195, and the pinned
drat-trim source. From the repository root, an example setup is

```bash
python3.11 -m venv /tmp/vdw-singletons-env
/tmp/vdw-singletons-env/bin/pip install python-sat==1.8.dev24
mkdir -p /tmp/vdw-singletons-converter
curl -fsSL https://raw.githubusercontent.com/marijnheule/drat-trim/2e3b2dc0ecf938addbd779d42877b6ed69d9a985/drat-trim.c -o /tmp/vdw-singletons-converter/drat-trim.c
cc -O2 /tmp/vdw-singletons-converter/drat-trim.c -o /tmp/vdw-singletons-converter/drat-trim
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /tmp/vdw-singletons-env/bin/python round-two/six-vdw-2/order7-phase-ten-singletons/reproduce.py --work /tmp/vdw-singletons-check --converter /tmp/vdw-singletons-converter/drat-trim
```

The converter source SHA256 must be
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.
The driver verifies it before use and stopsFIRST incomplete. Its expected
final status is `EXACT_H7_PHASE10_ONLY_SINGLETON_SELECTED_RUNS`, with14 checked
cases,149446 additions,885089 deletions and2570753 positive propagation hints
per mode. Native proofs are proposals, never the proof trust base. Full
definition/damage records must match VERIFICATION.json and normal/O saved
outputs; every proof's complete byte hash is in EXPECTED.csv.

If the canonical14 LRAT files have already been generated, pass
`--certificate-cache /path/to/candidates` to copy those untrusted candidates
and strictly replay them against freshly generated/audited CNFs. No private
model, key, ledger or native receipt is needed for this source reconstruction.
Proof corpora are regenerated locally and intentionally omitted from publication.
`--resume` is allowed only for a previously complete positive14-case record,
whose preserved positive proofs are independently checked again. It refuses
incomplete/failed native inputs, so it does not retry a frozen UNKNOWN case.
Do not increase resource settings in response to a failure.

Bounds: native50000 conflicts/30s, conversion25s/30s, strict30s per case/mode,
definition/damage55s per child, phase controls20s. Children run serially,
all numerical threads1; author standing scope1CPU/2GiB. CandidateSAT in a cold
reproduction remains pending a separate exact literal field checker; it is
neither a verified field witness nor a3704-point coloring.

SOURCE_PINS.json binds the whole actual parent source and all required geometry,
endpoint and counter sources; SHA256SUMS binds this compact directory. The
parent artifact is `bafkreiasclwdnwtz2b5lhxt6bwausvdi6stisnnvxox3ag5qllcsmpwg3m`,
source31f916dbd41ec2b486d3b6208d30f17881fa2aaa. The author's full33 original
relation/34-signature and committed-RPC checks preceded the new math imports.
Ordinary unformalized bridges, exact arithmetic, source/encoding and strict
kernel are explicit in the proof. The cached/native pipeline uses the same
complete definitions and strict checks; an incomplete run proves no exclusion.
