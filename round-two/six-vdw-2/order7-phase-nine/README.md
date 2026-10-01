# A 9..35 antipodal phase band for H7 templates over F617

**six-vdw-2, researcher.** The [proof](PROOF.md) excludes phase weights
8 and 36 for every H7-invariant, monochromatic-seven-AP-free coloring of
the punctured field F617. Together with the cited previous endpoint
exclusion, this advances the nonconstant/nonquadratic phase band from
8..36 to **9..35**, with antipodal equality and disagreement sets both
in **126..490**. It does not establish an interval-3704 witness or a
global bound for W(2,7).

The new argument needs eighteen exact refutations: two fixed equality
profiles, two maximum-majority-seven cases, twelve nonadjacent following
minorities, and two final forced profiles. The latter reduction uses the
directed rule that every gap of six must be followed by a zero gap.
All color orientations are retained. [PROOF.md](PROOF.md) states the
coverage argument and every mathematical input.

## Reproduce from source

Use a checkout containing this directory and its four sibling dependency
directories. [SOURCE_PINS.json](SOURCE_PINS.json) pins thirteen required
files before executing imported helpers. Python 3.11.2,
python-sat 1.8.dev24, six 1.17.0, CaDiCaL195 and a C compiler were used.
No solver or converter is a trusted proof checker.

```bash
python3 -m venv /tmp/vdw-phase9-env
/tmp/vdw-phase9-env/bin/pip install python-sat==1.8.dev24 six==1.17.0
mkdir -p /tmp/vdw-phase9-tools
curl -fL https://raw.githubusercontent.com/marijnheule/drat-trim/2e3b2dc0ecf938addbd779d42877b6ed69d9a985/drat-trim.c -o /tmp/vdw-phase9-tools/drat-trim.c
cc -O2 /tmp/vdw-phase9-tools/drat-trim.c -o /tmp/vdw-phase9-tools/drat-trim
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /tmp/vdw-phase9-env/bin/python round-two/six-vdw-2/order7-phase-nine/reproduce.py --work /tmp/vdw-phase9-proof --converter /tmp/vdw-phase9-tools/drat-trim
/tmp/vdw-phase9-env/bin/python round-two/six-vdw-2/order7-phase-nine/guards.py --checked-work /tmp/vdw-phase9-proof --work /tmp/vdw-phase9-damage
```

Use fresh work directories. Every stage is serial with threads fixed to
one: native proposals have 50000 conflicts and a 30-second external
guard; conversion has a 25-second internal and 30-second external guard;
each strict proof check has 30 seconds; each complete definition audit
has 55 seconds. UNKNOWN, timeout or interruption gives no mathematical
exclusion. `--resume` replays already checked positive certificates and
refuses identical bounded failures. An interrupted unchecked native
stage needs explicit diagnosis.

The expected final status is `EXACT_H7_PHASE_ENDPOINTS_8_36_EXCLUDED`,
with eighteen exact refutations, phase band `[9,35]`, 187010 checked
additions and 3062858 propagation hints per proof replay. Both normal
and `-O` checks must agree. [EXPECTED.csv](EXPECTED.csv) contains the
canonical model hashes and reference proof bytes/counts. A different
valid proof need not have the same proof hash or size.

`--certificate-cache PATH` is optional: cached CNF and LRAT bytes must
match the canonical fixture, and both strict checkers actually replay
each candidate proof. A cache flag or stored solver status is never
accepted as a proof. Large generated corpora are deliberately omitted;
the default command proposes fresh proofs from the published source.

[VALIDATION.md](VALIDATION.md) records the completed source replay and
negative controls. This is same-author checking by different algorithms,
with no independent-review verdict or proof-assistant formalization.
