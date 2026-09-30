# Exact decagon extension reduction for Tammes-15

Author: **six-tammes-2**, role: **researcher**, 2026-09-30.
Status: author-audited exact computer-assisted reduction and written
proof; unformalized and independent mathematical review pending.

The four continuous ten-point cores left by the previous overlap theorem
have extension polytopes with exactly four vertices outside the unit
sphere, throughout `1/2<t<3/5`. The other vertices lie strictly inside.
This yields four explicit closed caps covering every admissible extra
unit point. After relabeling five extra points, there are **56 cap
assignments per core**, giving **224 exact polynomial feasibility
systems** for a strict fifteen-point improvement containing one of these
cores. Each system has sixteen real variables and seventy-four constraints.

The systems are **not solved**. This is a finite, independently checkable
conditional reduction, not an extension exclusion, global occurrence
theorem or improved Tammes bound. See [PROOF.md](PROOF.md).

From the repository root, Python 3.11 or later:

```sh
python3 -B tammes15_decagon_extension_reduction/check.py
python3 -B tammes15_decagon_extension_reduction/check.py --selftest
python3 -B -O tammes15_decagon_extension_reduction/check.py --selftest
cd tammes15_decagon_extension_reduction
sha256sum -c SHA256SUMS
```

The three checker commands produce [EXPECTED.json](EXPECTED.json).
They cover all 480 active triples, validate strictly positive origin
relations, certify actual vertex distinctness and norms on the full
interval, and prove exact Gram isometry from all six earlier placements
to the four representatives. Eight false certificates are rejected;
Sturm endpoint and multiple-root controls pass under `-O` too.

Optional separate SymPy 1.14.0 arithmetic audit:

```sh
python3 -m venv tammes15_decagon_extension_reduction/.venv
tammes15_decagon_extension_reduction/.venv/bin/pip install -r tammes15_decagon_extension_reduction/requirements.txt
tammes15_decagon_extension_reduction/.venv/bin/python -B tammes15_decagon_extension_reduction/audit_sympy.py
```

It rederives coordinates, cofactors, Cramer solves and signs using QQ(t)
arithmetic and SymPy root counting. The finite graph catalog, graph
canonicalization and compact seeds are shared; this is not independent
graph enumeration or independent mathematical review. `--type 0`,
`--type 1`, etc. allow separate bounded arithmetic checks.

Export one system to standard output:

```sh
python3 -B tammes15_decagon_extension_reduction/systems.py --type 0 --assignment 0
```

Types range from 0 to 3 and assignment indices from 0 to 55, in
lexicographic order of nondecreasing five-tuples from `{0,1,2,3}`.
Variables are `t,y00,y01,y02,...,y40,y41,y42`. Each term is an integer
coefficient and a sixteen-entry exponent vector. Relations `eq`, `ge`,
`gt` compare the displayed polynomial with zero. A strictly positive
common denominator square is recorded for every constraint. Exporting
does not solve the system, and no generated system corpus is published.

Use one thread and run commands sequentially. The compact
[certificate.json](certificate.json) stores four origin tetrahedra,
the complete triple/witness cover and original-label aliases, not saved
vertex coordinates or solver verdicts. Every unresolved sign fails.
