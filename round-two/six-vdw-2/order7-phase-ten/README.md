# A 10..34 phase band for H7 templates over F617

**six-vdw-2, researcher.** The [proof](PROOF.md) excludes phase weights
9 and 35 for every H7-invariant, seven-AP-free coloring of the punctured
field F617. Combined with the explicit previous band, admissible
nonconstant/nonquadratic templates now have phase weight **10..34**, with
antipodal equality and disagreement sets each in **140..476**.
The interval-3704 witness and unrestricted W(2,7) remain open.

Twenty-four exact refutations establish a complete reduction: minimum
minority distance at most two, maximum majority run five or six,
fourteen branches excluding six, and four branches forcing every
gap of five to have a successor at most three. Disjoint pairing and
the small-gap condition then contradict the required gap sum35.
All color orientations and both phase backgrounds are covered.

## Reproduction

Use a checkout containing this directory and its pinned sibling
dependencies. Fifteen helper/proof files are checked before imported
helpers execute. Python 3.11.2, python-sat 1.8.dev24, six 1.17.0,
CaDiCaL195 and a C compiler were used.

```bash
python3 -m venv /tmp/vdw-phase10-env
/tmp/vdw-phase10-env/bin/pip install python-sat==1.8.dev24 six==1.17.0
mkdir -p /tmp/vdw-phase10-tools
curl -fL https://raw.githubusercontent.com/marijnheule/drat-trim/2e3b2dc0ecf938addbd779d42877b6ed69d9a985/drat-trim.c -o /tmp/vdw-phase10-tools/drat-trim.c
cc -O2 /tmp/vdw-phase10-tools/drat-trim.c -o /tmp/vdw-phase10-tools/drat-trim
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /tmp/vdw-phase10-env/bin/python round-two/six-vdw-2/order7-phase-ten/reproduce.py --work /tmp/vdw-phase10-proof --converter /tmp/vdw-phase10-tools/drat-trim
/tmp/vdw-phase10-env/bin/python round-two/six-vdw-2/order7-phase-ten/guards.py --checked-work /tmp/vdw-phase10-proof --work /tmp/vdw-phase10-damage
```

Use fresh work directories. Stages are serial and all solver/BLAS/OpenMP
threads are fixed to one. Native proposals have 50000 conflicts and a
30-second external guard; conversion has 25 seconds internally and 30
externally; strict checks have 30 seconds each and definition audits 55.
UNKNOWN, timeout or interruption excludes no mathematical case.
`--resume` replays checked positive proofs and refuses identical bounded
failures; an interrupted unchecked native stage needs diagnosis.

Expected final status: `EXACT_H7_PHASE_ENDPOINTS_9_35_EXCLUDED`, with
24 exact cases, phase band `[10,34]`, 400568 additions and 6672402
propagation hints per proof replay. Both Python modes must agree.
[EXPECTED.csv](EXPECTED.csv) records canonical model digests and
reference proof digests/counts. A different valid proof can have
different bytes or size.

An optional `--certificate-cache PATH` accepts only matching candidate
CNF/LRAT bytes and actually replays every proof through both strict
checkers. Cached acceptance flags, native UNSAT and converter acceptance
are not proof authorities. The default command proposes fresh proofs.
Large generated corpora are omitted from Git.

[VALIDATION.md](VALIDATION.md) gives the completed source replay and
meaningful damage controls. Generation and literal definition auditing
use separate author algorithms; independent review and formalization
are unclaimed. [SOURCE_PINS.json](SOURCE_PINS.json) and
[SHA256SUMS](SHA256SUMS) record exact source provenance.
