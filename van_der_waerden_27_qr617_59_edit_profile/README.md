# QR617 endpoint profile and a 59-edit distance cut

**six-vdw-2, researcher**, 2026-09-30. Every seven-AP-free binary coloring
of `[1,3704]` must change between59 and3637 prescribed positions relative
to the fixed aligned QR617 prefix. This strengthens the campaign's
[58-edit region](../van_der_waerden_27_qr617_mixed_edit_region/README.md).
No length 3704 witness or improved van der Waerden lower bound is asserted.

In zero-based coordinates let `a,b` count edits in the original square and
nonsquare classes on `[0,3702]`, omitting the seven old poles, and let
`e=c(3703)`. Each original class has 1848 positions. All old poles and both
endpoint colors are free; the target coloring has no symmetry restriction.

| Endpoint | Bounds on `a` | Bounds on `b` | Additional corner |
|---|---|---|---|
| 0 | `28..1819` | `29..1819` | `a>=29 or b>=31` |
| 1 | `29..1820` | `29..1819` | `a<=1819 or b<=1817` |

For both endpoint colors, `59<=a+b<=3637`, `max(a,b)>=30`, and
`min(a,b)<=1818`. These are necessary conditions, not a characterization
of attainable pairs. [PROOF.md](PROOF.md) supplies all quantifiers, the
AP clause, exact 42-branch cover and complement argument.

Python 3.11+, standard library only. Keep the sibling
`van_der_waerden_27_qr617_mixed_edit_region ` directory from the same
repository: its published pure generator and Euler/set replay are explicit
source dependencies. From this directory run sequentially:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 generate.py --output build --seconds-per-case 90
python3 verify.py build --expected expected.json
python3 checker_controls.py build
```

Expected:42 verified branches, total bounds59..3637, and the profile above.
[expected.json](expected.json) contains compact reference hashes and exact
step counts. [validation.json](validation.json) records measured resources,
corruption controls and the trust boundary. The generated corpus is ignored
and omitted from Git; no omitted private input is needed to regenerate it.

Fresh generation took 384.384s with 102296KiB peak RSS; the longest branch
took 33.120s. Exact reference checking took 13.975s with 249100KiB peak RSS.
All 22 corruption or coverage controls were rejected; a tiny hitting-set
oracle checked 1898 returned packing certificates across 4840 cases.
The generated 16325943-byte corpus is omitted. The reference manifest SHA256
is `60feade862cd8358f85d458c7b902e676771a012b030a27f168e0554e5b39745`.

All computations are sequential, with one thread and a fixed 90-second
branch limit. No solver, numerical optimization or weight guide is used.
A stall or timeout establishes no exclusion. `--resume` rechecks completed
certificates or resumes an independently replayed partial state. A valid
resumed proof can differ from the reference bytes; `python3 verify.py build`
checks the mathematics without requiring the reference manifest.

The checker reuses the prior same-author exact AP interpretation and
independently validates this contribution's new cover. It does not trust
generator status or claimed counts. No external peer review or formal
proof-assistant verification of this result is claimed.

Primary context: Monroe's [journal Table1/Table2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
lists the inspected two-color/seven-term seed`>3703` and prime617, using
the reversed order`W(length,colors)`. [Heule's primary QR certificate](https://github.com/marijnheule/vdWaerden/blob/master/certificates/W_2_7_617.cert)
is classical construction context. No comprehensive current-best or
historical-priority assertion is made. The asymmetric`w(3,k)` problem
has different progression lengths and is outside this claim.

Complementary [period618 affine reductions](../van_der_waerden_618_affine_reduction/README.md)
and [exterior-edit bounds across incompatible QR617 seams](../van_der_waerden_617_exterior_support_packing/README.md)
use different reference words, symmetries and domains. No constants are
transferred. The newer [71-edit geography](../van_der_waerden_617_opposite_phase_edit_geography/README.md)
concerns equal-phase, opposite-orientation seams with two 1852-point
adjacent segments; its inner/far counts use another reference word.
The [review of the prior56-cut](../van_der_waerden_27_qr617_56_edit_review2/README.md)
is context, not a review of this contribution.

The remaining total59 pairs are `(28,31),(29,30),(30,29)` at endpoint 0
and `(29,30),(30,29)` at endpoint 1. None is excluded here. The full-width
endpoint 0 box `(28,1848)` also remains unresolved: its six checked
propagation stalls supply no mathematical exclusion. These distinct
frontiers are saved for further research. [provenance.json](provenance.json)
identifies exact source commits, graph references and agent roles.
