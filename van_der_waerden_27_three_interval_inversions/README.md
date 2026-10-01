# Three-interval inversion barrier for two colors and seven terms

Author: **six-vdw-1**, role **researcher**, 2026-10-01.

For the literal QR617 near-word `base3704.bits`, every binary edit mask with
at most three maximal nonempty contiguous runs produces a monochromatic
nonconstant seven-term arithmetic progression. This excludes exactly

\[
1+\binom{3705}{2}+\binom{3705}{4}+\binom{3705}{6}
=3,577,985,539,042,435,691
\]

distinct masks, including 3,577,977,700,443,300,700 masks with three runs.
Any AP-free coloring of `[1,3704]` must have **at least four disagreement
runs and four agreement runs**, hence **at least seven adjacent transitions**
between matching and differing from this fixed word. Four disagreement runs
cannot cover both endpoints.

The new certificate excludes canonical masks with first edit bit zero and
at most three runs. The full-family statement explicitly imports the
[two-interval barrier](../van_der_waerden_27_two_interval_inversions/PROOF.md),
source commit `a761f917916a32b878e544fbc812a375a7beafdc`, to justify normalization
by global color complement. That earlier mathematical proof is a dependency;
it is not rerun by the new reproducer. See [PROOF.md](PROOF.md).

This does not produce a 3704-point coloring, a new W(2,7) bound, an exact
W value, or unrestricted nonexistence. It concerns only the specified
literal reference, including its poles and endpoint.

From the repository root, with Python 3.11+, a C compiler and pinned Python-SAT:

```sh
python3 -m pip install -r van_der_waerden_27_three_interval_inversions/requirements.txt
python3 van_der_waerden_27_three_interval_inversions/reproduce.py --output-dir /tmp/vdw-three-interval-replay
```

All stages run serially with one thread. The reproducer builds the canonical
CNF, independently audits every clause, generates an untrusted proof,
transforms it to positive RUP hints, and verifies every hint with a strict
standard-library Python checker in normal and optimized modes. It also
checks valid fixtures and rejects malformed encodings and proofs.

Only compact source and inputs are included. Generated instances, executables
and the approximately 28 MB hint trace stay in the selected output directory.
[VALIDATION.md](VALIDATION.md) records measured coverage and limits;
[DEPENDENCIES.md](DEPENDENCIES.md) records mathematical and software provenance.

The historical seed is from [Monroe Tables 1–2](https://arxiv.org/html/1603.03301v7):
length seven, two colors, `>3703`, using prime 617. Monroe orders arguments
as length then colors. No exhaustive priority or current-record claim is made.
