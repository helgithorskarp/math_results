# P17 second-generation star obstruction

Agent **six-heesch-1**, role **researcher**. A specified four-provider star,
known to receive six charges with one-generation interiority, cannot occur
with two incoming-provider generations interior. This is an all-real local
lemma, not a new Heesch number or a classification of every six-charge star.
Read [proof.md](proof.md) for the reduction and scope.

From the repository root, using CPython3.11 or later and the standard library:

```sh
python3 -B heesch_polyomino_second_generation/check.py
python3 -O -B heesch_polyomino_second_generation/check.py
python3 -B heesch_polyomino_second_generation/check.py --controls
```

The first two outputs must equal [expected.json](expected.json). The last
adds `malformed_controls_rejected: 4`. The checker independently reconstructs
the geometry and checks36 subsidiary sparse contradictions and the final
474-clause,40-addition RUP proof in [certificates.json](certificates.json).
No SAT library, native solver, downloaded executable or generated proof
corpus is needed. The sole imported theorem is the byte-pinned
[237 interior-pair library](../heesch_polyomino_corner_obstruction/pairs.json),
whose written justification is in that contribution's
[proof](../heesch_polyomino_corner_obstruction/proof.md).

Discovery used python-sat1.8.dev24 / Glucose4 with one thread and10,000-conflict
budgets, followed by drat-trim commit2e3b2dc0ecf938addbd779d42877b6ed69d9a985.
The public checker's forward unit-propagation validation supplies a different
proof-checking implementation and does not trust that discovery software.
Normal and disabled-assertion runs agree; four malformed controls reject.
No independent reviewer verdict or proof-assistant formalization is claimed.
