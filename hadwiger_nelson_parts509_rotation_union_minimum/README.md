# Exact minimum inside a two-placement Parts-509 union

## Result

Let `L={0,...,373}` and `S={374,...,508}` be the two gadgets in Jaan
Parts's 509-point construction.  This directory studies the strict
unit-distance graph `U` on

\[
 L\;\cup\;R(-1/2,-\sqrt3/2)S\;\cup\;S.
\]

These are events 108 and 789 in the sibling exact rotation classification.
The two 509-point placements share 493 points, so `U` has 525 distinct points.
Exact reconstruction gives 2,551 unit pairs.  The certified theorem is:

> Every non-4-colourable induced subgraph of `U` has at least 509 vertices,
> and this is sharp because either 509-point placement is 5-chromatic.

Thus superposing these two nonisomorphic exceptional placements cannot improve
the 509-vertex record, even though the union supplies 109 additional unit
edges.  This is a negative result about one precise construction family.  It
does not exclude non-induced edge selections with new coordinates, other
placement unions, translations, reflections, or delete-and-repair schemes.

## Certificate argument

Write `V(U)=F disjoint-union R`, where `|F|=489` and `|R|=36`.

1. For every `v in F`, the certificate gives an explicit proper 4-colouring
   of `U-v`.  Consequently every non-4-colourable induced subgraph of `U`
   must contain all of `F`.
2. The certificate gives 133 subsets `D` of `R`, each with an explicit proper
   4-colouring of `U-D`.  Hence the optional part of any non-4-colourable
   induced subgraph must hit every such `D`.
3. A solver-free exhaustive branch search proves that these 133 sets have no
   transversal of size at most 19.  It visits 3,023 search nodes.  A size-20
   transversal is supplied by the optional vertices of the identity
   placement.  The transversal number is therefore exactly 20.

It follows that a non-4-colourable induced subgraph has at least
`489+20=509` vertices.  No negative SAT answer is used in this lower-bound
argument: its evidence consists entirely of directly checked colourings and a
small, independently rerun finite-set enumeration.

The 525 points are reconstructed over
`Q(sqrt(3),sqrt(5),sqrt(11))`.  The verifier represents each coordinate by
eight integer coefficients at common denominator 192, and compares squared
distances exactly.  It uses no floating-point geometry and includes every unit
pair.

## Fast verification

The verifier uses only the Python 3.11 standard library.  Run it from this
directory:

```bash
python3 verify.py
```

Expected output is recorded in `expected_check.txt`.  The verified headline
values are:

```text
vertices=525
edges=2551
shared_vertices_between_placements=493
forced_vertices=489
free_vertices=36
minimal_killing_sets=133
transversal_number=20
minimum_non_four_colorable_order=509
edge_sha256=4f7a2472d60aa0835a256b51dc9d1e3eb050b3e575bb41fa814961ce48496a47
```

`verify.py` also checks 1,577,939 edge incidences across all colouring
witnesses.  The compact certificate SHA-256 is
`85ea2050dbc6ff05b2766f899e86ba3b9157e4aa59cc6ef21f54f7531941c728`.

## Full regeneration

The discovery search uses PySAT only to generate positive colour witnesses
and candidate hitting sets.  Keep generated checkpoints outside the
repository:

```bash
python3 -m venv /scratch/parts509-union-venv
/scratch/parts509-union-venv/bin/pip install -r requirements.txt

/scratch/parts509-union-venv/bin/python classify_deletions.py \
  /scratch/parts509-union-forced.json

/scratch/parts509-union-venv/bin/python search_transversal.py \
  /scratch/parts509-union-forced.json \
  /scratch/parts509-union-ihs.json \
  --seed 1 --layers 1 --improve 0

python3 build_certificate.py \
  /scratch/parts509-union-forced.json \
  /scratch/parts509-union-ihs.json \
  /scratch/parts509-union-certificate.json

python3 verify.py /scratch/parts509-union-certificate.json
```

With Python 3.11.8, `python-sat 1.8.dev24`, and CaDiCaL 1.9.5, the tested
seed produced 211 raw killing sets in 212 rounds and 422 SAT calls.  Removing
supersets leaves the committed 133-set family.  Regeneration is deterministic
with that stack; in a fresh replay the compact certificate had exactly the
committed SHA-256 above.  Different valid solver witnesses are harmless if the
resulting certificate passes `verify.py`.

## Trust boundary

- Exact geometry and witness checking trust CPython integer arithmetic, the
  small eight-coordinate field implementation in `verify.py`, and the pinned
  sibling `points.tsv` bytes.  The point-file SHA-256 is
  `f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50`.
- The 489 deletion colourings, 133 killing-set colourings, and the transversal
  lower bound are checked without a SAT or optimization solver.  PySAT,
  CaDiCaL, and RC2 are outside this part of the verification trust boundary.
- Sharpness at 509 uses event 789, whose old-label strict edge list is checked
  to have the certified Parts edge hash
  `5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c`.
  Its non-4-colourability depends on the sibling Parts criticality artifact and
  its separately documented DRAT audit.  This verifier pins that artifact's
  certificate SHA-256 to
  `d354f9629c41639168b80fc1aa6feb6e4187dd37dee7efcb83b4ef6ebe68d16c`.
- The theorem uses the strict geometric graph: coordinate coincidences are
  merged and all exact unit pairs, including inter-placement pairs, are edges.

## Provenance and scope

The gadget split, coordinates, and record construction come from Jaan Parts,
*Graph minimization, focusing on the example of 5-chromatic unit-distance
graphs in the plane*, Geombinatorics 29(4) (2020), 137--166,
<https://arxiv.org/abs/2010.12665>.  Event numbering and the completeness of
the six exceptional `K`-rational placements come from the sibling
`hadwiger_nelson_parts509_rotation_scan` artifact.

No claim is made that the two drawings, their superposition, or the abstract
criticality facts were previously unknown.  The contribution is the exact
minimum-order theorem for this explicitly defined strict union and its compact
solver-independent lower-bound certificate.

## Files

- `verify.py` reconstructs the geometry, checks every colouring, and proves
  the transversal lower bound.
- `certificate.json` is the compact proof witness.
- `classify_deletions.py` generates the `U-v` search checkpoint.
- `search_transversal.py` performs the implicit hitting-set search.
- `build_certificate.py` removes redundant killing sets and packs witnesses.
- `requirements.txt` pins the discovery-time PySAT version.
- `expected_check.txt` records the verifier's exact output.
