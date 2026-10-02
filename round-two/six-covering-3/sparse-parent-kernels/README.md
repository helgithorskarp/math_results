# Sparse-parent product kernels

Actual **six-covering-3, researcher**. For the free24-tail inventory at10080,
unit product kernels on at most two/three parents have sharp minima22/13
cofactor points and complete equality classifications. All common-q erasure
cuts are automatic on at most three supported parents.

The supplied complete BASE stage passes the full common-q hierarchy and
both older12/13 diagnostics, but contains the new three-parent52/51 kernel.
[proof.md](proof.md) gives all universal arguments, original resource scope
and citations. No L_min(8) bound improvement or whole-prefix exclusion is claimed.

Run from the repository root with Python3.10+ and stdlib only:

```
python3 -B round-two/six-covering-3/sparse-parent-kernels/check.py --expected round-two/six-covering-3/sparse-parent-kernels/expected.json
python3 -B round-two/six-covering-3/sparse-parent-kernels/audit.py --expected round-two/six-covering-3/sparse-parent-kernels/expected.json
python3 -B round-two/six-covering-3/sparse-parent-kernels/check.py --controls
python3 -B round-two/six-covering-3/sparse-parent-kernels/audit.py --controls
```

Repeat with `-O`. [fixture.json](fixture.json) is the entire mathematical input;
[expected.json](expected.json) records exact capacities and BASE clause hashes.
No private producer, solver or large proof corpus is a verification input.

[separate.py](separate.py) completely detects the cardinality-minimal
three-parent13 kernels in owned P. Give `--base-json` a list of36 `[n,a]`
original phases and `--out` a destination JSON path. A found kernel proves
only that stage nonextendible; passing excludes only this minimum kernel class.
