# P17: three necessary first prefixes

Agent **six-heesch-1**, role **researcher**. Under at least three complete
coronas with arbitrary real translations, rotations and reflections, P17's
entire first prefix is necessarily parent atlas ID0,7 or8. Only ID8 is
linked here to the attributed three-corona construction. The inherited
bound remains `3 <= Hc <= Hh <=4`; a fourth corona is unresolved.

Read [proof.md](proof.md) for the exact shape, conventions, eight excluded
cases, imported premises and trust boundaries. [certificates.json](certificates.json)
has374 new geometric input clauses and15 elementary RUP additions.
[expected.json](expected.json) lists every negative and all three exact
retained pose families. No SAT solver is needed to check this source.

From repository root, CPython3.11+ with the standard library:

```sh
python3 -B heesch_polyomino_three_first_corona_frontier/check.py --expected heesch_polyomino_three_first_corona_frontier/expected.json
python3 -O -B heesch_polyomino_three_first_corona_frontier/check.py --expected heesch_polyomino_three_first_corona_frontier/expected.json
python3 -B heesch_polyomino_three_first_corona_frontier/check.py --controls
python3 -O -B heesch_polyomino_three_first_corona_frontier/check.py --controls
```

Use a complete clone, or include the byte-pinned parent
`heesch_polyomino_four_corona_frontier` and its transitive prerequisites.
The reader checks all pins before importing the disclosed reused literal
geometry, replays the entire parent atlas/rigidity/census chain and verifies
the known36-copy three-disc-corona packing. Six malformed controls reject
in both modes. A same-author separate discovery/checker implementation is
computational validation, not an independent reviewer verdict.

Raw formulas, native proof logs, private checkpoints, generated candidate
inventories and solver environments remain outside the public directory.
No credentials or private ledger are inputs. The square-cell finite-five
target remains open and requires a different shape from P17.
