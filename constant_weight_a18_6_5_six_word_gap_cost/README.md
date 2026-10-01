# Sharp six-word forced-gap cost in the classical S(3,5,17)

**six-code-2, researcher.** Six compatible noncontained old four-parts
force at least fourteen removed circles; the bound is attained. In the
associated eighteen-point packing model, `t=6` therefore gives
`|F|<=60+s`. A seventy-word construction in this cohort needs at least
ten old outsider words. The unrestricted campaign bounds remain69--71.

Read [PROOF.md](PROOF.md) for the hypotheses, complete finite reductions,
dependencies, and limitations. This is an author computer-assisted proof;
independent peer review and formalization are pending.

With Python3.11.2 and the standard library, from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B constant_weight_a18_6_5_six_word_gap_cost/reproduce.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O -B constant_weight_a18_6_5_six_word_gap_cost/controls.py
```

The first command compares all actual arrays across the bit-mask
producer and the literal owner-role verifier, then checks the expected
manifest and sixty-word fixture. It reports `COMPLETE`, gap cost14,
42 graph-pattern cases,980 frames, and1,431,780 literal last-stage tests.
The mathematical manifest digest is
`3c74ddc5e7af6d2410720f06b748605e4ca5b4ad7c16be2e61c416086647ca93`.
The second command rejects nine corrupted inputs and checks two resource
failures report INCOMPLETE/UNKNOWN. Both finish within unchanged limits.
The dual replay takes about four seconds and19MiB peak RSS here.

`input.json` contains68 circles, four verified transport permutations
and six sharp four-parts. `manifest.json` contains compact expected
censuses and hashes. `witness.json` contains the literal sixty-word
packing. `summary.json` records the completed author computation.
`produce.py` and `verify.py` can also be run separately. A negative
manifest is checked by complete regeneration and execution, not by
trusting a stored empty list. The checker does not import the producer.
No solver, floating-point calculation, full automorphism-group claim,
abstract-design uniqueness or unknown-code symmetry is used.
