# Excluding two eight-point planes in a 72-point line-free set

Every 72-point line-free subset of \(\mathbb F_5^3\) has at most one
eight-point plane. This computer-assisted theorem eliminates AAA and AAB
from the earlier [global four-case cover](../low_planes72/README.md).
ABB and BBB remain open, and the numerical interval remains 70–72.

The [complete proof](THEOREM.md) reduces the hypothetical pair of small
planes to 4,442 projected weight matrices in 164 affine classes. Two exact
enumerations agree on the entire labeled list. All 164 lifting formulas
are UNSAT, with separately checked DRAT proofs. The 70-point construction
passes a positive lifting control.

## Reproduction

Tested with Python 3.12.14, GCC 12.2.0 and `python-sat==1.9.dev15`.
The repository's existing `../plane_caps.cpp` and `../known70.json` are
used as explicit prerequisites. No outside dataset or classification is
needed. From this directory:

```sh
python3 -m pip install -r requirements.txt
python3 verify.py --out /tmp/two-eight-verify
```

Expected status is `TWO_EIGHT_PLANE_REDUCTION_VERIFIED`, with 4,442 labeled
quotients, 164 affine classes, and all 164 CNF hashes matching the checked
inputs. This command verifies the reduction and input identities; it does
not recheck the omitted solver traces. Add `--sanitize` to compile both new
enumerations with address and undefined-behavior sanitizers.

For a full proof replay, build [DRAT-trim](https://github.com/marijnheule/drat-trim)
and run:

```sh
python3 replay.py --out /tmp/two-eight-proofs --drat-trim /path/to/drat-trim
```

The original checker source commit is
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; its binary hash is in
[certificates.json](certificates.json). The runner requires every CNF hash
to match the manifest and every independently checked proof to succeed.
`--start A --stop B` processes the half-open case interval \([A,B)\);
the complete family is \([0,164)\). A partial interval is not the theorem.

Proof export uses the flushed native binary stream. During development,
the Python-SAT text helper sometimes returned incomplete traces or failed
to decode a valid trace. The independent checker caught these failures;
they were not counted as verified cases. Original checked traces include
both ASCII and binary DRAT. The replay always writes binary DRAT, so its
proof hashes may differ from the original format-specific hashes. The
canonical CNF hashes must agree.

The original 164 solve-and-check records total about 221 seconds; the
largest case used 28,779 conflicts. These are recorded per-case durations,
not a hardware-independent runtime guarantee. The original traces total
451,847,578 bytes and remain outside the repository.

Generated CNFs, proofs, executables, and logs stay in the chosen output
directory. They are omitted from Git; the compact manifest and complete
generators are included. Proof checking, the cardinality encoder, ordinary
integer code, and the written normalization argument remain explicit trust
boundaries. There is no proof-assistant or independent peer-review claim.

## Context and scope

Elsholtz et al., *Maximal line-free sets in* \(\mathbb F_p^n\),
Periodica Mathematica Hungarica 90 (2025), 7–21
([primary paper](https://arxiv.org/abs/2310.03382v2),
[journal](https://doi.org/10.1007/s10998-024-00617-x)), supplies the named
extremal problem and the 70-point construction. Its published upper bound
is 73. The separate campaign [upper bound of 72](../upper_bound72.md) and
the [four-case reduction](../low_planes72/README.md) provide the current
graph context. Only the latter is needed for the AAA/AAB corollary; the
conditional two-plane exclusion does not assume either campaign result.

Targeted primary-literature and graph searches on 2026-09-26 found no earlier
statement of this two-eight-plane exclusion. This is search-relative
novelty, not a historical priority claim. The remaining full 72-point
existence problem is unresolved by this contribution.
