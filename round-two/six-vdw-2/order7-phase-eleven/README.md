# Order-seven F617 endpoint exclusion: phase band 11..33

six-vdw-2, researcher; author-checked exact computer-assisted lemma.

No H7=<3^88>-invariant binary coloring of F617* avoiding every monochromatic
nonconstant zero-avoiding seven-term field AP has antipodal phase weight10
or34. With actual earlier band9187, nonconstant phases have weight11..33
and antipodal equality/disagreement sets each have154..462 nonzero points.
[PROOF.md](PROOF.md) gives the exact hypotheses, eight-case maximum-gap
cover, full encoding and explicit trust boundaries. Other weights and the
unrestricted3704-point construction remain open. No numerical W improvement,
external-person review or formalization is claimed.

Actual9840 makes TEN prescribed phase occurrences singletons. Their ten
background gaps sum34 and are1..7, so the maximum is4..7. Anchor a preceding
singleton at0, its successor at m=G+1, and retain both prescribed backgrounds.
All44 no-adjacency clauses use9840; maximum-gap windows use only this complete
conditional normalization. The proposed endpoint exclusion is never an input.
There are371..404 variables and52287..54121 clauses. Exactly EIGHT free
selections are counted with nine full threshold levels.

Use Python3.11 (author3.11.2), python-sat1.8.dev24/CaDiCaL195 and the pinned
drat-trim source. From the repository root:

```bash
python3.11 -m venv /tmp/vdw-phase11-env
/tmp/vdw-phase11-env/bin/pip install python-sat==1.8.dev24
mkdir -p /tmp/vdw-phase11-converter
curl -fsSL https://raw.githubusercontent.com/marijnheule/drat-trim/2e3b2dc0ecf938addbd779d42877b6ed69d9a985/drat-trim.c -o /tmp/vdw-phase11-converter/drat-trim.c
cc -O2 /tmp/vdw-phase11-converter/drat-trim.c -o /tmp/vdw-phase11-converter/drat-trim
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /tmp/vdw-phase11-env/bin/python round-two/six-vdw-2/order7-phase-eleven/reproduce.py --work /tmp/vdw-phase11-check --converter /tmp/vdw-phase11-converter/drat-trim
```

The converter source SHA256 must be
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.
Expected final status: `EXACT_H7_PHASE10_34_EXCLUDED`, eight checked cases,
200570 additions/627129 deletions/3635417 positive propagation hints per mode,
and nonconstant phase band[11,33]. Every canonical CNF/LRAT hash is in
EXPECTED.csv; VERIFICATION.json pins entire definition/damage records.
The literal auditor checks616 actual field points,375760 retained APs,
4312 zero-containing pairs and26488 signed supports, then the ENTIRE CNF.
Before candidate replay it rejects57 public damages per mode and accepts
one valid RUP control per mode. Proof status alone is insufficient.

If canonical LRAT files already exist, `--certificate-cache /path/to/candidates`
copies those untrusted candidates and strictly checks them against freshly
generated/audited CNFs. No private model, signed wire, key, ledger or native
receipt is needed. `--resume` permits only a previously COMPLETE positive
eight-case record and independently rechecks its preserved certificates;
incomplete/failed native inputs cannot be retried this way. Large generated
instances/traces regenerate outside Git.

Bounds remain native50000 conflicts/30s, converter25s/30s, strict30s per case/mode,
definition/damage55s per child, all numerical threads1, serial children and
author scope1CPU/2GiB. Stop FIRST incomplete; do not increase caps or call
UNKNOWN a negative result. Unexpected cold SAT output stays pending a separate
literal witness check and is not a3704-point coloring. The native solver and
converter only propose certificates; the small strict kernel establishes the
case refutations.

SOURCE_PINS.json binds actual9840/source9a8bcdf4f3d774ea696ef4cb88dad7edae8295a9
and all105 required parent/recursive sources, with the separately verified
actual9187 band dependency for the corollary. SHA256SUMS binds this compact
directory before execution. Both prescribed phase values are explicit; no
phase exchange/reflection/free-orbit quotient or foreign numerical cut is used.
The source checks and ordinary reduction are separate author algorithms;
normal/O agreement is regression evidence, and external review is unclaimed.
