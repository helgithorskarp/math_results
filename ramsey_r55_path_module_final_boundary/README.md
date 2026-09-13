# Path/module trial: final boundary

**The final whole-good43 gate failed. The two-pass lane is parked.** No
good43 was produced or excluded, no complete physical class was closed,
and no finishable all-good43 residual was demonstrated. Reassignment
within R(5,5) is required before further research in this slot.

The corrected attempt retained actual Ramsey avoidance while seeking a
global decomposition around a maximum induced subset avoiding P5 and its
complement. The cross-edges remain unclosed. The previous disconnected
path-hypergraph class also remains unresolved.

[PROOF.md](PROOF.md) records an auxiliary general compatibility argument:
for every integer t>=16, more than 511/512 of all labelled graphs on 2^t
vertices simultaneously avoid monochromatic K_(2t+1), contain both colour
P5s in every 1024t-set, and remain prime after deletion of any at most
3*2^t/8 vertices. Thus these structural phenomena coexist with actual
Ramsey avoidance, and a path-free core can leave almost all vertices
outside it. This is a classical random-graph argument with explicit
constants, not a new Ramsey bound, supplied graph, or novelty claim.

The proposition does **not** apply to k=5,n=43 and is not a successful
campaign milestone. The exact first-moment term at that endpoint is
481299/256>1, so this probability estimate gives no conclusion there.
No interpolation from the large-parameter statement is justified.

From this directory, using Python 3.11 standard library only:

```sh
python3 -B verify.py | diff -u EXPECTED.json -
```

The written proof establishes the all-parameter proposition; the script
checks exact constants, base cases, induction margins, and all 1024
five-vertex words. It does not construct or search for a graph, invoke a
solver, or formalize the proof. The checked output explicitly records
`final_gate_met=false` and `new_good43_decisions=0`.

[REASSESSMENT.md](REASSESSMENT.md) records the exhausted trial and strict
stopping action. [DEPENDENCIES.md](DEPENDENCIES.md) preserves accepted
input and primary-literature boundaries. The complete previous certificate
at [the first-pass source](../ramsey_r55_path_module_coexistence_boundary)
and all older programs remain unchanged. No pending transaction is
resubmitted and no Discovery Net mathematical claim is submitted here.
