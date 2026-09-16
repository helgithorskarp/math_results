# Provenance and reproduction

## Reviewed inputs

The review targets
`hadwiger_nelson_ei19_first_lens_fourcolour_stop` at mathematical commit
`bada7569ddcfb515e608d6b043a0558416def00b`. It also audits the pinned source
certificate in `hadwiger_nelson_ei19_terminal_boundary`.

`independent_check.py` contains twelve literal SHA-256 expectations covering
the target theorem, proof, provenance, architecture, expected output, colour
word and executable sources, plus the EI19 source theorem, certificate and
checker. Later Discovery receipt-only additions to the target directory are
outside its mathematical input.

## Reviewer-owned computation

The review code was written independently and uses only the Python standard
library. In particular it does not import the target's `intervals.py`,
`verify.py`, `controls.py`, or the source's `geometry.py`. The target uses a
fixed-grid dyadic interval class with scale `2^160`; the reviewer retains
exact rational endpoints through every arithmetic operation and independently
rounds square roots at scale `2^192`.

The colour search is a direct deterministic backtracker rather than a SAT,
SMT, MILP or external graph-colouring solver. All positive deletion witnesses
are emitted in `EXPECTED.json`.

## Commands

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B hadwiger_nelson_ei19_first_lens_fourcolour_stop_review1/independent_check.py --check-expected
PYTHONDONTWRITEBYTECODE=1 python3 -O -B hadwiger_nelson_ei19_first_lens_fourcolour_stop_review1/independent_check.py --check-expected
PYTHONDONTWRITEBYTECODE=1 python3 -B hadwiger_nelson_ei19_first_lens_fourcolour_stop_review1/controls.py
cd hadwiger_nelson_ei19_first_lens_fourcolour_stop_review1 && sha256sum -c SHA256SUMS
```

Expected top-level verdict:

```text
ACCEPT_AND_STRENGTHEN_EI19_FIRST_LENS_FOUR_COLOUR_STOP
```

Expected controls verdict:

```text
ALL INDEPENDENT REVIEW CONTROLS PASS
```

No network access is required for reproduction after the repository is
cloned.

