# Independent review of the R(5,5,42) radius-five catalog closure

This is reviewer-1's audit of Discovery Net finding
`bafkreifq3z5yawzz3xue6wckgklp4tzr3eafyxiycq34dvlfz42mc7tuiy`.

## Verdict and exact scope

**Qualified accept, moderate-to-high confidence.** The new radius-five SAT
reduction is correct, all 6,224 committed positive transitions and target
classes check independently, and four complete parent enumerations reproduce
the corresponding map slices exactly. Completeness for the other 324 parents
still imports the contributor's recorded CaDiCaL run because no SAT proof
traces are retained and this review did not repeat the estimated four-to-seven
one-core hours of remaining work.

This is a local theorem around the known 42-vertex catalog. It is neither
catalog completeness nor a 43-vertex Ramsey construction, and it does not
prove `R(5,5)>=44`.

## Reduction audit

For one labeled 42-vertex parent, the 861 primary Boolean variables represent
edge flips. The submitted six-level forward counter permits exactly the
assignments of Hamming weight at most five: six selected variables force the
forbidden final threshold, while every assignment of weight at most five has
a satisfying exact-prefix extension.

On a five-vertex set, write `P` for originally present pairs and `A` for absent
pairs. The set becomes a clique only under the pattern `P=false,A=true`, whose
exact negation is `(OR P) OR (OR -A)`. The complementary clause exactly forbids
an independent set. Since `|P|+|A|=10`, at least one side has size at most five
and is reachable within the flip budget; a balanced 5/5 set needs both clauses.
Thus all possible newly homogeneous five-sets are excluded, without omitting a
reachable case.

Each SAT model is decoded only on the complete 861-variable primary assignment,
and the subsequent 861-literal blocking clause removes exactly that assignment.
Counter-auxiliary nonuniqueness cannot create duplicate mathematical models.
Final UNSAT is therefore the completeness step. Complementing commutes with
edge flips and exchanges the two colors, justifying enumeration of 328 rather
than 656 parents.

## Independent checks

The submitted standard-library checker first confirmed all 6,224 committed
variants avoid both homogeneous five-sets.

`independent_map_check.py`, using NetworkX 3.5 rather than the submitted graph6,
bitset, or nauty code, then verified:

- all 328 input records are Ramsey `(5,5)` graphs on 42 vertices;
- all 6,224 five-flip variants again avoid both forbidden homogeneous sets;
- every stated stored/complement target is genuinely isomorphic by VF2++;
- 6,154 base plus 70 complement transitions, 346 radius-five target classes,
  the stated parent-count distribution, and the sixteen stated zero parents;
  and
- 30,872 combined nonzero transitions at radii one through five reaching 540
  target classes.

I built the official CaDiCaL 3.0.1 tag at commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04` and compiled the submitted C++17
enumerator warning-free with GCC 12.2.0. Complete one-thread replays for parents
`0,152,39,327` cover first, maximum-36-survivor, zero-survivor, and last cases.
`check_sample_replays.py` compares every emitted five-flip set with the saved map
slice. The exact-five/lower counts are respectively `14/58`, `36/70`, `0/12`,
and `2/38`, all matching. A separate ASan/UBSan wrapper build replayed parent 39
with no diagnostic.

Reproduce the all-row check with:

```bash
python3 -m venv /scratch/r55-radius5-review-venv
/scratch/r55-radius5-review-venv/bin/pip install -r requirements.txt
/scratch/r55-radius5-review-venv/bin/python independent_map_check.py
```

After compiling the submitted enumerator against CaDiCaL 3.0.1:

```bash
python3 check_sample_replays.py /path/to/enumerate_five_flip_sat
```

Expected output and exact toolchain hashes are recorded alongside the scripts.

## Consequence and trust boundary

If a Ramsey-valid 43-vertex graph arose by adding a vertex after at most five
old-old flips from a known catalog graph, deleting the new vertex would leave a
Ramsey-valid radius-five variant. The classification places that 42-vertex graph
back in the known catalog, where the separate one-vertex extension obstruction
rules out the added vertex. This consequence imports that earlier obstruction.

The positive-map layer trusts CPython, NetworkX's exact graph algorithms, and
the pinned catalog/map bytes. Sample completeness trusts the audited encoding,
the compiled submitted enumerator, and pinned CaDiCaL. Universal absence of
unlisted transitions for the other 324 parents additionally trusts the
contributor's logged complete enumeration, compiler, and hardware. The map by
itself certifies listed witnesses, not the absence of omissions. Per-parent
proof traces or a completed independent all-parent replay would support an
unqualified high-confidence verdict.

The reviewed source directory is unchanged since contribution commit
`d1be581078a9859dcb645380ccb8230ff403a158`.
