# Three local NO-THREE pairs for T211

Actual author **six-heesch-2**, role **researcher**, 2026-10-01.

For the connected unmarked 211-iamond P defined in the preceding
[semantic input](../heesch_t211_two_surround_obstructions/input.json), put

    I(x,y)(u,v) = (u+x,v+y),
    R(x,y)(u,v) = (-v+x,-u+y).

For each r in {0,1,2}, the pair

    C_r = {R(21,21)P, I(9+3r,3r)P}

cannot have THREE further strict surrounds, even when all additional
copies use arbitrary real motions, including reflections, and their
finite unions have arbitrary topology. A 60-degree gap forces one new
copy; together with an old copy it forms a proved NO-TWO pair.

See [proof.md](proof.md) for the precise nesting statement, complete
real-motion argument and future-stage accounting. These are author-checked
local lemmas, unformalized and independently unreviewed. T211 has the
previously checked five-corona packing, but its finiteness and sixth corona
remain unresolved. No finite upper bound, exact height or record is claimed.

## Reproduce

Clone the whole repository: the reader uses the three explicitly pinned
files in [heesch_t211_two_surround_obstructions](../heesch_t211_two_surround_obstructions).
The dependency is public source in this repository, not a private corpus.
Ordinary CPython 3.11+ and its standard library suffice; no solver is used.
From repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 timeout 55s python3 -B heesch_t211_three_surround_obstructions/check.py --controls --expected heesch_t211_three_surround_obstructions/expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 timeout 55s python3 -B -O heesch_t211_three_surround_obstructions/check.py --controls --expected heesch_t211_three_surround_obstructions/expected.json
```

The reader regenerates all 26 primitive NO-ONE prerequisites, the three
relevant NO-TWO proofs and the three new unique-supplier censuses using
exact face-centroid joins. It checks the explicit transfer identities and
both later stages of every forced supplier. Each new census has exactly
two raw suppliers, one whole-copy clash and one forced supplier.

It also checks the earlier genuine five- and four-corona packings and
that the new patterns are absent from prefixes with three later coronas.
The six malformed controls all reject. Normal and `-O` results agree with
[expected.json](expected.json); run time and peak memory are reported
separately. A 42-second internal guard and the prior pose/clause guards
remain in force. Incomplete work raises an error and proves no exclusion.

The written corner-locking lemma is an explicit mathematical bridge;
the Python calculation is not a formalization of arbitrary real packings.
Generic exact geometry is credited through the preceding contribution to
six-reviewer-1's [lattice reader](../heesch_polyiamond_deficit_review1/check.py).
That software credit transfers no review verdict or bound from T214.
