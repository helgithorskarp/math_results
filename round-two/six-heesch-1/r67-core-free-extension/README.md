# A core-free obstruction to extending the R67 first-copy pattern

Actual author: **six-heesch-1**, role **researcher**. Author-checked exact
computer-assisted lemma; ordinary geometric bridges are unformalized and
independent review is pending.

Every nonempty disc polyomino in the specified 105-cell domain is excluded from
having a second complete corona extending this particular seven-copy first
pattern. All prototype cells may change. Second-corona motions may be arbitrary
rigid motions, with reflections and final holes allowed. Other first patterns
and global Heesch numbers remain open; the finite-five target is unmet.

From the repository root, run with standard-library CPython 3.11.2:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 round-two/six-heesch-1/r67-core-free-extension/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -O round-two/six-heesch-1/r67-core-free-extension/verify.py
```

Both outputs equal [expected.json](expected.json). The reader reconstructs a
945-variable, 77,425-clause necessary formula and checks all 11 RUP additions
in the **203-byte** [certificate](obstruction.rup). The formula uses 105
prototype variables and 840 complete conditional supplier options. It has
no forced core cells, geometry exclusions, prototype exceptions or bounded
second-copy layout. Nine damaged inputs/proofs must fail for their specified
reasons.

The reader checks the existing R67 first corona and its complete empty-sector
inventory, preserves a known S68 second corona and its actual whole supplier,
and checks a disabled contact antecedent, an existing gap owner outside the
fixed pair and the empty-mask control. The [proof](proof.md) explains why the
conditional demand is necessary for arbitrary second motions.

The native discovery solver was python-sat 1.8.dev24 / Glucose4. Verification
does not use its status or require a solver. The CNF and option tables are
regenerated; only compact inputs and the checked proof are stored. All imported
source and literal fixtures are pinned in [dependencies.json](dependencies.json).
The earlier classifier and tile-specific Heesch upper are not assumed.

Primary context: [Kaplan's paper](https://arxiv.org/abs/2105.09438) and
[the author census](https://cs.uwaterloo.ca/~csk/heesch/), refreshed 2026-10-02.
No exhaustive current record or historical priority claim is made.
