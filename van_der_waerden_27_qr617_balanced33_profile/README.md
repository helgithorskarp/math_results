# QR617 repair profile: balanced33 and an asymmetric boundary cut

**six-vdw-2, researcher**, 2026-10-01. This exact computer-assisted lemma
constrains arbitrary binary seven-AP-free colorings of `[0,3703]` relative
to one fixed quadratic-residue reference. Translation by one gives `[1,3704]`.

Let `D={x in [0,3702]:617 does not divide x}`. On `D`, let `q(x)=0` for
nonzero squares modulo617 and `q(x)=1` for nonsquares. For an actual
coloring `c`, put `a=#{x in D:q(x)=0,c(x)!=q(x)}`,
`b=#{x in D:q(x)=1,c(x)!=q(x)}`, and `e=c(3703)`.
Each original class has1848 positions. The seven old multiples of617 and
the endpoint are free and uncounted. No symmetry or periodicity of `c`
is required, and the original classes are not interchanged.

The complete new exclusions are:

| Endpoint `e` | Excluded original-class cap box |
| --- | --- |
| 0 | `a<=32 and b<=32` |
| 1 | `a<=32 and b<=32` |
| 0 | `a<=31 and b<=33` |

These three exclusions use no prior numerical repair bound. They give
`max(a,b)>=33` at either endpoint, and `a>=32 or b>=34` at endpoint0.
Whole-color complementation maps `(e,a,b)` to `(1-e,1848-a,1848-b)`;
therefore `min(a,b)<=1815` at either endpoint, and
`a<=1816 or b<=1814` at endpoint1.

With the separately cited [uniform64 profile](../van_der_waerden_27_qr617_uniform_total64/PROOF.md),
`30<=a,b<=1818` and `64<=a+b<=3632` remain valid. At total64 the
necessary pairs left after these cuts are:

| Endpoint | Remaining total64 pairs |
| --- | --- |
| 0 | `(30,34), (33,31), (34,30)` |
| 1 | `(30,34), (31,33), (33,31), (34,30)` |

These are necessary boundary possibilities; their attainability is unresolved.
The total lower bound remains64. No length3704 AP-free witness,
new van der Waerden lower bound, or global nonexistence conclusion is supplied.

The [proof](PROOF.md) specifies all18 covering root cases, all17 children,
and the exact implication/packing induction. [expected.json](expected.json)
contains the canonical forest hashes and full compact checking outputs.
[provenance.json](provenance.json) pins every imported source file.
[DEPENDENCIES.md](DEPENDENCIES.md) separates computational and numerical inputs.
[VALIDATION.md](VALIDATION.md) records the fresh public-source audit.

## Reproduction

Use Python3.11 or later on a Unix-like system (tested Linux), with a
clone of the whole repository; only the standard library is needed. From the repository root:

```bash
python3 van_der_waerden_27_qr617_balanced33_profile/reproduce.py \
  --output-dir /tmp/qr617-balanced33-reproduction
```

Choose a new output directory outside the repository. The command runs
35 generation primitives and86 audit partitions serially, with90seconds
per child and all thread settings at1. It requires exactly18 complete
forests with their expected bytes,18 full strict/generic parent-state
comparisons,210 meaningful rejected corruption controls per mode, and43
byte-identical normal/optimized partition pairs. Its successful status is
`BALANCED33_THREE_BOX_FULL_REPRODUCTION_PASSED`.

The regenerated proof corpus is16,729,372 bytes and stays outside Git.
No private transcript, solver, incumbent coloring or hidden data is an input.
To check saved completed work after an interruption:

```bash
python3 van_der_waerden_27_qr617_balanced33_profile/reproduce.py \
  --output-dir /tmp/qr617-balanced33-reproduction --resume
```

Resume revalidates source pins, file coverage, canonical bytes and audit
outputs. It skips only saved jobs that completed with exit0; it refuses
failed, timed-out or interrupted jobs rather than retrying them. Such a
failure provides no mathematical exclusion. The generator and exact
checker use different representations but share an author; no external
review or proof-assistant verification is claimed.
