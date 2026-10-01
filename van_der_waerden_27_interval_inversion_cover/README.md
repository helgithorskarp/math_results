# A complete obstruction to one-interval QR617 repair

Every one of the **6,861,660 nonempty contiguous interval inversions** of the
specified binary word on [1,3704] has a monochromatic nonconstant seven-term
arithmetic progression. Thus an AP-free coloring must differ from this word
on at least **two nonempty runs**. This is a construction-family barrier; no
new bound or exact value for W(2,7) follows.

For position t, put r=(t-1) mod617. At r!=0, the base bit is0 for quadratic
residues and1 for nonresidues. At r=0 it is0, except at t=3703 where it is1.
The endpoint t=3704 has bit0. `base3704.bits` specifies every bit literally;
`audit_base_formula.py` verifies the formula. Its normalized SHA256 is
`469fb855744015cefb59c822bb1cf62af5d393c987f9211847eaa9f8db1166e8`.
All1,141,450 APs are checked; the only original monochrome is a=2,d=617,
color0. The3703-prefix is therefore AP free. That known baseline is not new.

From this directory, with standard-library Python3.11+:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 reproduce.py --output-dir build
```

Expected final status:
`ALL6861660_SINGLE_INTERVAL_INVERSIONS_EXCLUDED_EXACTLY_BOTH_MODES`.
For an already completed, source-pinned prefix use the same command with
`--resume`; failed or interrupted child stages are not resumed automatically.

The compact certificate has two parts:289 actual APs whose cut rectangles
cover6,858,761 choices, then a directly checked AP for each of the remaining
2,899 choices. Sorted interval unions and integer bitsets independently
reconstruct identical coverage. Both proof-checking modes pass52 deliberate
mathematical corruptions. Residual positive APs are freshly regenerated with
fixed8,000-AP/32-point quotas and differences at most64; this generator is
not a proof premise. The baseline assertion checker runs only in normal
mode, with optimization explicitly disabled.

See [PROOF.md](PROOF.md) for the exact domain and gap argument,
[VALIDATION.md](VALIDATION.md) for limits and trust boundaries, and
[expected.json](expected.json) for all input hashes. There are no third-party
libraries, solver traces or private proof inputs. Same-author implementation
independence is claimed; external review or formalization is not claimed.

Primary context: [Monroe's paper](https://arxiv.org/html/1603.03301v7), Tables1/2,
records length7/two colors >3703 and prime617; it writes W(length,colors).
Here W(2,7) always means two colors/seven terms. The existing
[wustep QR617 attack](https://github.com/wustep/maths/blob/main/problems/vdw-w27/ATTACK.md)
is prior construction/local-search context; its solver outcomes are not proof
premises. These sources were re-read2026-10-01; bounded literature and campaign
reads support no exhaustive priority or current-record claim.

Author: six-vdw-1, role researcher,2026-10-01. This interval family differs
from the campaign's field-polynomial repair and phase-edit-floor families.
