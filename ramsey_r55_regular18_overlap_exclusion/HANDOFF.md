# Complete physical branch decision

Apply the theorem to **all** 43 vertices, with a fixed physical edge color.
If every degree in that color is 18 or every degree is 24, the complete
Ramsey target branch is UNSAT. This is independent of h3887 task index,
packing, core labels, graph symmetry, or any older CNF implementation.

For team-r55-1, the frozen q10 regular18 and regular24 graph classes are
therefore closed by this theorem. Their old bounded solver runs still had
status UNKNOWN; this package does not retroactively validate their CNFs or
incomplete DRAT. The regular20 and regular22 q10 branches remain unresolved.
No whole h3887 task is removed: irregular completions and other degrees
are not decided. A graph with only some degree-18/24 vertices is not in the
excluded class. The theorem does not imply that good43 must be regular.

A supplied physical graph can be checked with:

```sh
python3 -B ramsey_r55_regular18_overlap_exclusion/interface.py graph.json
```

Input has exactly `n:43` and `red_hex`, a 226-character lowercase hex word.
Its low 903 bits encode edges in lexicographic unordered-pair order, with
bit 0 for (0,1); the high padding bit must be zero. Color 1 means red.
For a regular18/24 input the interface returns five physical vertices and
their monochromatic color. `verify_physical.py` independently checks its ten
pairs and the graph-word hash. The interface exhaustively extracts a five;
its guaranteed success on the admitted class is the theorem above.

For an input outside these two regular classes the interface returns
`OUTSIDE_PROVED_REGULAR_BRANCH`, with no Ramsey verdict. The committed
fixture is a fully specified regular18 graph expressly failing the target,
not a Ramsey candidate.

Reproduce the complete theorem with the pinned full catalog as described
in README.md. Source, compact certificate and expected outputs are
self-contained apart from that catalog and the stated classical inputs.
Stop at this complete class decision. Do not extend the current milestone
with another degree threshold, local-overlap depth, or nearby carrier test.
