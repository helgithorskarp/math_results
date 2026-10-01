# Single-coset seven-lift obstruction

six-covering-1, researcher; author-checked elementary proof, 2026-10-01.

The29 distinct resources7d (d|720,d>=2) cannot cover a whole class
modulo6 at period5040. Their846 available hits cannot meet a forced
local minimum cost48 within a46-hit budget. Every singleton point-weight
capacity nevertheless passes, sharply by the factor141/140.

[proof.md](proof.md) gives the complete argument, a sharp LOCAL40-point
witness, the fractional phase mixture, and an exclusion of all30 parameters
in a specified two-stage construction route toward a minimum-eight cover
at15120. This does not exclude arbitrary coverings at15120 and changes
no global numerical bound. No independent review or priority is asserted.

Reproduce with CPython3.11 (tested3.11.2), standard library only, one process:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 check.py --expected expected.json
python3 -O check.py --expected expected.json
```

Expected compact output includes `status: CHECKED`, local minimum48,
target capacity846, hypothetical covering mass lower848, fractional
ratio[141,140], all30 construction parameters excluded, and
`global_numerical_bound_changed: false`. Full deterministic evidence is
in [expected.json](expected.json). Normal and optimized Python modes
use explicit runtime guards; correctness checks do not depend on `assert`.
`local40.py` supplies the small exact case-bound controls and the sharp
witness. No solver, external input, large proof corpus or raw log is needed.

Trust boundary: the mathematical reduction and case argument are written
but unformalized. The literal author checks support them and reject
damaged witnesses; they do not establish independent peer validation.
Uniform phase averaging and fractional obstructions are prior methods.

See the primary literature and internal source comparisons at the end of
the proof. The unresolved construction frontier now requires partial
target coverage or a union of cofactor cosets. The global candidates remain
10080,15120,20160, with only20160 witnessed.
