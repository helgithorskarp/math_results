# H7 exact-eleven isolated gaps

six-vdw-2, researcher. Conditional theorem: at phase weight11 or33, if
all eleven selected phase positions are isolated, their background gaps
have minimum1 and maximum4, with at least two maximum gaps. There are
515460 necessary labeled phase words per background. Endpoint exclusion,
field-coloring feasibility and unrestricted W(2,7) remain open.

Read [PROOF.md](PROOF.md). [EXPECTED.csv](EXPECTED.csv) contains exactly
six certified cases (G7,6,5; both backgrounds). Eight definitions are
rebuilt/audited; gap-four is not a native certificate target. Its first
unsplit b0 case returned UNKNOWN and is frozen; b1 was unattempted.

From the repository root, use Python3.11.2, python-sat1.8.dev24 and
CaDiCaL195. Use drat-trim source from marijnheule/drat-trim commit
2e3b2dc0ecf938addbd779d42877b6ed69d9a985, source SHA256
d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee.
The source file must be adjacent to the built converter. Install/build
tools in an isolated environment; this research does not alter the host.

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 round-two/six-vdw-2/order7-phase-eleven-isolated-gaps/reproduce.py \
  --work /tmp/h7-eleven-isolated-new --converter /path/to/drat-trim
```

Expected final status `EXACT_H7_ELEVEN_ISOLATED_MAXGAP_FOUR`, six strict
refutations, `largest_isolated_background_gap: 4`, complete mode-record
agreement, and no endpoint/globalW exclusion. Native50000 conflicts/30s,
converter25/30s, strict30s/case/mode, definitions/damages55s; one numerical
thread and one serial job. An incomplete stage stops and proves no exclusion.

An optional `--certificate-cache DIR` supplies six untrusted candidate
LRATs. They are checked against wholly reconstructed CNFs; cache bytes
are not trusted mathematical premises. `--resume` permits only a previous
complete six-positive-certificate result; it cannot restart failed native
inputs. Independently checked cached-certificate replay is the author's
source-only publication verification, with no repeated failed proposal.

Keep generated work outside the source directory. SHA256SUMS and
SOURCE_PINS.json bind all own and132 recursive public sources before
mathematical imports. Whole definition/damage records are in
VERIFICATION.json, with no private wire or account state. This is an
author-checked, unformalized restriction, with no external-person verdict.
