# Three-column robustness for F31 XOR C20 baselines

six-vdw-1, researcher, 2026-10-01.

For arbitrary binary f on F31 and g on Z20, and every set E of at most
three field residues, the baseline f(x mod31) XOR g(x mod20) has a
monochromatic nonconstant seven-term AP in [0,2479] avoiding E. Arbitrary,
even nonperiodic, changes on those three classes cannot repair the baseline
on3704 positions. The [proof](PROOF.md) includes the complete quantified
reduction and conditional period620 multiplicity/distance consequences.
No new W bound or general period620 exclusion is claimed.

Reproduction requires only Python3 and a C++17 compiler. The completed
fresh replay used Python3.11.2 and GCC12.2.0 on Linux; no solver or Python
package is required. From this directory:

```sh
sha256sum -c SHA256SUMS
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B reproduce.py --work /tmp/three-column-robust620-work
```

Choose a new work directory. The runner keeps child receipts, binary
outputs and generated evidence there; generated artifacts are omitted
from Git. It never rewrites the frozen expected.json. It runs one child
at a time, gives each35 seconds and sets numerical-library threads to1.
When DISCOVERY_RESEARCH_TEAM_ROOT is supplied, it checks campaign pause
and handover barriers before each child. A timeout or other incomplete
stage establishes no exclusion. See [validation](VALIDATION.md) for the
observed full replay, resource use and trust limits.

Expected final status:
`COMPLETE_AUTHOR_CHECKED_THREE_COLUMN_ROBUST620_LEMMA`,42 cases,
13285384 independently checked literal records,119568456 regenerated
record bytes, complete frozen evidence agreement. The completed replay
took162.896 seconds and453856 KiB peak child memory, including builds and
sanitizers. Full replay uses approximately0.3 GB of scratch disk.

The producer and native checker share no helpers. The checker proves
coverage from separate segment-path counts, literal membership, uniqueness
and every actual integer progression. Separate Python auditors verify the
full row and exceptional-triple partitions. Expected hashes aid regression;
they are not a substitute for these exact checks. Sanitizers and controls
are implementation checks, not peer review or formalization.

Files are deliberately compact. census.py/check_rows.py retain unchanged
row-reduction code credited to the earlier separable620 source, commit
933d56da9d6865fc7bf82d4e280f8eeeaaf0902e. They are rerun here, so copying
this directory suffices. orbits.py/check_orbits.py cover every exceptional
triple; enumerate.cpp/check.cpp cover every normalized regular assignment;
check_arithmetic.py audits the conditional edit arithmetic; reproduce.py
assembles the fresh source-only verification. Large generated corpora and
private operational receipts are not publication inputs.
