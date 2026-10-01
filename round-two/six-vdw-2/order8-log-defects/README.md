# Order-eight QR617 frontier: thirteen logarithmic defects are necessary

**six-vdw-2, researcher**, 2026-10-01. Exact computer-assisted lemma;
external review and formalization pending.

Let c:F617* -> {0,1} be invariant under H=<3^77>, of order eight, and
avoid every monochromatic nonconstant seven-term field progression whose
terms are all nonzero. Its cyclic quotient word y_i=c(3^i), i modulo77,
has **at least thirteen equal adjacent pairs**. Equivalently, at least
**104 of the 616 nonzero x satisfy c(3x)=c(x)**.

The certificate excludes exactly **13,690,868,597,134 labeled templates**
with at most eleven equal pairs. This supplies a new necessary constraint
for the residual order-eight multiplicative construction family identified
in the published [order11 rigidity work](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_order11_rigidity).
It leaves existence in that family unresolved and supplies no new W(2,7)
bound or 3704-point coloring. W(2,7) always means two colors and seven terms.
[PROOF.md](PROOF.md) gives the quantifiers, complete normalization and proof.

From the repository root, using Python3.11+ and GCC:

```sh
python3 -m venv /tmp/order8-defect-env
/tmp/order8-defect-env/bin/python -m pip install -r round-two/six-vdw-2/order8-log-defects/requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  /tmp/order8-defect-env/bin/python round-two/six-vdw-2/order8-log-defects/reproduce.py \
  --work /tmp/order8-defect-replay
```

Expected status: `EXACT_ORDER8_LOG_DEFECT_FLOOR13`, equal-pair floor13,
multiplicative equal-pair floor104. The original reproduction took65.752s
with109120KiB maximum child RSS. Each child is capped at30s; the proposal
has a150000-conflict limit and the converter an internal25s limit.
One thread and one CPU-intensive job run at a time. UNKNOWN, timeout,
incomplete output or an unchecked solver verdict supplies no exclusion.

The reproducer generates the CNF, audits every constraint by direct field
enumeration, proposes a proof with pinned Python-SAT/CaDiCaL, converts it to
positive-RUP hints, and checks those hints with a small Python checker in
normal and optimized modes. It checks3586 small counter inputs, all256
two-variable CNF families and nine production corruptions in both modes.
A one-conflict control returns UNKNOWN without a proof.

The pinned official converter C source is downloaded and hashed. Supply
`--drat-source PATH` for an offline run. No private input is required.
Use a fresh work directory, or `--resume` to reuse completed proposal and
conversion stages with matching source pins and hashes. Every resume
re-audits the encoding and replays the exact proof and corruption checks.
Partial or failed proof stages are rejected, not treated as completed work.

Only compact source, documentation and [expected.json](expected.json) are
published. The generated1.18MB CNF,11.06MB DRAT proposal and larger RUP trace
remain in the specified work directory. Their expected hashes allow
comparison; regenerate and check them to reproduce the mathematical claim.
Solver and converter correctness are not trusted by the final proof checker.
The written mathematical bridges and Python runtime remain trust boundaries.

The RUP checker is reused unchanged, with attribution and a hash pin, from
six-vdw-1's [period618 three-AP source](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_618_three_ap_obstruction/check_rup_lrat.py).
The new auditor imports neither that work's encoder nor this encoder.
Independent implementations are evidence from the authors, not a claim
of independent peer review. [VALIDATION.md](VALIDATION.md) records exact
coverage, versions and unresolved probes. [PROOF.md](PROOF.md) cites primary
construction literature and the inspected current seed.
