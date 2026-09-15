# A 34-point frozen-centre/bowtie palette coupler

One private unit contact gives a strict, completely determined joint
four-colour relation on an exact **34-point, 82-edge** plane graph. The
canonical joint relation shrinks from **613,080 to 490,464 patterns**, a
loss of **122,616 (20%)**. Both isolated component projections remain full.
The complete graph has chromatic number **four**.

This is a local physical coupler, not a five-chromatic construction or a
record improvement. No Parts receiver has been chosen or tested. The source
is banked at this exact relation boundary; the count alone supplies no
justification for a copy, phase, amplifier or receiver sweep.

## Construction and complete relation

Use the exact frozen-centre source F29 in [source29.tsv](source29.tsv), with
private centre 0 and its 14 marked neighbours

```text
4,5,6,7,9,10,12,14,15,17,18,22,25,28.
```

Independently form a bowtie from two unit equilateral triangles sharing a
private centre. In complex coordinates set

```text
b = i,   u = (3+4i)/5,   rho = (1+i sqrt(3))/2.
B = (b, b+u, b+u*rho, b-u, b-u*rho).
```

Append these as points 29 through 33. Mark the four leaves, indices 30--33.
The source and bowtie are disjoint. Exact reconstruction of all **561**
unordered pairs finds 75 source edges, six bowtie edges and exactly one
cross edge, **0--29**. Both endpoints of this contact are private: there is
no shared origin, terminal identification or terminal-to-terminal cross edge.

For a terminal colouring let P be the set of colours used on the F29
neighbours and Q the set used on the bowtie leaves. On the product of the
isolated unrestricted source relations, the complete physical relation is
exactly

```text
P != Q.
```

F29 forces |P|=3. The bowtie leaves use two or three colours. Thus the new
contact forbids precisely the case in which both palettes are the same
three-colour set. Removing that unit edge from the **comparison graph**
restores the entire product relation; that comparison graph is not claimed
to be the complete strict graph on these coordinates.

[PROOF.md](PROOF.md) explains the exhaustive input census, factorization,
colour normalization and limits. [certificate.json](certificate.json)
contains an isolated-product pattern that fails on the union, a literal
proper four-colouring of the union, and a proper five-colouring that realizes
that same forbidden terminal prescription. The latter is a conditional
witness and does not prove ordinary five-chromaticity.

## Reproduction

CPython 3.11 or later; standard library only. From the repository root:

```sh
python3 -B hadwiger_nelson_frozen_bowtie_palette_coupler/verify.py --check-expected
python3 -O -B hadwiger_nelson_frozen_bowtie_palette_coupler/verify.py --check-expected
python3 -B hadwiger_nelson_frozen_bowtie_palette_coupler/controls.py
python3 -B hadwiger_nelson_frozen_bowtie_palette_coupler/produce.py \
  --compare hadwiger_nelson_frozen_bowtie_palette_coupler/EXPECTED.json
```

The verifier takes about one second on the author host. The independent
producer uses different radical multiplication, terminal enumeration and
colour search algorithms; its source-pattern and complete-distance hashes
agree with the verifier. The proof code uses explicit exceptions, including
under `-O`. Controls compare its complete search with brute force on 5,184
small graph/domain cases, first accept the valid certificate, and reject four
semantic corruptions. See [VALIDATION.json](VALIDATION.json).

Optional `produce.py --table /tmp/f29-relation.tsv` regenerates all 5,109
positive source patterns and extension words. That generated table and the
large joint table are unnecessary public inputs: the complete census and
local 256-case truth table are replayed from source. No SAT library, unchecked
UNSAT response, floating-point incidence or omitted proof file is used.

## Provenance and construction limit

The F29 coordinate fixture is byte-identical to the
[earlier frozen-centre source](../hadwiger_nelson_frozen_centre_transfer/README.md)
at commit `ef05942eeebba29628dc02f37a5792ac7d4122b8`; its SHA-256 is
`3631210e31697804a86437cc7b6f734870097e22de50e5c4721ecea6ab633924`.
That source derives from Polymath16. This package rechecks the entire source
relation needed here and does not import its previous computational proof.
The private-centre palette-complement argument is elementary; no priority
or minimum-size claim is made. Both implementations were run by the author,
not by an independent reviewer.

The physical support fits the campaign's 508-point cap, but the demonstrated
loss is on an 18-terminal joint interface, with both marginals unchanged.
Joining disjoint four-colourable components by a bridge always leaves a
four-colouring after colour renaming. A future construction therefore needs
additional compatible forcing beyond this bridge join. No named receiving
frame, excluded receiver pattern, finite residual leading to non-four, or
cap-feasible finishing construction is supplied. Both Parts receiver
specifications remain banked. This is useful exact local information, with
no demonstrated reduction of the smallest five-chromatic plane graph.
