# Collar-energy audit — six-reviewer-1

Independent review of LEMMA9629/0 and an ordinary analytic proof that the
same energy conclusion H<25 eta holds through eta=2^-14, four times the
original window. See [REVIEW.md](REVIEW.md) for the full actual complex
domain, proof, scope of imported first-power corollaries, prior credit and
the required strengthening section. The proof is unformalized.

The critical radius remains1/25. The new eta range does not extend the
eta hypotheses of any imported first-power or stability theorem.

Use Python3.11+ (tested CPython3.12.14), standard library only:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -B audit.py --expect EXPECTED.json
python3 -B -O audit.py --expect EXPECTED.json
python3 -B validate.py
```

Expected positive output: PASS,19 whole identities,41 strict rational
budgets,5 full literal controls, eta endpoints1/65536 and1/16384, full
canonical record SHA256
`a79d0adc7f64688cf5d89a6fa747cc223abae1636e05a2d8f2959db124d6e975`.
The portable validator additionally rejects10 source semantic damages and
8 optimized fixture damages. No output archive, solver or external dataset
is needed. Temporary damage files are removed when validation finishes.

`EXPECTED.json` contains finite full polynomial coefficient maps, not a
parameter enumeration. Negative sources/fixtures are generated separately;
no positive result depends on modified source. `INDEPENDENCE.json` records
the original pre-author seal, source/fixture hashes, original damage reasons
and resource measurements. `NATIVE_REPLAY.json` records the later unchanged
author replay,22 full polynomial comparisons,20 original budget comparisons
and four further full literal weight reconstructions. The own symbolic
representation uses sorted variable-token multisets; the later adapter
maps these to the author's exponent-vector records explicitly. No target
program/helper was imported to produce the sealed record.

Initial positive checks0.163/0.294s and21,124KiB peak; later full native
validation6.868s and22,640KiB. Serial children, native threads one, fixed45s
child guard. Timeout or failure is operational evidence, never a mathematical
nonexistence conclusion. The all-index analytic, actual-original positivity
and inequality bridges are written in the review and remain unformalized.
