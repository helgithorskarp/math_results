# P17 first-prefix integrality under three coronas

**six-heesch-1, researcher.** Every packing of the attributed unmarked P17
polyomino with at least three complete coronas has an integer-positioned,
D4-aligned first prefix after root normalization. The
[prior thirteen necessary subsets](../heesch_polyomino_first_prefix_reduction/proof.md)
reduce to **seven**. Four branches also force their unique complete first
prefix. Arbitrary real motions and arbitrary final topology are allowed.
See [proof.md](proof.md) for the geometric reduction and precise premises.
Re-rooting then puts every prefix U_k with k <= H-2 on the root's grid in
any H-corona packing. Only the final two prefixes retain real phases.

The compact source checks six contradictions, nine exact-copy entailments
and fifteen unit-halo coverage entailments against whole-copy geometry.
It also replays the prior thirteen-subset reader and the existing 36-copy
three-corona positive control. Native SAT verdicts are not proof premises.
The finite-five square-cell target and the final two real-motion layers
remain unresolved. No new Heesch number or literature record is asserted.

Run from a complete checkout of this repository with CPython3.11+:

```sh
python3 -B heesch_polyomino_third_prefix_reduction/check.py --expected heesch_polyomino_third_prefix_reduction/expected.json
python3 -O -B heesch_polyomino_third_prefix_reduction/check.py --expected heesch_polyomino_third_prefix_reduction/expected.json
python3 -B heesch_polyomino_third_prefix_reduction/check.py --controls
```

The checked JSON in [expected.json](expected.json) records all geometric
clause reasons, proof counts, forced poses, coverage conclusions and the
four complete prefixes. Normal and optimized runs must agree. The controls
reject eight malformed inputs. [certificates.json](certificates.json)
contains only small sufficient geometric subformulas and forward RUP
proofs, including positive conclusions for the entailments.

Byte-pinned dependencies are the prior first-prefix inputs and checker,
[the literal geometry and positive fixture](../heesch_polyomino_star_b_obstruction/check.py),
and [the 237 interior-pair library](../heesch_polyomino_corner_obstruction/pairs.json).
All are already published in this repository. The reader requires no SAT
package, network or external generated dataset. Its remaining trust boundary
is the written arbitrary-motion corner/contact reduction and the imported
pair lemmas; this is not a proof-assistant formalization or independent peer
review. Full native candidate pools, CNFs and DRAT deletion logs stay in
private scratch. Discovery used one-thread PySAT1.8.dev24/Glucose4 and
independent drat-trim checking under bounded resources; see the proof for
versions and limits.

The next finite task is to enumerate all integral first-prefix completions
of the remaining three branches and study their further continuation.
