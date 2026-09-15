# Universal extension for the fixed G19–F29 translation

The exact union of the 19-point Moser/palette private bridge **G19** with the
native frozen-centre graph **F29 translated by +i** has **45 distinct points
and 107 complete unit edges**. Every proper four-colouring of G19 extends to
this entire graph. Thus this driver gives **no relation gain**, on the original
ten terminals or on any other subset of the original 19 points. The union is
four-chromatic and is not a five-chromatic construction or record candidate.

This freezes and retires one selected physical attachment. It does not classify
other placements of F29 or other drivers of G19. The positive G19 theorem is
unaffected; the next construction needs a different, explicitly justified
interaction rather than an enlargement of this frame.

The geometry is

```text
G19 unchanged;
F29 vertex j -> native F29 vertex j + i.
```

The 48 raw labels merge in precisely these three places:

| F29 label | G19 label | Role in G19 |
|---:|---:|---|
| 0 | 11 | retained private palette cap P1 |
| 25 | 15 | palette terminal X1 |
| 28 | 16 | palette terminal Y1 |

These points form a unit triangle. There are 106 distinct inherited edges
(34 + 75 − 3), and exactly one additional contact: **G19 vertex 7 to translated
F29 vertex 22**, which has merged label 40. All 990 unordered point pairs are
checked exactly; no contact or collision is decided by a numerical tolerance.

Two proper F29 four-colour words suffice to prove universal extension:

```text
03011122222033313210001121332
03011122222033313210003121332
```

Both give colours `(0,1,2)` to F29 vertices `(0,25,28)`. They differ only at
vertex 22, where their colours are 1 and 3. Normalize the colours of any given
G19 colouring on the shared triangle to `(0,1,2)`. At least one of these two
words avoids the given colour of G19 vertex 7 at the sole new contact. Undo the
normalization and merge. This works for every old colouring. The checker also
verifies all 24 named triangle assignments and four choices for vertex 7,
covering 96 boundary assignments without an assumption on the old relation.

The inherited-edge union and the complete unit graph therefore both preserve
the complete G19 relation. Using the previously independently accepted G19
census, the ten-terminal projection still contains **11,624 canonical patterns
and 278,496 named assignments**. No new terminal census is needed for this
consequence: the extension proof preserves every full source colouring.

The directly checked whole-graph words are

```text
four colours: 120102302100012211232011230221213132132120033
five colours: 420102302100012211232011230221213132132120033
```

The second uses all five colours; it is not a chromatic lower bound. The
inherited Moser spindle supplies the lower bound four.

## Reproduction and proof boundary

Use Python 3.11 or later, standard library only, from this directory:

```bash
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
python3 -B controls.py
python3 -B produce.py --out /tmp/g19-f29-fresh.json
cmp certificate.json /tmp/g19-f29-fresh.json
sha256sum -c SHA256SUMS
```

Choose an unused output path for regeneration. Expected headline:
`UNIVERSAL_EXTENSION_DRIVER_RETIRED`. Verification takes about one second on
the author's host; controls take about six seconds.

`produce.py` constructs G19 in a flat exact monomial algebra and adds the 29
translated points. `verify.py` uses a separate quadratic-tower multiplication,
checks the source geometry from its cap/diamond identities, reconstructs every
collision and unit edge, and checks both extension words and the global colour
words. It imports no producer code. The controls compare the two arithmetic
implementations on all 990 distance rows and reject six corrupted certificates.
The normal and optimized checks agree, and regeneration is byte-identical.

All coordinates use

```text
s = sqrt(3), t = sqrt(11), y = sqrt((4-s)/2), positive real roots;
s^a t^b y^c, indexed a + 2b + 4c, a,b,c in {0,1}.
```

This is a basis of degree eight. In Q(sqrt(3)), 11 is not a square. For
`h=2-s/2`, neither h nor h/11 is a square there: their rational norms are
13/4 and 13/484, both nonsquares. A square in Q(sqrt(3),sqrt(11)) lying in
Q(sqrt(3)) must be a square or 11 times a square in the smaller field.
Therefore adjoining y doubles the degree. Equality of displayed rational
coefficient vectors is exact equality of these real coordinates.

The trust boundary is this elementary field argument, the explicit colouring
extension argument, Python's exact rational arithmetic, and ordinary hardware.
This attachment has author verification, not an independent review or a
proof-assistant formalization. No external solver, hidden input, numerical
filter, or omitted proof trace is required.

## Provenance and campaign scope

The selected driver was frozen before its exact contact gate. Its rationale
was to introduce F29's demonstrated frozen-centre palette obstruction at a
private vertex of G19. The full geometry reveals that the remaining coupling
is only the flexible single contact above, which defeats that rationale.
The 508-point cap was never at risk; failure is chromatic neutrality.

The source G19 coordinates and generator derive from
[the original private-bridge package](https://github.com/helgithorskarp/math_results/blob/2e26eadaa928d089c86462f567e3e29dfa9f0511/hadwiger_nelson_moser_palette_private_bridge/README.md),
commit `2e26eadaa928d089c86462f567e3e29dfa9f0511`.
Its independent acceptance and contact-subset refinement are in
[the independent review](https://github.com/helgithorskarp/math_results/blob/375c085a03163307ba8abacf8e6cc1ba6d805647/hadwiger_nelson_moser_palette_private_bridge_review1/README.md),
commit `375c085a03163307ba8abacf8e6cc1ba6d805647`.
The native F29 table is copied byte for byte from
[its frozen-centre source](https://github.com/helgithorskarp/math_results/blob/ef05942eeebba29628dc02f37a5792ac7d4122b8/hadwiger_nelson_frozen_centre_transfer/points.tsv),
commit `ef05942eeebba29628dc02f37a5792ac7d4122b8`.
`source_g19.json` retains only the old geometric data needed by this proof.

Primary sources checked on 2026-09-15 still give Parts's
[509-point, 2,442-edge graph](https://arxiv.org/abs/2010.12665) as the
[unrestricted vertex record](https://arxiv.org/html/2608.04542v4).
This negative result changes neither that record nor the global
Hadwiger–Nelson bounds.

The Discovery index remains stale at 4363/RPC 4364. This result is published as
compact repository evidence without another Discovery submission. The earlier
G19 source's CheckTx-5 rejection and the review's accepted-but-pending receipt
remain distinct; neither is represented as committed evidence.
