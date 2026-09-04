# Exact minimum inside a three-placement Parts-509 union

## Result

Let `L={0,...,373}` and `S={374,...,508}` be the two gadgets in Jaan
Parts's 509-point construction. This directory studies the strict
unit-distance graph `U` on

\[
 L\;\cup\;R(-1/2,-\sqrt3/2)S\;\cup\;R(-1/2,+\sqrt3/2)S\;\cup\;S.
\]

These are events 108, 109, and 789 in the sibling exact rotation
classification. Each pair of placements shares 493 points, while all three
share 485. Thus `U` has 533 distinct points. Exact reconstruction gives 2,607
unit pairs. The certified theorem is:

> Every non-4-colourable induced subgraph of `U` has at least 509 vertices,
> and this is sharp because each constituent placement has 509 vertices.

Therefore superposing this complete compact cluster of three exceptional
placements cannot improve the 509-vertex record, despite adding 165 strict
unit edges to the identity placement. This is a negative result about one
precise construction family. It does not exclude other placement unions,
translations, reflections, new coordinates, non-induced edge selections, or
delete-and-repair constructions.

## Certificate argument

Write `V(U)=F disjoint-union R`, where `|F|=470` and `|R|=63`.

1. For every `v in F`, the certificate gives an explicit proper 4-colouring
   of `U-v`. Consequently every non-4-colourable induced subgraph of `U` must
   contain all of `F`.
2. The certificate gives 330 subsets `D` of `R`, each with an explicit proper
   4-colouring of `U-D`. Hence the optional part of any non-4-colourable
   induced subgraph must hit every such `D`.
3. A solver-free exhaustive branch search proves that these 330 sets have no
   transversal of size at most 38. It visits 73,946 search nodes. The 39
   optional vertices in the identity placement hit every `D`, so the
   transversal number is exactly 39.

It follows that a non-4-colourable induced subgraph has at least
`470+39=509` vertices. No negative SAT answer is used in this lower-bound
argument: the evidence consists of directly checked colourings and a small,
independently rerun finite-set enumeration.

The 533 points are reconstructed over
`Q(sqrt(3),sqrt(5),sqrt(11))`. The verifier represents each coordinate by
eight integer coefficients at common denominator 192 and compares squared
distances exactly. It uses no floating-point geometry and includes every unit
pair.

## Fast verification

The verifier uses only the Python 3.11 standard library. Run it from this
directory:

```bash
python3 verify.py
```

Expected output is recorded in `expected_check.txt`. The verified headline
values are:

```text
vertices=533
edges=2607
pairwise_shared_vertices=493,493,493
shared_vertices_all_three=485
forced_vertices=470
free_vertices=63
minimal_killing_sets=330
transversal_number=39
minimum_non_four_colorable_order=509
edge_sha256=cc3f6ad98f3d1198b6bde17628326d690b17789bd880f84303a2c6ff58be454f
```

`verify.py` also checks 2,071,951 edge incidences across all colouring
witnesses. The compact certificate SHA-256 is
`fdbcc767159a8b72d70515dce516775b83c03db5f2a79e956e3877bec8274df9`.

## Full regeneration

PySAT is used only to discover positive colouring witnesses and candidate
hitting sets. Keep generated checkpoints outside the repository:

```bash
python3 -m venv /scratch/parts509-triple-venv
/scratch/parts509-triple-venv/bin/pip install -r requirements.txt

/scratch/parts509-triple-venv/bin/python classify_deletions.py \
  /scratch/parts509-triple-forced.json

/scratch/parts509-triple-venv/bin/python search_transversal.py \
  /scratch/parts509-triple-forced.json \
  /scratch/parts509-triple-broad.json \
  --seed 1 --layers 1 --improve 0 --max-rounds 544

/scratch/parts509-triple-venv/bin/python search_target508.py \
  /scratch/parts509-triple-forced.json \
  /scratch/parts509-triple-broad.json \
  /scratch/parts509-triple-target.json \
  --seed 3 --chains 1 --improve 25

python3 build_certificate.py \
  /scratch/parts509-triple-forced.json \
  /scratch/parts509-triple-target.json \
  /scratch/parts509-triple-certificate.json

python3 verify.py /scratch/parts509-triple-certificate.json
```

With Python 3.11.8, `python-sat 1.8.dev24`, and CaDiCaL 1.9.5, the tested
run first accumulated 544 broad killing sets. The target-cardinality phase
then tested 304 distinct 508-vertex candidates, all colourable, and stored 848
raw killing sets before its master closed. Removing supersets leaves the 330
sets in the committed certificate. A fresh run may return different valid
solver colourings; the result is accepted only if the solver-free verifier
passes.

## Trust boundary

- Exact geometry and witness checking trust CPython integer arithmetic, the
  small eight-coordinate field implementation in `verify.py`, and the pinned
  sibling `points.tsv` bytes. The point-file SHA-256 is
  `f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50`.
- The 470 deletion colourings, 330 killing-set colourings, and the transversal
  lower bound are checked without a SAT or optimization solver. PySAT,
  CaDiCaL, and RC2 are outside this part of the verification trust boundary.
- Sharpness at 509 uses event 789, whose identity-labelled strict edge list is
  checked against the certified Parts edge hash
  `5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c`.
  Its non-4-colourability depends on the sibling Parts criticality artifact
  and its separately documented DRAT audit. This verifier pins that
  artifact's certificate SHA-256 to
  `d354f9629c41639168b80fc1aa6feb6e4187dd37dee7efcb83b4ef6ebe68d16c`.
- The theorem uses the strict geometric graph: coordinate coincidences are
  merged and all exact unit pairs, including inter-placement pairs, are
  edges.

## Provenance and scope

The gadget split, coordinates, and record construction come from Jaan Parts,
*Graph minimization, focusing on the example of 5-chromatic unit-distance
graphs in the plane*, Geombinatorics 29(4) (2020), 137--166,
<https://arxiv.org/abs/2010.12665>. Event numbering and the completeness of
the six exceptional `K`-rational placements come from the sibling
`hadwiger_nelson_parts509_rotation_scan` artifact.

No claim is made that the drawings, their superposition, or the abstract
criticality facts were previously unknown. The contribution is the exact
minimum-order theorem for this explicitly defined strict union and its compact
solver-independent lower-bound certificate.

## Files

- `verify.py` reconstructs the geometry, checks every colouring, and proves
  the transversal lower bound.
- `certificate.json` is the compact proof witness.
- `classify_deletions.py` generates the `U-v` checkpoint.
- `search_transversal.py` accumulates a broad initial killing-set family.
- `search_target508.py` performs the target-cardinality CEGAR search.
- `build_certificate.py` removes redundant killing sets and packs witnesses.
- `requirements.txt` pins the discovery-time PySAT version.
- `expected_check.txt` records the verifier's exact output.
