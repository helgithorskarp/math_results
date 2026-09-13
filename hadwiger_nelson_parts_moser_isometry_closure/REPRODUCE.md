# Reproduction and evidence boundary

All commands run from a complete repository checkout. Tested with CPython
3.11.2. The verifier, geometry check and controls use only the standard library.
Choose fresh output locations outside Git; expanded geometry is several MiB.

## Full theorem check

```sh
python3 -B hadwiger_nelson_parts_moser_isometry_closure/verify.py --check-expected
python3 -O -B hadwiger_nelson_parts_moser_isometry_closure/verify.py --check-expected
```

Both runs must match every field of EXPECTED.json and end with
`all_sub509_subgraphs_four_colourable=true`. Validation uses explicit exceptions,
so Python optimization does not disable safety checks. The producer and final
verifier have different list-colouring algorithms; their full geometric inputs,
conservative obstruction sets and residual instances were compared.

## Additional arithmetic implementation and controls

First emit the reconstructed geometry and the finite residual frontier:

```sh
python3 -B hadwiger_nelson_parts_moser_isometry_closure/verify.py \
  --emit-frontier /scratch/parts-moser-frontier.json
python3 -B hadwiger_nelson_parts_moser_isometry_closure/independent_geometry.py \
  /scratch/parts-moser-frontier.json
python3 -B hadwiger_nelson_parts_moser_isometry_closure/controls.py \
  /scratch/parts-moser-frontier.json
```

The emit-only run deliberately reports that the full theorem has **not** been
verified in that invocation: it has not replayed the final target colourings.
The normal invocation above is required for the complete result.

The additional implementation uses the signed complex field
`Q(t,r,s), t^2=-3, r^2=-11, s^2=5`, and rational Gaussian elimination for inverses.
It imports no producer or primary-verifier code. It must report complete
entrywise geometry agreement for 25,590 images, 24,751 external coordinates,
and all relevant unit-neighbour lists and fresh internal edges. These are
independent algorithms/representations run by the author, not external review.

The controls exhaust 16,932 singleton colour assignments and 33,296 arbitrary
list assignments on small graphs, find the Moser counts 0 and 384 in three and
four colours, and reject five deliberately corrupted certificates.

## Optional witness regeneration

Create a separate external environment with `python-sat==1.8.dev24`; it provides
the CaDiCaL 1.9.5 backend used here. This dependency is unnecessary for checking.

```sh
/path/to/pysat-python -B hadwiger_nelson_parts_moser_isometry_closure/produce.py \
  /scratch/parts-moser-frontier.json /scratch/parts-moser-new-certificate.json \
  --log /scratch/parts-moser-production.json
python3 -B hadwiger_nelson_parts_moser_isometry_closure/verify.py \
  --certificate /scratch/parts-moser-new-certificate.json
```

There are 42 queries, each with a 250,000-conflict limit. The recorded run found
all 42 witnesses in about 2.2 solver seconds. Each graph has exactly 508
vertices. For vertex v and colour c the SAT variable is `4*v+c+1`. Each vertex
has an at-least-one clause, each unit edge forbids each common colour, and a
retained triangle receives three distinct colours. Any ordinary colouring can
be colour-permuted to satisfy the pins. In a satisfying assignment, choose any
true colour at each vertex; the edge clauses guarantee a proper colouring.
At-most-one clauses are not required for either direction.

A failure to obtain a positive witness saves the status and CNF and stops;
UNKNOWN is inconclusive, and an UNSAT answer would require a separately checked
proof before any record claim. The present certificate uses SAT models only.

Regenerated valid colourings can differ, so their certificate hash may differ.
Do not pass `--check-expected` for a different valid certificate; that option
also checks the original byte hash. The ordinary verifier still requires exact
coverage and checks all geometry and colouring claims.

The original Parts coordinate-expression bridge was additionally rerun using
its existing parser and SymPy 1.14.0, confirming every entry of the pinned
integer table. That parser is not executed by the ordinary verifier. Its source
input and this additional check are described in VALIDATION.json.
