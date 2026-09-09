# Exact frontier returned to HN3

HN2 retains synthesis, physical realization, chromatic testing, and candidate
ownership. This milestone completely closes one named subset of the existing
A5 architecture: the six first-step binomial anchor circles. This exclusion
holds at **every** active count. No second parameter locus or support-profile
search is started in this pass.

## Reusable parameter condition

For every possible non-four-colourable member, all six equations
`|1+epsilon*z|=1` must fail, where epsilon ranges over the Eisenstein units.
In the original 2,797-curve inventory, the excluded curve IDs are

```
591, 592, 1277, 1278, 2208, 2209.
```

Writing z=x+i sqrt(3)y, these are the respective zero sets:

| ID | exact polynomial |
|---|---|
| 591 | x^2+3y^2-x-3y |
| 592 | x^2+3y^2+x-3y |
| 1277 | x^2+3y^2-x+3y |
| 1278 | x^2+3y^2+x+3y |
| 2208 | x^2+3y^2-2x |
| 2209 | x^2+3y^2+2x |

The inventory SHA-256 is
`85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9`.
The set is invariant under the named physical D3 action. Any active-set,
pair-system, or exact-five-pencil search may exclude these curves globally
for non-four candidates. This is a chromatic exclusion, not a claim that
the circles have no physical points or no common intersections.

The two 243-point, 603-edge, eight-active fixtures at
`z=+/-(-1+i sqrt(7))/4` provide exact concrete chromatic decisions. Their
coordinates and all unit edges are independently checked in `physical.py`.
They are exactly three-chromatic.

## Composition with h4177 and h4181

Use h4177's original pair/stabilizer rows, first applying h4181's 192
exact-five-to-at-least-six moves. This yields the previous baseline of
131,356 whole pair systems with allowance 3,846,704. The present consumer
performs two distinct transformations:

1. Delete all 424 global pair rows incident to an excluded anchor curve.
   They account for allowance 3,012. Of these rows, 400 were exact-five
   compatible and 24 were already in at-least-six mode.
2. Among retained exact-five rows, move the 4,784 whose unique affine pencil
   contains the first-coordinate normal e1 to at-least-six mode. Their
   allowance is 146,256. These rows are **retained** in the global frontier.

The second step follows because every realized e1 section has nonzero
constant and its bucket consists of excluded anchor curves. Two nonparallel
affine signatures determine their unique full five-pencil, so a pair cannot
obtain a different exactly-five cover. This does not exclude the pair when
six or more other curves are active.

| mode | pair systems | possible non-four orbit allowance |
|---|---:|---:|
| exact-five compatible | 123,240 | 3,614,164 |
| requires at least six active curves | 7,692 | 229,528 |
| whole frontier | 130,932 | 3,843,692 |

Allowance means the conservative sum of floor(2kl/|Hq|), including
intersection multiplicity. It is not a count of distinct physical roots.
The count imports h4117 quotient completeness and h4175 free action through
h4177; this package does not independently review those dependencies. No
simultaneous chamber restriction is imposed on globally canonical pairs.

## Complete exact-five-pencil effect

Exactly 243 realized five-pencils contain the e1 section. Among them, 27
were already closed by h4181. The 216 newly closed pencils have 3,760,128
raw curve lifts and **3,354,048** lifts surviving the accepted h4167
constraints. There remain **5,112** realized exact-five pencils and
**128,871,936** surviving lifts. This is an exclusion from the accepted
h4171 finite classification, not an increasing active-count search.

The consumer independently constructs F4 pencil spans and enumerates the
selected lifts with the pinned incidence exclusions. All six exported
row/pencil arrays agree entrywise with the pilot based on HN3's original
span and bitmask lift counter. Detailed hashes are in `FRONTIER_EFFECT.json`.

## Reproduction and durable interface

From the repository root, standard-library Python suffices:

```sh
python3 -B hadwiger_nelson_radix_five_active_orbits/produce.py \
  --out /tmp/hn-anchor-source-orbits.json \
  --export-interface /tmp/hn-anchor-source-interface.json
python3 -B hadwiger_nelson_radix_incidence_geometry/verify.py \
  --export-interface /tmp/hn-anchor-incidence.json
python3 -B hadwiger_nelson_radix_first_step_anchor/frontier.py \
  --interface /tmp/hn-anchor-source-interface.json \
  --incidence /tmp/hn-anchor-incidence.json \
  --export-interface /tmp/hn-anchor-frontier.json --check-expected
```

Output paths must not exist. The exact input canonical hashes are checked
by the consumer. The new regenerable interface has canonical SHA-256
`5496087ac2e75104443c73022ec58bdcc71bb3bafb4605c79aed487fdd3f1da3`.
It contains excluded curve IDs, removed pair rows, mode-moved rows, both
remaining modes, all 216 new pencil signatures, and lift counts per pencil.
Rows retain the h4177 format `[curve_a,curve_b,stabilizer_mask,2kl,allowance]`.
The bulky explicit table is intentionally kept outside the repository.

The concrete complementary interface for HN3 is to check/consume these six
global curve exclusions and the resulting unique-pencil mode transformation,
and carry the remaining parameter/embedding frontier forward. HN3 need not
repeat physical colouring on the closed anchor circles. Team-internal checks
remain separate from reviewer-1's independent verdict. The unsolved wider
A5 frontier and the preserved open eight-active checkpoint remain open;
this pass ends at the complete anchor-locus classification.
