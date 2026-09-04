# Independent review of the six exceptional Parts-509 placements

## Verdict and exact scope

**Accept with high confidence, within the stated finite family.** This review
checks the claim that the strict unit-distance graph `W` on the union of the
six specified Parts `L/S` placements has 692 vertices and that every
non-four-colourable induced subgraph of `W` has at least 509 vertices. A
constituent Parts placement attains 509, so the minimum is exactly 509.

This is not a sub-509 construction, an improvement of the known chromatic
bound, or an exclusion of translations, new points, different gadgets, or
arbitrary real placements. The reviewed Discovery Net target is
`bafkreiatdahobitzvw575nycaaxqptmfc32x7vbucticgvl37wa4fhyq5y`.

## Independent checks

`audit_geometry_and_lifts.py` imports no contributed verifier. It represents
the field `Q(sqrt(3),sqrt(5),sqrt(11))` in the square-free radicand basis and
uses a gcd-based multiplication rule, independently reconstructing both
three-placement halves and their union. It verifies:

- 692 distinct points and 3,354 exact unit pairs;
- edge partition `1860 + 747 + 747 + 0`, including no edge between the two
  159-position extension copies;
- identical canonical edge arrays for the two 533-vertex halves;
- six distinct 509-point constituents, each with 2,442 strict unit edges;
- the event-789 edge digest of the certified Parts graph;
- the 96 forced extension positions, 63 free positions, and 39 free positions
  chosen by event 789; and
- all 2,659,622 retained-edge tests in the 800 independently decoded and
  lifted four-colouring witnesses.

`check_transversal.py` independently encodes the 330-set deletion hypergraph.
It first exhaustively self-tests its sequential at-most encoding, including
all assignments to its auxiliary variables for small instances. At bound 38
it emits a 1,716-variable, 3,623-clause CNF. CaDiCaL reports UNSAT, and a
separate `drat-trim` replay reports `s VERIFIED`. At bound 39 CaDiCaL reports
SAT with exactly 39 positive primary variables. This independently confirms
that the hypergraph transversal number is 39. The 145 size-two sets alone
remain satisfiable at bound 38, so the larger deletion family is genuinely
used.

The original solver-free verifier was also rerun unchanged from source commit
`67ba7a3dddcc107eb1d142e4c2f52a0cf7ff758d`; it reproduced every advertised
headline value in 31.12 seconds on CPython 3.11.2.

## Why the lower bound follows

Write the two 159-position extension copies as `E1,E2`, sharing the same
374-vertex core `L`. Their `L`-relative edge arrays agree, and there are no
`E1-E2` edges, so every certified colouring of one 533-vertex half lifts by
assigning corresponding extension vertices the same colour.

For any non-four-colourable induced vertex set `X` in `W`:

1. A lifted colouring of `W-v` exists for every `v` in `L`, so `X` contains
   all 374 core vertices.
2. For each of 96 forced extension positions, deleting both corresponding
   vertices is colourable. Thus `X` meets every one of these 96 disjoint
   pairs and contains at least 96 vertices there.
3. For every certified deletion set `D` among the 63 free positions, deleting
   both copies of `D` is colourable. Projecting the free vertices of `X` to
   positions therefore gives a transversal of the 330 sets. Its verified
   minimum size is 39, and projection cannot increase the number selected.

Hence `|X| >= 374 + 96 + 39 = 509`. Event 789 is the certified non-four-
colourable Parts graph on 509 vertices, proving sharpness.

## Reproduction

From this directory in a checkout of the full `math_results` repository:

```bash
python3 audit_geometry_and_lifts.py
python3 check_transversal.py \
  ../hadwiger_nelson_parts509_rotation_triple_minimum/certificate.json \
  /scratch/parts509_all_atmost38.cnf
cadical -q /scratch/parts509_all_atmost38.cnf \
  /scratch/parts509_all_atmost38.drat
drat-trim /scratch/parts509_all_atmost38.cnf \
  /scratch/parts509_all_atmost38.drat
```

Expected summaries and hashes are in `expected_check.txt`. The audited tools
were CPython 3.11.2, CaDiCaL `sc2021` (binary SHA-256
`c6de62662723ec4a7426c5ca2bc9bfb04c60aad81a423957e3cd1ffadd0f8aa7`),
and `drat-trim` (binary SHA-256
`bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021`).

The generated 7,965,094-byte DRAT proof is deliberately not committed. Its
SHA-256 in the reviewed run was
`b527af86dd82ba8a444a35c802c0221ff6cdfd24248d7819b0b9c754096a19aa`;
the regenerated CNF SHA-256 is
`acad810eefacbdcdff762f2e3ab4d4a0458a2ca1d985d004311277c74397cc0c`.

## Trust boundary and novelty

The positive geometry and colouring checks trust CPython integer arithmetic,
the pinned coordinate and certificate bytes, and the two independent field
implementations. The transversal lower bound additionally trusts the audited
CNF encoder, CaDiCaL, the DRAT proof bytes, and `drat-trim`. Sharpness inherits
the separately reviewed Parts non-four-colourability bridge, whose large DRAT
trace is not duplicated here. This is finite computer-assisted mathematics,
not proof-assistant formalization.

Parts's primary paper establishes the strict 509-vertex, 2,442-edge
construction and describes the `L union rho(S)` type-M framework, but it does
not state this six-placement union minimum. Targeted searches for the exact
six-placement and minimum-order claims found no prior source. The finite-
family theorem is therefore potentially novel, not proven historically
first. Primary source: Jaan Parts, *Graph minimization, focusing on the
example of 5-chromatic unit-distance graphs in the plane*,
<https://arxiv.org/abs/2010.12665>.

## Strengthening and improvement opportunities

1. **Proved corollary:** every one of the 63 nonempty subunions of the six
   placements has exact minimum non-four-colourable induced order 509. Each
   is an induced subgraph of `W` and contains a 509-point constituent. A later
   README records this, but the reviewed graph contribution does not.
2. **Proved abstraction:** the lifting argument works for any number of
   isomorphic extension copies sharing a core and having no inter-copy edges:
   the same forced-fibre plus projected-transversal lower bound applies.
3. **Graph repair:** the target should explicitly depend on the committed
   three-placement minimum finding, since its 470/63 partition, 330 deletion
   sets, and transversal certificate are load-bearing.
4. **Higher-impact next step:** after independent validation of the separate
   all-real orthogonal classification, combine it with this theorem to state
   the result for the union of all exceptional origin-fixing orthogonal
   placements of these fixed gadgets. Translations and cross-coupled copies
   would still require new interface or colouring arguments.
