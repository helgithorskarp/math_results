# Two exact fresh-centre exchange families are four-colourable through order 508

This package closes two concrete non-Parts construction supports based on
Heule's exact 510-point unit-distance graph `H510` and whole-plane completion
centres from the published exact census:

| added centre IDs | parent points | strict unit edges | old attachment degrees |
|---|---:|---:|---:|
| `319` | 511 | 2,510 | 6 |
| `1074,1269` | 512 | 2,518 | 7 and 6 |

The centres in the second row are themselves unit-separated.  Their old
neighbourhoods have 12 distinct H510 points; centre 412 is the sole common
old neighbour.  Centre 319 is outside the earlier closed 553-point
Parts/Heule union and parked 1,111-point ambient.  Centre 1269 is also outside
those ambients, so the second support is not contained in the independently
closed H517 support.

**Exact computer-assisted result.** For each support and every old H510
vertex `v`, the certificate gives a proper four-colouring after deleting
`v`.  Consequently every subgraph of either support on at most **508**
vertices is four-colourable: it must omit at least one of the 510 old
vertices, and the corresponding word restricts to it.  This includes all
508-point exchanges

```text
(H510 - three old points) + centre 319
(H510 - four old points) + centres 1074 and 1269.
```

This is a fixed-support exclusion, not a global theorem and not a record
improvement.  It says nothing about the other 119 fresh centres, different
multi-centre supports, geometric deformations, or points outside the exact
census.  The current published comparison remains Parts's 509-point graph.

## Exact physical gate

Coordinates lie in

```text
Q(sqrt(3),sqrt(5),sqrt(11))
```

in the ordered basis

```text
1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165).
```

The solver-free checker reads the hash-pinned H510 coordinates and fresh
centre rows, proves all physical points distinct, and rebuilds the complete
unit edge set from every point pair by rational coefficient comparison.  It
does not trust archived neighbour lists to define either graph.  This gives
exactly the two point/edge counts above and verifies the mutual fresh edge in
the second support.

[`certificate.json`](certificate.json) contains 1,020 packed colour words,
one for each old-vertex deletion in each support.  Four colours need two bits,
so each word occupies 128 bytes before base64 encoding.  The verifier decodes
every word, checks its unique implicit omission, and checks **2,554,245**
retained edge inequalities.  The 188,207-byte certificate has SHA-256
`f5ca4de28bf9739598310d61af69ff5748a7b1690e1a1aa7b59ef8d50cfb73b6`.
The canonical unpacked streams have SHA-256

```text
centre 319:       02cfccea990e81d363cf81abc193f264be3eba8dd1b0125a02ca41120153ae5f
centres 1074,1269: 3cca81897da3e5e0f4ca6c9affac000c73189c6a6cae672a057fc791d1f10876
```

The logical order bound uses only these positive colourings and restriction.
It does not import H510's non-four-colourability, any SAT UNSAT answer, or a
completeness assumption about a colouring library.

## Reproduction

CPython 3.11 or later and its standard library suffice for the proof replay:

```sh
python3 -B hadwiger_nelson_heule_fresh_exchange_cover/verify.py --check-expected
python3 -O -B hadwiger_nelson_heule_fresh_exchange_cover/verify.py --check-expected
python3 -B hadwiger_nelson_heule_fresh_exchange_cover/controls.py
sha256sum -c hadwiger_nelson_heule_fresh_exchange_cover/SHA256SUMS
```

Optional witness regeneration uses `python-sat==1.8.dev17` and CaDiCaL 1.9.5:

```sh
python3 -m venv /tmp/hn-fresh-exchange-env
/tmp/hn-fresh-exchange-env/bin/pip install -r \
  hadwiger_nelson_heule_fresh_exchange_cover/requirements.txt
/tmp/hn-fresh-exchange-env/bin/python -B \
  hadwiger_nelson_heule_fresh_exchange_cover/produce.py \
  --out /tmp/hn-fresh-exchange-certificate.json
cmp /tmp/hn-fresh-exchange-certificate.json \
  hadwiger_nelson_heule_fresh_exchange_cover/certificate.json
```

The producer uses activated four-colour formulas, with all 510 old activation
values fixed on every query and the first fresh centre normalized to colour
zero.  At-most-one clauses are unnecessary: each active vertex has a nonempty
true-colour set and adjacent sets are disjoint, so selecting one true colour
per vertex gives a proper colouring.  The public checker nevertheless uses
only the selected explicit colour, not this encoding argument.

The discovery runs made 510 SAT calls per support, with a 200,000-conflict
per-query cap.  There were no UNSAT or UNKNOWN outcomes.  CaDiCaL used
1,261,297 conflicts for centre 319 and 1,245,440 for the pair.  Search timings
were about 307 and 311 seconds on one thread.  These operational figures are
not proof premises.

Remaining trust lies in the hash-pinned coordinate sources, elementary
independence of the radical basis, Python exact arithmetic and complete finite
loops.  The checker is author-run, not independent-author review or formal
proof-assistant verification.

## Construction decision

The first isolated degree-six centre and the strongest adjacent fresh pair
by distinct old-neighbour count both fail more strongly than the original
508-point exchange question: deleting **any one** old point restores a checked
four-colouring.  Further isolated-centre sampling is therefore not proposed.
A successor should change the forcing core or use a coupled fresh component
whose interaction is not already dominated by singleton deletion witnesses.
