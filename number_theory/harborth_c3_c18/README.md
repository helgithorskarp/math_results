**g(C3 ⊕ C18)=21.** Every 21-element subset of (Z/3Z) ⊕ (Z/18Z)
contains 18 distinct elements summing to zero. A 20-element obstruction
shows that the value is sharp. The upper bound is an exact
computer-assisted result, new to the primary sources searched on
11 September 2026; the lower construction is prior work.

The [proof](proof.md) reduces every possible total sum to one of three
representatives, with no anchor assumptions. Each representative gives an
exact CNF whose refutation was independently checked by DRAT-trim.
The generator and semantic audits use Python 3.11+ and its standard
library; the recorded full replay used Linux.
[Literature and priority limits](literature.md).

Run the definition-level lower-bound check and the semantic controls:

```bash
python3 check_witness.py
python3 audit.py
```

For the complete proof replay, provide Kissat and DRAT-trim executables:

```bash
python3 reproduce.py --kissat /path/to/kissat --drat-trim /path/to/drat-trim --work /tmp/harborth-c3-c18
```

The command regenerates all three CNFs, checks their hashes, produces and
independently verifies three refutations, and writes `verified.json` with
status `VERIFIED_g_C3_C18_EQUALS_21`. A timeout, UNKNOWN result, failed
certificate or semantic mismatch is an error. The recorded proof traces
total 88,289,188 bytes; keep generated evidence outside the repository.
Other solver versions may produce different valid proofs, which are
accepted only after checking. See [reproducibility.json](reproducibility.json)
for the clean replay's timings, memory and tool hashes.

The recorded tool sources and build commands are:

```bash
git clone --branch rel-4.0.4 --depth 1 https://github.com/arminbiere/kissat
cd kissat
./configure --quiet
make -j2
```

The Kissat tag resolves to `8af8e56f174b778aef3aa45af9f739b2a5f492c2`.
For the checker, in a separate tools directory:

```bash
git clone https://github.com/marijnheule/drat-trim
cd drat-trim
git checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
gcc -O2 drat-trim.c -o drat-trim
```

The package includes:

- `encode.py`: full membership, cardinality, residue and triple constraints.
- `audit.py`: all 54 affine normalizers, all small-case primary assignments,
  an independent production triple-list derivation and rejection controls.
- `check_witness.py` and `witness20.json`: direct checking of all 190
  possible 18-element subsets of the lower-bound example.
- `expected.json`: exact CNF hashes, recorded proof hashes, sizes and
  complete expected semantic-audit output.
- `reproduce.py`: the full generation, solving and checking entry point.

The trust boundary includes the written reduction, Python generator,
DRAT-trim implementation and execution environment. The result is not a
proof-assistant formalization or independent peer review. Solver status
alone is not the upper-bound certificate.
