# Uniform individual198 edit floor for QR617 reflection references

Actual author: **six-vdw-3**, role **researcher**. Complete author
computer-assisted combinatorial lemma; external independent review pending.

Every binary word of length3704 with no monochromatic nonconstant seven-term
integer arithmetic progression differs in **at least198 positions in each
original colour class** from **each of the617 QR617 reflection-seam references**
defined in [PROOF.md](PROOF.md). Each class also has at most1651 edits; phase1
has the stronger upper bound1650. Poles are free and uncounted. The candidate
word is arbitrary: reflection, balance and periodicity are not assumed.

The new step is phase611, formerly the sole individual197 phase. Two new
ordinary-AP integer packings close roots605 and3405 of the actual anchor
AP(45,560). Five historical root chains are completely replayed under only
the opposite class's197 cap. This proves phase611 individual198 without a
bound on the other class. The earlier other616-phase results are explicit
mathematical imports. The uniform total interval396..3302 is retained.
No length3704 colouring, new W(2,7) lower bound, exact value or attainment
claim is supplied.

From repository root, CPython3.11+ and its standard library suffice:

```bash
python3 van_der_waerden_617_uniform198_anchor611/reproduce.py --work /tmp/qr617-individual198-frozen
```

Expected exact status: `EXACT_QR617_UNIFORM_INDIVIDUAL198_ANCHOR611`.
Expected-result SHA256: `bb53393a1ce5fdaaa90a36b2215eba8dd46d6736118f5d280f4693d6909c2f0f`.

Optional fresh source-only numerical proposal and exact replay:

```bash
python3 -m venv /tmp/qr617-individual198-env
/tmp/qr617-individual198-env/bin/python -m pip install -r van_der_waerden_617_uniform198_anchor611/requirements.txt
/tmp/qr617-individual198-env/bin/python van_der_waerden_617_uniform198_anchor611/reproduce.py --fresh --work /tmp/qr617-individual198-fresh
```

Use a new work directory for each run; failed or incomplete work is preserved.
Fresh coefficient bytes need not equal the frozen bytes. The complete fresh
exact result must agree between normal and optimized Python and have the same
combined profile as the frozen proof.

[verify.py](verify.py) checks actual APs and integer capacities, importing
no numerical proposer. [generate.py](generate.py) constructs the two numerical
proposals; solver status is never mathematical evidence. [manifest.json](manifest.json)
requires every anchor root. [expected.json](expected.json) records all checked
stages. [VALIDATION.md](VALIDATION.md), [evidence.json](evidence.json) and
[DEPENDENCIES.md](DEPENDENCIES.md) specify measured checks, trust boundaries and
attributed imports. [provenance.json](provenance.json) pins the historical files;
[SHA256SUMS](SHA256SUMS) hashes every other public file.
