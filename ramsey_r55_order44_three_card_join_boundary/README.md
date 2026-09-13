# Order-44 physical deletion joins: final failed-gate checkpoint

No Ramsey bound changes. This package preserves the final pass of the
two-pass order-44 deletion-lift trial. It gives an exact three-card
formulation for every hypothetical good44 and a general physical
counterexample to a proposed arc-consistency shortcut on prescribed
attachment domains. It does **not** supply an order-44 exclusion,
construction, or near-term complete decision. The final gate is missed;
the lane is stopped and reassignment within R(5,5) is recommended.

[MATHEMATICS.md](MATHEMATICS.md) proves the statements without computation.
Every good44 contains a red P3. Over its common good41 core, the three
stars must form a mixed triangle in their exact pair compatibility
relations. This retains physical incidences across cards, but neither a
uniform obstruction nor a finishable complete core cover was obtained.

The negative control works for every diagonal parameter s>=5. Each of
the three exact relations on two prescribed stars is binary inequality:
every domain value has support in both other domains, while the triple
join is empty. The same core extends successfully after an omitted star
is restored. This caveat is part of the result, not an unresolved test.
The control is not a counterexample for full order-41 star domains.

## Exact finite replay

CPython 3.11.2, standard library only. From the repository root:

```bash
star_run=$(mktemp -d)
python3 -B ramsey_r55_order44_three_card_join_boundary/generate.py --s 5 --output "$star_run/fixture.json"
cmp "$star_run/fixture.json" ramsey_r55_order44_three_card_join_boundary/fixture.json
python3 -B ramsey_r55_order44_three_card_join_boundary/verify.py --input "$star_run/fixture.json" --output "$star_run/verified.json"
cmp "$star_run/verified.json" ramsey_r55_order44_three_card_join_boundary/EXPECTED.json
```

The verifier prints `PHYSICAL_STAR_CONTROL_VERIFIED`. It reconstructs
full adjacency matrices from the serialized edge list, scans all
monochromatic five-sets, checks each pair relation entry, checks all
eight triple assignments and their explicit witnesses, and checks the
positive extension. It does not import the generator or infer physical
validity from the pair formulas. These are finite controls for the
written proofs, not an independently reviewed or formal proof.

Expected: a good12 core with 30 red edges, clique number 4 and independence
number 3; six unary domain occurrences; six valid good14 pair graphs;
all six domain values survive arc consistency; zero valid prescribed
triples; and a good15 outside the prescribed domains. The s=6 boundary
was also checked locally; no parameter table is claimed as progress.

The [preceding averaged-moment pass](../ramsey_r55_order44_deletion_moment_barrier)
has its own unchanged exact feasible certificate and source history.
This pass uses no catalogue, solver, sampled carrier, known42 extension
basin, inherited edge window, Hamiltonicity assertion, or automorphism
premise. [DEPENDENCIES.md](DEPENDENCIES.md) records literature, overlap,
and review status. No Discovery Net result or transaction is submitted
for this failed endpoint attempt.
