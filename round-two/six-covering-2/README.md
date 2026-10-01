# A forced modulus-sixteen phase at period 10080

Actual author: **six-covering-2**, role **researcher**, 2026-10-01.

**Exact computer-assisted conditional theorem.** A finite distinct covering
whose moduli are at least eight and divide 10080, retaining

    8:0, 9:0, 10:1, 14:1, 12:3

(modulus:phase), must contain modulus **16**, with phase **4 or 12**.
The two permitted phases are necessary possibilities, not covering witnesses.
The five-class prefix itself is not excluded. The unrestricted frontier
remains `L_min(8) in {10080,15120,20160}`; minimum exactly eight is required
in that parameter. The theorem above already includes modulus eight.

[proof.md](proof.md) gives the reduction, fractional-group inequality,
phase classification, attribution and trust boundary. Four complete trees
have **816 nodes**, 2,909 actual branch phases and 414,402 selected
phase-pair entries. All are checked by literal exact arithmetic and explicit
finite coordinate permutations. This is author verification, not an
independent reviewer verdict or a formal-kernel proof.

The complete generated trees are omitted from publication. The source
regenerates them; no private checkpoint or prior unpublished computation is
required. `manifest.json` records every case's counters and full event,
permutation and pair-table hashes. Recorded discovery used CPython3.12.14,
NumPy2.4.6, SciPy1.17.1, all numerical threads one, 180-second resumable
batches and two-second LP limits. The complete literal replay used
CPython3.11.2, took 25.604 seconds and peaked at51324 KiB RSS. All work used the
existing one-CPU/two-GiB scope.

From this directory, Python3.12 with a local virtual environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-discovery.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  .venv/bin/python -B reproduce.py --generate
```

Expected final exact totals: `nodes=816`, `raw_phases=2909`,
`positive_transports=2738`, `pair_entries=414402`, with the stated forced
phase. It generates each case sequentially, resuming when a voluntary batch
ends. A deadline, unmatched manifest or incomplete case raises an error and
establishes no exclusion. Generated files stay in the ignored `generated/`.
Once generated, `python3 -B reproduce.py` replays without SciPy or NumPy.

The compact supplied odd-cycle certificate is separately reproducible
using Python3.10+ and the standard library only:

```sh
python3 -B check.py odd-cycle.json --expected odd-cycle-expected.json
python3 -B controls.py
```

It excludes a specified nine-class prefix at10080: integer demand1000318,
twice-capacity1995046, strict doubled gap5590. Its actual LCM is10080, so
any distinct minimum-eight covering retaining that prefix has LCM at least
20160. This is another conditional statement. The controls verify all16
phase classifications, five genuine-cover prefixes and reject14 malformed
certificates. The ordinary individual-resource bound is nonstrict for this
particular weight; the supplied fractional pair groups improve its bound.
No assertion that all other ordinary pair certificates fail is made.

Published prior art: the
[six-class phase-one exclusion](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_10080_anchor16_phase1/proof.md)
already excludes representative16:1. This pass reproduces that case with a
fresh95-node tree; the exclusions of0,2,3 and the combined phase restriction
are the new application. The
[residual quotient](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md)
and
[joint capacities](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_joint_capacity/proof.md)
are published framework inputs. Fractional subadditivity and tree
automorphisms are standard principles; no historical-priority claim is made.

Primary context refreshed2026-10-01:
[Zhang–Zhang](https://arxiv.org/html/2607.19029) claims L_min(7)=10080;
[Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644)
treat prime support2,3,5. Neither paper's numerical exclusion is a premise
of the present theorem.
