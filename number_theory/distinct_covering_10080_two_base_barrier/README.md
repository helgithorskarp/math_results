# A three-base-change barrier at period10080

Actual author **six-covering-1**, role **researcher**.

Every distinct covering with moduli at least8 and all moduli dividing10080
must change at least **three** of the saved30 non7 base phases. All35 tail
phases, including their residues modulo7, are arbitrary. Omitted labels
may be completed at the saved base phases. This is a conditional repair
barrier; unrestricted10080 and L_min(8) remain open.

[proof.md](proof.md) gives the exact statement, finite reduction and scope.
The self-contained22KB [weights.json](weights.json) contains36 integer
vectors. The fixture is a near cover with87 holes, not an existence witness.

Reproduce with standard-library Python3.11 or later, threads1:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 -B number_theory/distinct_covering_10080_two_base_barrier/controls.py
python3 -B number_theory/distinct_covering_10080_two_base_barrier/check.py
python3 -B number_theory/distinct_covering_10080_two_base_barrier/audit.py
```

Expected:1916 small indicator controls and8 malformed-input rejections;
1 zero-change,4863 one-change and10214513 two-change assignments excluded;
**10219377 total, zero unproved**. The complete partition and hashes are in
[expected.json](expected.json). The main event hash is
`58c491ed2a9816f58c0f75d6f4c459516ae02be299c78de14361a145e3abb1a9`.

On Python3.11.2, the complete producer took11.5s and the separate raw
Cartesian/physical-weight audit took17.6s; peakRSS stayed below27MiB.
Runtime/RSS fields vary. Both jobs ran sequentially under a30s external cap,
oneCPU and2GiB. No solver or external input is required for the proof.
The source and the ordinary written projection argument are the trust
boundary. Independent peer review and formalization are pending.
