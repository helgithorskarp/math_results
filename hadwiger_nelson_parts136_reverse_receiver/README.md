# Parts136: a complete reverse receiving relation

Retain the small part of the physical Parts509 graph together with the origin,
and remove the large part without its origin. The exact host has 136 points,
564 unit edges and 19 independent boundary pins. Its entire unrestricted
four-colour boundary relation has 41,025 canonical patterns. The original
373-point removed module blocks every pattern. A replacement may add at most
372 distinct new physical points to stay at 508 total.

This is a receiving specification. No replacement or sub-509 candidate is
supplied. The relation completeness proof is author-side and DRAT-checked;
the parent's previously reviewed non-four certificate is replayed against an
identically regenerated instance. No independent review of this new census
is claimed.

The advantage declared before enumeration was more replacement space and
fewer actual boundary pins than the separate
[Parts373 receiver](../hadwiger_nelson_parts373_receiver_relation/README.md).
The tradeoff is a much larger relation, so neither specification dominates.

| Quantity | Parts373 receiver | Parts136 receiver here |
|---|---:|---:|
| Retained physical points | 373 | 136 |
| Retained complete unit edges | 1,856 | 564 |
| Actual boundary pins | 23 | 19 |
| Canonical unrestricted host patterns | 468 | 41,025 |
| Maximum new replacement points | 135 | 372 |
| Original removed module points | 136 | 373 |
| Saving needed against the original module | 1 | 1 |

The physical parent is [Parts's 509-point construction](https://arxiv.org/abs/2010.12665),
still the supported unrestricted record. Haugland's
[v4 introduction](https://arxiv.org/html/2608.04542v4) explicitly retains 509;
its spindle-free construction concerns a different restriction.

Use zero-based row indices in `points.tsv`. Each row contains eight integer
coefficients for x followed by eight for y, divided by 96, in the basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

Let P be all 509 rows, H = {0} union {374,...,508}, and D = {1,...,373}.
All 129,286 unordered pairs are checked exactly, with both subset-mask
radical multiplication and squarefree-radical/gcd multiplication. The rows
are distinct and the complete strict unit graph has 2,442 edges: 564 in H,
1,836 in D, and 42 crossing edges. Its actual host boundary B = N(D) intersect H
is independent and has the following fixed pattern order:

```text
0,430,432,434,476,478,480,481,482,483,484,485,486,487,488,489,490,491,492.
```

The relation consists of restrictions to B of **all** ordinary proper
four-colourings of H, modulo global colour permutations. No phase, residue,
symmetry or palette assumption restricts the colourings. Fix vertex 0 to
colour 0, and take the lexicographic minimum under the six permutations fixing
0. Exactly 41,025 representatives occur:

| Colours used on B | Canonical patterns |
|---|---:|
| 2 | 7 |
| 3 | 1,500 |
| 4 | 39,518 |

These represent 984,516 fully labelled boundary patterns. A monochromatic B
is impossible, although it is feasible on the bare independent boundary.
Two-colour boundary patterns do occur; a replacement cannot presume four
colours on every host boundary.

Each generated pattern has a literal proper 136-digit host word. `verify.py`
checks every word and restriction. The sorted stream of 19-digit patterns,
each followed by a newline, has 820,500 bytes and SHA-256

```text
f67f18e35fcd20c46c405c2b7458712091afd12f5fdeaee6443555735fb56649
```

For completeness, regenerate the ordinary one-hot four-colour CNF for H,
fix vertex 0, and block all six images of every listed pattern. The resulting
544-variable, 249,359-clause instance has a checked DRAT refutation. Its hash is

```text
a3c7d8754b49818f25b4319397ff489406e785b4ddc2c08a7cf7dd958d179287
```

The original-module blocking proof is a gluing argument. If a colouring of H
and a colouring of the complete physical graph on D union B agreed on B,
they would four-colour P: every parent edge is internal to one side or among
the 42 recorded crossing edges. The checked parent refutation rules this out.
Together with the complete positive census, this proves that the original
module blocks **every** host pattern. The literal parent five-word in
`fixtures.json` is checked on all 2,442 physical unit edges.

The regenerated parent CNF has 2,036 variables, 13,332 clauses and SHA-256

```text
bfad1c1cb96e983bfa83922b63d564da9db3cb9bd36012c15abe89240f227de8
```

It is byte-identical to the earlier receiver's parent CNF. That proof is
reused and checked here; a fresh solve is optional. The independent
[Parts373 review](../hadwiger_nelson_parts373_receiver_relation_review1/README.md)
also proved parent non-four-colourability using a separate two-bit encoding.
That review does not establish this new host relation.

For a future exact replacement let X be its distinct points outside H after
collision merging. The cap is |X| <= 372. A replacement listing all 19 shared
B pins can have at most 391 total points including those pins. If every
contact from X to H lies at B, empty intersection between this full host
relation and the full relation of X union B is necessary and sufficient for
ordinary non-four-colourability. One surviving shared pattern retires that
replacement. With extra contacts to H outside B, expand the actual interface
or decide the complete union directly. In every case reconstruct all old--new
and new--new edges and check a proper five-word on the same physical graph.
The parent's five-word says nothing about an unknown replacement's colouring.

The benchmark blocker D is exact and only one point over the replacement
allowance. A different blocker with at most 372 new points remains missing.
The specification gives a finite compatibility decision for a frozen exact
replacement; it does not supply a finite coordinate pool or a search over all
replacements. Merely deleting a parent point or relocating the intact full
large gadget is not a new mechanism: registered criticality and full-gadget
placement closures still apply. No Parts373 replacement search is performed.
The old 66,332-pattern small-side observation concerned a different 31-pin
interface and is not a premise here.

Reproduction uses Python 3.11 and `python-sat==1.8.dev24` with `cadical195`
for generation. The exact checker uses only the standard library. External
proof generation used CaDiCaL 1.9.5 and `drat-trim`; provide executable paths.
Keep generated files outside the repository.

```bash
# Geometry, parent five-word and nine compact positive fixtures only:
python3 verify.py --out /tmp/parts136-fixtures

# Entire relation, every positive word, canonical hash and both CNFs:
python3 generate.py --out /tmp/parts136-full --seconds 1200 --max-patterns 100000
python3 verify.py --out /tmp/parts136-check --relation /tmp/parts136-full/host_relation.tsv

# Both independently checked negative obligations:
python3 certify.py --out /tmp/parts136-proof \
  --relation /tmp/parts136-full/host_relation.tsv \
  --cadical /path/to/cadical --drat-trim /path/to/drat-trim
```

The generator preserves partial rows on timeout and reports an incomplete
status. UNKNOWN proves nothing. `certify.py` can instead receive existing raw
proofs through `--completeness-proof` and `--parent-proof`; both checker runs
must exit zero and print `s VERIFIED`. Positive fixtures, hash agreement or
a solver UNSAT line alone do not establish the full theorem.

The 6,440,925-byte witness table, 820,500-byte pattern stream, approximately
22.7 MB completeness CNF and 35.1 MB proof are omitted from Git. Source
regenerates them; canonical hashes, nine positive fixtures and proof-check
metadata are public. Full author outputs are preserved in campaign pass81
scratch evidence. Proof bytes may vary with solver builds: validate the
regenerated instance and proof rather than requiring identical proof bytes.
Complete positive-word checking and a checked refutation are both required.

Coordinate SHA-256:
`f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50`.
The points and parent five-word are copied from the earlier public Parts
packages. Parts373 dependency commit:
`0fdb37bb7772a835307f904403589ba1d4676f20`; independent review commit:
`d86266c0e09db808865b6c379d68d1c133a86756`. This package establishes a
complete alternative receiver, not an improvement of the 509-point record.
