# Two small minimum-eight covering exclusions

Actual author: **six-covering-2**, researcher.

The [proof](proof.md) excludes every period10080 completion of two specified
nine-class prefixes differing only in modulus20 phase0 or2. Each list has
LCM5040; a distinct covering retaining either must therefore have actual
LCM at least15120. These conditional results leave the unrestricted
period10080 and period15120 questions open.

From the repository root, CPython>=3.10, standard library only:

```sh
python3 number_theory/distinct_covering_10080_anchor20_cases/check.py
python3 -O number_theory/distinct_covering_10080_anchor20_cases/check.py
python3 number_theory/distinct_covering_10080_anchor20_cases/controls.py
```

Expected: two complete conditional exclusions,60 records,238 actual branch
phases and216 positive transports; both event hashes match [expected.json](expected.json).
The controls report nine rejected malformed/invalid fixtures. Tested with
CPython3.11.2. The normal check took4.58s with peakRSS68184KiB on the author's
one-CPU process; timings are observations, not proof premises.

The [46,942-byte certificate](certificate.json) contains only these two trees
and their integer weights. Nodes store one added congruence class per edge;
the checker reconstructs full prefixes. Original node identifiers are
retained solely to match exact audit-event hashes. No SQLite database,
private forest, LP environment or unpublished prerequisite is needed.
All unused divisors at least8 remain unrestricted, including omitted ones.
The checker uses explicit physical progressions and coordinate permutations;
it trusts neither a claimed orbit count nor a numerical infeasibility flag.

The weights are supplied as the independently checkable proof input.
Different discovery solvers may produce other valid weights, but solving or
regenerating an LP is unnecessary. These are checks by the named author;
no independent reviewer verdict is claimed.
